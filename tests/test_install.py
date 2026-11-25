import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.install import find_installation, is_typecraft_installation

ROOT = Path(__file__).resolve().parents[1]


class FindInstallationTests(unittest.TestCase):
    def test_matches_repository_source_url(self):
        row = {
            "skillName": "typecraft-skills",
            "sourceURL": "https://github.com/krupakar5535Kk/typecraft-skills/",
            "scope": "user",
            "agentHosts": ["claude-code"],
        }
        self.assertTrue(is_typecraft_installation(row))
        self.assertIs(find_installation([row], "claude-code", "user"), row)

    def test_matches_shared_install_when_source_url_is_blank(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "typecraft-skills"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\nname: typecraft-skills\ndescription: Typography design\n---\n"
                "# TypeCraft Skills\n",
                encoding="utf-8",
            )
            row = {
                "skillName": "typecraft-skills",
                "sourceURL": "",
                "path": str(skill_dir),
                "scope": "user",
                "agentHosts": ["claude-code", "codex"],
            }
            self.assertTrue(is_typecraft_installation(row))
            self.assertIs(find_installation([row], "codex", "user"), row)

    def test_does_not_match_unrelated_or_incomplete_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "typecraft-skills"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\nname: another-skill\n---\n# Another Skill\n",
                encoding="utf-8",
            )
            row = {
                "skillName": "typecraft-skills",
                "sourceURL": "",
                "path": str(skill_dir),
                "scope": "user",
                "agentHosts": ["claude-code"],
            }
            self.assertFalse(is_typecraft_installation(row))
            self.assertIsNone(find_installation([row], "claude-code", "user"))

    def test_respects_agent_and_scope(self):
        row = {
            "skillName": "typecraft-skills",
            "sourceURL": "https://github.com/krupakar5535Kk/typecraft-skills",
            "scope": "user",
            "agentHosts": ["claude-code"],
        }
        self.assertIsNone(find_installation([row], "codex", "user"))
        self.assertIsNone(find_installation([row], "claude-code", "project"))


class DirectScriptExecutionTests(unittest.TestCase):
    def test_direct_script_execution_list_from_repo_root(self):
        """python scripts/install.py --list succeeds when executed from repository root."""
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "install.py"), "--list"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Stderr: {result.stderr}")
        self.assertIn("TYPECRAFT REGISTERED AGENTS", result.stdout)
        self.assertIn("antigravity", result.stdout)

    def test_direct_script_execution_list_from_scripts_dir(self):
        """python install.py --list succeeds when executed from inside scripts/ directory."""
        result = subprocess.run(
            [sys.executable, "install.py", "--list"],
            cwd=str(ROOT / "scripts"),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Stderr: {result.stderr}")
        self.assertIn("TYPECRAFT REGISTERED AGENTS", result.stdout)
        self.assertIn("antigravity", result.stdout)

    def test_direct_script_execution_list_from_arbitrary_dir(self):
        """python <path>/install.py --list succeeds when executed from an arbitrary cwd."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "install.py"), "--list"],
                cwd=temp_dir,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"Stderr: {result.stderr}")
            self.assertIn("TYPECRAFT REGISTERED AGENTS", result.stdout)

    def test_module_execution_list_from_repo_root(self):
        """python -m scripts.install --list succeeds when executed from repository root."""
        result = subprocess.run(
            [sys.executable, "-m", "scripts.install", "--list"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Stderr: {result.stderr}")
        self.assertIn("TYPECRAFT REGISTERED AGENTS", result.stdout)

    def test_direct_install_url_execution_help(self):
        """python scripts/install_url.py --help succeeds from arbitrary directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "install_url.py"), "--help"],
                cwd=temp_dir,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"Stderr: {result.stderr}")
            self.assertIn("usage:", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
