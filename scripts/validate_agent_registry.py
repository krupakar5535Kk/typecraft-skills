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

print("TYPECRAFT AGENT REGISTRY VALIDATION")
print("-----------------------------------")
print("YAML syntax:             PASS")
print("GitHub CLI targets:      ", len(targets))
print("Agent catalog records:   ", len(catalog))
print("Unique agent IDs:        ", len(set(catalog_ids)))
print("Platform records:        ", len(platforms))
print("Compatibility statuses:  PASS")
print("Required metadata:       PASS")
print("-----------------------------------")
print("RESULT: REGISTRY VALID")
