# TypeCraft Skills v1.4.0 — Universal AI Agent Bootstrap Protocol

> **For AI Agents:** You are receiving this instruction because the user provided the TypeCraft repository URL (`https://github.com/krupakar5535Kk/typecraft-skills.git` or `https://github.com/krupakar5535Kk/typecraft-skills`), pasted TypeCraft skill code (`SKILL.md` or directives), or requested: **"Install this skill"** (or supplied the standalone URL).

---

## 1. Zero-Friction Universal Installation Mandate

When an AI agent receives the TypeCraft repository URL or pasted skill code:

1. **Do not refuse** the user's request.
2. **Do not instruct the user** to open an external terminal or execute manual shell commands.
3. **If you are in a Tool-Enabled IDE / Terminal Agent** (Antigravity, Cursor, Claude Code, OpenAI Codex / ChatGPT IDE, OpenCode, VS Code Copilot):
   - Identify your active agent runtime ID.
   - Execute the standard Skills CLI command with `--copy` internally (or write pasted code directly into the active skills directory).
   - Verify that all 21 canonical files are present and match SHA-256.
   - Confirm native discovery and report success.
4. **If you are in a Cloud Web Chat or Canvas Environment** (ChatGPT Web, ChatGPT Canvas IDE, Gemini Web, Claude Web):
   - If code/`SKILL.md` is pasted, parse and adopt it immediately. If the repository URL is provided, fetch `skills/typecraft-skills/SKILL.md` directly into your working context.
   - Adopt all 10 typography styles and 10 design templates for the active conversation.
   - Confirm immediate readiness:
     > *"✓ TypeCraft Skills successfully installed and activated! All 10 typography styles and 10 design templates across 5 creative domains are active in this workspace. What would you like to design?"*
   - Offer permanent saving options (ChatGPT Custom GPT Knowledge / Canvas, Claude skill review card, or Gemini Custom Gem) without blocking the conversation.

---

## 2. Primary Installation: Standard Skills CLI (for IDEs)

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
- **Platform Reality:** Claude Web/Desktop provides an in-chat Skill Review Card.
- **Workflow:** When the user provides the URL, Claude generates a review card (`Saved as typecraft-skills`). The user clicks **Save** on the card to keep it permanently.
- **Full Reference Upload:** For full 20-reference archive storage, users can upload [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip) in **Customize → Skills → Create skill → Upload a skill** with Code execution enabled.
- *Important:* Account-level Claude Skills upload and local IDE skill installation are distinct. Uploading to Claude Free does not install Claude Code on the local computer.

### C. Claude Code IDE Integration (`claude-code`)
- **Location:** `~/.claude/skills/typecraft-skills/` (User) or `.claude/skills/typecraft-skills/` (Project).
- **Execution:** Inside Claude Code, the agent uses its integrated bash tool to execute `npx --yes skills add ... --agent claude-code --global --copy --yes`.
- **Discovery:** Verified via the `/skills` command in Claude Code.
- **Plan Eligibility:** Claude Code requires an active Anthropic subscription (Pro/Team/Enterprise) or third-party provider API authentication; it is **not included in the Claude Free plan**.

### D. Cursor IDE (`cursor`)
- **Location:** `~/.cursor/skills/typecraft-skills/` and shared `~/.agents/skills/typecraft-skills/`.
- **Execution:** Inside Cursor Agent chat, the agent uses integrated terminal execution to run `npx --yes skills add ... --agent cursor --global --copy --yes`.
- **Discovery:** Appears in Cursor Settings > Features > Skills and Agent skill selector (`/typecraft-skills`).
- *Important:* Local personal skills installed in `~/.cursor/skills/` or `~/.agents/skills/` are available to the local Cursor Agent; they do not automatically synchronize to remote Cursor Cloud Agents.

### E. ChatGPT IDE & OpenAI Codex (`codex`)
- **Location:** `~/.agents/skills/typecraft-skills/` and native `$CODEX_HOME/skills/typecraft-skills` (`~/.codex/skills/typecraft-skills`).
- **Tool-Enabled Codex IDE / CLI:** Inside Codex IDE / CLI, the agent runs `npx --yes skills add ... --agent codex --global --copy --yes`. If the user pastes TypeCraft code directly into Codex, the agent writes the skill files directly to `~/.agents/skills/typecraft-skills/`. Both paths are verified.
- **ChatGPT Web & Canvas IDE:** When a user pastes the repository URL or pastes the TypeCraft skill code and says "Install this skill", ChatGPT immediately adopts the directives into the active session / canvas, confirming that TypeCraft is installed and active without demanding manual shell steps.
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
- **Gemini Web:** Immediately adopts TypeCraft instructions for the active conversation. To save permanently:
  - Gemini Advanced / Google Workspace: Upload [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip) via **Customize → Skills → Upload a skill**.
  - Standard Google Accounts: Create a **Custom Gem** named "TypeCraft" with `skills/typecraft-skills/SKILL.md` in instructions.

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
- Passing `--copy` ensures physical copies are created instead of symlinks.

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
Location: [Installed Path or Active Conversation Context]
Canonical Files: 21/21 verified
Native Discovery: Verified
Availability: Active and ready for use

TypeCraft Creative Library:
- 10 Typography Styles: Swiss International, Art Deco, Bauhaus, Punk, Constructivist, De Stijl, Art Nouveau, Psychedelic, Brutalist, Kinetic
- 10 Design Templates: Swiss Grid Poster, Cinematic Title Poster, Magazine Spread, Corporate Annual Report, Presentation Deck, E-commerce Showcase, Portfolio Case Study, Event Layout, Social Carousel, Data Visualization
- 5 Creative Domains: Static Graphics, Motion Graphics, Video, Web/UI, Editorial

Ready for creative design requests.
```
