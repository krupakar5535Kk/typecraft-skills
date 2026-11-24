import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.install_url import SKILL_SOURCE, verify_skill_tree


GEMINI_PACKAGE = "@google/gemini-cli@0.70.0"


def run_gemini(project, environment, *arguments):
    result = subprocess.run(
        [
            "npm",
            "exec",
            "--yes",
            "--package",
            GEMINI_PACKAGE,
            "--",
            "gemini",
            *arguments,
        ],
        cwd=project,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=300,
    )
    if result.returncode:
        raise RuntimeError(
            f"Gemini CLI command failed: {' '.join(arguments)}\n"
            f"{result.stderr or result.stdout}"
        )
    return result.stdout.strip()


def main():
    source = SKILL_SOURCE.resolve()
    with tempfile.TemporaryDirectory(prefix="typecraft-gemini-cli-") as directory:
        root = Path(directory)
        project = root / "project"
        home = root / "home"
        project.mkdir()
        home.mkdir()
        npm_config = root / "npmrc"
        npm_config.write_text("registry=https://registry.npmjs.org/\n", encoding="utf-8")

        environment = os.environ.copy()
        for key in list(environment):
            if any(
                marker in key.upper()
                for marker in ("TOKEN", "PASSWORD", "SECRET", "CREDENTIAL", "API_KEY")
            ):
                environment.pop(key)
        environment.update(
            {
                "HOME": str(home),
                "XDG_CONFIG_HOME": str(home / ".config"),
                "npm_config_cache": str(root / "npm-cache"),
                "npm_config_userconfig": str(npm_config),
            }
        )

        version = run_gemini(project, environment, "--version")
        if version != "0.70.0":
            raise RuntimeError(f"Unexpected Gemini CLI version: {version}")

        run_gemini(
            project,
            environment,
            "skills",
            "install",
            str(source),
            "--scope",
            "user",
            "--consent",
        )

        destination = home / ".gemini" / "skills" / "typecraft-skills"
        if not verify_skill_tree(source, destination):
            raise RuntimeError("Gemini CLI installation differs from canonical files")
        references = list((destination / "references").rglob("*.md"))
        if len(references) != 20:
            raise RuntimeError(
                f"Expected 20 reference files after install, found {len(references)}"
            )

        listing = run_gemini(project, environment, "skills", "list", "--all")
        if not re.search(r"(?m)^typecraft-skills(?:\s|$)", listing):
            raise RuntimeError("Gemini CLI did not discover typecraft-skills")

        print(
            "PASS: Gemini CLI 0.70.0 installed the canonical user-scope skill, "
            "verified all files by SHA-256, and listed it without model access."
        )


if __name__ == "__main__":
    main()
