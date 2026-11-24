# TypeCraft Skills — Platform Compatibility

## What the status means

The [compatibility registry](../registry/agents.yaml) is the source of truth
for official documentation, installation method and scope, native installer
availability, file verification, runtime discovery, evidence, limitations, and
remaining user action.

- **verified** — TypeCraft files were installed and the platform itself
  discovered the skill in the recorded environment.
- **compatible** — current official product documentation establishes a
  supported Agent Skills format and route; TypeCraft end-to-end testing is
  incomplete.
- **research_required** — product support, installation paths, or runtime
  behavior is uncertain. An installer host ID is not a compatibility result.
- **unsupported** — no persistent installation route is supported.

The registry documents the date checked for official sources. The platform
matrix below is intentionally conservative; it does not claim that every
surface sharing a product name uses the same skill directory.

Each platform record includes its documentation review date and verification
environment. For unverified surfaces, that environment explicitly means
documentation review only—not a product install or runtime test. The Copilot
record preserves the separate historical runtime environment and evidence.
Installation, native discovery, and actual skill invocation are distinct
verification stages; a successful skill listing does not establish invocation.

## Platform verification matrix

| Platform surface | Status | Documented install | File verification | Runtime discovery |
|---|---|---|---|---|
| Claude Code, local | compatible | `~/.claude/skills/` or `.claude/skills/` | Not tested in this environment | Not tested. A user reported that an existing local copy was listed and its full `SKILL.md` read; source equality and version were not checked. |
| OpenAI Codex | compatible | Codex `$skill-installer`; `~/.agents/skills/` or `.agents/skills/` | Not tested | Not tested |
| GitHub Copilot, VS Code Agent in Codespaces | verified | GitHub CLI managed; user scope | Verified: `SKILL.md` and 20 references | Verified in one fresh VS Code Agent session |
| GitHub Copilot CLI | compatible | Documented `~/.copilot/skills/` or `.github/skills/` directory; `copilot skill add <DIRECTORY>` registers an alternate location | Not tested | Not tested |
| GitHub Copilot app | compatible | Skills configured for repositories or Copilot CLI; manage in app UI | Not tested | Not tested |
| GitHub Copilot cloud agent and code review | compatible | Project skill in the repository | Not tested | Not tested in a fresh cloud task |
| Cursor local Agent | compatible | Shared `~/.agents/skills/` or `.agents/skills/` | Not tested | Not tested. Local user skills do not automatically sync to Cloud Agents. |
| Gemini CLI | verified | Native local-directory install; user or workspace scope | Verified: all files and 20 references matched by SHA-256 in user scope | Verified by `gemini skills list --all` in Gemini CLI 0.70.0; no model invocation |
| Google Antigravity App | compatible | `~/.gemini/config/skills/` or workspace `.agents/skills/` | Not tested | Not tested in the App |
| Antigravity CLI | research_required | GitHub CLI preview fallback only if the installed CLI advertises the host | Not tested | Not tested; official App path is not assumed to be the CLI path |
| OpenCode | compatible | Shared `~/.agents/skills/` or `.agents/skills/` | Not tested | Not tested; OpenCode has additional native locations that should be checked for duplicates |
| ChatGPT Skills | compatible | ZIP upload in Plugins → Plugin Directory → Skills | Package integrity tests pass locally; no ChatGPT upload test | Not verified; upload, scan, and confirmation require the user and an eligible workspace |
| Windsurf | research_required | No route advertised here | Not tested | Not tested; the former Windsurf skills URL redirects to Devin documentation |
| Other GitHub CLI host IDs | research_required unless separately documented above | Preview `gh skill install` only when the installed CLI explicitly lists the ID | Installer preview only | Not verified for TypeCraft |

### Actual GitHub Copilot evidence

On November 23, 2026, TypeCraft **1.1.0** was installed at user scope in
GitHub Copilot for Visual Studio Code running in GitHub Codespaces:

`/home/codespace/.copilot/skills/typecraft-skills/`

The fresh Agent session discovered the skill, read `SKILL.md`, and exercised
four references: Art Deco Typographic Style, Swiss International Typographic
Style, E-commerce Product Showcase Layout, and Cinematic Title Poster. The
installation record reports all 20 reference files present.

This evidence applies only to the named VS Code + Codespaces environment. It
does not verify Copilot CLI, the Copilot app, cloud agent, other editors, or
other install scopes. It is historical evidence for TypeCraft 1.1.0; the
current repository registry version is `1.2.0`.

### Actual Gemini CLI evidence

Gemini CLI 0.70.0 installed the canonical local skill into an isolated
user-scope directory on Ubuntu, then listed `typecraft-skills` with
`gemini skills list --all`. SHA-256 tree verification confirmed the manifest and all 20 reference files.
The Ubuntu CI job is configured to repeat the check without account
credentials or a model session. Gemini CLI's native consent option was used
only in the isolated test. Workspace discovery was not claimed because the
CLI requires project trust; actual skill invocation was not attempted.

### User-reported Claude Code observation

The user reported that local Claude Code listed
`~/.claude/skills/typecraft-skills`, loaded its complete `SKILL.md`, and
identified 10 styles and 10 templates. Claude had inspected the existing copy
only. No fresh installation, comparison with the current GitHub tree, exact
file equality, or installed version was established. The registry records this
as user-reported discovery, not as `verified` platform evidence. The separate
Codespaces environment cannot inspect the user's Mac home directory.

## Product-surface distinctions

- **Claude Code:** local `~/.claude/skills/` is not automatically equivalent
  to Cowork, claude.ai account skills, or remote cloud-session skills.
- **GitHub Copilot:** VS Code, CLI, app, and cloud agent/code review have
  different management and persistence behavior. The verified VS Code
  observation is not transferable to the other surfaces.
- **Cursor:** a local user skill is not automatically synced to Cloud Agents;
  project skills and Cloud Agent synchronization are separate.
- **Gemini CLI:** supports native `gemini skills install`, user/workspace scope,
  discovery listing, and consent during installation. The router uses the native
  command only when the installed CLI advertises scoped installation. User
  scope has automated file and discovery evidence; workspace discovery and
  model invocation remain unverified.
- **Antigravity:** the current official skills page describes App locations.
  It does not establish a CLI-specific path, so the registry leaves the CLI
  route to a checked GitHub CLI preview rather than guessing.
- **OpenCode:** discovers multiple compatible directories. Use one shared
  skill source and inspect all active locations to avoid duplicate IDs.
- **ChatGPT Skills:** creating a ZIP is only packaging. The user must upload,
  wait for scanning, and confirm product installation.
- **Windsurf:** its former documentation URL redirects to Devin docs, which
  mention legacy Windsurf paths. This alone does not establish present
  Windsurf-specific TypeCraft support.

GitHub CLI currently advertises 48 host IDs in the locally inspected
`gh 2.103.3` preview command. CI's `--dry-run` and registry checks exercise
installer routing; neither an installer preview nor an inventory item proves
that TypeCraft was installed, discovered, or invoked in the target agent.

## Remaining verification

Run an actual installation and fresh-session discovery test for each compatible
surface. Capture the precise product version, operating system, scope, path,
full source-file comparison, native discovery evidence, any actual invocation,
and remaining user action before changing a registry status.
