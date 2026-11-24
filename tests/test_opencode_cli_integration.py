import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.install_url import SKILL_SOURCE, execute_install, verify_skill_tree

OPENCODE_VERSION = "1.19.6"
REQUEST = (
    "https://github.com/krupakar5535Kk/typecraft-skills "
    "Install this skill."
)


class OpenCodeCliIntegrationTests(unittest.TestCase):
    def test_project_install_integrity_and_native_discovery(self):
        executable = shutil.which("opencode")
        if not executable:
            self.skipTest("OpenCode CLI is not installed")

        with tempfile.TemporaryDirectory(prefix="typecraft-opencode-test-") as tmp:
            root = Path(tmp)
            home = root / "home"
            project = root / "project"
            home.mkdir()
            project.mkdir()
            marker = root / "project-plugin-executed"
            plugin = project / ".opencode" / "plugins" / "acceptance-probe.js"
            plugin.parent.mkdir(parents=True)
            plugin.write_text(
                "import { writeFileSync } from 'node:fs';\n"
                f"writeFileSync({str(marker)!r}, 'loaded');\n"
                "export default async () => ({});\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            for key in list(environment):
                if any(
                    marker in key.upper()
                    for marker in ("TOKEN", "PASSWORD", "SECRET", "CREDENTIAL", "API_KEY")
                ) or key.upper().startswith("OPENCODE_CONFIG"):
                    environment.pop(key)
            environment["HOME"] = str(home)
            environment["XDG_CONFIG_HOME"] = str(home / ".config")

            with patch.dict(os.environ, environment, clear=True):
                version = subprocess.run(
                    [executable, "--version"],
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.strip()
                self.assertEqual(version, OPENCODE_VERSION)
                result = execute_install(
                    REQUEST,
                    "opencode",
                    scope="project",
                    project_root=project,
                    home=home,
                )

            destination = Path(result.location)
            self.assertEqual(result.installation, "SUCCESS")
            self.assertEqual(result.file_verification, "SUCCESS")
            self.assertEqual(result.skill_discovery, "VERIFIED")
            self.assertTrue(verify_skill_tree(SKILL_SOURCE, destination))
            self.assertFalse(marker.exists(), "OpenCode executed a project plugin")
            self.assertEqual(
                len(list((destination / "references").rglob("*.md"))),
                20,
            )
            print(
                f"OpenCode {version}: project install, SHA-256 tree match, "
                "pure-mode discovery verified without executing a project plugin; "
                "invocation not attempted."
            )


if __name__ == "__main__":
    unittest.main()
