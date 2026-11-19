#!/usr/bin/env python3

from pathlib import Path
import sys

from skills_ref import validate

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "typecraft-skills"

if not SKILL_DIR.is_dir():
    print(f"ERROR: Skill directory not found: {SKILL_DIR}")
    sys.exit(1)

errors = validate(SKILL_DIR)

if errors:
    print("SKILL VALIDATION FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Valid skill: skills/typecraft-skills")
