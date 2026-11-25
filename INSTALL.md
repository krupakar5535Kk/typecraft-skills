# TypeCraft Skills — Installation Guide

Canonical repository:
`https://github.com/krupakar5535Kk/typecraft-skills.git`

Canonical installable skill: `skills/typecraft-skills/`

---

## 1. Fast Installation (Standard Agent Skills CLI)

TypeCraft adopts the standard Agent Skills distribution ecosystem. If you are using any compatible AI coding agent with command execution capabilities, install TypeCraft directly:

```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --global \
  --agent <ACTIVE_AGENT_ID> \
  --yes
```

### Installation Scope Options:
- **Active Agent Global (Recommended):** `--global --agent <ACTIVE_AGENT_ID>`
- **All Local Agents:** `--global --agent '*'`
- **Project Scope (Current Workspace):** Omit `--global`

### Supported Agent Platform Identifiers:
- `antigravity` — Google Antigravity App / IDE (`~/.gemini/config/skills/typecraft-skills/`)
- `antigravity-cli` — Google Antigravity CLI (`~/.gemini/antigravity-cli/skills/typecraft-skills/`)
- `claude-code` — Claude Code CLI (`~/.claude/skills/typecraft-skills/`)
- `cursor` — Cursor IDE (`~/.agents/skills/typecraft-skills/`)
- `codex` — OpenAI Codex CLI (`~/.agents/skills/typecraft-skills/`)
- `opencode` — OpenCode (`~/.agents/skills/typecraft-skills/`)
- `gemini-cli` — Gemini CLI (`~/.gemini/skills/typecraft-skills/`)
- `github-copilot` — GitHub Copilot Agent / VS Code (`~/.copilot/skills/typecraft-skills/`)

---

## 2. One-URL Installation in Fresh Agent Sessions

To install TypeCraft in a fresh conversation with a compatible AI agent, simply provide the canonical repository URL:

```text
https://github.com/krupakar5535Kk/typecraft-skills.git
Install this skill.
```

The receiving agent inspects this repository, discovers `skills/typecraft-skills/`, identifies its own host platform ID, and executes the standard `skills add` command globally.

---

## 3. Collision Protection

Before installing:
- Check if `typecraft-skills` is already present at your agent's skill location.
- If an existing installation matches the canonical 21 files, it is already verified.
- If an existing installation contains local modifications or an unrelated skill shares the folder name, preserve the files and notify the user rather than silently overwriting.

---

## 4. Offline / Python Fallback Route

If Node.js or `npx` is unavailable in the environment, use TypeCraft's bundled Python installer:

```bash
python3 -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope user
```

*(Use `--force` only if you explicitly authorize replacing an existing copy).*

---

## 5. Browser-Based Platform Route

For browser-only chat environments (ChatGPT Web, Claude.ai, Gemini Web) without local filesystem access:

1. Download the verified release archive:
   - [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip)
   - [SHA256SUMS](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/SHA256SUMS)
2. Follow platform-specific upload steps:
   - **Gemini Web:** Open **Customize → Skills → Upload a skill** (available on Gemini Advanced or Workspace with custom skills enabled). Alternatively, paste `skills/typecraft-skills/SKILL.md` into a **Custom Gem**.
   - **Claude.ai / Claude Cowork:** Open **Customize → Skills → Create skill → Upload a skill** (or add `SKILL.md` to Project Knowledge).
   - **ChatGPT Web:** Open **Plugins → Plugin Directory → Skills → Create → Upload from your computer** (or attach to Custom GPT Knowledge).

---

## 6. Verification Checklist

A complete installation contains:
- `skills/typecraft-skills/SKILL.md`
- 10 typography styles under `references/design-styles/`
- 10 design templates under `references/design-templates/`
- Total: Exactly 21 canonical files.
