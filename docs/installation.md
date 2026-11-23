# TypeCraft Skills — Installation

## One URL, one canonical skill

Paste this URL alone into a compatible agent:

`https://github.com/krupakar5535Kk/typecraft-skills.git`

The URL alone is an installation request. The same applies to the canonical URL
without `.git`, including ordinary Markdown links and trailing punctuation.
Questions about the repository are not installation requests.

The agent must inspect [INSTALL.md](../INSTALL.md), identify its actual runtime,
and install only `skills/typecraft-skills/`. Do not infer the product from the
operating system, browser, repository name, or installed applications. If the
active agent cannot supply its exact supported host ID, ask which platform to
target; do not install to a guessed location.

There is exactly one TypeCraft implementation, with 10 typography styles and
10 design templates. Install or package its full directory, including
`SKILL.md` and every reference. Do not execute scripts in the downloaded skill.

## Platform routes

The [compatibility registry](../registry/agents.yaml) records documentation
URLs, current route, scopes, file checks, runtime checks, and outstanding user
actions. `compatible` means the official documentation supports a route;
`verified` requires TypeCraft installation and native runtime discovery.
Actual skill invocation is tracked separately and is never inferred from
discovery.

| Surface | Documented route and scope | Discovery and limits |
|---|---|---|
| Claude Code, local | Native personal `~/.claude/skills/` or project `.claude/skills/` | Check `/skills`. A local personal install does not automatically reach Cowork or remote cloud sessions. |
| OpenAI Codex | `$skill-installer` or native `~/.agents/skills/` / project `.agents/skills/` | Check `/skills` or invoke `$typecraft-skills`; restart if needed. |
| Cursor local Agent | Native shared `~/.agents/skills/` or project `.agents/skills/` | Check Cursor's skill picker. Personal local skills are not automatically synced to Cloud Agents. |
| GitHub Copilot in VS Code | `gh skill install` or native project/personal skills | The only TypeCraft runtime-verified environment is VS Code in GitHub Codespaces; see the compatibility guide. |
| GitHub Copilot CLI | Router copies to the documented `~/.copilot/skills/` or `.github/skills/` directory; `copilot skill add <DIRECTORY>` registers an alternate location | Check `copilot skill list` or `/skills info typecraft-skills`; this surface is not TypeCraft-tested. |
| GitHub Copilot app | Use skills configured for a repository or Copilot CLI; manage in **Customize → Skills** | App discovery and installation are not the same as VS Code or CLI verification. |
| GitHub Copilot cloud agent/code review | Add a project skill to the repository's documented skills directory | A personal local copy is not cloud persistence. Test a fresh cloud task separately. |
| Gemini CLI | Native local-directory install with user or workspace scope; safe directory copy if the installed CLI lacks scoped install support | User-scope install and `gemini skills list --all` verified with Gemini CLI 0.70.0 in isolated Ubuntu CI. Review the install consent prompt. Workspace discovery requires the project to be trusted; model invocation was not tested. |
| Google Antigravity App | Native global `~/.gemini/config/skills/` or workspace `.agents/skills/` | Check discovery in the App. The registry does not claim TypeCraft runtime testing. |
| Antigravity CLI | GitHub CLI preview fallback only when that installed CLI advertises `antigravity-cli` | Official documentation names the CLI surface but does not establish a CLI-specific directory here; no path is guessed. |
| OpenCode | Shared native `~/.agents/skills/` or `.agents/skills/` | OpenCode also reads its own directories. The shared path avoids installing a duplicate when possible; inspect all active sources. |
| ChatGPT Skills | Create a ZIP, then use **Plugins → Plugin Directory → Skills → Create → Upload from your computer** | ZIP creation is not installation. The user must upload, wait for scanning, and confirm availability. |
| Windsurf | No route is advertised by this project yet | The former skills documentation URL redirects to Devin documentation. Current Windsurf-specific behavior needs verification. |

Other `gh skill` host IDs are installer integrations only. At the time of this
registry check, GitHub CLI 2.103.3 advertised 48 host IDs. That proves only the
installed CLI's host list, not the platform's TypeCraft compatibility or
runtime discovery. The router checks the actual CLI help before using it.

## Optional local router

From a reviewed repository checkout, with Python and the pinned dependency
installed:

```bash
python -m pip install -r requirements-installer.txt
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <HOST_ID> \
  --scope user
```

Use `--agent auto` only when the active runtime sets `TYPECRAFT_AGENT` to its
exact host ID. An explicit `--agent <HOST_ID>` is also supported. Unknown or
missing identity fails closed. Use `--scope project` only when requested.
`--json` emits the same report as machine-readable JSON.

The router compares complete source and destination trees by file SHA-256.
Identical installs are left untouched. A different existing directory is never
replaced without explicit approval (`--force`). Native directory updates stage
and verify the replacement, preserve extra files, and restore the old directory
if the replacement fails. Symlinks and unsafe paths are rejected. For
GitHub-CLI-managed updates, the CLI's own update behavior applies; review the
target and use `--force` only after authorizing replacement.

The result reports project version, actual host ID, location, file verification,
runtime discovery, and remaining user action independently. File equality,
the GitHub CLI inventory, and successful ZIP creation are not runtime discovery.

## ChatGPT package

The router prepares the complete canonical skill with `typecraft-skills/` at
the ZIP root:

```bash
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent chatgpt \
  --package-output ./typecraft-skills.zip
```

It verifies ZIP integrity, exact file paths, and content hashes. The user must
upload the archive, wait for ChatGPT's scan, and confirm installation. Account
eligibility and workspace permissions may apply.

## Chat-only fallback

When persistent installation is not supported, state that explicitly. If the
agent can read the entire canonical directory, it may use it for the current
conversation only. Never report that as a persistent install.

## Maintainer multi-target utility

`scripts/install.py` is for maintainers intentionally targeting GitHub CLI
hosts, not the URL-first current-agent flow. Preview before installing:

```bash
python -m scripts.install --list
python -m scripts.install --all --scope user --dry-run
```
