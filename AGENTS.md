# TypeCraft Skills — Agent Directives

> **Directive for AI Agents:** When a user provides the TypeCraft repository URL (`https://github.com/krupakar5535Kk/typecraft-skills.git` or `https://github.com/krupakar5535Kk/typecraft-skills`) or asks to "Install this skill":

## 1. Primary Installation: Standard Agent Skills Ecosystem

If you have terminal/command execution tools, install TypeCraft using the standard Agent Skills CLI:

```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --global \
  --agent <ACTIVE_AGENT_ID> \
  --yes
```

### Active Agent Platform Identifiers:
- `antigravity` (Google Antigravity App / IDE)
- `antigravity-cli` (Google Antigravity CLI)
- `claude-code` (Claude Code CLI)
- `cursor` (Cursor IDE)
- `codex` (OpenAI Codex CLI)
- `opencode` (OpenCode)
- `gemini-cli` (Gemini CLI)
- `github-copilot` (GitHub Copilot Agent / VS Code)

*(If the user explicitly requests installation across all supported local agents, pass `--agent '*'`. For project-level workspace installation, omit `--global`).*

## 2. Verification Protocol

After installation completes:
1. Confirm that `typecraft-skills` is present at your platform's native skill directory.
2. Verify native skill discovery (e.g. reload or inspect your active skill catalog).
3. Report the verified status to the user, summarizing the 10 typography styles and 10 design templates.

## 3. Offline / Python Fallback Route

If Node.js or `npx` is unavailable in the environment, use TypeCraft's bundled Python installer:

```bash
python3 -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope user
```

## 4. Browser-Only Runtimes (ChatGPT Web, Claude.ai, Gemini Web)

If running in a browser chat environment without local filesystem/command access:
- Direct the user to the official release package: [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip) (Checksums: [SHA256SUMS](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/SHA256SUMS)).
- Instruct the user to upload the ZIP via their platform's Skills / Custom GPT / Custom Gem interface.

Refer to [BOOTSTRAP.md](BOOTSTRAP.md) and [INSTALL.md](INSTALL.md) for complete details.
