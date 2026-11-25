# TypeCraft Skills — Installation

**ONE URL. ONE SKILL. EVERY COMPATIBLE AI AGENT.**

TypeCraft Skills is distributed as a single, canonical Agent Skill containing exactly 20 production-approved creative resources (10 typography styles and 10 design templates) located in `skills/typecraft-skills/`.

---

## 1. Quick Start: Install with One GitHub URL

Paste the canonical repository URL into your AI agent:

```text
https://github.com/krupakar5535Kk/typecraft-skills.git
Install this skill.
```

The URL alone (with or without `.git` or followed by "Install this skill") signals installation intent. Tool-enabled agents with command execution permissions inspect the repository, read [BOOTSTRAP.md](../BOOTSTRAP.md) and [INSTALL.md](../INSTALL.md), identify their active platform, and install TypeCraft globally using the standard Agent Skills CLI.

---

## 2. Standard Installation Route (Official Skills CLI)

TypeCraft adopts the standard Agent Skills distribution ecosystem using the official Vercel Skills CLI (`skills`).

### Primary Command (Active Agent, Global Scope)

```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --global \
  --agent <ACTIVE_AGENT_ID> \
  --yes
```

### Installation Scope Options:
- **Active Agent Global (Default & Recommended):** `--global --agent <ACTIVE_AGENT_ID>` installs the skill into the user's persistent global directory for that agent.
- **All Local Agents:** `--global --agent '*'` installs TypeCraft across all supported AI coding agents detected on the local system.
- **Project Scope:** Omit `--global` to link or copy the skill into the current repository workspace (e.g. `.agents/skills/` or `.claude/skills/`).

### Target Agent Platform Identifiers:
- `antigravity` — Google Antigravity App / IDE (`~/.gemini/config/skills/typecraft-skills/`)
- `antigravity-cli` — Google Antigravity CLI (`~/.gemini/antigravity-cli/skills/typecraft-skills/`)
- `claude-code` — Claude Code CLI (`~/.claude/skills/typecraft-skills/`)
- `cursor` — Cursor IDE (`~/.agents/skills/typecraft-skills/`)
- `codex` — OpenAI Codex CLI (`~/.agents/skills/typecraft-skills/`)
- `opencode` — OpenCode (`~/.agents/skills/typecraft-skills/`)
- `gemini-cli` — Gemini CLI (`~/.gemini/skills/typecraft-skills/`)
- `github-copilot` — GitHub Copilot Agent / VS Code (`~/.copilot/skills/typecraft-skills/`)

---

## 3. Offline / Maintainer Python Fallback Route

If Node.js or `npx` is unavailable in the environment, or for offline/sandboxed execution, use TypeCraft's bundled Python installer:

```bash
# User scope (global):
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope user

# Project scope:
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope project
```

On Windows PowerShell:
```powershell
python -m scripts.install_url `
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." `
  --agent <ACTIVE_AGENT_ID> `
  --scope user
```

### Automated Collision & Overwrite Safety
TypeCraft checks candidate destinations before writing files:
- **No existing copy:** Installs all 21 canonical files cleanly.
- **Identical installation:** Detects matching SHA-256 tree; reports verified without rewriting.
- **Modified copy:** Safely halts (`ExistingInstallationError`) to protect local user customizations unless `--force` is explicitly provided.
- **Name collision:** Safely halts if a different skill shares the folder name.

---

## 4. Browser-Based Platform Route (ChatGPT, Claude.ai, Gemini Web)

Browser-based chat platforms operate in sandboxed browser environments without local terminal or filesystem access. For these platforms, download the official release package and upload it directly:

- **Latest Downloadable Asset:** [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip)
- **Checksum Verification:** [SHA256SUMS](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/SHA256SUMS)

### Local Package Generation
You can also build the verified release archive locally from source:

```bash
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git" \
  --agent chatgpt \
  --package-output ./typecraft-skills.zip
```

The router verifies ZIP integrity, exact file paths (`typecraft-skills/` root), and content hashes.

### Platform Upload Steps
- **Gemini Web:**
  - *Custom Skills Upload (Primary):* Open **Customize → Skills** (or **More → Customize → Skills**), select **Upload a skill** (or **Upload file**), and upload `typecraft-skills.zip`. Review the parsed metadata and save. In chat, invoke via `@typecraft-skills` or `/typecraft-skills`. Custom Skills upload is available on Gemini Advanced or eligible Google Workspace (Business, Enterprise, Education) accounts with custom skills enabled.
  - *Custom Gems (Legacy / Fallback):* For standard consumer accounts or environments where Custom Skills upload is unavailable, open **Gem Manager → New Gem**, paste the contents of `skills/typecraft-skills/SKILL.md` into the Gem instructions, or attach `SKILL.md` directly into the chat session.
- **Claude.ai / Claude Cowork:** Open **Customize → Skills → Create skill → Upload a skill** (or add `typecraft-skills/SKILL.md` to **Project Knowledge**). Enable the skill after upload.
- **ChatGPT Web:** Open **Plugins → Plugin Directory → Skills → Create → Upload from your computer** (or attach the ZIP / `SKILL.md` to **Custom GPT → Knowledge**). Availability is subject to workspace plan and policy.

---

## 5. Platform Evaluation Stages & Compatibility Matrix

To prevent misleading claims, TypeCraft strictly separates four lifecycle stages:
1. **Installation** — Files copied to a documented native directory or archive uploaded.
2. **Discovery** — The platform's native skill catalog affirmatively indexes TypeCraft (`copilot skill list`, `gemini skills list`, `/skills` in Claude Code, `$skill-installer` in Codex).
3. **Invocation** — The agent model actually accesses, parses, and applies TypeCraft typography styles or design templates in a real creative task.
4. **Persistence** — Availability across fresh, independent conversations without reinstallation.

### Evaluation Summary

| Surface | Status | Route | Verified Evidence |
|---|---|---|---|
| **GitHub Copilot CLI** | **verified** | Native directory (`~/.copilot/skills/`) | Full installation, discovery (`copilot skill list`), and model invocation verified on CLI 1.0.105 & 1.0.114. |
| **GitHub Copilot VS Code Agent** | **verified** | GitHub CLI managed (`~/.copilot/skills/`) | Historical installation, discovery, and invocation verified in GitHub Codespaces (v1.1.0). |
| **Gemini CLI** | **verified** | Native directory (`~/.gemini/skills/`) | User-scope installation and native discovery verified via `gemini skills list --all`; live model invocation blocked by headless OAuth requirement. |
| **Google Antigravity App / CLI** | **compatible** | Standard CLI (`~/.gemini/config/skills/`, `~/.gemini/antigravity-cli/skills/`) | Live installation and catalog inspection verified; `/skills reload` supported. |
| **Claude Code CLI** | **compatible** | Standard CLI (`~/.claude/skills/`) | Route documented and verified with `skills add`; user-reported discovery observed; model invocation unverified in CI. |
| **Cursor IDE** | **compatible** | Standard CLI (`~/.agents/skills/`) | Route documented and verified with `skills add`; local user skills do not automatically sync to Cloud Agents. |
| **OpenAI Codex** | **compatible** | Standard CLI (`~/.agents/skills/`, `~/.codex/skills/`) | Route documented and verified with `skills add`; live invocation blocked by upstream account usage limit. |
| **OpenCode** | **compatible** | Standard CLI (`~/.agents/skills/`) | Route documented and verified with `skills add`. |
| **ChatGPT / Claude.ai / Cowork / Gemini Web** | **compatible** | Release ZIP upload | Verified local packaging; upload, scan, and confirmation require user action and account eligibility. |
| **Windsurf** | **research_required** | Unconfirmed | Former documentation URL redirects to Devin; native route unconfirmed. |

See the complete [Compatibility Guide](compatibility.md) for detailed audit logs and recorded evidence.
