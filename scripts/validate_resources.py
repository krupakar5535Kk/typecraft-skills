from pathlib import Path
from strictyaml import load
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/typecraft-skills"
REGISTRY = ROOT / "registry/resource-ids.yaml"

EXPECTED = {
    "typography_style": 10,
    "design_template": 10,
}

VALID_STATUSES = {"draft", "review", "approved", "deprecated"}
SCHEMA_VERSION = "1.2"
RESOURCE_VERSION = "1.0.0"

errors = []
resources = {}
resource_names = {}

def error(message):
    errors.append(message)

def read_yaml(path):
    try:
        text = path.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError("Invalid YAML frontmatter")
        return load(parts[1]).data
    except Exception as exc:
        error(f"{path.name}: {exc}")
        return None

def scan(resource_type, folder):
    files = sorted(folder.glob("*.md"))

    if len(files) != EXPECTED[resource_type]:
        error(
            f"{resource_type}: expected {EXPECTED[resource_type]}, "
            f"found {len(files)}"
        )

    for path in files:
        data = read_yaml(path)
        if data is None:
            continue

        required = {
            "id", "name", "resource_type", "schema_version",
            "resource_version", "version", "status", "summary",
            "domains", "tags"
        }

        missing = required - set(data)
        if missing:
            error(f"{path.name}: missing {sorted(missing)}")
            continue

        if data["resource_type"] != resource_type:
            error(f"{path.name}: incorrect resource_type")

        if data["schema_version"] != SCHEMA_VERSION:
            error(f"{path.name}: incorrect schema_version")

        if str(data["resource_version"]) != RESOURCE_VERSION:
            error(f"{path.name}: incorrect resource_version")

        if str(data["version"]) != RESOURCE_VERSION:
            error(f"{path.name}: incorrect version")

        if data["status"] not in VALID_STATUSES:
            error(f"{path.name}: invalid lifecycle status")

        if not data["domains"] or not data["tags"]:
            error(f"{path.name}: empty domains or tags")

        resource_id = data["id"]
        if resource_id in resources:
            error(f"Duplicate resource ID: {resource_id}")
        else:
            resources[resource_id] = resource_type
        resource_name = (resource_type, str(data["name"]).casefold())
        if resource_name in resource_names:
            error(
                f"Duplicate resource name: {data['name']} "
                f"({resource_names[resource_name]} and {path.name})"
            )
        else:
            resource_names[resource_name] = path.name

def main():
    scan(
        "typography_style",
        SKILL / "references/design-styles"
    )

    scan(
        "design_template",
        SKILL / "references/design-templates"
    )

    try:
        registry = load(
            REGISTRY.read_text(encoding="utf-8")
        ).data

        if registry["schema_version"] != SCHEMA_VERSION:
            error("Incorrect registry schema version")

        registry_ids = {}

        for entry in registry["resources"]:
            rid = entry["id"]

            if rid in registry_ids:
                error(f"Duplicate registry ID: {rid}")

            registry_ids[rid] = entry["resource_type"]

            if entry["registry_status"] != "active":
                error(f"{rid}: registry status is not active")

        for rid, resource_type in resources.items():
            if registry_ids.get(rid) != resource_type:
                error(f"Registry mismatch: {rid}")

        for rid in registry_ids:
            if rid not in resources:
                error(f"Registry references missing resource: {rid}")

    except Exception as exc:
        error(f"Registry validation error: {exc}")

    if errors:
        print("RESOURCE VALIDATION FAILED")
        for item in errors:
            print("ERROR:", item)
        return 1

    print("PASS: 10 typography styles")
    print("PASS: 10 design templates")
    print("PASS: Unique resource IDs")
    print("PASS: Metadata and lifecycle statuses")
    print("PASS: Registry consistency")
    print("RESOURCE VALIDATION PASSED")
    return 0

if __name__ == "__main__":
    sys.exit(main())
