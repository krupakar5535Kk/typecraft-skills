# TypeCraft Skills v1.4.0 — Universal AI Agent Bootstrap Protocol

> **For AI Agents:** You are receiving this instruction because the user provided the TypeCraft repository URL (`https://github.com/krupakar5535Kk/typecraft-skills.git` or `https://github.com/krupakar5535Kk/typecraft-skills`) and requested: **"Install this skill"** (or supplied the standalone URL).

---

## 1. Zero-Friction Autonomous IDE Installation

When an AI coding agent with command execution capabilities receives the TypeCraft repository URL:

1. **Do not** instruct the user to open an external terminal or execute manual shell commands.
2. **Do not** require the user to install Python packages or clone repositories manually.
3. **Do not** install TypeCraft to every tool on the computer unless explicitly requested via `--agent '*'`.
4. **Identify** your active agent platform ID.
5. **Install** the canonical `typecraft-skills` globally for your active agent using the standard Agent Skills ecosystem with physical copying (`--copy`).
6. **Verify** that all 21 canonical files are present and uncorrupted.
7. **Confirm** native skill discovery in your active environment.
8. **Report** the verified result and summarize the typography and design library.

---

## 2. Primary Installation: Standard Skills CLI

Execute the standard Agent Skills command:

```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --global \
  --agent <ACTIVE_AGENT_ID> \
  --copy \
  --yes
```

### Installation Scope Options:
- **Active Agent Global (Default & Recommended):** `--global --agent <ACTIVE_AGENT_ID> --copy` (physically installs into the user's persistent global directory).
- **All Local Agents:** `--global --agent '*' --copy` (use only when the user explicitly asks to install across all supported local tools).
- **Project Scope:** Omit `--global` (installs into the current repository's `.agents/skills/` or equivalent).

---

## 3. Supported Agent Targets & Native Paths

| Agent Target ID | Product Surface | User-Scope Persistent Directory | Project-Scope Directory | Native Discovery |
|---|---|---|---|---|
| **`antigravity`** | Google Antigravity App / IDE | `~/.gemini/config/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | App skill catalog / auto-load |
| **`antigravity-cli`** | Google Antigravity CLI | `~/.gemini/antigravity-cli/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | `/skills reload` command |
| **`claude-code`** | Claude Code IDE / CLI | `~/.claude/skills/typecraft-skills/` | `.claude/skills/typecraft-skills/` | `/skills` command in session |
| **`cursor`** | Cursor IDE | `~/.cursor/skills/typecraft-skills/` & `~/.agents/skills/` | `.cursor/skills/` or `.agents/skills/` | Cursor Features > Skills panel |
| **`codex`** | OpenAI Codex IDE / CLI | `~/.agents/skills/` & `~/.codex/skills/` | `.agents/skills/typecraft-skills/` | Native `$CODEX_HOME/skills` / `.agents` |
| **`opencode`** | OpenCode IDE / CLI | `~/.config/opencode/skills/` & `~/.agents/skills/` | `.opencode/skills/` or `.agents/skills/` | `opencode skills list` |
| **`gemini-cli`** | Gemini CLI | `~/.gemini/skills/typecraft-skills/` | `.gemini/skills/typecraft-skills/` | `gemini skills list --all` |
| **`github-copilot`** | GitHub Copilot Agent (VS Code) | `~/.copilot/skills/typecraft-skills/` | `.github/skills/typecraft-skills/` | Copilot Agent Skills inventory |

---

## 4. Deep-Dive: Target IDE and Agent Environments

### A. Google Antigravity IDE (`antigravity`)
- **Location:** `~/.gemini/config/skills/typecraft-skills/` (User) or `.agents/skills/typecraft-skills/` (Workspace).
- **Behavior:** Antigravity IDE automatically discovers and indexes skills placed in `~/.gemini/config/skills/`. The agent in Antigravity chat autonomously runs `npx --yes skills add ... --global --agent antigravity --copy --yes`, verifying all 21 files. Skill is immediately available in session context without restarting.

### B. Claude Free — Claude Web/Desktop Skills
- **Platform Reality:** Claude Free runs in a sandboxed conversational interface without terminal access.
- **Official Route:**
  1. Open user avatar/profile → **Settings** → **Capabilities**.
  2. Ensure **Code execution and file creation** is enabled.
  3. Navigate to **Customize** → **Skills**.
  4. Select **Create skill** → **Upload a skill**.
  5. Upload [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip) (verified SHA256 checksum in [SHA256SUMS](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/SHA256SUMS)).
  6. Confirm TypeCraft appears in the Skills list and is toggled **Enabled**.
- *Important:* Account-level Claude Skills upload and local IDE skill installation are distinct. Uploading to Claude Free does not install Claude Code on the local computer.

### C. Claude Code IDE Integration (`claude-code`)
- **Location:** `~/.claude/skills/typecraft-skills/` (User) or `.claude/skills/typecraft-skills/` (Project).
- **Execution:** Inside Claude Code, the agent uses its integrated bash tool to execute `npx --yes skills add ... --agent claude-code --global --copy --yes`.
- **Discovery:** Verified via the `/skills` command in Claude Code.
- **Plan Eligibility:** Claude Code requires an active Anthropic subscription (Pro/Team/Enterprise) or third-party provider API authentication; it is **not included in the Claude Free plan**. Do not promise Claude Code activation on a Free account.

### D. Cursor IDE (`cursor`)
- **Location:** `~/.cursor/skills/typecraft-skills/` and shared `~/.agents/skills/typecraft-skills/`.
- **Execution:** Inside Cursor Agent chat, the agent uses integrated terminal execution to run `npx --yes skills add ... --agent cursor --global --copy --yes`.
- **Discovery:** Appears in Cursor Settings > Features > Skills and Agent skill selector (`/typecraft-skills`).
- *Important:* Local personal skills installed in `~/.cursor/skills/` or `~/.agents/skills/` are available to the local Cursor Agent; they do not automatically synchronize to remote Cursor Cloud Agents.

### E. OpenAI Codex IDE (`codex`)
- **Location:** `~/.agents/skills/typecraft-skills/` and native `$CODEX_HOME/skills/typecraft-skills` (`~/.codex/skills/typecraft-skills`).
- **Execution:** Inside Codex IDE / CLI, the agent runs `npx --yes skills add ... --agent codex --global --copy --yes`.
- **Discovery:** Verified via Codex's internal skill registry and bundled `$skill-installer`.
- **Usage Limits:** Codex is available on ChatGPT Free with strict usage rate limits. If a prompt triggers `ERROR: You’ve hit your usage limit. Upgrade to Plus to continue using Codex`, this reflects an upstream account quota constraint, not an installation failure.

### F. OpenCode IDE / Agent Environment (`opencode`)
- **Location:** `~/.config/opencode/skills/typecraft-skills/` and `~/.agents/skills/typecraft-skills/`.
- **Execution:** Inside OpenCode Agent conversation, executes `npx --yes skills add ... --agent opencode --global --copy --yes`.
- **Discovery:** Verified via `opencode skills list` or native discovery.

### G. VS Code with GitHub Copilot Agent (`github-copilot`)
- **Location:** `~/.copilot/skills/typecraft-skills/` (User) or `.github/skills/typecraft-skills/` (Project).
- **Execution:** Copilot Agent runs the installation command into the user's Copilot skills directory.
- **Discovery:** Automatically indexed in the VS Code Copilot Agent Skills inventory.

### H. Gemini CLI (`gemini-cli`) vs Gemini Web
- **Gemini CLI:** Terminal agent. Installs to `~/.gemini/skills/typecraft-skills/`. Verified via `gemini skills list --all`.
- **Gemini Web:** Browser chat without local disk access. Direct eligible users (Gemini Advanced / Workspace) to **Customize → Skills → Upload a skill** with `typecraft-skills.zip`. For standard accounts, fallback to creating a **Custom Gem** pasting `skills/typecraft-skills/SKILL.md`.

### I. Additional Officially Supported IDE Agents
The Vercel Skills CLI registry supports over 40 agent platforms:
- **Windsurf:** `~/.codeium/windsurf/skills/` (`--agent windsurf`)
- **Zed:** `~/.agents/skills/` (`--agent zed`)
- **Cline:** `~/.agents/skills/` (`--agent cline`)
- **Roo Code:** `~/.roo/skills/` (`--agent roo`)
- **Devin:** `~/.config/devin/skills/` (`--agent devin`)
- **Trae:** `~/.trae/skills/` (`--agent trae`)
- **Universal Wildcard:** `--agent '*'` installs across all detected local coding agents simultaneously.

---

## 5. Collision & Overwrite Safety

Before writing files:
- Inspect the destination directory.
- If TypeCraft is already installed and matches the canonical files (21/21 matching SHA-256), report it as already installed and verified.
- If an existing installation contains user modifications or a different skill shares the folder name, preserve the files and notify the user rather than silently overwriting.
- Passing `--copy` ensures physical copies are created instead of symlinks, preventing broken links if source repositories move.

---

## 6. Offline / Python Fallback Route

If Node.js or `npx` is not installed or the environment is offline, use TypeCraft's bundled Python installer:

```bash
python3 -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope user
```

*(Pass `--force` if you explicitly authorize overwriting an existing local copy).*

---

## 7. Verification & Success Acknowledgement

Confirm that:
1. Manifest `SKILL.md` is present.
2. All 10 styles in `references/design-styles/` and 10 templates in `references/design-templates/` exist (21 canonical files total).
3. The platform's native discovery mechanism recognizes the skill.

**Report Format:**

```text
TypeCraft Skills v1.4.0 successfully installed and verified.

Platform: [Active Agent Name and Version]
Location: [Installed Path]
Canonical Files: 21/21 verified
Native Discovery: Verified
Availability: Global user installation

TypeCraft Creative Library:
- 10 Typography Styles: Swiss International, Art Deco, Bauhaus, Punk, Constructivist, De Stijl, Art Nouveau, Psychedelic, Brutalist, Kinetic
- 10 Design Templates: Swiss Grid Poster, Cinematic Title Poster, Magazine Spread, Corporate Annual Report, Presentation Deck, E-commerce Showcase, Portfolio Case Study, Event Layout, Social Carousel, Data Visualization
- 5 Creative Domains: Static Graphics, Motion Graphics, Video, Web/UI, Editorial

Ready for creative design requests.
```
