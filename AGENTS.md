# TypeCraft Skills — Agent Directives

> **Directive for AI Agents:** When a user provides the TypeCraft repository URL (`https://github.com/krupakar5535Kk/typecraft-skills.git` or `https://github.com/krupakar5535Kk/typecraft-skills`) or asks to "Install this skill":

## 1. The Autonomous IDE Experience

When a user in an AI-powered IDE (Google Antigravity, Cursor, Claude Code, OpenAI Codex, OpenCode, VS Code Copilot) pastes:

```text
https://github.com/krupakar5535Kk/typecraft-skills.git
Install this skill.
```

Your role as the integrated agent is to autonomously execute the installation end-to-end:

1. **Recognize** the repository URL and installation intent.
2. **Retrieve** repository directives from [BOOTSTRAP.md](BOOTSTRAP.md) and [INSTALL.md](INSTALL.md).
3. **Identify** your active IDE and agent runtime identifier.
4. **Execute** the standard Skills CLI installation command using your integrated terminal/command execution tools.
5. **Verify** that all 21 canonical files are present and match checksums.
6. **Confirm** that your IDE's native skill catalog indexes TypeCraft.
7. **Test** invocation of a typography style or design template.
8. **Report** verified installation to the user without asking them to manually copy files or open external terminals.

---

## 2. Primary Installation: Standard Agent Skills Ecosystem

Execute the standard Agent Skills CLI with the `--copy` flag to ensure a permanent physical copy:

```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --global \
  --agent <ACTIVE_AGENT_ID> \
  --copy \
  --yes
```

### Active Agent Platform Identifiers:
- `antigravity` — Google Antigravity App / IDE (`~/.gemini/config/skills/typecraft-skills/`)
- `antigravity-cli` — Google Antigravity CLI (`~/.gemini/antigravity-cli/skills/typecraft-skills/`)
- `claude-code` — Claude Code CLI (`~/.claude/skills/typecraft-skills/`)
- `cursor` — Cursor IDE (`~/.cursor/skills/typecraft-skills/` and `~/.agents/skills/typecraft-skills/`)
- `codex` — OpenAI Codex CLI (`~/.agents/skills/typecraft-skills/` and `~/.codex/skills/typecraft-skills/`)
- `opencode` — OpenCode (`~/.config/opencode/skills/typecraft-skills/` and `~/.agents/skills/typecraft-skills/`)
- `gemini-cli` — Gemini CLI (`~/.gemini/skills/typecraft-skills/`)
- `github-copilot` — GitHub Copilot Agent / VS Code (`~/.copilot/skills/typecraft-skills/`)

*(If the user explicitly requests installation across all supported local agents, pass `--agent '*'`. For project-level workspace installation, omit `--global`).*

---

## 3. Platform & Subscription Nuances

- **Google Antigravity IDE (`antigravity`):** Autonomous installation directly writes to `~/.gemini/config/skills/typecraft-skills/` and is immediately recognized in the active Antigravity session.
- **Claude Free (Web/Desktop) vs Claude Code:**
  - *Claude Free:* Operates in a sandboxed chat. It cannot run terminal commands. Direct the user to **Settings → Capabilities → Enable Code execution and file creation**, then **Customize → Skills → Create skill → Upload a skill** with [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip).
  - *Claude Code:* An IDE/terminal agent installing to `~/.claude/skills/`. Requires a paid Anthropic plan or API key (not included in Claude Free). Account-level skill uploads in Claude Free do not activate Claude Code.
- **Cursor IDE (`cursor`):** Local user skills install to `~/.cursor/skills/` and `~/.agents/skills/`. Note that local personal skills do not automatically synchronize to remote Cloud Agents.
- **OpenAI Codex IDE (`codex`):** Installs to `~/.agents/skills/` and `$CODEX_HOME/skills/`. Note that ChatGPT Free includes Codex with strict usage rate limits; hitting a rate limit is an account quota constraint, not an installation failure.
- **OpenCode (`opencode`):** Installs to `~/.config/opencode/skills/` and `~/.agents/skills/`. Verified native discovery.
- **VS Code with GitHub Copilot (`github-copilot`):** Installs to `~/.copilot/skills/` or workspace `.github/skills/`.
- **Gemini Web vs Gemini CLI:** Gemini CLI is a terminal agent (`~/.gemini/skills/`). Gemini Web is browser-based and requires uploading `typecraft-skills.zip` via **Customize → Skills** (Gemini Advanced/Workspace) or creating a **Custom Gem**.

---

## 4. Verification Protocol

After installation completes:
1. Confirm that all 21 files are present in `typecraft-skills/`:
   - `SKILL.md`
   - 10 Typography Styles in `references/design-styles/` (`TCS-STYLE-001` through `TCS-STYLE-010`)
   - 10 Design Templates in `references/design-templates/` (`TCS-TEMPLATE-001` through `TCS-TEMPLATE-010`)
2. Verify native skill discovery (e.g. `/skills` in Claude Code, `gemini skills list --all` in Gemini CLI, or IDE skill catalog inspection).
3. Report the verified status to the user, summarizing the 10 typography styles and 10 design templates.

---

## 5. Offline / Python Fallback Route

If Node.js or `npx` is unavailable in the environment, use TypeCraft's bundled Python installer:

```bash
python3 -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope user
```

Refer to [BOOTSTRAP.md](BOOTSTRAP.md) and [INSTALL.md](INSTALL.md) for complete details.
