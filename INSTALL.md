# TypeCraft Skills — Installation Guide

Canonical repository:
`https://github.com/krupakar5535Kk/typecraft-skills.git`

Canonical installable skill: `skills/typecraft-skills/`

---

## 1. Fast Installation (Standard Agent Skills CLI)

TypeCraft adopts the standard Agent Skills distribution ecosystem using the official Vercel Skills CLI (`skills`). If you are using any compatible AI coding agent with command execution capabilities, install TypeCraft directly:

```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --global \
  --agent <ACTIVE_AGENT_ID> \
  --copy \
  --yes
```

### Installation Scope Options:
- **Active Agent Global (Recommended):** `--global --agent <ACTIVE_AGENT_ID> --copy` (creates a permanent physical copy in the user's persistent skill directory).
- **All Local Agents:** `--global --agent '*' --copy` (installs across all supported AI coding agents detected on the machine).
- **Project Scope (Current Workspace):** Omit `--global` (installs into the active workspace's `.agents/skills/` or equivalent).

### Supported Agent Platform Identifiers:
- `antigravity` — Google Antigravity App / IDE (`~/.gemini/config/skills/typecraft-skills/`)
- `antigravity-cli` — Google Antigravity CLI (`~/.gemini/antigravity-cli/skills/typecraft-skills/`)
- `claude-code` — Claude Code CLI / IDE (`~/.claude/skills/typecraft-skills/`)
- `cursor` — Cursor IDE (`~/.cursor/skills/typecraft-skills/` & `~/.agents/skills/typecraft-skills/`)
- `codex` — OpenAI Codex CLI / IDE (`~/.agents/skills/typecraft-skills/` & `~/.codex/skills/typecraft-skills/`)
- `opencode` — OpenCode (`~/.config/opencode/skills/typecraft-skills/` & `~/.agents/skills/typecraft-skills/`)
- `gemini-cli` — Gemini CLI (`~/.gemini/skills/typecraft-skills/`)
- `github-copilot` — GitHub Copilot Agent / VS Code (`~/.copilot/skills/typecraft-skills/`)

---

## 2. One-URL Installation in Fresh Agent Sessions

To install TypeCraft in a fresh conversation with a compatible AI agent, simply provide the canonical repository URL:

```text
https://github.com/krupakar5535Kk/typecraft-skills.git
Install this skill.
```

The receiving agent inspects this repository, discovers `skills/typecraft-skills/`, identifies its own host platform ID, and autonomously executes the standard `skills add` command globally without requiring the user to open a separate terminal.

---

## 3. Detailed Guide by IDE and Agent Environment

### 1. Google Antigravity IDE (`antigravity`)
- **Target:** `~/.gemini/config/skills/typecraft-skills/`
- **Installation:** Agent autonomously runs `npx --yes skills add ... --global --agent antigravity --copy --yes`.
- **Discovery:** Antigravity IDE immediately indexes `typecraft-skills` into the live session context.
- **Persistence:** All 21 canonical files are copied physically to disk.

### 2. Claude Free — Claude Web/Desktop Skills
- **Platform Reality:** Claude Free operates in a sandboxed chat interface without local terminal tools.
- **Official Route:**
  1. Open user avatar/profile → **Settings** → **Capabilities**.
  2. Ensure **Code execution and file creation** is enabled.
  3. Navigate to **Customize** → **Skills**.
  4. Click **Create skill** → **Upload a skill**.
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

## 4. Collision & Overwrite Safety

Before writing files:
- Check if `typecraft-skills` is already present at your agent's skill location.
- If an existing installation matches the canonical 21 files, it is already verified.
- If an existing installation contains local modifications or an unrelated skill shares the folder name, preserve the files and notify the user rather than silently overwriting.
- Passing `--copy` guarantees physical copies are created instead of symlinks.

---

## 5. Offline / Python Fallback Route

If Node.js or `npx` is unavailable in the environment, use TypeCraft's bundled Python installer:

```bash
python3 -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope user
```

*(Use `--force` only if you explicitly authorize replacing an existing copy).*

---

## 6. Verification Checklist

A complete installation contains:
- `skills/typecraft-skills/SKILL.md`
- 10 typography styles under `references/design-styles/`
- 10 design templates under `references/design-templates/`
- Total: Exactly 21 canonical files.
