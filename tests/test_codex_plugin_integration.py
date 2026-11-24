import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CODEX_VERSION = "0.172.0"
REPOSITORY_URL = "https://github.com/krupakar5535Kk/typecraft-skills"
INSTALL_REQUEST = f"{REPOSITORY_URL} Install this skill."

import sys

sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.install_url import SKILL_SOURCE, is_install_request, verify_skill_tree


class CodexPluginIntegrationTests(unittest.TestCase):
    def test_url_request_installs_and_discovers_plugin_in_isolated_codex_home(self):
        executable = shutil.which("codex")
        if not executable:
            self.skipTest("Codex CLI is not installed")
        self.assertTrue(is_install_request(INSTALL_REQUEST))

        with tempfile.TemporaryDirectory(
            prefix="typecraft-codex-test-",
            dir=Path.home(),
        ) as temp_dir:
            codex_home = Path(temp_dir) / ".codex"
            codex_home.mkdir()
            environment = {
                key: value
                for key, value in os.environ.items()
                if not any(
                    marker in key.upper()
                    for marker in (
                        "TOKEN",
                        "PASSWORD",
                        "SECRET",
                        "CREDENTIAL",
                        "API_KEY",
                    )
                )
                and not key.upper().startswith("CODEX_")
            }
            environment["CODEX_HOME"] = str(codex_home)

            def run(*arguments):
                result = subprocess.run(
                    [executable, *arguments],
                    cwd=REPOSITORY_ROOT,
                    env=environment,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=120,
                )
                self.assertEqual(
                    result.returncode,
                    0,
                    result.stderr or result.stdout,
                )
                return result.stdout.strip()

            version = run("--version")
            self.assertIn(CODEX_VERSION, version)

            run("plugin", "marketplace", "add", str(REPOSITORY_ROOT), "--json")
            available = json.loads(
                run("plugin", "list", "--available", "--json")
            )
            self.assertTrue(
                any(
                    item.get("pluginId") == "typecraft-skills@typecraft-skills"
                    for item in available["available"]
                )
            )

            installed = json.loads(
                run(
                    "plugin",
                    "add",
                    "typecraft-skills@typecraft-skills",
                    "--json",
                )
            )
            self.assertEqual(installed["version"], "1.2.0")
            skill_directory = (
                Path(installed["installedPath"])
                / "skills"
                / "typecraft-skills"
            )
            self.assertTrue(verify_skill_tree(SKILL_SOURCE, skill_directory))

            inventory = json.loads(run("plugin", "list", "--json"))
            installed_entry = next(
                item
                for item in inventory["installed"]
                if item.get("pluginId") == "typecraft-skills@typecraft-skills"
            )
            self.assertTrue(installed_entry["installed"])
            self.assertTrue(installed_entry["enabled"])
            self.assertEqual(
                Path(installed_entry["source"]["path"]).resolve(),
                REPOSITORY_ROOT.resolve(),
            )
            print(
                f"Codex CLI {version}: canonical URL request recognized; "
                "marketplace plugin installed in isolated CODEX_HOME, all files "
                "SHA-256 verified, and native plugin inventory confirmed. "
                "Invocation was not attempted without model authentication."
            )


if __name__ == "__main__":
    unittest.main()
