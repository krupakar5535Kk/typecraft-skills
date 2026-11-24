import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
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
    main,
    package_skill,
    resolve_native_destination,
    resolve_native_destinations,
    print_result,
    verify_skill_tree,
    _verify_cli_files,
    _verify_native_discovery,
    _verify_zip_archive,
)


URL = "https://github.com/krupakar5535Kk/typecraft-skills.git"
REQUEST = f"{URL} Install this skill."


class UniversalInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source = self.root / "canonical" / "typecraft-skills"
        (self.source / "references" / "design-styles").mkdir(parents=True)
        (self.source / "references" / "design-styles" / "style.md").write_bytes(
            b"canonical reference\n"
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
        self.assertTrue(
            is_install_request(f"[TypeCraft skills]({URL.removesuffix('.git')})")
        )
        self.assertTrue(is_install_request(f"<{URL}>"))
        self.assertTrue(is_install_request(f"[Install]({URL})"))
        self.assertTrue(is_install_request(REQUEST))
        self.assertTrue(is_install_request(f"{URL}."))
        self.assertTrue(is_install_request(f"{URL},"))
        self.assertTrue(is_install_request(f"{URL}!"))
        self.assertFalse(is_install_request(f"What is in this repository? {URL}"))
        self.assertFalse(is_install_request(f"Can you explain this URL? {URL}"))
        self.assertFalse(is_install_request(f"How do I install this? {URL}"))
        self.assertFalse(is_install_request(f"Do not install this skill: {URL}"))
        self.assertFalse(
            is_install_request("https://github.com/krupakar5535Kk/typecraft-skills.evil")
        )
        self.assertFalse(
            is_install_request(
                "https://github.com.evil.example/krupakar5535Kk/typecraft-skills"
            )
        )
        self.assertFalse(
            is_install_request(
                "https://github.com@evil.example/krupakar5535Kk/typecraft-skills"
            )
        )
        self.assertFalse(
            is_install_request("http://github.com/krupakar5535Kk/typecraft-skills")
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

    def test_routes_cline_roo_and_kilo_to_their_native_directories(self):
        project = self.root / "project"
        home = self.root / "home"
        expected = {
            "cline": (".cline", "~/.cline"),
            "roo": (".roo", "~/.roo"),
            "kilo": (".kilo", "~/.kilo"),
        }
        for platform, (project_directory, user_directory) in expected.items():
            with self.subTest(platform=platform):
                self.assertEqual(get_route(platform, self.registry), "native_directory")
                project_path = resolve_native_destination(
                    platform,
                    "project",
                    self.registry,
                    project_root=project,
                    home=home,
                )
                user_path = resolve_native_destination(
                    platform,
                    "user",
                    self.registry,
                    project_root=project,
                    home=home,
                )
                self.assertEqual(
                    project_path,
                    project / project_directory / "skills" / "typecraft-skills",
                )
                self.assertEqual(
                    user_path,
                    home / user_directory.removeprefix("~/") / "skills"
                    / "typecraft-skills",
                )
                self.assertEqual(
                    self.registry["platforms"][platform]["compatibility"],
                    "compatible",
                )
                self.assertEqual(
                    self.registry["platforms"][platform][
                        "runtime_discovery_verification"
                    ],
                    "not_tested",
                )

    def test_routes_every_advertised_github_cli_host_and_registered_native_adapter(self):
        for agent_id in self.registry["installers"]["github_cli"]["supported_agents"]:
            with self.subTest(agent_id=agent_id):
                route = (
                    "native_directory"
                    if agent_id in self.registry["native_adapters"]
                    else "github_cli"
                )
                self.assertEqual(get_route(agent_id, self.registry), route)
        for agent_id in self.registry["native_adapters"]:
            with self.subTest(agent_id=agent_id):
                self.assertEqual(get_route(agent_id, self.registry), "native_directory")

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
            (self.root / "home" / ".agents" / "skills" / "typecraft-skills").resolve(),
        )

    def test_rejects_registry_path_traversal(self):
        unsafe_registry = dict(self.registry)
        unsafe_adapter = dict(self.registry["native_adapters"]["codex"])
        unsafe_adapter["scope_paths"] = {
            "user": "~/.agents/skills",
            "project": "../outside",
        }
        unsafe_registry["native_adapters"] = {
            **self.registry["native_adapters"],
            "codex": unsafe_adapter,
        }
        with self.assertRaisesRegex(InstallationError, "Unsafe installation path"):
            resolve_native_destination(
                "codex",
                "project",
                unsafe_registry,
                project_root=self.root / "project",
            )

    def test_antigravity_app_and_cli_have_documented_surface_specific_routes(self):
        project = self.root / "project"
        home = self.root / "home"
        self.assertEqual(get_route("antigravity", self.registry), "native_directory")
        self.assertEqual(
            get_route("antigravity-cli", self.registry), "native_directory"
        )

        app_destination = resolve_native_destination(
            "antigravity",
            "user",
            self.registry,
            project_root=project,
            home=home,
        )
        self.assertEqual(
            app_destination,
            (home / ".gemini" / "config" / "skills" / "typecraft-skills").resolve(),
        )

        app_project_destination = resolve_native_destination(
            "antigravity",
            "project",
            self.registry,
            project_root=project,
            home=home,
        )
        self.assertEqual(
            app_project_destination,
            (project / ".agents" / "skills" / "typecraft-skills").resolve(),
        )

        cli_destinations = resolve_native_destinations(
            "antigravity-cli",
            "user",
            self.registry,
            project_root=project,
            home=home,
        )
        self.assertEqual(
            cli_destinations,
            [
                (
                    home
                    / ".gemini"
                    / "antigravity-cli"
                    / "skills"
                    / "typecraft-skills"
                ).resolve(),
                (home / ".gemini" / "config" / "skills" / "typecraft-skills").resolve(),
                (home / ".gemini" / "skills" / "typecraft-skills").resolve(),
            ],
        )
        self.assertEqual(
            self.registry["platforms"]["antigravity"]["compatibility"], "compatible"
        )
        self.assertEqual(
            self.registry["platforms"]["antigravity_cli"]["compatibility"],
            "compatible",
        )
        self.assertIn("antigravity-cli", self.registry["native_adapters"])
        self.assertEqual(
            get_route("github-copilot-cli", self.registry), "native_directory"
        )
        cli = self.registry["platforms"]["antigravity_cli"]
        self.assertEqual(cli["runtime_discovery_verification"], "not_tested")

    def test_antigravity_cli_installs_files_without_claiming_runtime_discovery(self):
        project = self.root / "project"
        project.mkdir()
        home = self.root / "home"
        result = execute_install(
            REQUEST,
            "antigravity-cli",
            source=self.source,
            registry=self.registry,
            project_root=project,
            home=home,
        )
        self.assertEqual(
            result.installation, "FILES_INSTALLED_DISCOVERY_UNVERIFIED"
        )
        self.assertEqual(result.file_verification, "SUCCESS")
        self.assertEqual(result.skill_discovery, "NOT_VERIFIED")
        self.assertEqual(
            Path(result.location).parts[-4:],
            (".gemini", "antigravity-cli", "skills", "typecraft-skills"),
        )
        self.assertIn("/skills reload", result.user_action_remaining)

    def test_copilot_cli_discovery_requires_the_exact_installed_path(self):
        destination = self.root / "project" / ".github" / "skills" / "typecraft-skills"
        inventory = json.dumps([
            {
                "name": "typecraft-skills",
                "path": str(destination),
                "source": "project",
                "enabled": True,
            }
        ])
        with (
            patch("scripts.install_url.shutil.which", return_value="/usr/bin/copilot"),
            patch(
                "scripts.install_url.subprocess.run",
                return_value=subprocess.CompletedProcess(
                    args=[], returncode=0, stdout=inventory, stderr=""
                ),
            ) as run,
        ):
            status, message = _verify_native_discovery(
                "github-copilot-cli",
                cwd=destination.parents[2],
                destination=destination,
            )
        self.assertEqual(status, "VERIFIED")
        self.assertIn("at the installed location", message)
        self.assertEqual(
            run.call_args.args[0],
            ["/usr/bin/copilot", "skill", "list", "--json"],
        )

        other_path = destination.parent / "other-skill"
        other_inventory = json.dumps([
            {
                "name": "typecraft-skills",
                "path": str(other_path),
                "source": "project",
                "enabled": True,
            }
        ])
        with (
            patch("scripts.install_url.shutil.which", return_value="/usr/bin/copilot"),
            patch(
                "scripts.install_url.subprocess.run",
                return_value=subprocess.CompletedProcess(
                    args=[], returncode=0,
                    stdout=other_inventory,
                    stderr="",
                ),
            ),
        ):
            status, message = _verify_native_discovery(
                "github-copilot-cli",
                cwd=destination.parents[2],
                destination=destination,
            )
        self.assertEqual(status, "NOT_VERIFIED")
        self.assertIn("did not list", message)

    def test_opencode_discovery_requires_the_exact_installed_manifest(self):
        destination = self.root / "project" / ".agents" / "skills" / "typecraft-skills"
        inventory = json.dumps([
            {
                "name": "typecraft-skills",
                "location": str(destination / "SKILL.md"),
            }
        ])
        with (
            patch("scripts.install_url.shutil.which", return_value="/usr/bin/opencode"),
            patch(
                "scripts.install_url.subprocess.run",
                return_value=subprocess.CompletedProcess(
                    args=[], returncode=0, stdout=inventory, stderr=""
                ),
            ) as run,
        ):
            status, message = _verify_native_discovery(
                "opencode",
                cwd=destination.parents[3],
                destination=destination,
            )
        self.assertEqual(status, "VERIFIED")
        self.assertIn("at the installed location", message)
        self.assertEqual(
            run.call_args.args[0],
            ["/usr/bin/opencode", "--pure", "debug", "skill"],
        )

        other_path = destination.parent / "other-skill" / "SKILL.md"
        other_inventory = json.dumps([
            {"name": "typecraft-skills", "location": str(other_path)}
        ])
        with (
            patch("scripts.install_url.shutil.which", return_value="/usr/bin/opencode"),
            patch(
                "scripts.install_url.subprocess.run",
                return_value=subprocess.CompletedProcess(
                    args=[], returncode=0, stdout=other_inventory, stderr=""
                ),
            ),
        ):
            status, message = _verify_native_discovery(
                "opencode",
                cwd=destination.parents[3],
                destination=destination,
            )
        self.assertEqual(status, "NOT_VERIFIED")
        self.assertIn("did not list", message)

    def test_registry_rejects_runtime_verified_status_without_test_evidence(self):
        repository_root = Path(__file__).resolve().parents[1]
        registry_text = (
            repository_root / "registry" / "agents.yaml"
        ).read_text(encoding="utf-8")
        unverified_claim = registry_text.replace(
            "    compatibility: compatible\n"
            "    official_documentation_url: https://antigravity.google/docs/skills\n",
            "    compatibility: verified\n"
            "    official_documentation_url: https://antigravity.google/docs/skills\n",
            1,
        ).replace(
            "      kind: documentation_review\n"
            "      environment: \"Official Antigravity skills documentation reviewed; Antigravity App was not run and TypeCraft was not installed.\"\n",
            "      kind: historical_runtime_test\n"
            "      environment: \"Runtime test environment not recorded.\"\n",
            1,
        )
        self.assertNotEqual(unverified_claim, registry_text)

        registry = self.root / "registry"
        registry.mkdir()
        (registry / "agents.yaml").write_text(
            unverified_claim, encoding="utf-8"
        )
        result = subprocess.run(
            [sys.executable, str(repository_root / "scripts" / "validate_agent_registry.py")],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "verified compatibility requires complete runtime evidence",
            result.stdout,
        )

    def test_copilot_runtime_verification_records_tested_environment_and_references(self):
        platforms = self.registry["platforms"]
        verified = [
            platform_id
            for platform_id, platform in platforms.items()
            if platform["compatibility"] == "verified"
        ]
        self.assertEqual(
            verified,
            [
                "github_copilot",
                "github_copilot_cli",
                "opencode",
                "gemini_cli",
            ],
        )
        opencode = platforms["opencode"]
        self.assertEqual(
            opencode["runtime_verification"]["installation"]["sha256_tree_match"],
            "true",
        )
        self.assertEqual(
            opencode["runtime_verification"]["skill_discovery"]["command"],
            "opencode --pure debug skill",
        )
        self.assertEqual(
            opencode["skill_invocation_verification"], "not_tested"
        )

        verification = platforms["github_copilot"]["runtime_verification"]
        self.assertEqual(verification["tested_at"], "2026-11-23")
        self.assertEqual(verification["skill_version"], "1.1.0")
        self.assertEqual(
            verification["environment"],
            {
                "product": "GitHub Copilot",
                "editor": "Visual Studio Code",
                "host": "GitHub Codespaces",
                "session": "Fresh Copilot Agent session",
            },
        )
        self.assertEqual(
            verification["installation"],
            {
                "tested": "true",
                "scope": "user",
                "method": "github_cli_managed",
                "path": "/home/codespace/.copilot/skills/typecraft-skills/",
                "skill_manifest_present": "true",
                "reference_files_present": "20",
            },
        )
        self.assertEqual(
            verification["invocation"]["references_exercised"],
            [
                "Art Deco Typographic Style",
                "Swiss International Typographic Style",
                "E-commerce Product Showcase Layout",
                "Cinematic Title Poster",
            ],
        )
        copilot_cli = platforms["github_copilot_cli"]
        self.assertEqual(copilot_cli["runtime_verification"]["skill_version"], "1.2.0")
        self.assertEqual(
            copilot_cli["runtime_verification"]["environment"]["cli_version"],
            "1.0.105",
        )
        self.assertEqual(
            copilot_cli["runtime_verification"]["installation"]["scope"], "project"
        )
        self.assertEqual(
            copilot_cli["runtime_verification"]["installation"]["reference_files_present"],
            "20",
        )
        self.assertEqual(
            copilot_cli["runtime_verification"]["skill_discovery"]["result"],
            "confirmed",
        )
        self.assertEqual(
            copilot_cli["runtime_verification"]["invocation"]["references_exercised"],
            ["Swiss International Typographic Style", "Cinematic Title Poster"],
        )
        copilot = next(
            entry
            for entry in self.registry["agent_catalog"]
            if entry["agent_id"] == "github-copilot"
        )
        self.assertEqual(copilot["installation_verified"], "true")
        self.assertEqual(copilot["skill_discovery_verified"], "true")
        gemini = next(
            entry
            for entry in self.registry["agent_catalog"]
            if entry["agent_id"] == "gemini-cli"
        )
        self.assertEqual(gemini["installation_verified"], "true")
        self.assertEqual(gemini["skill_discovery_verified"], "true")
        gemini_platform = platforms["gemini_cli"]
        self.assertEqual(
            gemini_platform["skill_invocation_verification"], "not_tested"
        )
        self.assertEqual(
            gemini_platform["runtime_verification"]["invocation"]["tested"],
            "false",
        )
        self.assertTrue(
            all(
                entry["installation_verified"] == "false"
                and entry["skill_discovery_verified"] == "false"
                for entry in self.registry["agent_catalog"]
                if entry["agent_id"]
                not in {
                    "github-copilot",
                    "github-copilot-cli",
                    "gemini-cli",
                    "opencode",
                }
            )
        )

    def test_registry_rejects_verified_platform_without_matching_installer_evidence(self):
        repository_root = Path(__file__).resolve().parents[1]
        registry_text = (
            repository_root / "registry" / "agents.yaml"
        ).read_text(encoding="utf-8")
        invalid_registry = registry_text.replace(
            "    installation_verified: true\n"
            "    skill_discovery_verified: true\n",
            "    installation_verified: false\n"
            "    skill_discovery_verified: false\n",
            1,
        )
        self.assertNotEqual(invalid_registry, registry_text)

        registry = self.root / "registry"
        registry.mkdir()
        (registry / "agents.yaml").write_text(
            invalid_registry, encoding="utf-8"
        )
        result = subprocess.run(
            [
                sys.executable,
                str(repository_root / "scripts" / "validate_agent_registry.py"),
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "verified compatibility requires complete runtime evidence "
            "and matching verified installer metadata",
            result.stdout,
        )

    def test_compatibility_matrix_covers_every_github_cli_host_id(self):
        repository_root = Path(__file__).resolve().parents[1]
        contents = (
            repository_root / "docs" / "compatibility.md"
        ).read_text(encoding="utf-8")
        documented_ids = [
            line.split("|", 2)[1].strip().strip("`")
            for line in contents.splitlines()
            if line.startswith("| `")
        ]
        allowed_statuses = {
            "verified",
            "compatible",
            "research_required",
            "unsupported",
        }
        matrix_statuses = [
            line.split("|")[3].strip()
            for line in contents.splitlines()
            if line.startswith("| `")
        ]
        catalog_ids = [
            entry["agent_id"] for entry in self.registry["agent_catalog"]
        ]
        self.assertEqual(len(documented_ids), len(set(documented_ids)))
        self.assertCountEqual(documented_ids, catalog_ids)
        self.assertTrue(set(matrix_statuses).issubset(allowed_statuses))

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
        self.assertEqual(result.version, self.registry["project_version"])

        output = io.StringIO()
        with redirect_stdout(output):
            print_result(result, json_output=True)
        report = json.loads(output.getvalue())
        self.assertEqual(report["platform"], "codex")
        self.assertEqual(report["version"], self.registry["project_version"])
        self.assertEqual(report["file_verification"], "SUCCESS")
        self.assertEqual(report["skill_discovery"], "NOT_VERIFIED")

    def test_all_native_adapters_install_complete_skill_at_both_scopes(self):
        with patch("scripts.install_url.shutil.which", return_value=None):
            for platform in self.registry["native_adapters"]:
                for scope in ("user", "project"):
                    root = self.root / f"{platform}-{scope}"
                    project = root / "project"
                    project.mkdir(parents=True)
                    home = root / "home"

                    result = execute_install(
                        REQUEST,
                        platform,
                        scope=scope,
                        source=SKILL_SOURCE,
                        registry=self.registry,
                        project_root=project,
                        home=home,
                    )
                    destination = Path(result.location)
                    self.assertEqual(
                        result.installation,
                        "FILES_INSTALLED_DISCOVERY_UNVERIFIED",
                    )
                    self.assertTrue(verify_skill_tree(SKILL_SOURCE, destination))
                    self.assertEqual(
                        len(list((destination / "references").rglob("*.md"))),
                        20,
                    )

                    repeated = execute_install(
                        REQUEST,
                        platform,
                        scope=scope,
                        source=SKILL_SOURCE,
                        registry=self.registry,
                        project_root=project,
                        home=home,
                    )
                    self.assertEqual(
                        repeated.installation,
                        "FILES_ALREADY_PRESENT_DISCOVERY_UNVERIFIED",
                    )

    def test_file_verification_detects_missing_and_modified_reference_files(self):
        destination = self.root / "installed"
        shutil.copytree(self.source, destination)
        self.assertTrue(verify_skill_tree(self.source, destination))
        reference = destination / "references" / "design-styles" / "style.md"
        reference.unlink()
        self.assertFalse(verify_skill_tree(self.source, destination))
        reference.parent.mkdir(parents=True, exist_ok=True)
        reference.write_text("changed reference\n", encoding="utf-8")
        self.assertFalse(verify_skill_tree(self.source, destination))

    def test_existing_shared_alias_prevents_duplicate_installation(self):
        alias = self.root / "home" / ".cursor" / "skills" / "typecraft-skills"
        alias.parent.mkdir(parents=True)
        shutil.copytree(self.source, alias)
        result = execute_install(
            REQUEST,
            "cursor",
            source=self.source,
            registry=self.registry,
            home=self.root / "home",
        )
        self.assertEqual(
            result.installation, "FILES_ALREADY_PRESENT_DISCOVERY_UNVERIFIED"
        )
        self.assertEqual(Path(result.location), alias.resolve())
        self.assertFalse(
            (self.root / "home" / ".agents" / "skills" / "typecraft-skills").exists()
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
        self.assertTrue((destination / "custom.txt").exists())
        self.assertTrue(
            verify_skill_tree(self.source, destination, allow_extra_files=True)
        )

    def test_explicit_update_preserves_extra_files_in_a_known_typecraft_copy(self):
        destination = resolve_native_destination(
            "codex", "user", self.registry, home=self.root / "home"
        )
        destination.mkdir(parents=True)
        shutil.copy2(self.source / "SKILL.md", destination / "SKILL.md")
        (destination / "user-notes.txt").write_text("keep me", encoding="utf-8")
        (destination / "references").mkdir()

        with self.assertRaisesRegex(ExistingInstallationError, "update available"):
            execute_install(
                REQUEST,
                "codex",
                source=self.source,
                registry=self.registry,
                home=self.root / "home",
            )

        result = execute_install(
            REQUEST,
            "codex",
            source=self.source,
            registry=self.registry,
            home=self.root / "home",
            overwrite=True,
        )
        self.assertEqual(result.installation, "FILES_UPDATED_DISCOVERY_UNVERIFIED")
        self.assertEqual((destination / "user-notes.txt").read_text(), "keep me")
        self.assertTrue(verify_skill_tree(self.source, destination, allow_extra_files=True))

    def test_refuses_symlinked_source_and_destination(self):
        source_link = self.root / "linked-source"
        home = self.root / "home"
        destination = home / ".agents" / "skills" / "typecraft-skills"
        try:
            source_link.symlink_to(self.source, target_is_directory=True)
            destination.parent.mkdir(parents=True)
            destination.symlink_to(self.root / "outside", target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Directory symlinks are unavailable on this platform")

        with self.assertRaisesRegex(InstallationError, "source cannot be a symlink"):
            verify_skill_tree(source_link, self.root / "unused")
        with self.assertRaisesRegex(InstallationError, "Refusing to replace a symlink"):
            execute_install(
                REQUEST,
                "codex",
                source=self.source,
                registry=self.registry,
                home=home,
            )

    def test_failed_atomic_replace_restores_existing_directory(self):
        destination = resolve_native_destination(
            "codex", "user", self.registry, home=self.root / "home"
        )
        destination.mkdir(parents=True)
        shutil.copytree(self.source, destination, dirs_exist_ok=True)
        (destination / "user-notes.txt").write_text("preserve", encoding="utf-8")
        real_replace = __import__("os").replace
        replacements = 0

        def fail_install(source, target):
            nonlocal replacements
            replacements += 1
            if replacements == 2:
                raise OSError("simulated rename failure")
            return real_replace(source, target)

        with patch("scripts.install_url.os.replace", side_effect=fail_install):
            with self.assertRaisesRegex(InstallationError, "previous directory was restored"):
                execute_install(
                    REQUEST,
                    "codex",
                    source=self.source,
                    registry=self.registry,
                    home=self.root / "home",
                    overwrite=True,
                )
        self.assertTrue((destination / "user-notes.txt").exists())
        self.assertTrue(verify_skill_tree(self.source, destination, allow_extra_files=True))

    def test_zip_contains_entire_canonical_skill_and_requires_manual_upload(self):
        output = self.root / "typecraft-skills.zip"
        package, count = package_skill(self.source, output)
        self.assertEqual(package, output.resolve())
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
        self.assertIn("upload", result.user_action_remaining.lower())

    def test_claude_chat_and_cowork_use_zip_upload_routes(self):
        for platform in ("claude_ai", "claude_cowork", "chatgpt"):
            with self.subTest(platform=platform):
                result = execute_install(
                    REQUEST,
                    platform,
                    source=self.source,
                    registry=self.registry,
                    package_output=self.root / f"{platform}.zip",
                )
                self.assertEqual(
                    get_route(platform, self.registry), "zip_upload"
                )
                self.assertEqual(
                    result.installation, "PACKAGE_READY_USER_ACTION_REQUIRED"
                )
                self.assertEqual(result.skill_discovery, "NOT_VERIFIED")
                self.assertIn("upload", result.user_action_remaining.lower())

    @patch("scripts.install_url.execute_install", side_effect=PermissionError("denied"))
    def test_cli_reports_filesystem_errors_without_a_traceback(self, _install):
        output = io.StringIO()
        with redirect_stderr(output):
            exit_code = main(
                [
                    "--request",
                    REQUEST,
                    "--agent",
                    "codex",
                ]
            )
        self.assertEqual(exit_code, 1)
        self.assertIn("File or process operation failed: denied", output.getvalue())

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
        references = [name for name in expected if name.startswith("typecraft-skills/references/")]
        self.assertEqual(len(references), 20)
        self.assertEqual(len([name for name in references if "/design-styles/" in name]), 10)
        self.assertEqual(len([name for name in references if "/design-templates/" in name]), 10)
        self.assertTrue(
            _verify_zip_archive(
                package,
                SKILL_SOURCE.resolve(),
                [path for path in SKILL_SOURCE.rglob("*") if path.is_file()],
            )
        )

    def test_package_does_not_replace_an_existing_archive_without_approval(self):
        output = self.root / "typecraft-skills.zip"
        output.write_bytes(b"existing package")
        with self.assertRaises(ExistingInstallationError):
            package_skill(self.source, output)
        self.assertEqual(output.read_bytes(), b"existing package")

    def test_zip_verification_detects_corrupt_archive_bytes(self):
        output = self.root / "typecraft-skills.zip"
        package, _ = package_skill(self.source, output)

        source_files = sorted(path for path in self.source.rglob("*") if path.is_file())
        self.assertTrue(_verify_zip_archive(package, self.source.resolve(), source_files))
        with zipfile.ZipFile(output, "w") as archive:
            archive.writestr("typecraft-skills/SKILL.md", "modified")
        self.assertFalse(_verify_zip_archive(output, self.source.resolve(), source_files))

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
            f"---\nname: typecraft-skills\ndescription: TypeCraft\n"
            f"metadata:\n  sourceURL: {URL}\n"
            "---\n# TypeCraft Skills\n",
            encoding="utf-8",
        )
        self.assertTrue(_verify_cli_files(self.source, row))

        invalid_manifests = (
            f"---\nname: typecraft-skills\ndescription: TypeCraft\n"
            "metadata:\n  sourceURL: https://github.com/attacker/repo\n"
            "---\n# TypeCraft Skills\n",
            f"---\nname: typecraft-skills\ndescription: TypeCraft\n"
            f"metadata:\n  sourceURL: {URL}\n  permissions: [network]\n"
            "---\n# TypeCraft Skills\n",
            f"---\nname: typecraft-skills\ndescription: Altered\n"
            f"metadata:\n  sourceURL: {URL}\n"
            "---\n# TypeCraft Skills\n",
            f"---\nname: typecraft-skills\ndescription: TypeCraft\n"
            f"metadata:\n  sourceURL: {URL}\n"
            "---\n# Altered Skill\n",
        )
        for manifest in invalid_manifests:
            with self.subTest(manifest=manifest):
                manifest_path.write_text(manifest, encoding="utf-8")
                self.assertFalse(_verify_cli_files(self.source, row))

    @patch("scripts.install_url.subprocess.run")
    @patch("scripts.install_url.shutil.which", return_value="/usr/bin/gh")
    @patch("scripts.install_url._load_gh_inventory")
    def test_github_cli_project_install_uses_requested_project_root(
        self, inventory, _which, run
    ):
        project = self.root / "project"
        project.mkdir()
        destination = project / ".agents" / "skills" / "typecraft-skills"
        destination.parent.mkdir(parents=True)
        shutil.copytree(self.source, destination)
        inventory.side_effect = [
            [],
            [{
                "skillName": "typecraft-skills",
                "sourceURL": URL,
                "agentHosts": ["github-copilot"],
                "scope": "project",
                "path": str(destination),
            }],
        ]
        run.return_value = SimpleNamespace(
            returncode=0, stdout="github-copilot", stderr=""
        )

        result = execute_install(
            REQUEST,
            "github-copilot",
            scope="project",
            source=self.source,
            registry=self.registry,
            project_root=project,
        )

        self.assertEqual(
            result.installation, "FILES_INSTALLED_DISCOVERY_UNVERIFIED"
        )
        self.assertTrue(
            all(call.kwargs.get("cwd") == project.resolve() for call in inventory.call_args_list)
        )
        self.assertTrue(
            all(call.kwargs.get("cwd") == project.resolve() for call in run.call_args_list)
        )

    @unittest.skipUnless(shutil.which("gh"), "GitHub CLI is not installed")
    def test_real_github_cli_installs_and_discovers_complete_skill_in_temp_project(self):
        help_result = subprocess.run(
            ["gh", "skill", "install", "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        if help_result.returncode:
            self.skipTest("Installed GitHub CLI has no Agent Skills support")

        repository_root = Path(__file__).resolve().parents[1]
        source = SKILL_SOURCE.resolve()
        with tempfile.TemporaryDirectory(prefix="typecraft-gh-install-") as temp:
            root = Path(temp)
            project = root / "project"
            config = root / "gh-config"
            project.mkdir()
            config.mkdir()
            subprocess.run(
                ["git", "init", "--quiet", str(project)],
                check=True,
                capture_output=True,
                text=True,
            )
            environment = os.environ.copy()
            environment["GH_CONFIG_DIR"] = str(config)
            environment.pop("GH_TOKEN", None)
            environment.pop("GITHUB_TOKEN", None)
            command = [
                "gh", "skill", "install", str(repository_root), "typecraft-skills",
                "--from-local", "--agent", "github-copilot", "--scope", "project",
            ]
            installed = subprocess.run(
                command,
                cwd=project,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                installed.returncode,
                0,
                installed.stderr or installed.stdout,
            )

            listing = subprocess.run(
                [
                    "gh", "skill", "list", "--scope", "project", "--json",
                    "skillName,sourceURL,agentHosts,path,version,scope",
                ],
                cwd=project,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(listing.returncode, 0, listing.stderr)
            rows = json.loads(listing.stdout or "[]")
            row = next(
                (
                    item for item in rows
                    if item.get("skillName") == "typecraft-skills"
                    and item.get("scope") == "project"
                    and "github-copilot" in (item.get("agentHosts") or [])
                ),
                None,
            )
            self.assertIsNotNone(row, "GitHub CLI did not discover the installed skill")
            self.assertEqual(
                row["sourceURL"],
                str(source),
            )
            self.assertTrue(
                _verify_cli_files(source, row, metadata_source=str(source))
            )
            self.assertEqual(
                len(list((Path(row["path"]) / "references").rglob("*.md"))),
                20,
            )

            repeated = subprocess.run(
                command,
                cwd=project,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(repeated.returncode, 0)
            self.assertIn("already installed", repeated.stderr.lower())

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

    @patch("scripts.install_url.subprocess.run")
    @patch("scripts.install_url.shutil.which", return_value="/usr/bin/gemini")
    def test_gemini_prefers_its_native_installer_without_skipping_consent(
        self, _which, run
    ):
        destination = (
            self.root / "gemini-home" / ".gemini" / "skills" / "typecraft-skills"
        )

        def fake_gemini(command, **_kwargs):
            if command[-1] == "--help":
                return SimpleNamespace(
                    returncode=0,
                    stdout="--scope user|workspace",
                    stderr="",
                )
            if "install" in command:
                shutil.copytree(self.source, destination)
                return SimpleNamespace(returncode=0, stdout="", stderr="")
            return SimpleNamespace(
                returncode=0, stdout="typecraft-skills\n", stderr=""
            )

        run.side_effect = fake_gemini
        result = execute_install(
            REQUEST,
            "gemini-cli",
            source=self.source,
            registry=self.registry,
            home=self.root / "gemini-home",
        )
        self.assertEqual(result.installation, "SUCCESS")
        self.assertEqual(result.skill_discovery, "VERIFIED")
        install_command = next(
            call.args[0]
            for call in run.call_args_list
            if "install" in call.args[0] and call.args[0][-1] != "--help"
        )
        self.assertEqual(
            install_command,
            [
                "/usr/bin/gemini",
                "skills",
                "install",
                str(self.source.resolve()),
                "--scope",
                "user",
            ],
        )
        self.assertNotIn("--consent", install_command)


if __name__ == "__main__":
    unittest.main()
