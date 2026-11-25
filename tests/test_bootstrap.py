import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.install_url import (
    ExistingInstallationError,
    InstallationError,
    PROJECT_VERSION,
    REPOSITORY,
    SKILL_NAME,
    SKILL_SOURCE,
    check_destination_collision,
    detect_platform,
    execute_install,
    is_install_request,
    load_registry,
    resolve_all_candidate_destinations,
    resolve_native_destinations,
    verify_skill_tree,
)

CANONICAL_URL = "https://github.com/krupakar5535Kk/typecraft-skills.git"
INSTALL_REQUEST = f"{CANONICAL_URL} Install this skill."


class TypeCraftBootstrapV13Tests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name).resolve()
        self.home = (self.root / "home").resolve()
        self.home.mkdir()
        self.project = (self.root / "project").resolve()
        self.project.mkdir()
        self.registry = load_registry()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_clean_first_installation_user_and_project_scope(self):
        """Clean first installation places all 21 canonical files and passes verification."""
        for agent in ("antigravity", "claude-code"):
            # User scope
            result_user = execute_install(
                INSTALL_REQUEST,
                agent,
                scope="user",
                source=SKILL_SOURCE,
                registry=self.registry,
                project_root=self.project,
                home=self.home,
            )
            dest_user = Path(result_user.location)
            self.assertEqual(result_user.file_verification, "SUCCESS")
            self.assertTrue(verify_skill_tree(SKILL_SOURCE, dest_user))
            self.assertEqual(len(list((dest_user / "references").rglob("*.md"))), 20)

            # Project scope
            result_proj = execute_install(
                INSTALL_REQUEST,
                agent,
                scope="project",
                source=SKILL_SOURCE,
                registry=self.registry,
                project_root=self.project,
                home=self.home,
            )
            dest_proj = Path(result_proj.location)
            self.assertEqual(result_proj.file_verification, "SUCCESS")
            self.assertTrue(verify_skill_tree(SKILL_SOURCE, dest_proj))

    def test_existing_identical_installation_skips_overwriting(self):
        """Identical installation is detected and reported as already installed without rewrite."""
        res1 = execute_install(
            INSTALL_REQUEST,
            "cursor",
            scope="user",
            source=SKILL_SOURCE,
            registry=self.registry,
            project_root=self.project,
            home=self.home,
        )
        self.assertEqual(res1.file_verification, "SUCCESS")

        res2 = execute_install(
            INSTALL_REQUEST,
            "cursor",
            scope="user",
            source=SKILL_SOURCE,
            registry=self.registry,
            project_root=self.project,
            home=self.home,
        )
        self.assertEqual(res2.installation, "FILES_ALREADY_PRESENT_DISCOVERY_UNVERIFIED")
        self.assertEqual(res2.file_verification, "SUCCESS")

    def test_modified_existing_installation_stops_safely(self):
        """Existing installation with user modifications stops safely and does not overwrite."""
        res = execute_install(
            INSTALL_REQUEST,
            "codex",
            scope="user",
            source=SKILL_SOURCE,
            registry=self.registry,
            project_root=self.project,
            home=self.home,
        )
        dest = Path(res.location)
        manifest = dest / "SKILL.md"
        manifest.write_text(manifest.read_text(encoding="utf-8") + "\n# User Custom Notes\n", encoding="utf-8")

        with self.assertRaises(ExistingInstallationError) as ctx:
            execute_install(
                INSTALL_REQUEST,
                "codex",
                scope="user",
                source=SKILL_SOURCE,
                registry=self.registry,
                project_root=self.project,
                home=self.home,
            )
        self.assertIn("differs from the current source", str(ctx.exception))
        # Confirm user changes were not wiped
        self.assertIn("User Custom Notes", manifest.read_text(encoding="utf-8"))

    def test_different_skill_name_collision_stops_safely(self):
        """Different skill with the same folder name triggers safe block without --force."""
        dest = self.home / ".agents" / "skills" / SKILL_NAME
        dest.mkdir(parents=True)
        (dest / "SKILL.md").write_text("---\nname: other-skill\n---\n# Unrelated Skill\n", encoding="utf-8")

        with self.assertRaises(ExistingInstallationError) as ctx:
            execute_install(
                INSTALL_REQUEST,
                "codex",
                scope="user",
                source=SKILL_SOURCE,
                registry=self.registry,
                project_root=self.project,
                home=self.home,
            )
        self.assertIn("Different or incomplete skill already exists", str(ctx.exception))

    def test_explicit_force_behavior_allows_update_and_replacement(self):
        """Passing overwrite=True (--force) merges or replaces after explicit approval."""
        res = execute_install(
            INSTALL_REQUEST,
            "opencode",
            scope="user",
            source=SKILL_SOURCE,
            registry=self.registry,
            project_root=self.project,
            home=self.home,
        )
        dest = Path(res.location)
        # Add a custom file to test extra file preservation on update
        custom_file = dest / "my_notes.txt"
        custom_file.write_text("keep my notes", encoding="utf-8")

        # Update with force
        updated = execute_install(
            INSTALL_REQUEST,
            "opencode",
            scope="user",
            source=SKILL_SOURCE,
            registry=self.registry,
            project_root=self.project,
            home=self.home,
            overwrite=True,
        )
        self.assertEqual(updated.file_verification, "SUCCESS")
        self.assertTrue(custom_file.is_file())
        self.assertEqual(custom_file.read_text(encoding="utf-8"), "keep my notes")

    def test_all_eight_supported_agent_mappings(self):
        """All 8 target agents resolve to distinct documented paths under home/project."""
        agents = [
            "antigravity",
            "antigravity-cli",
            "claude-code",
            "codex",
            "cursor",
            "gemini-cli",
            "opencode",
            "github-copilot",
        ]
        for agent in agents:
            candidates_user = resolve_all_candidate_destinations(
                agent, "user", registry=self.registry, project_root=self.project, home=self.home
            )
            self.assertTrue(len(candidates_user) >= 1)
            for c in candidates_user:
                self.assertTrue(str(c).startswith(str(self.home)))

            candidates_proj = resolve_all_candidate_destinations(
                agent, "project", registry=self.registry, project_root=self.project, home=self.home
            )
            self.assertTrue(len(candidates_proj) >= 1)
            for c in candidates_proj:
                self.assertTrue(str(c).startswith(str(self.project)))

        # Specific verification for codex candidate destinations including native $CODEX_HOME/skills
        codex_user = resolve_all_candidate_destinations(
            "codex", "user", registry=self.registry, project_root=self.project, home=self.home
        )
        self.assertIn(self.home / ".agents" / "skills" / "typecraft-skills", codex_user)
        self.assertIn(self.home / ".codex" / "skills" / "typecraft-skills", codex_user)

    def test_invalid_and_unrelated_repository_urls(self):
        """Installer rejects non-canonical or malicious URLs and informational queries."""
        self.assertFalse(is_install_request("https://github.com/attacker/malicious-skill.git"))
        self.assertFalse(is_install_request("https://github.com/krupakar5535Kk/typecraft-skills.evil"))
        self.assertFalse(is_install_request(f"What styles are included in {CANONICAL_URL}?"))
        self.assertFalse(is_install_request(f"Do not install {CANONICAL_URL}"))
        self.assertTrue(is_install_request(CANONICAL_URL))
        self.assertTrue(is_install_request(f"{CANONICAL_URL} Install this skill."))
        self.assertTrue(is_install_request(f"[{CANONICAL_URL}]({CANONICAL_URL})"))

    def test_active_agent_detection_and_signals(self):
        """Active agent is detected from TYPECRAFT_AGENT or unambiguous runtime signals."""
        self.assertEqual(detect_platform({"TYPECRAFT_AGENT": "antigravity"}), "antigravity")
        self.assertEqual(detect_platform({"CLAUDE_CODE": "1"}), "claude-code")
        self.assertEqual(detect_platform({"AGY_VERSION": "2.0.0"}), "antigravity")
        self.assertEqual(detect_platform({"CURSOR_AGENT": "1"}), "cursor")
        self.assertEqual(detect_platform({"OPENCODE": "1"}), "opencode")
        self.assertEqual(detect_platform({"AGY_CLI": "1"}), "antigravity-cli")
        # Preference to TYPECRAFT_AGENT over ambient signals
        self.assertEqual(
            detect_platform({"TYPECRAFT_AGENT": "codex", "CLAUDE_CODE": "1"}),
            "codex",
        )

    def test_unknown_or_ambiguous_agent_behavior_fails_closed(self):
        """Unknown runtime identity fails closed and requests explicit host ID."""
        self.assertIsNone(detect_platform({}))
        self.assertIsNone(detect_platform({"TYPECRAFT_AGENT": "auto"}))
        # Multiple conflicting signals without TYPECRAFT_AGENT return None
        self.assertIsNone(detect_platform({"CLAUDE_CODE": "1", "CURSOR_AGENT": "1"}))

        with self.assertRaises(InstallationError) as ctx:
            execute_install(
                INSTALL_REQUEST,
                "auto",
                source=SKILL_SOURCE,
                registry=self.registry,
                env={},
            )
        self.assertIn("Could not identify the active agent", str(ctx.exception))

    @patch("scripts.install_url.subprocess.run")
    @patch("scripts.install_url.shutil.which", return_value="/usr/local/bin/npx")
    def test_vercel_installer_execution_with_collision_protection(self, _which, mock_run):
        """Vercel installer executes npx skills add but stops before execution on collision."""
        target_dir = self.home / ".claude" / "skills" / SKILL_NAME

        def fake_npx(cmd, **kwargs):
            # Simulate npx installing canonical files
            shutil.copytree(SKILL_SOURCE, target_dir)
            return MagicMock(returncode=0, stdout="installed", stderr="")

        mock_run.side_effect = fake_npx

        # Clean install works
        res = execute_install(
            INSTALL_REQUEST,
            "claude-code",
            scope="user",
            source=SKILL_SOURCE,
            registry=self.registry,
            project_root=self.project,
            home=self.home,
            engine="vercel",
        )
        self.assertEqual(res.file_verification, "SUCCESS")
        self.assertTrue(mock_run.called)
        mock_run.reset_mock()

        # Modify file to induce collision
        (target_dir / "SKILL.md").write_text("Modified", encoding="utf-8")

        # Collision stops BEFORE npx is called
        with self.assertRaises(ExistingInstallationError):
            execute_install(
                INSTALL_REQUEST,
                "claude-code",
                scope="user",
                source=SKILL_SOURCE,
                registry=self.registry,
                project_root=self.project,
                home=self.home,
                engine="vercel",
            )
        # CRITICAL: Verify npx was NEVER called during the collision!
        self.assertFalse(mock_run.called)

    @patch("scripts.install_url.subprocess.run")
    @patch("scripts.install_url.shutil.which", return_value="/usr/bin/gh")
    def test_github_cli_fallback_with_collision_protection(self, _which, mock_run):
        """GitHub CLI fallback checks collisions before invoking gh skill install."""
        mock_run.return_value = MagicMock(returncode=0, stdout="github-copilot", stderr="")
        target_dir = self.home / ".copilot" / "skills" / SKILL_NAME
        target_dir.parent.mkdir(parents=True)
        target_dir.mkdir()
        (target_dir / "SKILL.md").write_text("Different skill", encoding="utf-8")

        with self.assertRaises(ExistingInstallationError):
            execute_install(
                INSTALL_REQUEST,
                "github-copilot",
                scope="user",
                source=SKILL_SOURCE,
                registry=self.registry,
                project_root=self.project,
                home=self.home,
                engine="gh",
            )
        # Confirm gh skill install command was NOT invoked
        install_calls = [
            call for call in mock_run.call_args_list
            if "install" in call.args[0] and REPOSITORY in call.args[0]
        ]
        self.assertEqual(len(install_calls), 0)

    def test_sha256_verification_detects_tampered_files(self):
        """SHA-256 verification detects corrupted or truncated reference files."""
        res = execute_install(
            INSTALL_REQUEST,
            "codex",
            scope="user",
            source=SKILL_SOURCE,
            registry=self.registry,
            project_root=self.project,
            home=self.home,
        )
        dest = Path(res.location)
        style_file = dest / "references" / "design-styles" / "art-deco-typographic-style.md"
        style_file.write_text("Corrupted content", encoding="utf-8")

        self.assertFalse(verify_skill_tree(SKILL_SOURCE, dest))

    def test_canonical_files_preservation(self):
        """Canonical skill has exactly 21 files, 10 approved styles, 10 approved templates."""
        files = sorted([p for p in SKILL_SOURCE.rglob("*") if p.is_file()])
        self.assertEqual(len(files), 21)
        styles = [p for p in files if "design-styles" in p.parts]
        templates = [p for p in files if "design-templates" in p.parts]
        self.assertEqual(len(styles), 10)
        self.assertEqual(len(templates), 10)
        manifest = SKILL_SOURCE / "SKILL.md"
        self.assertTrue(manifest.is_file())
        manifest_text = manifest.read_text(encoding="utf-8")
        self.assertIn("name: typecraft-skills", manifest_text)
        self.assertIn("# TypeCraft Skills", manifest_text)


if __name__ == "__main__":
    unittest.main()
