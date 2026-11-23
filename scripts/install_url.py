#!/usr/bin/env python3

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

from strictyaml import load

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "registry" / "agents.yaml"
SKILL_SOURCE = ROOT / "skills" / "typecraft-skills"
SKILL_NAME = "typecraft-skills"
REPOSITORY = "krupakar5535Kk/typecraft-skills"

URL_PATTERN = re.compile(
    r"https?://github\.com/krupakar5535Kk/typecraft-skills(?:\.git)?/?"
    r"(?=$|[\s)\]>,'\"!?]|\.(?:$|\s))",
    re.IGNORECASE,
)
URL_ONLY_PUNCTUATION = re.compile(r"""^[\s\[\]()<>"'`.,:;!?…-]*$""")
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


def load_registry():
    if not REGISTRY_PATH.is_file():
        raise InstallationError(f"Registry not found: {REGISTRY_PATH}")
    return load(REGISTRY_PATH.read_text(encoding="utf-8")).data


def is_install_request(message):
    if not URL_PATTERN.search(message or ""):
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
    if platform == "chatgpt":
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
    source = Path(source).resolve(strict=True)
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        raise InstallationError(f"Not a complete Agent Skill directory: {source}")

    files = []
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise InstallationError(f"Skill source contains a symlink: {path}")
        if path.is_file():
            files.append(path)
    return source, files


def verify_skill_tree(source, destination):
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
    if destination_files != expected_files:
        return False

    return all(
        (destination / relative).read_bytes() == (source / relative).read_bytes()
        for relative in expected_files
    )


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
            raise ExistingInstallationError(
                f"Different or incomplete skill already exists at {destination}; "
                "request explicit overwrite approval before using --force."
            )
        if not destination.is_dir():
            raise ExistingInstallationError(
                f"Installation target exists and is not a directory: {destination}"
            )

    destination.parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(
        tempfile.mkdtemp(prefix=f".{SKILL_NAME}-install-", dir=destination.parent)
    )
    staged_skill = stage_root / SKILL_NAME
    backup = None
    try:
        shutil.copytree(source, staged_skill)
        if not verify_skill_tree(source, staged_skill):
            raise InstallationError("Staged skill failed complete-file verification.")

        if destination.exists():
            backup = Path(
                tempfile.mkdtemp(prefix=f".{SKILL_NAME}-backup-", dir=destination.parent)
            )
            backup.rmdir()
            os.replace(destination, backup)
        try:
            os.replace(staged_skill, destination)
        except OSError:
            if backup is not None and backup.exists():
                os.replace(backup, destination)
                backup = None
            raise

        if backup is not None:
            shutil.rmtree(backup)
            backup = None
    finally:
        shutil.rmtree(stage_root)

    if not verify_skill_tree(source, destination):
        raise InstallationError(f"Installed skill failed file verification: {destination}")
    return "SUCCESS"


def resolve_native_destination(
    platform, scope, registry, project_root=None, home=None
):
    adapters = registry.get("native_adapters", {})
    adapter = adapters.get(platform)
    if adapter is None:
        raise InstallationError(f"No verified native directory adapter for {platform}.")

    paths = adapter.get("scope_paths", {})
    path_value = paths.get(scope)
    if not path_value:
        raise InstallationError(
            f"No documented {scope}-scope location for {platform}."
        )

    home_path = Path.home() if home is None else Path(home)
    project = Path.cwd() if project_root is None else Path(project_root)
    expanded = Path(path_value).expanduser() if "~" in path_value else Path(path_value)
    if path_value.startswith("~/") and home is not None:
        expanded = home_path / path_value[2:]
    elif not expanded.is_absolute():
        expanded = project / expanded
    return expanded.resolve(strict=False) / SKILL_NAME


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
        with zipfile.ZipFile(temporary) as archive:
            names = set(archive.namelist())
            expected = {
                (Path(SKILL_NAME) / path.relative_to(source)).as_posix()
                for path in files
            }
            if names != expected:
                raise InstallationError("ZIP package failed complete-file verification.")
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return output, len(files)


def _load_gh_inventory(platform, scope):
    fields = "skillName,sourceURL,agentHosts,path,version,scope"
    result = subprocess.run(
        [
            "gh", "skill", "list", "--agent", platform, "--scope", scope,
            "--json", fields,
        ],
        capture_output=True,
        text=True,
        check=False,
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


def _verify_cli_files(source, row):
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
            if _manifest_signature(installed.read_text(encoding="utf-8")) != (
                _manifest_signature(path.read_text(encoding="utf-8"))
            ):
                return False
        elif installed.read_bytes() != path.read_bytes():
            return False
    return True


def _manifest_signature(text):
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        return None
    values = []
    for field in ("name", "description"):
        match = re.search(rf"(?m)^{field}:\s*(.*?)\s*$", parts[1])
        values.append(match.group(1).strip("\"'") if match else None)
    return tuple(values) + (parts[2],)


def _install_with_github_cli(platform, scope, source, overwrite):
    if not shutil.which("gh"):
        raise InstallationError(
            f"No verified native directory adapter for {platform}, and GitHub CLI is unavailable."
        )
    help_result = subprocess.run(
        ["gh", "skill", "install", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    if help_result.returncode:
        raise InstallationError("GitHub CLI Agent Skills support is unavailable.")
    help_text = f"{help_result.stdout}\n{help_result.stderr}"
    if not re.search(rf"(?<![\w-]){re.escape(platform)}(?![\w-])", help_text):
        raise InstallationError(
            f"The installed GitHub CLI does not advertise support for {platform}."
        )

    rows = _load_gh_inventory(platform, scope)
    existing = _matching_rows(rows, platform, scope)
    if existing:
        current = next((row for row in existing if _is_typecraft_source(row)), None)
        if current and not overwrite:
            if not _verify_cli_files(source, current):
                raise InstallationError(
                    "GitHub CLI reports TypeCraft installed, but complete file "
                    "verification failed."
                )
            return InstallResult(
                platform, "FILES_ALREADY_PRESENT_DISCOVERY_UNVERIFIED",
                current.get("path", ""),
                "SUCCESS", "NOT_VERIFIED", "Check the platform's own skill list.",
                "The GitHub CLI inventory and files match TypeCraft.",
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
    result = subprocess.run(command, check=False)
    if result.returncode:
        raise InstallationError(
            f"GitHub CLI installation failed for {platform} (exit {result.returncode})."
        )

    refreshed = _load_gh_inventory(platform, scope)
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
    )


def _verify_native_discovery(platform):
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
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        return "NOT_VERIFIED", (
            f"Gemini CLI discovery check failed: {detail or result.returncode}"
        )
    if re.search(r"\btypecraft-skills\b", result.stdout, re.IGNORECASE):
        return "VERIFIED", "Gemini CLI listed typecraft-skills."
    return "NOT_VERIFIED", "Gemini CLI did not list typecraft-skills."


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
    registry = load_registry() if registry is None else registry
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
            raise InstallationError(
                "ChatGPT requires a package file. Provide --package-output; "
                "upload and install confirmation remain a user action."
            )
        output, count = package_skill(source, package_output, overwrite)
        return InstallResult(
            platform, "PACKAGE_READY_USER_ACTION_REQUIRED", str(output),
            f"SUCCESS ({count} files)", "NOT_VERIFIED",
            "Upload the ZIP in ChatGPT Skills and confirm installation.",
            "Packaging is not an installation.",
        )
    if route == "session_only":
        fallback = registry["fallbacks"][platform]
        return InstallResult(
            platform, "NOT_PERSISTENTLY_SUPPORTED", "",
            "NOT_APPLICABLE", "NOT_SUPPORTED",
            fallback.get("user_action", "Use the skill only in this conversation."),
            fallback.get("notes", ""),
        )
    if route == "unsupported":
        raise InstallationError(f"Unsupported platform ID: {platform}")
    if route == "native_directory":
        destination = resolve_native_destination(
            platform, scope, registry, project_root=project_root, home=home
        )
        status = _replace_directory(source, destination, overwrite)
        discovery, message = _verify_native_discovery(platform)
        if discovery == "VERIFIED" and platform == "gemini-cli":
            action = (
                "Gemini may request consent when the skill is activated."
            )
        elif discovery == "VERIFIED":
            action = "none"
        else:
            action = "Reload or inspect the platform's own skill list."
        if discovery == "VERIFIED":
            installation = (
                "ALREADY_INSTALLED" if status == "ALREADY_INSTALLED" else "SUCCESS"
            )
        elif status == "ALREADY_INSTALLED":
            installation = "FILES_ALREADY_PRESENT_DISCOVERY_UNVERIFIED"
        else:
            installation = "FILES_INSTALLED_DISCOVERY_UNVERIFIED"
        return InstallResult(
            platform, installation, str(destination), "SUCCESS", discovery, action,
            message,
        )
    return _install_with_github_cli(platform, scope, source, overwrite)


def print_result(result):
    print("TypeCraft Skills installation report")
    print(f"Platform: {result.platform}")
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

    print_result(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
