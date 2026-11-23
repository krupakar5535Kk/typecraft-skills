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

    file_status = platform.get("file_installation_verification")
    discovery_status = platform.get("runtime_discovery_verification")
    if file_status not in {"verified", "not_tested", "failed", "not_applicable"}:
        fail(f"{key}: invalid file installation verification status")
    if discovery_status not in {
        "verified", "not_tested", "failed", "not_supported"
    }:
        fail(f"{key}: invalid runtime discovery verification status")

    if status == "verified":
        verification = platform.get("runtime_verification", {})
        environment = verification.get("environment", {})
        installation = verification.get("installation", {})
        discovery = verification.get("skill_discovery", {})
        references = discovery.get("references_exercised", [])
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
                for field in ("product", "editor", "host", "session")
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
            and discovery.get("skill_read") == "true"
            and isinstance(references, list)
            and references
            and all(isinstance(reference, str) and reference for reference in references)
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
    elif file_status == "verified" or discovery_status == "verified":
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
