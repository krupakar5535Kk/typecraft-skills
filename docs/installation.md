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

The URL alone (with or without `.git` or followed by "Install this skill") signals installation intent. Tool-enabled agents with command execution permissions inspect the repository, read [BOOTSTRAP.md](../BOOTSTRAP.md) and [INSTALL.md](../INSTALL.md), identify their active platform, and autonomously install TypeCraft globally using the standard Agent Skills CLI.

---

## 2. Standard Installation Route (Official Skills CLI)

TypeCraft adopts the standard Agent Skills distribution ecosystem using the official Vercel Skills CLI (`skills`).

### Primary Command (Active Agent, Global Scope)

```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --global \
  --agent <ACTIVE_AGENT_ID> \
  --copy \
  --yes
```

### Installation Scope Options:
- **Active Agent Global (Default & Recommended):** `--global --agent <ACTIVE_AGENT_ID> --copy` installs the skill physically into the user's persistent global directory for that agent.
- **All Local Agents:** `--global --agent '*' --copy` installs TypeCraft across all supported AI coding agents detected on the local system.
- **Project Scope:** Omit `--global` to link or copy the skill into the current repository workspace (e.g. `.agents/skills/` or `.claude/skills/`).

### Target Agent Platform Identifiers:
- `antigravity` — Google Antigravity App / IDE (`~/.gemini/config/skills/typecraft-skills/`)
- `antigravity-cli` — Google Antigravity CLI (`~/.gemini/antigravity-cli/skills/typecraft-skills/`)
- `claude-code` — Claude Code CLI / IDE (`~/.claude/skills/typecraft-skills/`)
- `cursor` — Cursor IDE (`~/.cursor/skills/typecraft-skills/` & `~/.agents/skills/typecraft-skills/`)
- `codex` — OpenAI Codex CLI / IDE (`~/.agents/skills/typecraft-skills/` & `~/.codex/skills/typecraft-skills/`)
- `opencode` — OpenCode (`~/.config/opencode/skills/typecraft-skills/` & `~/.agents/skills/typecraft-skills/`)
- `gemini-cli` — Gemini CLI (`~/.gemini/skills/typecraft-skills/`)
- `github-copilot` — GitHub Copilot Agent / VS Code (`~/.copilot/skills/typecraft-skills/`)

---

## 3. Detailed Guide by IDE and Agent Environment

### 1. Google Antigravity IDE (`antigravity`)
- **Target:** `~/.gemini/config/skills/typecraft-skills/`
- **Mechanism:** In the Antigravity conversation, the agent runs `npx --yes skills add ... --global --agent antigravity --copy --yes`.
- **Discovery:** Verified natively in the Antigravity IDE skill catalog and live session context.
- **Persistence:** All 21 canonical files are copied physically to disk.

### 2. Claude Free — Claude Web/Desktop Skills
- **Platform Reality:** Claude Free operates in a sandboxed chat interface without local terminal tools.
- **Official Route:**
  1. Open user avatar/profile → **Settings** → **Capabilities**.
  2. Ensure **Code execution and file creation** is enabled.
  3. Navigate to **Customize** → **Skills**.
  4. Select **Create skill** → **Upload a skill**.
  5. Upload [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip).
  6. Confirm TypeCraft appears in the Skills list and is toggled **Enabled**.
- *Important:* Account-level Claude Skills upload and local IDE skill installation are separate. Uploading to Claude Free does not install or entitle local Claude Code CLI.

### 3. Claude Code IDE Integration (`claude-code`)
- **Target:** `~/.claude/skills/typecraft-skills/`
- **Installation:** Run `npx --yes skills add ... --global --agent claude-code --copy --yes`.
- **Discovery:** Verified via the `/skills` command.
- **Plan Eligibility:** Claude Code requires an active Anthropic subscription (Pro/Team/Enterprise) or supported API key; it is **not included in Claude Free**.

### 4. Cursor IDE (`cursor`)
- **Target:** `~/.cursor/skills/typecraft-skills/` and shared `~/.agents/skills/typecraft-skills/`.
- **Installation:** Run `npx --yes skills add ... --global --agent cursor --copy --yes`.
- **Discovery:** Discovered in Cursor Features > Skills and Agent skill selector (`/typecraft-skills`).
- *Important:* Local personal skills do not automatically synchronize to remote Cursor Cloud Agents.

### 5. OpenAI Codex IDE (`codex`)
- **Target:** `~/.agents/skills/typecraft-skills/` and `$CODEX_HOME/skills/typecraft-skills` (`~/.codex/skills/typecraft-skills`).
- **Installation:** Run `npx --yes skills add ... --global --agent codex --copy --yes`.
- **Discovery:** Verified via internal index and bundled `$skill-installer`.
- **Usage Limits:** ChatGPT Free includes Codex with strict rate limits. Hitting a rate limit (`hit your usage limit`) is an upstream quota boundary, not an installation failure.

### 6. OpenCode IDE / Agent Environment (`opencode`)
- **Target:** `~/.config/opencode/skills/typecraft-skills/` and `~/.agents/skills/typecraft-skills/`.
- **Installation:** Run `npx --yes skills add ... --global --agent opencode --copy --yes`.
- **Discovery:** Verified via `opencode skills list` and native file discovery.

### 7. VS Code with GitHub Copilot Agent (`github-copilot`)
- **Target:** `~/.copilot/skills/typecraft-skills/` (User) or `.github/skills/typecraft-skills/` (Project).
- **Installation:** Copilot Agent runs the command into the user's Copilot skills directory.
- **Discovery:** Automatically indexed in the VS Code Copilot Agent Skills inventory.

### 8. Gemini CLI (`gemini-cli`) vs Gemini Web
- **Gemini CLI:** Terminal agent. Installs to `~/.gemini/skills/typecraft-skills/`. Verified via `gemini skills list --all`.
- **Gemini Web:** Browser chat without local disk access. Direct eligible users (Gemini Advanced / Workspace) to **Customize → Skills → Upload a skill** with `typecraft-skills.zip`. For standard accounts, fallback to creating a **Custom Gem** with `skills/typecraft-skills/SKILL.md`.

### 9. Additional Officially Supported IDE Agents
Supported targets in the Vercel Skills CLI registry:
- **Windsurf:** `~/.codeium/windsurf/skills/` (`--agent windsurf`)
- **Zed:** `~/.agents/skills/` (`--agent zed`)
- **Cline:** `~/.agents/skills/` (`--agent cline`)
- **Roo Code:** `~/.roo/skills/` (`--agent roo`)
- **Devin:** `~/.config/devin/skills/` (`--agent devin`)
- **Trae:** `~/.trae/skills/` (`--agent trae`)
- **Universal Wildcard:** `--agent '*'` installs across all detected local coding agents simultaneously.

---

## 4. Offline / Maintainer Python Fallback Route

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

## 5. Browser-Based Platform Route (ChatGPT, Claude.ai, Gemini Web)

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

---

## 6. Platform Evaluation Stages & Compatibility Matrix

To prevent misleading claims, TypeCraft strictly separates four lifecycle stages:
1. **Installation** — Files copied to a documented native directory or archive uploaded.
2. **Discovery** — The platform's native skill catalog affirmatively indexes TypeCraft (`copilot skill list`, `gemini skills list`, `/skills` in Claude Code, `$skill-installer` in Codex).
3. **Invocation** — The agent model actually accesses, parses, and applies TypeCraft typography styles or design templates in a real creative task.
4. **Persistence** — Availability across fresh, independent conversations without reinstallation.

### Evaluation Summary

| Surface | Status | Route | Verified Evidence |
|---|---|---|---|
| **Google Antigravity App / IDE** | **verified** | Standard CLI (`~/.gemini/config/skills/`) | Live installation, catalog indexing, and in-session model invocation verified in Antigravity v2.31.0. |
| **GitHub Copilot CLI** | **verified** | Native directory (`~/.copilot/skills/`) | Full installation, discovery (`copilot skill list`), and model invocation verified on CLI 1.0.105 & 1.0.114. |
| **GitHub Copilot VS Code Agent** | **verified** | GitHub CLI managed (`~/.copilot/skills/`) | Historical installation, discovery, and invocation verified in GitHub Codespaces (v1.1.0). |
| **Gemini CLI** | **verified** | Native directory (`~/.gemini/skills/`) | User-scope installation and native discovery verified via `gemini skills list --all`; live model invocation blocked by headless OAuth requirement. |
| **Claude Code CLI / IDE** | **compatible** | Standard CLI (`~/.claude/skills/`) | Route documented and verified with `skills add`; discovery confirmed via `/skills`; model invocation requires paid Anthropic plan / login. |
| **Cursor IDE** | **compatible** | Standard CLI (`~/.cursor/skills/`, `~/.agents/skills/`) | Route documented and verified with `skills add`; local user skills do not automatically sync to Cloud Agents. |
| **OpenAI Codex** | **compatible** | Standard CLI (`~/.agents/skills/`, `~/.codex/skills/`) | Route documented and verified with `skills add`; live invocation on Free accounts subject to upstream usage quota limits. |
| **OpenCode** | **compatible** | Standard CLI (`~/.config/opencode/skills/`, `~/.agents/skills/`) | Route documented and verified with `skills add`; native discovery confirmed. |
| **ChatGPT / Claude.ai / Cowork / Gemini Web** | **compatible** | Release ZIP upload | Verified local packaging; upload, scan, and confirmation require user action and account eligibility. |
| **Windsurf** | **compatible** | Standard CLI (`~/.codeium/windsurf/skills/`) | Route documented in Vercel Skills CLI registry. |

See the complete [Compatibility Guide](compatibility.md) for detailed audit logs and recorded evidence.
