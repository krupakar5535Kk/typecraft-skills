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

The URL alone (with or without `.git` or followed by "Install this skill") signals installation intent. Tool-enabled agents with terminal and filesystem permissions inspect the repository, read [BOOTSTRAP.md](../BOOTSTRAP.md) and [INSTALL.md](../INSTALL.md), detect their active platform identity, and install the complete canonical skill atomically using TypeCraft's safe installer.

Do not prompt the user to run terminal commands manually when the agent has execution capabilities.

---

## 2. Local-Agent Installation Route (CLI & Terminal Agents)

When running inside an interactive terminal, local CLI agent, or reviewed checkout, run TypeCraft's authoritative collision-protected installer:

### Command Syntax

```bash
# From repository root with Python environment:
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent auto \
  --scope user
```

On Windows PowerShell:
```powershell
python -m scripts.install_url `
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." `
  --agent auto `
  --scope user
```

### Options & Flags
- `--agent auto`: Automatically detects the host runtime from environment signals (`TYPECRAFT_AGENT` or unambiguous host signals).
- `--agent <HOST_ID>`: Targets an explicit agent identity (e.g. `claude-code`, `gemini-cli`, `codex`, `cursor`, `antigravity`, `antigravity-cli`, `opencode`, `github-copilot`).
- `--scope user`: Installs globally to the user's home configuration directory (default, recommended for persistence across sessions).
- `--scope project`: Installs locally into the current repository workspace (e.g. `.claude/skills/`, `.agents/skills/`, or `.github/skills/`).
- `--engine auto|native|vercel|gh`: Selects the installation engine. External engines (`vercel` and `gh`) are pre-checked by TypeCraft's collision guard.
- `--force`: Authorizes replacing or updating an existing installation after explicit review.
- `--json`: Outputs machine-readable installation status.

### Automated Collision & Overwrite Safety
TypeCraft checks candidate destinations before writing files:
- **No existing copy:** Installs all 21 canonical files cleanly.
- **Identical installation:** Detects matching SHA-256 tree; reports verified without rewriting.
- **Modified copy:** Safely halts (`ExistingInstallationError`) to protect local user customizations unless `--force` is explicitly provided.
- **Name collision:** Safely halts if a different skill shares the folder name.

---

## 3. Browser-Based Platform Route (ChatGPT, Claude.ai, Gemini Web)

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
- **ChatGPT Web:** Open **Plugins → Plugin Directory → Skills → Create → Upload from your computer** (or attach the ZIP / `SKILL.md` to **Custom GPT → Knowledge**). Availability is subject to workspace plan and policy.
- **Claude.ai / Claude Cowork:** Open **Customize → Skills → Create skill → Upload a skill** (or add `typecraft-skills/SKILL.md` to **Project Knowledge**). Enable the skill after upload.
- **Gemini Web:** Attach `typecraft-skills/SKILL.md` to your conversation or embed it into a **Custom Gem**.

---

## 4. Platform Evaluation Stages & Compatibility Matrix

To prevent misleading claims, TypeCraft strictly separates four lifecycle stages:
1. **Installation** — Files copied to a documented native directory or archive uploaded.
2. **Discovery** — The platform's native skill catalog affirmatively indexes TypeCraft (`copilot skill list`, `gemini skills list`, `/skills` in Claude Code, `$skill-installer` in Codex).
3. **Invocation** — The agent model actually accesses, parses, and applies TypeCraft typography styles or design templates in a real creative task.
4. **Persistence** — Availability across fresh, independent conversations without reinstallation.

### Status Definitions
- **verified** — TypeCraft files were installed and the platform itself discovered the skill in the recorded environment.
- **compatible** — Official product documentation establishes a supported Agent Skills format and route; full end-to-end model invocation is unverified.
- **research_required** — Product support, installation paths, or runtime behavior is unconfirmed.
- **unsupported** — No persistent installation route is available.

### Platform Summary Matrix

| Platform Surface | Status | Documented Route & Scope | File Verification | Native Discovery | Model Invocation | Persistence |
|---|---|---|---|---|---|---|
| **GitHub Copilot CLI** | **verified** | `~/.copilot/skills/` or `.github/skills/` | Verified: 21/21 files SHA-256 matched | Verified (`copilot skill list --json`) in CLI 1.0.105 & 1.0.114 | Verified: Swiss Style & Cinematic Poster exercised | User & project directory |
| **GitHub Copilot VS Code Agent** | **verified** | GitHub CLI managed (`~/.copilot/skills/`) | Verified: 21/21 files matched | Verified in VS Code Agent in Codespaces | Verified (historical v1.1.0 Codespaces session) | User scope in Codespaces |
| **Gemini CLI** | **verified** | `~/.gemini/skills/` or `.gemini/skills/` | Verified: 21/21 files SHA-256 matched | Verified (`gemini skills list --all` in v0.70.0 & v0.71.1) | Not verified (headless execution blocked by interactive browser OAuth) | User directory |
| **OpenAI Codex** | **compatible** | `~/.agents/skills/` or `~/.codex/skills/` | Verified in test suite (21/21 files matched) | Native index and bundled `$skill-installer` registered | Not verified (live CLI execution blocked by upstream account usage quota limit) | User directory |
| **Claude Code, local** | **compatible** | `~/.claude/skills/` or `.claude/skills/` | Isolated installer & SHA-256 verified | Documented (`/skills`); user-reported discovery observed | Not tested | User directory |
| **Cursor local Agent** | **compatible** | Shared `~/.agents/skills/` or `.agents/skills/` | Isolated installer & SHA-256 verified | Documented (Cursor Features > Skills panel) | Not tested | User directory |
| **Google Antigravity App** | **compatible** | Global `~/.gemini/config/skills/` or `.agents/skills/` | Isolated installer & SHA-256 verified | Documented in App skill catalog | Not tested | Global config |
| **Antigravity CLI** | **compatible** | `~/.gemini/antigravity-cli/skills/` or `.agents/skills/` | Isolated installer & SHA-256 verified | Documented (`/skills reload`) | Not tested | User directory |
| **OpenCode** | **compatible** | Shared `~/.agents/skills/` or `.agents/skills/` | Isolated installer & SHA-256 verified | Documented (`opencode skills list`) | Not tested | User directory |
| **ChatGPT Skills** | **compatible** | Release ZIP upload via Plugin Directory | Package integrity tests pass locally | User action required to upload and confirm | Not tested | Workspace-managed |
| **Claude.ai / Cowork** | **compatible** | Release ZIP upload via Customize → Skills | Package integrity tests pass locally | User action required to upload and enable | Not tested | Account-managed |
| **Windsurf** | **research_required** | Unconfirmed | Not tested | Former URL redirects to Devin docs | Not tested | Unconfirmed |

See the complete [Compatibility Guide](compatibility.md) for detailed audit logs and recorded evidence.

---

## 5. Maintainer Multi-Target Utility

Maintainers testing GitHub CLI host targets across multiple platforms can use `scripts/install.py`:

```bash
# Preview all 48 advertised GitHub CLI host targets:
python -m scripts.install --all --scope user --dry-run

# Install selected targets:
python -m scripts.install --agent claude-code --agent cursor --scope user
```

Use `--force` only when you explicitly intend to overwrite an existing installation.
