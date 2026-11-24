#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path

from strictyaml import StrictYAMLError, load

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "registry" / "agents.yaml"
SKILL_SOURCE = ROOT / "skills" / "typecraft-skills"
INSTALL_GUIDE = ROOT / "INSTALL.md"
SKILL_NAME = "typecraft-skills"
REPOSITORY = "krupakar5535Kk/typecraft-skills"
PROJECT_VERSION = "1.2.0"

URL_PATTERN = re.compile(
    r"https://github\.com/krupakar5535Kk/typecraft-skills(?:\.git)?/?"
    r"(?=$|[\s)\]>,'\"!?]|\.(?:$|\s))",
    re.IGNORECASE,
)
URL_ONLY_PUNCTUATION = re.compile(r"""^[\s\[\]()<>"'`.,:;!?…-]*$""")
MARKDOWN_CANONICAL_LINK = re.compile(
    r"""\[[^\]]*\]\(\s*<?(https://github\.com/"""
    r"""krupakar5535Kk/typecraft-skills(?:\.git)?/?)>?\s*\)""",
    re.IGNORECASE,
)
INSTALL_INTENT = re.compile(
    r"\b(?:install|add|set\s+up|setup)\b[\w\s'-]{0,40}"
    r"\b(?:this|the|typecraft|skill|repo|repository)\b|"
    r"\b(?:this|the|typecraft|skill|repo|repository)\b[\w\s'-]{0,40}"
    r"\b(?:install|add|set\s+up|setup)\b",
    re.IGNORECASE,
)
NEGATED_INSTALL = re.compile(
    r"\b(?:do\s+not|don't|never|shouldn't|should\s+not)\s+"
    r"(?:install|add|set\s+up|setup)\b",
    re.IGNORECASE,
)
INSTALLATION_QUESTION = re.compile(
    r"\b(?:how\s+(?:do|can|should)|where\s+(?:do|can)|"
    r"should\s+(?:i|we)|is\s+it\s+possible)\b",
    re.IGNORECASE,
)


class InstallationError(RuntimeError):
    pass


class ExistingInstallationError(InstallationError):
    pass


@dataclass(frozen=True)
class InstallResult:
    platform: str
    installation: str
    location: str
    file_verification: str
    skill_discovery: str
    user_action_remaining: str
    message: str = ""
    version: str = PROJECT_VERSION


def load_registry():
    if not REGISTRY_PATH.is_file():
        raise InstallationError(f"Registry not found: {REGISTRY_PATH}")
    return load(REGISTRY_PATH.read_text(encoding="utf-8")).data


def inspect_installation_guide():
    if not INSTALL_GUIDE.is_file():
        raise InstallationError(f"Installation guide not found: {INSTALL_GUIDE}")
    try:
        contents = INSTALL_GUIDE.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise InstallationError(f"Could not inspect {INSTALL_GUIDE}: {exc}") from exc
    if "skills/typecraft-skills/" not in contents:
        raise InstallationError(
            "INSTALL.md does not identify the canonical TypeCraft skill directory."
        )


def is_install_request(message):
    message = MARKDOWN_CANONICAL_LINK.sub(r"\1", message or "")
    if not URL_PATTERN.search(message):
        return False

    remainder = URL_PATTERN.sub("", message).strip()
    if URL_ONLY_PUNCTUATION.fullmatch(remainder):
        return True
    if NEGATED_INSTALL.search(remainder) or INSTALLATION_QUESTION.search(remainder):
        return False
    return bool(INSTALL_INTENT.search(remainder))


def detect_platform(env=None):
    """Resolve an explicit host identity supplied by the running agent."""
    variables = os.environ if env is None else env
    value = variables.get("TYPECRAFT_AGENT", "").strip().lower()
    if not value or value == "auto":
        return None
    return value


def get_route(platform, registry):
    platform_data = registry.get("platforms", {}).get(platform, {})
    installation = platform_data.get("installation", {})
    if installation.get("method") == "zip_upload_with_user_confirmation":
        return "zip_upload"
    if platform in registry.get("native_adapters", {}):
        return "native_directory"
    if platform in registry.get("fallbacks", {}):
        return "session_only"
    targets = registry["installers"]["github_cli"]["supported_agents"]
    if platform in targets:
        return "github_cli"
    return "unsupported"


def _skill_files(source):
    source = Path(source).expanduser()
    if source.is_symlink():
        raise InstallationError(f"Skill source cannot be a symlink: {source}")
    source = source.resolve(strict=True)
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        raise InstallationError(f"Not a complete Agent Skill directory: {source}")

    files = []
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise InstallationError(f"Skill source contains a symlink: {path}")
        if path.is_file():
            files.append(path)
    return source, files


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 128), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_skill_tree(source, destination, allow_extra_files=False):
    source, source_files = _skill_files(source)
    destination = Path(destination)
    if not destination.is_dir() or destination.is_symlink():
        return False

    destination_files = set()
    for path in destination.rglob("*"):
        if path.is_symlink():
            return False
        if path.is_file():
            destination_files.add(path.relative_to(destination))
    expected_files = {path.relative_to(source) for path in source_files}
    if (
        expected_files - destination_files
        or (not allow_extra_files and destination_files != expected_files)
    ):
        return False

    return all(
        _sha256(destination / relative) == _sha256(source / relative)
        for relative in expected_files
    )


def _is_typecraft_copy(path):
    manifest = Path(path) / "SKILL.md"
    if not manifest.is_file() or manifest.is_symlink():
        return False
    try:
        text = manifest.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    parsed = _parse_manifest(text)
    if parsed is None:
        return False
    frontmatter, body = parsed
    return (
        frontmatter.get("name") == SKILL_NAME
        and "# TypeCraft Skills" in body[:1000]
    )


def _verify_zip_archive(archive_path, source, source_files):
    try:
        source = Path(source).resolve(strict=True)
        source_files = [Path(path).resolve(strict=True) for path in source_files]
        expected = {
            (Path(SKILL_NAME) / path.relative_to(source)).as_posix()
            for path in source_files
        }
        with zipfile.ZipFile(archive_path) as archive:
            if archive.testzip() is not None:
                return False
            if set(archive.namelist()) != expected:
                return False
            return all(
                hashlib.sha256(
                    archive.read(
                        (Path(SKILL_NAME) / path.relative_to(source)).as_posix()
                    )
                ).hexdigest()
                == _sha256(path)
                for path in source_files
            )
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
        return False


def _replace_directory(source, destination, overwrite):
    source, _ = _skill_files(source)
    destination = Path(destination).expanduser()
    resolved_destination = destination.resolve(strict=False)
    if (
        resolved_destination == source
        or source in resolved_destination.parents
        or resolved_destination in source.parents
    ):
        raise InstallationError(
            "Installation destination cannot overlap the canonical skill directory."
        )

    if destination.is_symlink():
        raise InstallationError(f"Refusing to replace a symlink: {destination}")
    if destination.exists():
        if verify_skill_tree(source, destination):
            return "ALREADY_INSTALLED"
        if not overwrite:
            if _is_typecraft_copy(destination):
                raise ExistingInstallationError(
                    f"A TypeCraft copy at {destination} differs from the current "
                    "source (update available). Review it, then use --force to "
                    "merge the update; extra files will be preserved."
                )
            raise ExistingInstallationError(
                f"Different or incomplete skill already exists at {destination}; "
                "request explicit overwrite approval before using --force."
            )
        if not destination.is_dir():
            raise ExistingInstallationError(
                f"Installation target exists and is not a directory: {destination}"
            )

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        stage_root = Path(
            tempfile.mkdtemp(prefix=f".{SKILL_NAME}-install-", dir=destination.parent)
        )
    except OSError as exc:
        raise InstallationError(
            f"Could not prepare installation destination {destination}: {exc}"
        ) from exc
    staged_skill = stage_root / SKILL_NAME
    backup = None
    existing = destination.exists()
    known_typecraft = existing and _is_typecraft_copy(destination)
    try:
        if existing:
            for path in destination.rglob("*"):
                if path.is_symlink():
                    raise InstallationError(
                        f"Refusing to update an installation containing a symlink: {path}"
                    )
            shutil.copytree(destination, staged_skill)
            shutil.copytree(source, staged_skill, dirs_exist_ok=True)
        else:
            shutil.copytree(source, staged_skill)
        if not verify_skill_tree(source, staged_skill, allow_extra_files=existing):
            raise InstallationError("Staged skill failed complete-file verification.")

        if existing:
            backup = Path(
                tempfile.mkdtemp(prefix=f".{SKILL_NAME}-backup-", dir=destination.parent)
            )
            backup.rmdir()
            os.replace(destination, backup)
        try:
            os.replace(staged_skill, destination)
            if not verify_skill_tree(
                source, destination, allow_extra_files=existing
            ):
                raise InstallationError(
                    f"Installed skill failed file verification: {destination}"
                )
        except (OSError, InstallationError) as exc:
            if destination.exists():
                shutil.rmtree(destination)
            if backup is not None and backup.exists():
                os.replace(backup, destination)
                backup = None
            if isinstance(exc, OSError):
                raise InstallationError(
                    f"Installation failed and the previous directory was restored: {exc}"
                ) from exc
            raise

        if backup is not None:
            shutil.rmtree(backup)
            backup = None
    finally:
        shutil.rmtree(stage_root)

    if not verify_skill_tree(source, destination, allow_extra_files=existing):
        raise InstallationError(f"Installed skill failed file verification: {destination}")
    if known_typecraft:
        return "UPDATED"
    return "SUCCESS"


def _resolve_scope_path(path_value, project_root=None, home=None):
    home_path = (Path.home() if home is None else Path(home)).resolve(strict=False)
    project = (
        Path.cwd() if project_root is None else Path(project_root)
    ).resolve(strict=False)
    if path_value.startswith("~/"):
        root = home_path
        relative = Path(path_value[2:])
    else:
        root = project
        relative = Path(path_value)
    if relative.is_absolute() or ".." in relative.parts:
        raise InstallationError(f"Unsafe installation path in registry: {path_value}")

    parent = root
    for part in relative.parts:
        parent = parent / part
        if parent.is_symlink():
            raise InstallationError(f"Refusing a symlinked installation directory: {parent}")
    return parent / SKILL_NAME


def resolve_native_destinations(
    platform, scope, registry, project_root=None, home=None
):
    adapter = registry.get("native_adapters", {}).get(platform)
    if adapter is None:
        raise InstallationError(f"No verified native directory adapter for {platform}.")

    path_values = [adapter.get("scope_paths", {}).get(scope)]
    path_values.extend(adapter.get("alternate_scope_paths", {}).get(scope, []))
    if not path_values[0]:
        raise InstallationError(
            f"No documented {scope}-scope location for {platform}."
        )

    destinations = []
    seen = set()
    for path_value in path_values:
        destination = _resolve_scope_path(path_value, project_root, home)
        key = os.path.normcase(str(destination))
        if key not in seen:
            destinations.append(destination)
            seen.add(key)
    return destinations


def resolve_native_destination(
    platform, scope, registry, project_root=None, home=None
):
    return resolve_native_destinations(
        platform, scope, registry, project_root=project_root, home=home
    )[0]


def package_skill(source, output, overwrite=False):
    source, files = _skill_files(source)
    output = Path(output).expanduser()
    if output.is_symlink():
        raise InstallationError(f"Refusing to replace a symlink: {output}")
    output = output.resolve(strict=False)
    if output.suffix.lower() != ".zip":
        raise InstallationError("The package output must use a .zip extension.")
    if output == source or source in output.parents:
        raise InstallationError("ZIP output cannot be written inside the canonical skill.")
    if output.exists() and not overwrite:
        raise ExistingInstallationError(
            f"Package already exists at {output}; use --force only with explicit approval."
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
    )
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                archive.write(path, (Path(SKILL_NAME) / path.relative_to(source)).as_posix())
        if not _verify_zip_archive(temporary, source, files):
            raise InstallationError(
                "ZIP package failed integrity, completeness, or content verification."
            )
        os.replace(temporary, output)
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        raise InstallationError(f"Could not create or verify ZIP package: {exc}") from exc
    finally:
        temporary.unlink(missing_ok=True)
    return output, len(files)


def _load_gh_inventory(platform, scope, cwd=None):
    fields = "skillName,sourceURL,agentHosts,path,version,scope"
    result = subprocess.run(
        [
            "gh", "skill", "list", "--agent", platform, "--scope", scope,
            "--json", fields,
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=cwd,
    )
    if result.returncode:
        raise InstallationError(
            "Could not inspect GitHub CLI skill inventory: "
            + (result.stderr.strip() or result.stdout.strip())
        )
    try:
        rows = json.loads(result.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise InstallationError(f"Invalid JSON from gh skill list: {exc}") from exc
    if not isinstance(rows, list):
        raise InstallationError("Unexpected GitHub CLI installed-skills inventory.")
    return rows


def _matching_rows(rows, platform, scope):
    return [
        row for row in rows
        if row.get("skillName") == SKILL_NAME
        and row.get("scope") == scope
        and platform in (row.get("agentHosts") or [])
    ]


def _is_typecraft_source(row):
    source = (row.get("sourceURL") or "").strip().rstrip("/").removesuffix(".git")
    return source.lower() == f"https://github.com/{REPOSITORY}".lower()


def _verify_cli_files(source, row, metadata_source="repository"):
    path_value = row.get("path")
    if not path_value:
        return False
    source, source_files = _skill_files(source)
    destination = Path(path_value).expanduser()
    if destination.is_symlink() or not destination.is_dir():
        return False
    expected = {path.relative_to(source) for path in source_files}
    installed_files = set()
    for path in destination.rglob("*"):
        if path.is_symlink():
            return False
        if path.is_file():
            installed_files.add(path.relative_to(destination))
    if installed_files != expected:
        return False

    for path in source_files:
        relative = path.relative_to(source)
        installed = destination / relative
        if not installed.is_file():
            return False
        if relative == Path("SKILL.md"):
            expected_signature = _manifest_signature(
                path.read_text(encoding="utf-8")
            )
            installed_signature = _manifest_signature(
                installed.read_text(encoding="utf-8"),
                metadata_source=metadata_source,
            )
            if expected_signature is None or installed_signature != expected_signature:
                return False
        elif _sha256(installed) != _sha256(path):
            return False
    return True


def _parse_manifest(text):
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        return None
    try:
        frontmatter = dict(load(parts[1]).data)
    except StrictYAMLError:
        return None
    return frontmatter, parts[2]


def _manifest_signature(text, metadata_source=None):
    parsed = _parse_manifest(text)
    if parsed is None:
        return None

    frontmatter, body = parsed
    metadata = frontmatter.pop("metadata", None)
    if metadata is not None:
        if not isinstance(metadata, dict):
            return None
        if metadata_source == "repository":
            if (
                set(metadata) != {"sourceURL"}
                or not _is_typecraft_source({"sourceURL": metadata["sourceURL"]})
            ):
                return None
        elif (
            metadata_source is None
            or set(metadata) != {"local-path"}
            or metadata["local-path"] != metadata_source
        ):
            return None

    normalized = json.dumps(
        frontmatter,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    body = body.lstrip("\r\n")
    return hashlib.sha256(f"{normalized}\n---\n{body}".encode("utf-8")).hexdigest()


def _install_with_github_cli(
    platform, scope, source, overwrite, version, project_root=None
):
    if not shutil.which("gh"):
        raise InstallationError(
            f"No verified native directory adapter for {platform}, and GitHub CLI is unavailable."
        )
    cwd = None
    if scope == "project":
        project = Path.cwd() if project_root is None else Path(project_root)
        if not project.is_dir():
            raise InstallationError(
                f"Project installation directory does not exist: {project}"
            )
        cwd = project.resolve()
    help_result = subprocess.run(
        ["gh", "skill", "install", "--help"],
        capture_output=True,
        text=True,
        check=False,
        cwd=cwd,
    )
    if help_result.returncode:
        raise InstallationError("GitHub CLI Agent Skills support is unavailable.")
    help_text = f"{help_result.stdout}\n{help_result.stderr}"
    if not re.search(rf"(?<![\w-]){re.escape(platform)}(?![\w-])", help_text):
        raise InstallationError(
            f"The installed GitHub CLI does not advertise support for {platform}."
        )

    rows = _load_gh_inventory(platform, scope, cwd=cwd)
    existing = _matching_rows(rows, platform, scope)
    if existing:
        current = next((row for row in existing if _is_typecraft_source(row)), None)
        if current and not overwrite:
            if not _verify_cli_files(source, current):
                raise ExistingInstallationError(
                    "A known TypeCraft copy is present, but its files differ from "
                    "the current source (update available). Review the target and "
                    "rerun with --force only after authorizing the GitHub CLI update."
                )
            return InstallResult(
                platform, "FILES_ALREADY_PRESENT_DISCOVERY_UNVERIFIED",
                current.get("path", ""),
                "SUCCESS", "NOT_VERIFIED", "Check the platform's own skill list.",
                "The GitHub CLI inventory and files match TypeCraft.",
                version,
            )
        if not overwrite:
            raise ExistingInstallationError(
                f"A skill named {SKILL_NAME} already exists for {platform}; "
                "explicit approval is required before replacement."
            )

    command = [
        "gh", "skill", "install", REPOSITORY, SKILL_NAME,
        "--agent", platform, "--scope", scope,
    ]
    if overwrite:
        command.append("--force")
    result = subprocess.run(command, check=False, cwd=cwd)
    if result.returncode:
        raise InstallationError(
            f"GitHub CLI installation failed for {platform} (exit {result.returncode})."
        )

    refreshed = _load_gh_inventory(platform, scope, cwd=cwd)
    installed = next(
        (
            row for row in _matching_rows(refreshed, platform, scope)
            if _is_typecraft_source(row)
        ),
        None,
    )
    if installed is None or not _verify_cli_files(source, installed):
        raise InstallationError(
            "GitHub CLI returned success, but the installed skill could not be "
            "verified in its inventory and files."
        )
    return InstallResult(
        platform, "FILES_INSTALLED_DISCOVERY_UNVERIFIED",
        installed.get("path", ""),
        "SUCCESS", "NOT_VERIFIED", "Check the platform's own skill list.",
        "The CLI inventory and complete reference-file set were verified.",
        version,
    )


def _verify_native_discovery(platform, cwd=None, destination=None):
    if platform == "github-copilot-cli":
        executable = shutil.which("copilot")
        if not executable:
            return (
                "NOT_VERIFIED",
                "GitHub Copilot CLI is unavailable for a discovery check.",
            )
        if destination is None:
            return (
                "NOT_VERIFIED",
                "The installed skill location is required to verify Copilot discovery.",
            )

        try:
            result = subprocess.run(
                [executable, "skill", "list", "--json"],
                capture_output=True,
                text=True,
                check=False,
                cwd=cwd,
            )
        except OSError as exc:
            return (
                "NOT_VERIFIED",
                f"Could not run GitHub Copilot CLI discovery: {exc}",
            )
        if result.returncode:
            detail = result.stderr.strip() or result.stdout.strip()
            return "NOT_VERIFIED", (
                "GitHub Copilot CLI discovery failed: "
                f"{detail or result.returncode}"
            )
        try:
            skills = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            return "NOT_VERIFIED", f"Invalid JSON from copilot skill list: {exc}"
        if not isinstance(skills, list):
            return "NOT_VERIFIED", "Unexpected GitHub Copilot CLI skill inventory."

        expected = Path(destination).resolve(strict=False)
        if any(
            isinstance(skill, dict)
            and skill.get("name") == SKILL_NAME
            and isinstance(skill.get("path"), str)
            and Path(skill["path"]).resolve(strict=False) == expected
            for skill in skills
        ):
            return (
                "VERIFIED",
                "GitHub Copilot CLI listed typecraft-skills at the installed location.",
            )
        return (
            "NOT_VERIFIED",
            "GitHub Copilot CLI did not list typecraft-skills at the installed location.",
        )

    if platform == "opencode":
        executable = shutil.which("opencode")
        if not executable:
            return "NOT_VERIFIED", "OpenCode is unavailable for a discovery check."
        if destination is None:
            return (
                "NOT_VERIFIED",
                "The installed skill location is required to verify OpenCode discovery.",
            )

        try:
            result = subprocess.run(
                [executable, "--pure", "debug", "skill"],
                capture_output=True,
                text=True,
                check=False,
                cwd=cwd,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            return "NOT_VERIFIED", "OpenCode skill discovery timed out."
        except OSError as exc:
            return "NOT_VERIFIED", f"Could not run OpenCode skill discovery: {exc}"
        if result.returncode:
            detail = result.stderr.strip() or result.stdout.strip()
            return "NOT_VERIFIED", (
                f"OpenCode skill discovery failed: {detail or result.returncode}"
            )
        try:
            skills = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            return "NOT_VERIFIED", f"Invalid JSON from OpenCode skill list: {exc}"
        if not isinstance(skills, list):
            return "NOT_VERIFIED", "Unexpected OpenCode skill inventory."

        expected = Path(destination).resolve(strict=False)
        expected_manifest = (expected / "SKILL.md").resolve(strict=False)
        if any(
            isinstance(skill, dict)
            and skill.get("name") == SKILL_NAME
            and isinstance(skill.get("location"), str)
            and Path(skill["location"]).resolve(strict=False)
            in {expected, expected_manifest}
            for skill in skills
        ):
            return "VERIFIED", (
                "OpenCode listed typecraft-skills at the installed location."
            )
        return (
            "NOT_VERIFIED",
            "OpenCode did not list typecraft-skills at the installed location.",
        )

    if platform != "gemini-cli":
        return "NOT_VERIFIED", "Confirm discovery in the platform's own skill list or UI."

    executable = shutil.which("gemini")
    if not executable:
        return "NOT_VERIFIED", "Gemini CLI is unavailable for a discovery check."

    result = subprocess.run(
        [executable, "skills", "list", "--all"],
        capture_output=True,
        text=True,
        check=False,
        cwd=cwd,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        return "NOT_VERIFIED", (
            f"Gemini CLI discovery check failed: {detail or result.returncode}"
        )
    if re.search(r"\btypecraft-skills\b", result.stdout, re.IGNORECASE):
        return "VERIFIED", "Gemini CLI listed typecraft-skills."
    return "NOT_VERIFIED", "Gemini CLI did not list typecraft-skills."


def _gemini_native_installer_supported(executable):
    result = subprocess.run(
        [executable, "skills", "install", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    help_text = f"{result.stdout}\n{result.stderr}"
    return (
        result.returncode == 0
        and "--scope" in help_text
    )


def _install_with_gemini_cli(
    source, destination, scope, overwrite, version, executable, project_root
):
    if destination.exists():
        status = _replace_directory(source, destination, overwrite)
        discovery, message = _verify_native_discovery(
            "gemini-cli",
            cwd=project_root if scope == "project" else None,
            destination=destination,
        )
        installation = (
            "ALREADY_INSTALLED"
            if status == "ALREADY_INSTALLED" and discovery == "VERIFIED"
            else "FILES_ALREADY_PRESENT_DISCOVERY_UNVERIFIED"
            if status == "ALREADY_INSTALLED"
            else "UPDATED"
            if status == "UPDATED" and discovery == "VERIFIED"
            else "FILES_UPDATED_DISCOVERY_UNVERIFIED"
            if status == "UPDATED"
            else "FILES_INSTALLED_DISCOVERY_UNVERIFIED"
        )
        return InstallResult(
            "gemini-cli",
            installation,
            str(destination),
            "SUCCESS",
            discovery,
            "Review Gemini's consent prompt when activating the skill."
            if discovery == "VERIFIED"
            else "Inspect Gemini CLI's skill list and reload if needed.",
            message,
            version,
        )

    native_scope = "user" if scope == "user" else "workspace"
    command = [
        executable,
        "skills",
        "install",
        str(Path(source).resolve()),
        "--scope",
        native_scope,
    ]
    result = subprocess.run(
        command,
        check=False,
        cwd=project_root if scope == "project" else None,
    )
    if not verify_skill_tree(source, destination):
        return InstallResult(
            "gemini-cli",
            "PARTIAL_INSTALLATION" if destination.exists() else "FAILED",
            str(destination),
            "FAILED",
            "NOT_VERIFIED",
            "Inspect the destination and resolve any partial native install.",
            (
                "Gemini CLI exited successfully but the canonical file tree "
                "could not be verified."
                if result.returncode == 0
                else f"Gemini CLI installation failed with exit code {result.returncode}."
            ),
            version,
        )

    discovery, message = _verify_native_discovery(
        "gemini-cli", cwd=project_root if scope == "project" else None
    )
    if result.returncode:
        installation = "FILES_INSTALLED_NATIVE_COMMAND_FAILED"
        message = (
            f"Gemini CLI returned exit code {result.returncode}, but complete files "
            f"were verified. {message}"
        )
    else:
        installation = "SUCCESS" if discovery == "VERIFIED" else (
            "FILES_INSTALLED_DISCOVERY_UNVERIFIED"
        )
    action = (
        "Review Gemini's consent prompt when activating the skill."
        if discovery == "VERIFIED"
        else "Inspect Gemini CLI's skill list and reload if needed."
    )
    return InstallResult(
        "gemini-cli",
        installation,
        str(destination),
        "SUCCESS",
        discovery,
        action,
        message,
        version,
    )


def execute_install(
    request,
    platform,
    scope="user",
    source=SKILL_SOURCE,
    registry=None,
    project_root=None,
    home=None,
    package_output=None,
    overwrite=False,
    env=None,
):
    if not is_install_request(request):
        raise InstallationError(
            "The request does not contain the canonical TypeCraft URL as an install request."
        )
    inspect_installation_guide()
    registry = load_registry() if registry is None else registry
    version = registry.get("project_version", PROJECT_VERSION)
    if platform == "auto":
        platform = detect_platform(env)
    if not platform:
        raise InstallationError(
            "Could not identify the active agent. Set TYPECRAFT_AGENT to its exact "
            "host ID or pass --agent explicitly; no platform will be guessed."
        )

    route = get_route(platform, registry)
    if route == "zip_upload":
        if not package_output:
            display_name = registry["platforms"][platform]["display_name"]
            raise InstallationError(
                f"{display_name} requires a package file. Provide --package-output; "
                "upload and installation confirmation remain a user action."
            )
        output, count = package_skill(source, package_output, overwrite)
        user_action = registry["platforms"][platform]["discovery"].get(
            "user_action",
            "Upload the ZIP in the platform and confirm installation.",
        )
        return InstallResult(
            platform, "PACKAGE_READY_USER_ACTION_REQUIRED", str(output),
            f"SUCCESS ({count} files)", "NOT_VERIFIED",
            user_action,
            "Packaging is not an installation.",
            version,
        )
    if route == "session_only":
        fallback = registry["fallbacks"][platform]
        return InstallResult(
            platform, "NOT_PERSISTENTLY_SUPPORTED", "",
            "NOT_APPLICABLE", "NOT_SUPPORTED",
            fallback.get("user_action", "Use the skill only in this conversation."),
            fallback.get("notes", ""),
            version,
        )
    if route == "unsupported":
        raise InstallationError(f"Unsupported platform ID: {platform}")
    if route == "native_directory":
        destinations = resolve_native_destinations(
            platform, scope, registry, project_root=project_root, home=home
        )
        destination = next(
            (path for path in destinations if path.exists() or path.is_symlink()),
            destinations[0],
        )
        gemini = shutil.which("gemini") if platform == "gemini-cli" else None
        if gemini and _gemini_native_installer_supported(gemini):
            return _install_with_gemini_cli(
                source,
                destination,
                scope,
                overwrite,
                version,
                gemini,
                project_root,
            )
        status = _replace_directory(source, destination, overwrite)
        discovery, message = _verify_native_discovery(
            platform,
            cwd=project_root if scope == "project" else None,
            destination=destination,
        )
        if discovery == "VERIFIED" and platform == "gemini-cli":
            action = (
                "Gemini may request consent when the skill is activated."
            )
        elif discovery == "VERIFIED" and platform == "opencode":
            action = (
                "Restart any running OpenCode session; new sessions discover the skill."
            )
        elif discovery == "VERIFIED":
            action = "none"
        else:
            platform_id = platform.replace("-", "_")
            platform_record = registry.get("platforms", {}).get(
                platform,
                registry.get("platforms", {}).get(platform_id, {}),
            )
            action = platform_record.get("discovery", {}).get(
                "user_action",
                "Reload or inspect the platform's own skill list.",
            )
        if discovery == "VERIFIED":
            installation = (
                "ALREADY_INSTALLED"
                if status == "ALREADY_INSTALLED"
                else "UPDATED"
                if status == "UPDATED"
                else "SUCCESS"
            )
        elif status == "ALREADY_INSTALLED":
            installation = "FILES_ALREADY_PRESENT_DISCOVERY_UNVERIFIED"
        elif status == "UPDATED":
            installation = "FILES_UPDATED_DISCOVERY_UNVERIFIED"
        else:
            installation = "FILES_INSTALLED_DISCOVERY_UNVERIFIED"
        return InstallResult(
            platform, installation, str(destination), "SUCCESS", discovery, action,
            message,
            version,
        )
    return _install_with_github_cli(
        platform, scope, source, overwrite, version, project_root=project_root
    )


def print_result(result, json_output=False):
    if json_output:
        print(json.dumps(asdict(result), indent=2))
        return
    print("TypeCraft Skills installation report")
    print(f"Platform: {result.platform}")
    print(f"Version: {result.version}")
    print(f"Installation: {result.installation}")
    print(f"Location: {result.location or 'not applicable'}")
    print(f"File verification: {result.file_verification}")
    print(f"Skill discovery: {result.skill_discovery}")
    print(f"User action remaining: {result.user_action_remaining}")
    if result.message:
        print(f"Details: {result.message}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Install or package TypeCraft from its canonical GitHub URL."
    )
    parser.add_argument("--request", required=True, help="User message containing the TypeCraft URL.")
    parser.add_argument("--agent", default="auto", help="Active agent host ID, or auto.")
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--package-output", type=Path)
    parser.add_argument(
        "--force", action="store_true",
        help="Replace an existing installation or package after explicit approval.",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Print the installation result as machine-readable JSON.",
    )
    args = parser.parse_args(argv)

    try:
        result = execute_install(
            args.request,
            args.agent,
            scope=args.scope,
            project_root=args.project_root,
            package_output=args.package_output,
            overwrite=args.force,
        )
    except InstallationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR: File or process operation failed: {exc}", file=sys.stderr)
        return 1

    print_result(result, json_output=args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
