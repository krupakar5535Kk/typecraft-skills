# TypeCraft Skills — Agent Directives

> **Discovery Note:** This directive file is active when this repository or workspace is accessible to your active agent. If you received this repository URL in a fresh conversation, retrieve this repository to access these instructions and the safe authoritative installer.

## User Intent: "Install this skill" or Standalone GitHub URL

When a user provides the TypeCraft repository URL (`https://github.com/krupakar5535Kk/typecraft-skills.git` or `https://github.com/krupakar5535Kk/typecraft-skills`) or asks to "Install this skill":

1. **Do not prompt the user to run terminal commands or clone the repository manually.**
2. If you are an AI agent with terminal and filesystem execution tools, execute TypeCraft's authoritative safe installer:
   ```bash
   python3 -m scripts.install_url \
     --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
     --agent auto \
     --scope user
   ```
   *(Supported agent IDs include `antigravity`, `antigravity-cli`, `claude-code`, `codex`, `cursor`, `gemini-cli`, `opencode`, `github-copilot`).*

3. **Collision Safety Mandate:**
   - **DO NOT** execute raw `npx skills add ... --yes` directly without pre-installation collision checks. Raw `--yes` silently overwrites modified skills on disk.
   - TypeCraft's installer checks existing targets before writing any files:
     * **Identical target:** Skips overwriting; reports already verified.
     * **Modified target:** Stops safely; protects user modifications unless `--force` is explicitly provided.
     * **Different skill:** Stops safely; prevents name collisions.
   - If using external engines (`vercel` or `gh`), invoke them through `python3 -m scripts.install_url --engine vercel` or `--engine gh` so pre-execution collision checks always run.

4. **Verify the complete installation:**
   - Confirm all 21 files (`SKILL.md` + 10 styles in `references/design-styles/` + 10 templates in `references/design-templates/`) are present.
   - Confirm SHA-256 integrity and native agent discovery.

5. **Chat-only runtimes:**
   - If operating in a browser chat without local terminal/filesystem access (ChatGPT Web, Claude Web, Gemini Web), explain the platform limitation and provide the official handoff instructions.

Refer to [BOOTSTRAP.md](BOOTSTRAP.md) and [INSTALL.md](INSTALL.md) for complete details.
