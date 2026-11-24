from datetime import date
from pathlib import Path
from strictyaml import load, YAMLValidationError
import sys

REGISTRY = Path("registry/agents.yaml")

ALLOWED_STATUSES = {
    "verified",
    "compatible",
    "research_required",
    "unsupported",
}
CANONICAL_REFERENCES = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "typecraft-skills"
    / "references"
)
REFERENCE_FILE_COUNT = len(list(CANONICAL_REFERENCES.rglob("*.md")))
STYLE_FILE_COUNT = len(list((CANONICAL_REFERENCES / "design-styles").glob("*.md")))
TEMPLATE_FILE_COUNT = len(list((CANONICAL_REFERENCES / "design-templates").glob("*.md")))

def fail(message):
    print(f"ERROR: {message}")
    sys.exit(1)

if not REGISTRY.is_file():
    fail(f"Registry not found: {REGISTRY}")

try:
    data = load(REGISTRY.read_text()).data
except YAMLValidationError as exc:
    fail(f"Invalid YAML: {exc}")

installers = data.get("installers", {})
github = installers.get("github_cli", {})
targets = github.get("supported_agents", [])
catalog = data.get("agent_catalog", [])
platforms = data.get("platforms", {})
native_adapters = data.get("native_adapters", {})
fallbacks = data.get("fallbacks", {})

if not targets:
    fail("No GitHub CLI targets found.")

target_set = set(targets)
catalog_ids = [entry.get("agent_id") for entry in catalog]

if len(target_set) != len(targets):
    fail("Duplicate GitHub CLI target IDs.")

if len(catalog_ids) != len(set(catalog_ids)):
    fail("Duplicate agent catalog IDs.")

if target_set != set(catalog_ids):
    missing = target_set - set(catalog_ids)
    extra = set(catalog_ids) - target_set
    fail(f"Catalog mismatch. Missing: {missing}; Extra: {extra}")

for entry in catalog:
    for field in ("agent_id", "display_name", "installer",
                  "installation_method", "installation_verified",
                  "skill_discovery_verified"):
        if field not in entry:
            fail(f"{entry.get('agent_id')}: missing {field}")
    for field in ("installation_verified", "skill_discovery_verified"):
        if entry[field] not in {"true", "false"}:
            fail(f"{entry.get('agent_id')}: {field} must be true or false")
    if (
        entry["skill_discovery_verified"] == "true"
        and entry["installation_verified"] != "true"
    ):
        fail(f"{entry['agent_id']}: discovery cannot be verified without installation")

for key, platform in platforms.items():
    status = platform.get("compatibility")
    if status not in ALLOWED_STATUSES:
        fail(f"{key}: invalid compatibility status {status}")
    try:
        date.fromisoformat(str(platform.get("documentation_checked", "")))
    except ValueError:
        fail(f"{key}: documentation_checked must be an ISO date")

    for field in (
        "display_name",
        "product_surface",
        "documentation_checked",
        "native_installer_available",
        "file_installation_verification",
        "runtime_discovery_verification",
    ):
        if not platform.get(field):
            fail(f"{key}: missing {field}")
        if platform.get("native_installer_available") not in {"true", "false", "unknown"}:
            fail(f"{key}: invalid native installer availability")
    environment = platform.get("verification_environment", {})
    if (
        not isinstance(environment, dict)
        or environment.get("kind") not in {
            "documentation_review",
            "historical_runtime_test",
            "manual_runtime_test",
            "automated_runtime_test",
        }
        or not environment.get("environment")
    ):
        fail(f"{key}: missing verification environment details")
    runtime_test = environment.get("kind") in {
        "historical_runtime_test",
        "manual_runtime_test",
        "automated_runtime_test",
    }
    if (status == "verified") != runtime_test:
        fail(f"{key}: verification environment conflicts with compatibility status")
    documentation_url = platform.get("official_documentation_url")
    if status in {"compatible", "verified"} and not (
        isinstance(documentation_url, str)
        and documentation_url.startswith("https://")
    ):
        fail(f"{key}: {status} requires an official documentation URL")
    if status == "research_required" and documentation_url not in (None, "null") and not (
        isinstance(documentation_url, str)
        and documentation_url.startswith("https://")
    ):
        fail(f"{key}: invalid official documentation URL")
    installation = platform.get("installation", {})
    discovery = platform.get("discovery", {})
    if not installation.get("method"):
        fail(f"{key}: missing installation method")
    for field in ("user_scope_directory", "project_scope_directory"):
        if field not in installation:
            fail(f"{key}: missing installation.{field}")
    if not discovery.get("mechanism") or not discovery.get("user_action"):
        fail(f"{key}: missing discovery mechanism or remaining user action")
    if installation.get("method") == "zip_upload_with_user_confirmation":
        if (
            installation.get("package_required") != "true"
            or installation.get("package_root") != "typecraft-skills/"
        ):
            fail(f"{key}: upload platforms must declare the canonical package root")

    file_status = platform.get("file_installation_verification")
    discovery_status = platform.get("runtime_discovery_verification")
    invocation_status = platform.get("skill_invocation_verification", "not_tested")
    if file_status not in {"verified", "not_tested", "failed", "not_applicable"}:
        fail(f"{key}: invalid file installation verification status")
    if discovery_status not in {
        "verified", "not_tested", "failed", "not_supported"
    }:
        fail(f"{key}: invalid runtime discovery verification status")
    if invocation_status not in {
        "verified", "not_tested", "failed", "not_supported"
    }:
        fail(f"{key}: invalid skill invocation verification status")

    if status == "verified":
        verification = platform.get("runtime_verification", {})
        environment = verification.get("environment", {})
        installation = verification.get("installation", {})
        discovery = verification.get("skill_discovery", {})
        invocation = verification.get("invocation", {})
        references = invocation.get("references_exercised", [])
        agent_id = verification.get("agent_id")
        catalog_entry = next(
            (entry for entry in catalog if entry.get("agent_id") == agent_id),
            None,
        )
        if not (
            agent_id
            and verification.get("tested_at")
            and verification.get("skill_version")
            and all(
                environment.get(field)
                for field in ("product", "host", "session")
            )
            and installation.get("tested") == "true"
            and installation.get("scope") in {"user", "project"}
            and installation.get("method")
            and installation.get("path")
            and installation.get("skill_manifest_present") == "true"
            and installation.get("reference_files_present")
            == str(REFERENCE_FILE_COUNT)
            and discovery.get("tested") == "true"
            and discovery.get("result") == "confirmed"
            and invocation.get("tested") in {"true", "false"}
            and (
                invocation.get("tested") == "true"
            ) == (invocation_status == "verified")
            and catalog_entry
            and catalog_entry.get("installation_verified") == "true"
            and catalog_entry.get("skill_discovery_verified") == "true"
            and file_status == "verified"
            and discovery_status == "verified"
        ):
            fail(
                f"{key}: verified compatibility requires complete runtime evidence "
                "and matching verified catalog flags"
            )
        if invocation.get("tested") == "true" and not (
            invocation.get("result") == "confirmed"
            and isinstance(references, list)
            and references
            and all(isinstance(reference, str) and reference for reference in references)
        ):
            fail(f"{key}: invocation evidence requires confirmed exercised references")
    elif (
        file_status == "verified"
        or discovery_status == "verified"
        or invocation_status == "verified"
    ):
        fail(f"{key}: verification statuses require compatibility: verified")

    user_report = platform.get("user_reported_runtime_verification")
    if user_report:
        if (
            status == "verified"
            or user_report.get("source") != "user_report"
            or user_report.get("installation_tested") != "false"
            or user_report.get("exact_source_match") != "not_tested"
            or user_report.get("installed_version") != "not_established"
            or not user_report.get("reported_at")
            or not user_report.get("reported_location")
            or user_report.get("skill_listed") != "true"
            or user_report.get("skill_manifest_read") != "true"
            or user_report.get("reported_style_count") != str(STYLE_FILE_COUNT)
            or user_report.get("reported_template_count") != str(TEMPLATE_FILE_COUNT)
        ):
            fail(f"{key}: user-reported evidence must not imply a verified installation")

for entry in catalog:
    if (
        entry.get("installation_verified") == "true"
        or entry.get("skill_discovery_verified") == "true"
    ):
        verified_platform = any(
            platform.get("compatibility") == "verified"
            and platform.get("runtime_verification", {}).get("agent_id")
            == entry.get("agent_id")
            for platform in platforms.values()
        )
        if not verified_platform:
            fail(
                f"{entry['agent_id']}: catalog verification flags require "
                "matching platform runtime evidence"
            )

for agent_id, adapter in native_adapters.items():
    platform_id = adapter.get("platform")
    if platform_id not in platforms:
        fail(f"{agent_id}: native adapter references unknown platform {platform_id}")

    scope_paths = adapter.get("scope_paths", {})
    if set(scope_paths) != {"user", "project"}:
        fail(f"{agent_id}: native adapter must define user and project locations")
    if not all(isinstance(path, str) and path for path in scope_paths.values()):
        fail(f"{agent_id}: native adapter contains an empty installation path")
    if not adapter.get("evidence"):
        fail(f"{agent_id}: native adapter is missing official documentation evidence")
    user_path = Path(scope_paths["user"])
    project_path = Path(scope_paths["project"])
    if (
        not scope_paths["user"].startswith("~/")
        or project_path.is_absolute()
        or ".." in project_path.parts
        or ".." in user_path.parts
    ):
        fail(f"{agent_id}: native adapter contains an unsafe scope path")
    platform_installation = platforms[platform_id].get("installation", {})
    if (
        platform_installation.get("user_scope_directory") != scope_paths["user"]
        or platform_installation.get("project_scope_directory")
        != scope_paths["project"]
    ):
        fail(f"{agent_id}: adapter paths contradict the platform record")
    for scope, paths in adapter.get("alternate_scope_paths", {}).items():
        if scope not in {"user", "project"} or not isinstance(paths, list):
            fail(f"{agent_id}: invalid alternate scope paths")
        for value in paths:
            if not isinstance(value, str) or not value:
                fail(f"{agent_id}: unsafe alternate installation path {value}")
            path = Path(value)
            if (
                (scope == "user" and not value.startswith("~/"))
                or (scope == "project" and path.is_absolute())
                or ".." in path.parts
            ):
                fail(f"{agent_id}: unsafe alternate installation path {value}")

app = platforms.get("antigravity", {})
cli = platforms.get("antigravity_cli", {})
app_adapter = native_adapters.get("antigravity", {})
cli_adapter = native_adapters.get("antigravity-cli", {})
if (
    app.get("product_surface") != "Antigravity App"
    or cli.get("product_surface") != "Antigravity CLI"
):
    fail("Antigravity App and CLI must be registered as separate product surfaces.")
if not app_adapter or not cli_adapter:
    fail("Antigravity App and CLI must have separate native adapters.")
app_paths = app_adapter.get("scope_paths", {})
cli_paths = cli_adapter.get("scope_paths", {})
if (
    app_paths.get("user") == cli_paths.get("user")
    or app_paths.get("project") != cli_paths.get("project")
    or cli_paths.get("user") != "~/.gemini/antigravity-cli/skills"
):
    fail("Antigravity adapter paths do not match the documented surface scopes.")
if cli.get("compatibility") == "verified":
    fail("Antigravity CLI cannot be runtime-verified without recorded test evidence.")

for agent_id, fallback in fallbacks.items():
    if fallback.get("persistent_installation") != "unsupported":
        fail(f"{agent_id}: chat fallback must not claim persistent installation")
    if not fallback.get("user_action"):
        fail(f"{agent_id}: chat fallback is missing its user guidance")

print("TYPECRAFT AGENT REGISTRY VALIDATION")
print("-----------------------------------")
print("YAML syntax:             PASS")
print("GitHub CLI targets:      ", len(targets))
print("Agent catalog records:   ", len(catalog))
print("Unique agent IDs:        ", len(set(catalog_ids)))
print("Platform records:        ", len(platforms))
print("Native adapters:         ", len(native_adapters))
print("Chat fallbacks:          ", len(fallbacks))
print("Compatibility statuses:  PASS")
print("Required metadata:       PASS")
print("-----------------------------------")
print("RESULT: REGISTRY VALID")
