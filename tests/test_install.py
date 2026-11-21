import tempfile
import unittest
from pathlib import Path

from scripts.install import find_installation, is_typecraft_installation


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


if __name__ == "__main__":
    unittest.main()
