# TypeCraft Skills — Installation Guide

TypeCraft is distributed as one canonical Agent Skill:

`skills/typecraft-skills/`

The complete skill includes `SKILL.md` and every file in `references/`. Always install the complete directory.

## 1. URL-first installation

For supported local coding agents, users should be able to paste only this repository URL into the agent chat and press Enter:

`https://github.com/krupakar5535Kk/typecraft-skills`

The repository URL by itself is the install request. The agent should inspect `INSTALL.md`, detect its own host, install the complete skill, and verify the result without asking for a second prompt. This requires repository access, persistent filesystem access, and the platform's normal permission to write files.

See [INSTALL.md](../INSTALL.md) for the full machine-readable agent procedure, host IDs, platform exceptions, and verification contract.

## 2. Supported local-agent route

GitHub CLI provides a common installer for supported local Agent Skills hosts. For a detected host, the agent can use:

`gh skill install krupakar5535Kk/typecraft-skills typecraft-skills --agent <HOST_ID> --scope user`

Examples of host IDs include `claude-code`, `codex`, `antigravity`, `antigravity-cli`, and `opencode`. The agent must select the ID for its actual runtime and must not use `--all` for a single-host request.

GitHub CLI Agent Skills support is a preview feature. Check `gh skill --help` before relying on it. When it is unavailable, use the platform's official persistent skill directory and copy the complete skill folder without executing repository scripts.

## 3. Platform-specific routes

- **Claude Code:** personal skills use `~/.claude/skills/`. Check discovery with `/skills` in Claude Code.
- **OpenAI Codex:** user skills use `~/.agents/skills/`. Start or refresh a session if the installed skill does not appear.
- **Google Antigravity App:** global skills use `~/.gemini/config/skills/`.
- **Google Antigravity CLI:** global skills use `~/.gemini/antigravity-cli/skills/`. App and CLI discovery must be tested separately.
- **OpenCode:** global skills use `~/.config/opencode/skills/`; it also reads shared Agent Skills directories.
- **Cursor:** Cursor's documented GitHub-repository import requires a Cursor plugin package with `.cursor-plugin/marketplace.json` and installation through its plugin/marketplace flow. Do not claim that the URL-only repository import is ready until the TypeCraft Cursor adapter is packaged and tested.
- **ChatGPT Skills:** ChatGPT uses its own Create with chat or Upload from your computer process, with eligibility and workspace restrictions. It is not installed by the local GitHub CLI command. See [INSTALL.md](../INSTALL.md).

## 4. Manual multi-agent installer (maintainer workflow)

The repository also includes a registry-driven Python installer for maintainers who intentionally want to install TypeCraft for multiple GitHub CLI targets from a terminal. This is a maintainer utility, not the end-user URL-only workflow.

Prerequisites: Git, Python 3.12 or compatible, and GitHub CLI with `gh skill` support.

Clone and prepare the repository:

`git clone https://github.com/krupakar5535Kk/typecraft-skills.git`

`cd typecraft-skills`

`python3.12 -m venv .venv`

`.venv/bin/python -m pip install -r requirements-installer.txt`

List targets and preview before installing:

`.venv/bin/python scripts/install.py --list`

`.venv/bin/python scripts/install.py --all --scope user --dry-run`

Install all targets only when that is explicitly intended:

`.venv/bin/python scripts/install.py --all --scope user`

Existing installations are skipped by default. Use `--force` only with explicit permission to replace them. The number of agent targets does not necessarily equal the number of separate directories because some hosts share paths.

## 5. Verification requirements

Verify these separately:

1. The final target directory exists and is readable.
2. `SKILL.md` exists.
3. Every reference file from the source is present.
4. The target application's own discovery mechanism sees the skill.
5. Any required reload, new session, or user confirmation is reported.

A successful installer exit code or a file listing proves installation/file presence, not runtime discovery.

## Related documentation

- [AI Agent Installation Instructions](../INSTALL.md)
- [Compatibility Guide](compatibility.md)
- [Usage Guide](usage.md)
