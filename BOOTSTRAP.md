# TypeCraft Skills v1.4.0 — Universal AI Agent Bootstrap Protocol

> **For AI Agents:** You are receiving this instruction because the user provided the TypeCraft repository URL (`https://github.com/krupakar5535Kk/typecraft-skills.git` or `https://github.com/krupakar5535Kk/typecraft-skills`) and requested: **"Install this skill"** (or supplied the standalone URL).

---

## 1. Zero-Friction Installation Mandate

When an AI coding agent with command execution capabilities receives the TypeCraft repository URL:

1. **Do not** instruct the user to open a terminal or run manual clone commands.
2. **Do not** require the user to install Python packages just to install TypeCraft.
3. **Do not** install TypeCraft to every agent on the computer unless the user specifically asks for `--agent '*'`.
4. **Identify** your active agent platform ID.
5. **Install** the canonical `typecraft-skills` globally for your active agent using the standard Agent Skills ecosystem.
6. **Verify** that all 21 files are present and discoverable.
7. **Report** the verified result and summarize the typography and design library.

---

## 2. Primary Installation: Standard Skills CLI

Execute the standard Agent Skills command:

```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --global \
  --agent <ACTIVE_AGENT_ID> \
  --yes
```

### Installation Scope Options:
- **Active Agent Global (Default):** `--global --agent <ACTIVE_AGENT_ID>` (installs into user's persistent skill directory).
- **All Local Agents:** `--global --agent '*'` (use only when the user explicitly asks to install across all supported local tools).
- **Project Scope:** Omit `--global` (installs into the current repository's `.agents/skills/` or equivalent).

---

## 3. Supported Agent Targets & Native Paths

| Agent Target ID | Product Surface | User-Scope Persistent Directory | Project-Scope Directory | Native Discovery |
|---|---|---|---|---|
| **`antigravity`** | Google Antigravity App / IDE | `~/.gemini/config/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | App skill catalog |
| **`antigravity-cli`** | Google Antigravity CLI | `~/.gemini/antigravity-cli/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | `/skills reload` command |
| **`claude-code`** | Claude Code CLI | `~/.claude/skills/typecraft-skills/` | `.claude/skills/typecraft-skills/` | `/skills` command in session |
| **`cursor`** | Cursor IDE | `~/.agents/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | Cursor Features > Skills panel |
| **`codex`** | OpenAI Codex CLI | `~/.agents/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | Native `$CODEX_HOME/skills` / `.agents` |
| **`opencode`** | OpenCode | `~/.agents/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | `opencode skills list` |
| **`gemini-cli`** | Gemini CLI | `~/.gemini/skills/typecraft-skills/` | `.gemini/skills/typecraft-skills/` | `gemini skills list --all` |
| **`github-copilot`** | GitHub Copilot Agent (VS Code) | `~/.copilot/skills/typecraft-skills/` | `.github/skills/typecraft-skills/` | Copilot Agent Skills inventory |

### Surface Disambiguation
- **Antigravity App vs Antigravity CLI:** Antigravity App/IDE reads `~/.gemini/config/skills/`; CLI-specific target is `~/.gemini/antigravity-cli/skills/`. Both read workspace `.agents/skills/`.
- **Claude Code vs Claude.ai:** Claude Code has a local terminal and persistent directory (`~/.claude/skills/`). Claude.ai runs in the browser and requires account-level ZIP upload.
- **OpenAI Codex vs ChatGPT Web:** Codex uses `~/.agents/skills/`. ChatGPT web requires workspace skill or Custom GPT upload.
- **Gemini CLI vs Gemini Web/Mobile:** Gemini CLI is a terminal agent. Gemini Web requires Custom Skills ZIP upload or Custom Gems fallback.

---

## 4. Collision & Overwrite Safety

Before writing files:
- Inspect the destination directory.
- If TypeCraft is already installed and matches the canonical files, report it as already installed and verified.
- If an existing installation contains user modifications or a different skill shares the folder name, preserve the files and notify the user rather than silently overwriting.
- The standard CLI handles updates and linking; when explicit replacement is authorized, re-run with confirmation.

---

## 5. Offline / Python Fallback Route

If Node.js or `npx` is not installed or the environment is offline, use TypeCraft's bundled Python installer:

```bash
python3 -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope user
```

*(Pass `--force` if you explicitly intend to overwrite an existing local copy).*

---

## 6. Browser-Based Platform Handoff Protocol

If your runtime is a browser or mobile chat without persistent filesystem access:

1. **State the Platform Reality Honestly:**
   "This platform operates in a sandboxed browser environment without local filesystem installation capabilities. TypeCraft cannot be installed autonomously here."

2. **Provide Official Platform Handoff:**
   - **Gemini Web:** Direct eligible users (Gemini Advanced or Workspace) to **Customize → Skills → Upload a skill** with [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip). For standard accounts, fallback to creating a **Custom Gem** with `skills/typecraft-skills/SKILL.md` or attaching the file.
   - **Claude.ai / Claude Cowork:** Direct the user to **Customize → Skills → Create skill → Upload a skill** with `typecraft-skills.zip` (or add `SKILL.md` to Project Knowledge).
   - **ChatGPT Web:** Direct the user to **Plugins → Plugin Directory → Skills → Create → Upload from your computer** (or attach to Custom GPT Knowledge).

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
