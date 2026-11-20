#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from strictyaml import load

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry" / "agents.yaml"
REPOSITORY = "krupakar5535Kk/typecraft-skills"
SOURCE_URL = f"https://github.com/{REPOSITORY}"
SKILL = "typecraft-skills"

JSON_FIELDS = "skillName,sourceURL,agentHosts,path,version,scope,pinned"


def load_registry():
    if not REGISTRY.is_file():
        raise RuntimeError(f"Registry not found: {REGISTRY}")
    return load(REGISTRY.read_text()).data


def normalize_source(url):
    return (url or "").strip().rstrip("/").removesuffix(".git").lower()


def check_gh():
    if not shutil.which("gh"):
        raise RuntimeError("GitHub CLI (gh) is not installed.")

    result = subprocess.run(
        ["gh", "skill", "--help"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError("GitHub CLI Agent Skills support is unavailable.")


def list_installed(scope):
    result = subprocess.run(
        [
            "gh", "skill", "list",
            "--scope", scope,
            "--json", JSON_FIELDS
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Could not read installed skills: "
            + (result.stderr.strip() or result.stdout.strip())
        )

    try:
        rows = json.loads(result.stdout or "[]")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON from gh skill list: {exc}")

    if not isinstance(rows, list):
        raise RuntimeError("Unexpected installed-skills inventory format.")

    return rows


def find_installation(inventory, agent, scope):
    for row in inventory:
        if row.get("skillName") != SKILL:
            continue

        if normalize_source(row.get("sourceURL")) != normalize_source(SOURCE_URL):
            continue

        if row.get("scope") != scope:
            continue

        hosts = row.get("agentHosts") or []
        if agent in hosts:
            return row

    return None


def main():
    parser = argparse.ArgumentParser(
        description="TypeCraft Universal Agent Skill Installer"
    )

    parser.add_argument(
        "--agent",
        action="append",
        help="Agent ID to install. Repeat for multiple agents."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Select all GitHub CLI-supported agent targets."
    )
    parser.add_argument(
        "--scope",
        choices=["user", "project"],
        default="user",
        help="Installation scope (default: user)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without installing."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List registered GitHub CLI agent targets."
    )
    parser.add_argument(
        "--version",
        help="Optional Git tag or commit SHA to install."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Explicitly overwrite existing TypeCraft installations."
    )

    args = parser.parse_args()

    try:
        data = load_registry()
    except Exception as exc:
        print(f"ERROR: Could not load registry: {exc}")
        return 1

    targets = data["installers"]["github_cli"]["supported_agents"]
    catalog = data["agent_catalog"]
    names = {
        item["agent_id"]: item["display_name"]
        for item in catalog
    }

    if args.list:
        print("TYPECRAFT REGISTERED AGENTS")
        for agent in targets:
            print(f"{agent:20} {names.get(agent, agent)}")
        print(f"\nTotal: {len(targets)}")
        return 0

    if args.all and args.agent:
        parser.error("Use either --all or --agent, not both.")

    if args.all:
        selected = list(targets)
    elif args.agent:
        selected = list(dict.fromkeys(args.agent))
    else:
        parser.error("Specify --all, --agent AGENT_ID, or --list.")

    unknown = sorted(set(selected) - set(targets))
    if unknown:
        print("ERROR: Unknown agent IDs:", ", ".join(unknown))
        print("Run: python scripts/install.py --list")
        return 1

    print("TYPECRAFT UNIVERSAL INSTALLER")
    print("Repository:", REPOSITORY)
    print("Skill:", SKILL)
    print("Scope:", args.scope)
    print("Agent targets:", len(selected))
    print("Requested version:", args.version or "Latest available")
    print("Overwrite enabled:", args.force)
    print()

    # Dry-run remains useful even without GitHub CLI installed.
    if args.dry_run:
        inventory = []
        inventory_available = False

        if shutil.which("gh"):
            try:
                check_gh()
                inventory = list_installed(args.scope)
                inventory_available = True
            except Exception as exc:
                print(f"NOTE: Could not inspect installed skills: {exc}")
                print("Showing a general preview instead.\n")

        for agent in selected:
            existing = (
                find_installation(inventory, agent, args.scope)
                if inventory_available else None
            )

            if existing and not args.force:
                version = existing.get("version") or "unknown"
                requested = args.version.lstrip("@") if args.version else None

                if requested and requested != version:
                    print(
                        f"[SKIP] {agent} — installed {version}; "
                        f"requested {requested}. Use --force to replace."
                    )
                else:
                    print(f"[SKIP] {agent} — already installed ({version})")
            elif existing:
                print(f"[OVERWRITE PREVIEW] {agent} — existing installation")
            else:
                print(f"[PREVIEW] {agent} — {names.get(agent, agent)}")

        print("\nPreview complete. Nothing was installed.")
        return 0

    try:
        check_gh()
        inventory = list_installed(args.scope)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    successful = []
    skipped = []
    failed = []
    processed_paths = set()

    skill_argument = (
        f"{SKILL}@{args.version.lstrip('@')}"
        if args.version else SKILL
    )

    for agent in selected:
        existing = find_installation(inventory, agent, args.scope)

        if existing and not args.force:
            installed_version = existing.get("version") or "unknown"
            version_note = ""

            if args.version and installed_version != args.version.lstrip("@"):
                version_note = (
                    f"; requested {args.version}, use --force to replace"
                )

            print(
                f"\nSKIPPED: {agent} — already installed "
                f"({installed_version}{version_note})"
            )
            skipped.append(agent)
            continue

        existing_path = existing.get("path") if existing else None

        # Avoid overwriting the same shared directory repeatedly.
        if args.force and existing_path and existing_path in processed_paths:
            print(f"\nSKIPPED: {agent} — shared directory already processed")
            skipped.append(agent)
            continue

        command = [
            "gh", "skill", "install",
            REPOSITORY,
            skill_argument,
            "--agent", agent,
            "--scope", args.scope
        ]

        if args.force:
            command.append("--force")

        print(f"\nInstalling for {agent}...")

        result = subprocess.run(command)

        if result.returncode == 0:
            print(f"SUCCESS: {agent}")
            successful.append(agent)

            if existing_path:
                processed_paths.add(existing_path)

            # Refresh so newly registered shared-directory hosts are detected.
            try:
                inventory = list_installed(args.scope)
            except Exception as exc:
                print(f"WARNING: Could not refresh inventory: {exc}")
        else:
            print(f"FAILED: {agent}")
            failed.append(agent)

    print("\nINSTALLATION SUMMARY")
    print("Successful:", len(successful))
    print("Already installed / skipped:", len(skipped))
    print("Failed:", len(failed))

    if failed:
        print("Failed agents:", ", ".join(failed))
        return 1

    print("\nAll requested installation actions completed.")
    print("Installation success does not independently prove skill discovery.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
