# TypeCraft Skills — Installation Guide

TypeCraft is distributed as one canonical Agent Skill:

`skills/typecraft-skills/`

The complete skill includes `SKILL.md` and all files in `references/`. Always install the complete directory.

## 1. Install through an AI agent

Repository:

https://github.com/krupakar5535Kk/typecraft-skills

Ask your AI agent:

> Install this skill in your environment. Read INSTALL.md and follow its instructions. Install the complete typecraft-skills directory, including all references, and verify installation and skill discovery.

The agent needs repository access, permission to write to a persistent location, and a supported skill installation mechanism.

See [INSTALL.md](../INSTALL.md).

## 2. Install with GitHub CLI

The repository includes a registry-driven installer for 48 GitHub CLI-supported agent targets.

### Prerequisites

- Git
- Python 3.12 or a compatible version
- GitHub CLI with `gh skill` support
- GitHub CLI authentication where required

Check GitHub CLI:

`gh skill --help`

`gh auth status`

### Clone the repository

`git clone https://github.com/krupakar5535Kk/typecraft-skills.git`

`cd typecraft-skills`

### Set up the installer

`python3.12 -m venv .venv`

`.venv/bin/python -m pip install --upgrade pip`

`.venv/bin/python -m pip install -r requirements-installer.txt`

### List supported agents

`.venv/bin/python scripts/install.py --list`

### Preview all 48 targets

`.venv/bin/python scripts/install.py --all --scope user --dry-run`

### Install all targets

`.venv/bin/python scripts/install.py --all --scope user`

The default scope is `user`. Use `--scope project` for project-level installation.

### Install selected agents

`.venv/bin/python scripts/install.py --agent claude-code`

Select multiple agents by repeating `--agent`:

`.venv/bin/python scripts/install.py --agent claude-code --agent cursor`

### Select a specific version

Use `--version` to pin a release tag or commit SHA:

`.venv/bin/python scripts/install.py --agent claude-code --version v1.0.0`

The requested version must exist as a tag or commit in the repository.

### Existing installations and updates

Existing TypeCraft installations are skipped by default. This makes repeated installer runs safe.

When a different version is requested, the installer reports the installed and requested versions and skips the existing installation.

Use `--force` only when you explicitly intend to overwrite existing TypeCraft installations:

`.venv/bin/python scripts/install.py --agent claude-code --version v1.0.0 --force`

Review the requested version and target before using this option.

Some agent targets share physical installation directories. Therefore, 48 agent targets do not necessarily correspond to 48 separate directories.

## 3. ChatGPT and other installation routes

The 48 targets refer specifically to the GitHub CLI-supported agent catalog. They do not represent every AI application.

ChatGPT uses a separate distribution and skill-upload route. Do not assume the GitHub CLI installer installs skills into ChatGPT.

Other applications without a compatible GitHub CLI installation mechanism require their own documented installation procedure.

## 4. Verify installation

Check that the installed skill directory contains:

- `SKILL.md`
- The complete `references/` directory
- All expected reference Markdown files

Then check whether the target AI application discovers and activates the skill.

Installation success and skill discovery are separate verification steps. A successful file copy or installer exit code does not independently prove discovery.

## 5. Troubleshooting

**Missing Python dependency**

Create the virtual environment and install `requirements-installer.txt`.

**GitHub CLI skill command unavailable**

Install or update GitHub CLI to a version that provides `gh skill` support. Confirm using `gh skill --help`.

**Skill already installed**

The installer skips existing TypeCraft installations by default. Use `--force` only when replacement is intentional.

**Skill not discovered**

Check the target application's official skill-discovery mechanism, installation scope, and any required reload or restart procedure.

**References missing**

Install the complete `skills/typecraft-skills/` directory rather than only `SKILL.md`.

## Related documentation

- [AI Agent Installation Instructions](../INSTALL.md)
- [Compatibility Guide](compatibility.md)
- [Usage Guide](usage.md)
