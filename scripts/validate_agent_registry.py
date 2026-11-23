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

    if not platform.get("display_name"):
        fail(f"{key}: missing display_name")
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
        ):
            fail(
                f"{key}: verified compatibility requires complete runtime evidence "
                "and matching verified catalog flags"
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

app_paths = native_adapters.get("antigravity", {}).get("scope_paths", {})
cli_paths = native_adapters.get("antigravity-cli", {}).get("scope_paths", {})
if not app_paths or not cli_paths:
    fail("Antigravity App and CLI must have separate native adapters.")
if app_paths.get("user") == cli_paths.get("user"):
    fail("Antigravity App and CLI user-scope paths must remain separate.")
if app_paths.get("project") != cli_paths.get("project"):
    fail("Antigravity App and CLI must use the documented shared workspace path.")
if cli_paths.get("user") != "~/.gemini/antigravity-cli/skills":
    fail("Antigravity CLI user-scope path must match official documentation.")

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
