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

for key, platform in platforms.items():
    status = platform.get("compatibility")
    if status not in ALLOWED_STATUSES:
        fail(f"{key}: invalid compatibility status {status}")

    if not platform.get("display_name"):
        fail(f"{key}: missing display_name")

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
