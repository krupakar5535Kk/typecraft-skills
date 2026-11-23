import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts.install_url import (
    ExistingInstallationError,
    InstallationError,
    SKILL_SOURCE,
    detect_platform,
    execute_install,
    get_route,
    is_install_request,
    load_registry,
    package_skill,
    resolve_native_destination,
    verify_skill_tree,
    _verify_cli_files,
    _verify_native_discovery,
)


URL = "https://github.com/krupakar5535Kk/typecraft-skills.git"
REQUEST = f"{URL} Install this skill."


class UniversalInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source = self.root / "canonical" / "typecraft-skills"
        (self.source / "references" / "design-styles").mkdir(parents=True)
        (self.source / "references" / "design-styles" / "style.md").write_text(
            "canonical reference\n", encoding="utf-8"
        )
        (self.source / "SKILL.md").write_text(
            "---\nname: typecraft-skills\ndescription: TypeCraft\n---\n"
            "# TypeCraft Skills\n",
            encoding="utf-8",
        )
        self.registry = load_registry()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_recognizes_url_alone_and_explicit_install_request(self):
        self.assertTrue(is_install_request(URL))
        self.assertTrue(is_install_request(URL.removesuffix(".git")))
        self.assertTrue(is_install_request(f"[{URL}]({URL})"))
        self.assertTrue(is_install_request(REQUEST))
        self.assertTrue(is_install_request(f"{URL}."))
        self.assertFalse(is_install_request(f"What is in this repository? {URL}"))
        self.assertFalse(is_install_request(f"How do I install this? {URL}"))
        self.assertFalse(is_install_request(f"Do not install this skill: {URL}"))
        self.assertFalse(
            is_install_request("https://github.com/krupakar5535Kk/typecraft-skills.evil")
        )
        self.assertFalse(is_install_request("https://github.com/example/other"))

    def test_detects_only_an_explicit_runtime_host_identity(self):
        self.assertEqual(
            detect_platform({"TYPECRAFT_AGENT": "codex"}),
            "codex",
        )
        self.assertIsNone(detect_platform({}))
        self.assertIsNone(detect_platform({"TYPECRAFT_AGENT": "auto"}))

    def test_routes_native_chatgpt_chat_only_and_cli_hosts(self):
        self.assertEqual(get_route("codex", self.registry), "native_directory")
        self.assertEqual(get_route("chatgpt", self.registry), "zip_upload")
        self.assertEqual(get_route("chat-only", self.registry), "session_only")
        self.assertEqual(get_route("github-copilot", self.registry), "github_cli")
        self.assertEqual(get_route("unknown-agent", self.registry), "unsupported")

    def test_resolves_documented_native_destinations(self):
        destination = resolve_native_destination(
            "codex",
            "user",
            self.registry,
            project_root=self.root / "project",
            home=self.root / "home",
        )
        self.assertEqual(
            destination,
            (self.root / "home" / ".agents" / "skills" / "typecraft-skills"),
        )

    def test_native_install_copies_complete_skill_and_does_not_replace_identical_copy(self):
        result = execute_install(
            REQUEST,
            "codex",
            source=self.source,
            registry=self.registry,
            project_root=self.root / "project",
            home=self.root / "home",
        )
        destination = Path(result.location)
        self.assertEqual(
            result.installation, "FILES_INSTALLED_DISCOVERY_UNVERIFIED"
        )
        self.assertEqual(result.file_verification, "SUCCESS")
        self.assertEqual(result.skill_discovery, "NOT_VERIFIED")
        self.assertTrue(verify_skill_tree(self.source, destination))

        repeated = execute_install(
            REQUEST,
            "codex",
            source=self.source,
            registry=self.registry,
            project_root=self.root / "project",
            home=self.root / "home",
        )
        self.assertEqual(
            repeated.installation, "FILES_ALREADY_PRESENT_DISCOVERY_UNVERIFIED"
        )

    def test_native_install_requires_explicit_approval_to_replace_different_skill(self):
        destination = resolve_native_destination(
            "codex", "user", self.registry, home=self.root / "home"
        )
        destination.mkdir(parents=True)
        (destination / "custom.txt").write_text("keep until approved", encoding="utf-8")

        with self.assertRaises(ExistingInstallationError):
            execute_install(
                REQUEST,
                "codex",
                source=self.source,
                registry=self.registry,
                home=self.root / "home",
            )
        self.assertTrue((destination / "custom.txt").exists())

        result = execute_install(
            REQUEST,
            "codex",
            source=self.source,
            registry=self.registry,
            home=self.root / "home",
            overwrite=True,
        )
        self.assertEqual(
            result.installation, "FILES_INSTALLED_DISCOVERY_UNVERIFIED"
        )
        self.assertFalse((destination / "custom.txt").exists())
        self.assertTrue(verify_skill_tree(self.source, destination))

    def test_zip_contains_entire_canonical_skill_and_requires_manual_upload(self):
        output = self.root / "typecraft-skills.zip"
        package, count = package_skill(self.source, output)
        self.assertEqual(package, output)
        self.assertEqual(count, 2)
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(
                set(archive.namelist()),
                {
                    "typecraft-skills/SKILL.md",
                    "typecraft-skills/references/design-styles/style.md",
                },
            )
            self.assertEqual(
                archive.read("typecraft-skills/references/design-styles/style.md"),
                b"canonical reference\n",
            )

        result = execute_install(
            REQUEST,
            "chatgpt",
            source=self.source,
            registry=self.registry,
            package_output=output.with_name("chatgpt.zip"),
        )
        self.assertEqual(result.installation, "PACKAGE_READY_USER_ACTION_REQUIRED")
        self.assertEqual(result.skill_discovery, "NOT_VERIFIED")
        self.assertIn("Upload", result.user_action_remaining)

    def test_canonical_skill_install_and_zip_keep_every_source_file(self):
        install_result = execute_install(
            REQUEST,
            "codex",
            source=SKILL_SOURCE,
            registry=self.registry,
            home=self.root / "home",
        )
        destination = Path(install_result.location)
        self.assertTrue(verify_skill_tree(SKILL_SOURCE, destination))

        output = self.root / "canonical-typecraft.zip"
        package, count = package_skill(SKILL_SOURCE, output)
        expected = {
            (Path("typecraft-skills") / path.relative_to(SKILL_SOURCE)).as_posix()
            for path in SKILL_SOURCE.rglob("*")
            if path.is_file()
        }
        with zipfile.ZipFile(package) as archive:
            self.assertEqual(set(archive.namelist()), expected)
        self.assertEqual(count, len(expected))

    def test_package_does_not_replace_an_existing_archive_without_approval(self):
        output = self.root / "typecraft-skills.zip"
        output.write_bytes(b"existing package")
        with self.assertRaises(ExistingInstallationError):
            package_skill(self.source, output)
        self.assertEqual(output.read_bytes(), b"existing package")

    def test_chat_only_fallback_never_claims_persistent_installation(self):
        result = execute_install(
            REQUEST,
            "chat-only",
            source=self.source,
            registry=self.registry,
        )
        self.assertEqual(result.installation, "NOT_PERSISTENTLY_SUPPORTED")
        self.assertEqual(result.skill_discovery, "NOT_SUPPORTED")

    @patch("scripts.install_url.subprocess.run")
    @patch("scripts.install_url.shutil.which", return_value="/usr/bin/gh")
    @patch("scripts.install_url._load_gh_inventory")
    def test_github_cli_route_checks_inventory_and_files(
        self, inventory, _which, run
    ):
        destination = self.root / "installed" / "typecraft-skills"
        shutil.copytree(self.source, destination)
        installed_row = {
            "skillName": "typecraft-skills",
            "sourceURL": URL,
            "agentHosts": ["github-copilot"],
            "scope": "user",
            "path": str(destination),
        }
        inventory.side_effect = [[], [installed_row]]
        run.return_value = SimpleNamespace(
            returncode=0, stdout="github-copilot", stderr=""
        )

        result = execute_install(
            REQUEST,
            "github-copilot",
            source=self.source,
            registry=self.registry,
        )
        self.assertEqual(
            result.installation, "FILES_INSTALLED_DISCOVERY_UNVERIFIED"
        )
        self.assertEqual(result.file_verification, "SUCCESS")
        self.assertEqual(result.skill_discovery, "NOT_VERIFIED")
        install_command = run.call_args_list[-1].args[0]
        self.assertEqual(
            install_command[:5],
            [
                "gh", "skill", "install", "krupakar5535Kk/typecraft-skills",
                "typecraft-skills",
            ],
        )
        self.assertNotIn("--force", install_command)

    def test_github_cli_verification_allows_tracking_metadata_only(self):
        destination = self.root / "installed" / "typecraft-skills"
        shutil.copytree(self.source, destination)
        row = {"path": str(destination)}
        manifest_path = destination / "SKILL.md"
        manifest_path.write_text(
            "---\nname: typecraft-skills\ndescription: TypeCraft\n"
            "metadata:\n  sourceURL: https://github.com/source/repo\n"
            "---\n# TypeCraft Skills\n",
            encoding="utf-8",
        )
        self.assertTrue(_verify_cli_files(self.source, row))

        manifest_path.write_text(
            manifest_path.read_text(encoding="utf-8").replace(
                "# TypeCraft Skills", "# Altered Skill"
            ),
            encoding="utf-8",
        )
        self.assertFalse(_verify_cli_files(self.source, row))

    @patch("scripts.install_url.subprocess.run")
    @patch("scripts.install_url.shutil.which", return_value="/usr/bin/gh")
    @patch("scripts.install_url._load_gh_inventory")
    def test_github_cli_refuses_to_replace_same_named_other_skill(
        self, inventory, _which, run
    ):
        inventory.return_value = [
            {
                "skillName": "typecraft-skills",
                "sourceURL": "https://github.com/someone/else",
                "agentHosts": ["github-copilot"],
                "scope": "user",
                "path": str(self.root / "installed" / "typecraft-skills"),
            }
        ]
        run.return_value = SimpleNamespace(
            returncode=0, stdout="github-copilot", stderr=""
        )

        with self.assertRaises(ExistingInstallationError):
            execute_install(
                REQUEST,
                "github-copilot",
                source=self.source,
                registry=self.registry,
            )
        self.assertEqual(run.call_count, 1)
        self.assertEqual(
            run.call_args.args[0], ["gh", "skill", "install", "--help"]
        )

    @patch("scripts.install_url.subprocess.run")
    @patch("scripts.install_url.shutil.which", return_value="/usr/bin/gh")
    @patch("scripts.install_url._load_gh_inventory", return_value=[])
    def test_github_cli_requires_advertised_host_support(
        self, _inventory, _which, run
    ):
        run.return_value = SimpleNamespace(
            returncode=0, stdout="codex", stderr=""
        )
        with self.assertRaisesRegex(InstallationError, "does not advertise support"):
            execute_install(
                REQUEST,
                "github-copilot",
                source=self.source,
                registry=self.registry,
            )
        self.assertEqual(run.call_count, 1)

    def test_auto_install_fails_closed_without_runtime_identity(self):
        with self.assertRaisesRegex(InstallationError, "Could not identify"):
            execute_install(
                REQUEST,
                "auto",
                source=self.source,
                registry=self.registry,
                env={},
            )

    @patch("scripts.install_url.subprocess.run")
    @patch("scripts.install_url.shutil.which", return_value="/usr/bin/gemini")
    def test_gemini_discovery_requires_a_positive_native_listing(self, _which, run):
        run.return_value = SimpleNamespace(returncode=0, stdout="typecraft-skills\n", stderr="")
        status, _ = _verify_native_discovery("gemini-cli")
        self.assertEqual(status, "VERIFIED")

        run.return_value = SimpleNamespace(returncode=0, stdout="other-skill\n", stderr="")
        status, _ = _verify_native_discovery("gemini-cli")
        self.assertEqual(status, "NOT_VERIFIED")

        run.return_value = SimpleNamespace(returncode=1, stdout="", stderr="not ready")
        status, message = _verify_native_discovery("gemini-cli")
        self.assertEqual(status, "NOT_VERIFIED")
        self.assertIn("not ready", message)

        run.return_value = SimpleNamespace(
            returncode=0, stdout="typecraft-skills\n", stderr=""
        )
        result = execute_install(
            REQUEST,
            "gemini-cli",
            source=self.source,
            registry=self.registry,
            home=self.root / "gemini-home",
        )
        self.assertEqual(result.installation, "SUCCESS")
        self.assertEqual(result.skill_discovery, "VERIFIED")
        self.assertIn("consent", result.user_action_remaining)


if __name__ == "__main__":
    unittest.main()
