# TypeCraft Skills — Installation

The only canonical TypeCraft implementation is `skills/typecraft-skills/`.
Install or package that complete directory, including every file under
`references/`.

## URL request behavior

Treat either
`https://github.com/krupakar5535Kk/typecraft-skills` or its `.git` form as an
installation request when the URL is the whole user message, or is followed by
an explicit request such as “Install this skill.” If the user asks a different
question about the URL, answer that question instead.

Read [INSTALL.md](../INSTALL.md), identify the actual active platform, and use
its documented route. Never infer the platform from the repository, operating
system, browser, or installed applications.

## Local agents

TypeCraft ships native directory adapters for platforms with documented
Agent Skills paths:

| Platform | User location | Project location |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| OpenAI Codex | `~/.agents/skills/` | `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` |
| Google Antigravity App | `~/.gemini/config/skills/` | `.agents/skills/` |

These are supported file locations, not claims that TypeCraft has been
independently tested in every runtime. Check the target agent's own skill list
after installing. The Gemini CLI router can run `gemini skills list --all`;
other native adapters report discovery as `NOT_VERIFIED` until the host itself
confirms it. Gemini may request consent when the skill is activated.

GitHub CLI offers a preview `gh skill install` adapter for its documented
agent-host list. The registry tracks those installer targets separately from
platform compatibility and runtime discovery. The router uses that route only
when no TypeCraft native directory adapter exists and the host is registered.

### Optional local router

Run this from a checkout after reviewing the script:

```bash
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent codex \
  --scope user
```

For `--agent auto`, the active runtime must set `TYPECRAFT_AGENT` to its exact
registered host ID. If it is unset or unknown, the router stops rather than
guessing. A project-scope install requires `--scope project`.

The router compares existing installs before writing. Identical installations
are left unchanged. Different or incomplete installations are never replaced
without explicit user approval and `--force`.

## ChatGPT Skills

ChatGPT supports a distinct upload route for eligible accounts and workspaces.
The router can create a ZIP with `typecraft-skills/` at its root:

```bash
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent chatgpt \
  --package-output /tmp/typecraft-skills.zip
```

Packaging is not installation. The user must upload the ZIP under **Skills →
Create → Upload from your computer**, then confirm the scan and installation in
ChatGPT. Do not claim success or discovery until the product confirms it.

## Chat-only fallback

If the current chat agent cannot persist files or install skills, report that
persistent installation is unsupported. When it can read the entire canonical
directory, it may use those instructions only for the current conversation.
Otherwise, direct the user to a supported local agent or the ChatGPT upload
flow.

## Verification contract

Report the following independently:

1. **File installation:** destination exists, `SKILL.md` and every reference
   are present, and the installed reference contents match the source.
2. **Runtime discovery:** the platform itself lists or activates
   `typecraft-skills`.
3. **User action:** reload, new session, upload, approval, or confirmation still
   required.

An installer exit code, a host inventory record, or a ZIP file alone does not
prove runtime discovery.

## Maintainer multi-target utility

The registry-driven `scripts/install.py` remains a maintainer utility for
intentionally installing to multiple GitHub CLI targets. Preview before using
`--all`; it is not the URL-first, current-agent workflow:

```bash
python -m scripts.install --list
python -m scripts.install --all --scope user --dry-run
```
