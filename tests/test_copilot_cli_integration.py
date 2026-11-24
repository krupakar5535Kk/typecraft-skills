import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.install_url import SKILL_SOURCE, execute_install, load_registry, verify_skill_tree


URL = "https://github.com/krupakar5535Kk/typecraft-skills.git"
REQUEST = f"{URL} Install this skill."
MINIMUM_COPILOT_VERSION = (1, 0, 105)


def run_copilot(project, environment, *arguments):
    result = subprocess.run(
        ["copilot", "--no-auto-update", *arguments],
        cwd=project,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    if result.returncode:
        raise RuntimeError(
            f"Copilot CLI command failed: {' '.join(arguments)}\n"
            f"{result.stderr or result.stdout}"
        )
    return result.stdout.strip()


def verify_scope(scope, root, environment, registry):
    project = root / "project"
    home = root / "home"
    project.mkdir(parents=True)
    home.mkdir()
    scope_environment = {
        **environment,
        "HOME": str(home),
        "COPILOT_HOME": str(home / ".copilot"),
        "COPILOT_CACHE_HOME": str(home / ".cache" / "copilot"),
    }

    previous_values = {
        key: os.environ.get(key)
        for key in ("HOME", "COPILOT_HOME", "COPILOT_CACHE_HOME")
    }
    os.environ.update({
        "HOME": str(home),
        "COPILOT_HOME": str(home / ".copilot"),
        "COPILOT_CACHE_HOME": str(home / ".cache" / "copilot"),
    })
    try:
        result = execute_install(
            REQUEST,
            "github-copilot-cli",
            scope=scope,
            source=SKILL_SOURCE,
            registry=registry,
            project_root=project,
            home=home,
        )
    finally:
        for key, value in previous_values.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    destination = Path(result.location)
    if result.installation != "SUCCESS" or result.skill_discovery != "VERIFIED":
        raise RuntimeError(
            f"Copilot CLI {scope} install was not discovered: {result}"
        )
    if not verify_skill_tree(SKILL_SOURCE, destination):
        raise RuntimeError(f"Copilot CLI {scope} files differ from canonical files")
    references = list((destination / "references").rglob("*.md"))
    if len(references) != 20:
        raise RuntimeError(
            f"Expected 20 references in {scope} install, found {len(references)}"
        )

    listing = json.loads(
        run_copilot(project, scope_environment, "skill", "list", "--json")
    )
    if not any(
        skill.get("name") == "typecraft-skills"
        and Path(skill.get("path", "")).resolve() == destination.resolve()
        for skill in listing
    ):
        raise RuntimeError(
            f"Copilot CLI did not list the {scope} installation at {destination}"
        )
    return destination


def main():
    if not shutil.which("copilot"):
        raise RuntimeError("Copilot CLI is required for this integration test.")

    with tempfile.TemporaryDirectory(prefix="typecraft-copilot-cli-") as directory:
        root = Path(directory)
        for key in list(os.environ):
            if any(
                marker in key.upper()
                for marker in ("TOKEN", "PASSWORD", "SECRET", "CREDENTIAL", "API_KEY")
            ):
                os.environ.pop(key)
        environment = os.environ.copy()
        isolated_home = root / "cli-home"
        isolated_home.mkdir()
        environment.update({
            "HOME": str(isolated_home),
            "COPILOT_HOME": str(isolated_home / ".copilot"),
            "COPILOT_CACHE_HOME": str(isolated_home / ".cache" / "copilot"),
        })
        version = run_copilot(root, environment, "--version")
        version_match = re.search(r"\b(\d+)\.(\d+)\.(\d+)\b", version)
        if not version_match or tuple(map(int, version_match.groups())) < MINIMUM_COPILOT_VERSION:
            raise RuntimeError(
                f"Copilot CLI {MINIMUM_COPILOT_VERSION} or newer is required, got {version}"
            )

        project_path = verify_scope(
            "project", root / "project-scope", environment, load_registry()
        )
        user_path = verify_scope(
            "user", root / "user-scope", environment, load_registry()
        )
        print(
            f"PASS: Copilot CLI {version_match.group(0)} installed and discovered TypeCraft "
            f"at project scope ({project_path}) and user scope ({user_path}); "
            "all 20 references match the canonical files. No model invocation or "
            "account credentials were used."
        )


if __name__ == "__main__":
    main()
