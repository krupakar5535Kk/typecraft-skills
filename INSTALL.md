# TypeCraft Skills — Install from one URL

Canonical repository:

`https://github.com/krupakar5535Kk/typecraft-skills.git`

Canonical installable skill: `skills/typecraft-skills/`

## URL request

Treat the canonical URL alone (with or without `.git`) as an installation
request. Do the same when it is followed by an explicit request such as
“Install this skill.” Support normal Markdown links and trailing punctuation.
Do not install when the user asks an ordinary question about the repository.

Before acting, inspect this file and the complete canonical skill directory,
including all references. There are exactly 10 typography styles and 10 design
templates. Do not create a second implementation, change resource status, or
execute scripts from the downloaded skill.

## Identify the active platform

Use the current agent runtime's actual product/surface identity. Never infer it
from the operating system, browser, repository, or installed applications.

The local router accepts either:

- `TYPECRAFT_AGENT=<exact-host-id>` with `--agent auto`; or
- an explicit `--agent <exact-host-id>` supplied by the active agent.

Validate the ID against [registry/agents.yaml](registry/agents.yaml). If the
identity is unavailable, ask which platform to target. Do not guess or install
to every available host.

## Choose the platform route

Prefer a platform's documented native installer when available; otherwise use
its documented skill directory. The registry records surface-specific details.

- **Claude Code local:** `~/.claude/skills/` or project `.claude/skills/`.
  The local directory route is distinct from Claude account skills.
- **Claude.ai and Claude Cowork:** prepare the canonical ZIP, then use
  **Customize → Skills → Create skill → Upload a skill** and enable it.
  Claude.ai Skills are available on supported plans including Free when Code
  execution and file creation is enabled; Cowork requires an eligible paid
  plan. Organization policies may restrict uploads.
- **Codex:** use its `$skill-installer` when available, or
  `~/.agents/skills/` / project `.agents/skills/`.
- **Cursor local:** use the documented shared `.agents/skills` location.
  Local personal skills do not automatically sync to Cloud Agents.
- **Copilot VS Code, CLI, app, and cloud agent:** treat these as separate
  surfaces. The CLI documents `copilot skill add` and `copilot skill list`;
  use the registry's scope and do not treat Copilot VS Code verification as
  proof for another surface.
- **Gemini CLI:** when the installed CLI advertises native scoped installation,
  the router installs the checked canonical skill directory with
  `gemini skills install <canonical-skill-directory> --scope user|workspace`.
  The router does not pass `--consent`; review Gemini's prompt. Otherwise use
  the documented native directory.
- **Antigravity App:** global `~/.gemini/config/skills/` and workspace
  `.agents/skills/`.
- **Antigravity CLI:** CLI-specific global `~/.gemini/antigravity-cli/skills/`
  and workspace `.agents/skills/`. The CLI also reads
  `~/.gemini/config/skills/` (shared with the App) and `~/.gemini/skills/`.
  After installing, run `/skills reload` or start a new conversation and check
  for the `/typecraft-skills` command. TypeCraft runtime discovery is not yet
  tested on this platform.
- **OpenCode:** it supports several skill directories. The router prefers the
  shared `.agents/skills` location; check other active directories first to
  avoid duplicate skill IDs.
- **ChatGPT Skills:** prepare a ZIP, then have the user open
  **Plugins → Plugin Directory → Skills → Create → Upload from your computer**,
  wait for scanning, and confirm installation. Availability is subject to
  eligible workspace plan and administrator settings. Packaging is not
  installation.
- **Windsurf:** stop and report that the route needs confirmation. Its former
  documentation URL redirects to Devin docs, which is not sufficient evidence
  for current Windsurf-specific behavior.
- **Other GitHub CLI host IDs:** use `gh skill install` only when the installed
  CLI's `gh skill install --help` explicitly advertises that exact ID. Host
  support means installer support only, not verified compatibility.

## Optional local router

For a fresh local checkout, run these commands from the repository root to
create an isolated environment, install the router dependency, and then run
the installer:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements-installer.txt
.venv/bin/python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <HOST_ID> \
  --scope user
```

On Windows PowerShell, use:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-installer.txt
.venv\Scripts\python.exe -m scripts.install_url `
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." `
  --agent <HOST_ID> `
  --scope user
```

The script is an installation utility; the content inside the installed Agent
Skill is data and is never executed by the router.

Use `--scope project` only when requested. Use `--json` for machine-readable
output. A ChatGPT, Claude.ai, or Claude Cowork package can be prepared by
passing the corresponding platform ID:

```bash
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent chatgpt \
  --package-output ./typecraft-skills.zip
```

The router inspects this guide, verifies the complete source tree and compares
files by SHA-256. It rejects symlinks and unsafe paths, stages local directory
installs, and restores the previous directory if replacement fails.

### Collision Protection Table

| Existing Target State | Required Behavior |
|---|---|
| No installation | Install all 21 canonical files normally |
| Identical installation | Report already installed and verified without overwriting |
| Modified TypeCraft copy | Stop safely with `ExistingInstallationError`; protect user changes |
| Different skill with same name | Stop safely with `ExistingInstallationError`; refuse to clobber |
| Explicit overwrite requested | Require explicit `--force` flag with user authorization |

**Warning on External Package Managers:** Direct raw execution of `npx skills add ... --yes` bypasses collision checks and silently destroys modified files. Always invoke external engines through TypeCraft's installer (`--engine vercel` or `--engine gh`) to ensure pre-execution collision checks always run. Do not use `--force` to replace content without reviewing the target.

## Report installation and discovery separately

Report the actual platform and version, installation result and location,
complete file verification, runtime discovery, and any remaining user action.
A directory copy, ZIP, GitHub CLI inventory row, or successful command is not
proof that the target agent discovered or invoked the skill. The router reports
`NOT_VERIFIED` when the product's own discovery cannot be checked.

If persistent installation is unsupported, say so. If the agent can read the
canonical skill, it may use it for the current conversation only; do not call
that a persistent install.

See [Installation Guide](docs/installation.md) and
[Compatibility Matrix](docs/compatibility.md).
