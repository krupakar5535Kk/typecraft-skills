#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from strictyaml import load

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry" / "agents.yaml"
REPOSITORY = "krupakar5535Kk/typecraft-skills"
SKILL = "typecraft-skills"


def load_registry():
    if not REGISTRY.is_file():
        raise RuntimeError(f"Registry not found: {REGISTRY}")

    data = load(REGISTRY.read_text()).data
    return data


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
        help="Install for all GitHub CLI-supported agents."
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
        help="Preview installations without installing."
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List registered GitHub CLI agents."
    )

    args = parser.parse_args()

    try:
        data = load_registry()
    except Exception as exc:
        print(f"ERROR: Could not load registry: {exc}")
        return 1

    targets = data["installers"]["github_cli"]["supported_agents"]
    catalog = data["agent_catalog"]
    names = {item["agent_id"]: item["display_name"] for item in catalog}

    if args.list:
        print("TYPECRAFT REGISTERED AGENTS")
        for agent in targets:
            print(f"{agent:20} {names.get(agent, agent)}")
        print(f"\nTotal: {len(targets)}")
        return 0

    if args.all:
        selected = list(targets)
    elif args.agent:
        selected = list(dict.fromkeys(args.agent))
    else:
        parser.error("Specify --all, --agent AGENT_ID, or --list.")

    unknown = sorted(set(selected) - set(targets))
    if unknown:
        print("ERROR: Unknown agent IDs:", ", ".join(unknown))
        print("Run: python3 scripts/install.py --list")
        return 1

    print("TYPECRAFT UNIVERSAL INSTALLER")
    print("Repository:", REPOSITORY)
    print("Skill:", SKILL)
    print("Scope:", args.scope)
    print("Agent targets:", len(selected))
    print()

    if args.dry_run:
        for agent in selected:
            print(f"[PREVIEW] {agent} — {names.get(agent, agent)}")
        print("\nPreview complete. Nothing was installed.")
        return 0

    if not shutil.which("gh"):
        print("ERROR: GitHub CLI (gh) is not installed.")
        return 1

    check = subprocess.run(
        ["gh", "skill", "--help"],
        capture_output=True,
        text=True
    )

    if check.returncode != 0:
        print("ERROR: GitHub CLI Agent Skills support is unavailable.")
        return 1

    success = []
    failed = []

    for agent in selected:
        print(f"\nInstalling for {agent}...")

        command = [
            "gh", "skill", "install",
            REPOSITORY,
            SKILL,
            "--agent", agent,
            "--scope", args.scope
        ]

        result = subprocess.run(command)

        if result.returncode == 0:
            success.append(agent)
            print(f"SUCCESS: {agent}")
        else:
            failed.append(agent)
            print(f"FAILED: {agent}")

    print("\nINSTALLATION SUMMARY")
    print("Successful:", len(success))
    print("Failed:", len(failed))

    if failed:
        print("Failed agents:", ", ".join(failed))
        return 1

    print("All requested installations completed.")
    print("Note: installation success does not independently prove skill discovery.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
