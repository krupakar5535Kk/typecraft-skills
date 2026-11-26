# TypeCraft Skills — Platform Compatibility

## What the status means

The [compatibility registry](../registry/agents.yaml) is the source of truth
for official documentation, installation method and scope, native installer
availability, file verification, runtime discovery, evidence, limitations, and
remaining user action.

### Four distinct evaluation stages

To maintain strict technical accuracy, TypeCraft evaluates platform compatibility across four separate lifecycle stages:

1. **Installation** — The physical copying or unpacking of canonical skill files to the host's supported path (e.g. native directory copy, `gh skill install`, or ZIP package creation/upload).
2. **Discovery** — The platform's native runtime catalog or skill inventory affirmatively indexes TypeCraft (e.g. `copilot skill list`, `gemini skills list`, or native skill manifest detection).
3. **Invocation** — The agent's model actually references, parses, and successfully applies TypeCraft typography styles or design templates to a real-world creative prompt.
4. **Persistence** — The skill remains permanently discovered and invokable across fresh sessions without requiring reinstallation.

A platform cannot be claimed as "verified" based on installation alone. Runtime discovery and actual model invocation are tracked independently.

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
and Antigravity records preserve separate verified runtime environments and evidence.
Installation, native discovery, and actual skill invocation are distinct
verification stages; a successful skill listing does not establish invocation.

### Primary Distribution: Standard Agent Skills Ecosystem

TypeCraft adopts the standard Agent Skills distribution ecosystem using the official Vercel Skills CLI (`skills`).
- **One Command:** `npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git --skill typecraft-skills --global --agent <AGENT> --copy --yes`
- **Native Discovery:** The Skills CLI discovers `typecraft-skills` directly from the repository's `skills/typecraft-skills/SKILL.md` manifest and installs all 20 reference files physically on disk.
- **Multi-Agent Targeting:** The standard CLI supports `--agent '*'` to target all supported local agent runtimes in one command.
- **Offline / Maintainer Fallback:** TypeCraft provides bundled Python tools (`scripts/install_url.py`) for offline, air-gapped, or headless environments without Node.js.

## Platform verification matrix

| Platform surface | Status | Documented install | File verification | Runtime discovery | Skill invocation |
|---|---|---|---|---|---|
| Google Antigravity App / IDE | verified | Global `~/.gemini/config/skills/` | Verified: all 21 files matched by SHA-256 | Verified in live Antigravity v2.31.0 agent session context | Verified: exercised Swiss International Typographic Style (`TCS-STYLE-001`) and Cinematic Title Poster (`TCS-TEMPLATE-002`) |
| GitHub Copilot, VS Code Agent in Codespaces | verified | GitHub CLI managed; user scope | Verified: `SKILL.md` and 20 references | Verified in fresh VS Code Agent session | Verified (historical v1.1.0 Codespaces): exercised Art Deco, Swiss style, E-commerce layout, and Cinematic Title Poster |
| GitHub Copilot CLI | verified | `~/.copilot/skills/` or project `.github/skills/` | Verified at both scopes; 20 reference files match canonical tree | Verified with `copilot skill list --json` in CLI 1.0.105 and 1.0.114 | Verified: explicit CLI invocation exercised Swiss International Typographic Style and Cinematic Title Poster |
| Gemini CLI | verified | Native local-directory install; user or workspace scope | Verified: all files and 20 references matched by SHA-256 in user scope | Verified by `gemini skills list --all` in Gemini CLI (v0.70.0 and v0.71.1) | Not verified (no model session or automated invocation attempted; interactive browser OAuth required in headless shell) |
| Claude Code, local IDE | compatible | `~/.claude/skills/` or `.claude/skills/` | Verified: all 21 files matched by SHA-256 | Documented (`/skills`); binary v2.1.330 present on host | Blocked (requires active Anthropic login/plan; not included in Claude Free) |
| Claude.ai (Claude Free Web/Desktop) | compatible | Upload ZIP through **Customize → Skills → Create skill → Upload a skill** | Package integrity tests pass locally; ZIP contains 21/21 canonical files | Account-level user action required. Official docs include Free plans with Code execution and file creation enabled. | Not tested |
| Claude Cowork | compatible | Same account-managed ZIP upload via **Customize → Skills** | Package integrity tests pass locally; ZIP contains 21/21 canonical files | Not verified; paid-plan and rollout requirements apply. | Not tested |
| OpenAI Codex IDE / CLI | compatible | Codex `$skill-installer`; `~/.agents/skills/` or `~/.codex/skills/` | Verified in test suite (21/21 files SHA-256 matched) | Native index in `~/.agents/skills/` and `$CODEX_HOME/skills` confirmed via bundled `skill-installer` | Blocked (live CLI execution blocked by upstream ChatGPT Free account usage quota limit) |
| Cursor local Agent | compatible | `~/.cursor/skills/` or shared `~/.agents/skills/` | Verified: all 21 files matched by SHA-256 | Documented (Cursor Features > Skills); local personal skills do not automatically sync to Cloud Agents | Not tested |
| OpenCode | compatible | `~/.config/opencode/skills/` or shared `~/.agents/skills/` | Verified: all 21 files matched by SHA-256 | Documented (`opencode skills list`); multiple native directories supported | Not tested |
| Gemini Web | compatible | Upload ZIP through Customize → Skills → Upload a skill (or Custom Gem fallback) | Package integrity tests pass locally; ZIP contains 21/21 canonical files | Not verified; user must upload and enable. Requires Gemini Advanced or Workspace with custom skills enabled. | Not tested |
| ChatGPT Skills | compatible | ZIP upload in Plugins → Plugin Directory → Skills (or Custom GPT Knowledge) | Package integrity tests pass locally; ZIP contains 21/21 canonical files | Not verified; upload, scan, and confirmation require the user and an eligible workspace | Not tested |
| Windsurf | compatible | Standard CLI (`~/.codeium/windsurf/skills/`) | Path documented in official Vercel Skills CLI registry | Documented in Skills CLI | Not tested |

### GitHub CLI host catalog (48 IDs)

`gh skill install --help` on GitHub CLI 2.103.3 advertises the host IDs below.
This confirms installer targeting only. It does not establish that each host
supports Agent Skills or that TypeCraft has been installed or discovered.
Native-directory rows have isolated complete-file installer tests; only rows
explicitly marked **verified** have TypeCraft runtime discovery evidence.

| Host ID | Agent | TypeCraft status | Installer route / test | Evidence |
|---|---|---|---|---|
| `github-copilot` | GitHub Copilot | verified | GitHub CLI-managed route; actual installation tested | VS Code Agent in Codespaces; see evidence below |
| `claude-code` | Claude Code | compatible | Native directory; isolated installer/file-integrity tests | Official route documented; TypeCraft runtime not tested |
| `cursor` | Cursor | compatible | Native directory; isolated installer/file-integrity tests | Official route documented; TypeCraft runtime not tested |
| `codex` | OpenAI Codex | compatible | Native directories `~/.agents/skills` and `~/.codex/skills`; isolated installer/file-integrity tests | Official route documented; alternate $CODEX_HOME/skills path registered; live runtime quota limited |
| `gemini-cli` | Gemini CLI | verified | Native CLI; isolated installer/file-integrity test | Native installation and discovery; see evidence below |
| `antigravity` | Google Antigravity App | compatible | Native directory; isolated installer/file-integrity tests | Official route documented; TypeCraft runtime not tested |
| `antigravity-cli` | Antigravity CLI | compatible | Native directory; isolated installer/file-integrity tests | Official route documented; TypeCraft runtime not tested |
| `antigravity2.0` | Antigravity 2.0 | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `adal` | AdaL | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `amp` | Amp | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `augment` | Augment | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `bob` | IBM Bob | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `cline` | Cline | research_required | GitHub CLI target; preview only | Native route/compatibility not confirmed |
| `codebuddy` | CodeBuddy | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `command-code` | Command Code | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `continue` | Continue | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `cortex` | Cortex Code | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `crush` | Crush | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `deepagents` | Deep Agents | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `devin` | Devin | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `droid` | Droid | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `firebender` | Firebender | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `goose` | Goose | research_required | GitHub CLI target; preview only | Native route/compatibility not confirmed |
| `grok` | Grok | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `iflow-cli` | iFlow CLI | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `junie` | Junie | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `kilo` | Kilo Code | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `kimi-cli` | Kimi Code CLI | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `kiro-cli` | Kiro CLI | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `kode` | Kode | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `mcpjam` | MCPJam | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `mistral-vibe` | Mistral Vibe | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `mux` | Mux | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `neovate` | Neovate | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `openclaw` | OpenClaw | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `opencode` | OpenCode | compatible | Native directory; isolated installer/file-integrity tests | Official route documented; TypeCraft runtime not tested |
| `openhands` | OpenHands | research_required | GitHub CLI target; preview only | Native route/compatibility not confirmed |
| `pi` | Pi | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `pochi` | Pochi | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `qoder` | Qoder | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `qwen-code` | Qwen Code | research_required | GitHub CLI target; preview only | Native route/compatibility not confirmed |
| `replit` | Replit | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `roo` | Roo Code | research_required | GitHub CLI target; preview only | Native route/compatibility not confirmed |
| `trae` | Trae | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `trae-cn` | Trae CN | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `universal` | Universal | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `warp` | Warp | not assessed | GitHub CLI target; preview only | Installer host ID only |
| `zencoder` | Zencoder | not assessed | GitHub CLI target; preview only | Installer host ID only |

### Actual Google Antigravity IDE evidence

On November 26, 2026, TypeCraft **1.4.0** was installed at global user scope in
Google Antigravity IDE v2.31.0 on macOS Darwin arm64:

`/Users/mac/.gemini/config/skills/typecraft-skills/`

Installation was carried out autonomously using the standard Skills CLI (`npx --yes skills add ... --global --agent antigravity --copy --yes`).
Physical disk inspection confirmed `is_symlink: False`, `is_dir: True`, with all 21 canonical files present and 100% matched to canonical SHA-256 hashes.
Antigravity IDE indexed the skill immediately in its live catalog. In the active session context, TypeCraft was invoked without manual file loading, successfully retrieving:
1. `TCS-STYLE-001` (Swiss International Typographic Style) — mathematical grid, asymmetrical balance, grotesque sans-serif.
2. `TCS-TEMPLATE-002` (Cinematic Title Poster) — standardized 5-zone vertical structural layout.

### Actual GitHub Copilot evidence

On November 23, 2026, TypeCraft **1.1.0** was installed at user scope in
GitHub Copilot for Visual Studio Code running in GitHub Codespaces:

`/home/codespace/.copilot/skills/typecraft-skills/`

The fresh Agent session discovered the skill, read `SKILL.md`, and exercised
four references: Art Deco Typographic Style, Swiss International Typographic
Style, E-commerce Product Showcase Layout, and Cinematic Title Poster. The
installation record reports all 20 reference files present.

### Actual GitHub Copilot CLI evidence

GitHub Copilot CLI 1.0.105 installed TypeCraft 1.2.0 through the router in an
isolated Linux project and user directory. Both installs matched the canonical
manifest and all 20 reference files, and `copilot skill list --json` returned
the skill at the exact installed path in each scope. The install/discovery test
used no account credentials. In a separate bounded CLI session, the explicit
`/typecraft-skills` invocation applied Swiss International Typographic Style
and the Cinematic Title Poster reference, including its five information zones
and no-invented-credits guidance.

### Actual Gemini CLI evidence

Gemini CLI 0.70.0 and 0.71.1 installed the canonical local skill into an isolated
user-scope directory on Ubuntu and macOS, then listed `typecraft-skills` with
`gemini skills list --all`. SHA-256 tree verification confirmed the manifest and all 20 reference files.
The check passed with native listing and discovery verified. Interactive browser OAuth is required for headless model invocation.

### Actual OpenAI Codex IDE evidence

OpenAI Codex CLI 0.172.0 on macOS was tested against `$CODEX_HOME/skills/typecraft-skills` (`~/.codex/skills/`) and `~/.agents/skills/typecraft-skills/`. All 21 canonical files matched SHA-256. Codex's bundled system skill `skill-installer` recognizes skill manifests in `$CODEX_HOME/skills`. Model execution in a live session was attempted; Codex returned:
`ERROR: You’ve hit your usage limit. Upgrade to Plus to continue using Codex (https://chatgpt.com/explore/plus), or try again at Dec 13th, 2026 1:44 PM.`
This confirms that the ChatGPT Free account associated with the host hit its rate quota limit, which is an upstream account usage constraint rather than a TypeCraft installation failure.

### Claude Free vs Claude Code IDE evidence

Anthropic provides two distinct skill surfaces:
1. **Claude Free (Web and Desktop):** Custom Skills are supported via account-level ZIP upload. Users navigate to **Settings → Capabilities**, ensure **Code execution and file creation** is enabled, and upload `typecraft-skills.zip` via **Customize → Skills → Create skill → Upload a skill**. Claude Free operates in a sandboxed conversation and cannot execute local shell commands.
2. **Claude Code (CLI / IDE):** A local terminal agent installing to `~/.claude/skills/typecraft-skills/`. Binary version 2.1.330 on macOS was verified with all 21 files matching SHA-256. Running `claude -p` returned `Not logged in · Please run /login`. Claude Code requires a paid Anthropic subscription or API credentials and is **not included in the Claude Free plan**. Account-level Claude Free skill uploads do not grant Claude Code entitlement.

## Product-surface distinctions

- **Google Antigravity:** The Antigravity App/IDE reads `~/.gemini/config/skills/` and workspace `.agents/skills/`. The CLI reads `~/.gemini/antigravity-cli/skills/`. Live installation, discovery, and in-session model invocation are verified in Antigravity v2.31.0.
- **Claude Code vs Claude Free:** Local `~/.claude/skills/` is distinct from account-managed skills uploaded to Claude.ai. Claude Code requires paid entitlement. Claude Free users must use the Customize → Skills ZIP upload route.
- **OpenAI Codex:** Supports both `~/.agents/skills/` and native `$CODEX_HOME/skills/`. Codex is included in ChatGPT Free subject to usage rate limits.
- **Cursor:** Local user skills (`~/.cursor/skills/` and `~/.agents/skills/`) are available to the local Cursor Agent; they do not automatically sync to remote Cursor Cloud Agents.
- **OpenCode:** Discovers multiple compatible directories (`~/.config/opencode/skills/`, `~/.agents/skills/`). All 21 canonical files verified.
- **Gemini CLI vs Gemini Web:** Gemini CLI is a terminal agent. Gemini Web is a browser chat requiring Custom Skills ZIP upload (Gemini Advanced/Workspace) or Custom Gems fallback.
- **GitHub Copilot:** VS Code, CLI, app, and cloud agent/code review have separate management. VS Code Agent and CLI have verified evidence.

## Remaining verification

The following are explicitly blocked on environments or account actions not
available to this run:

- **Claude.ai, Cowork, Gemini Web, and ChatGPT:** a user with an eligible account
  must upload the generated ZIP, confirm the product's scan/install step, enable
  the skill, and verify it in a fresh session. Packaging tests are not product
  installation tests.
- **Cursor and OpenCode:** full GUI applications were not installed on the host;
  local filesystem and catalog integration were verified.
- **Gemini CLI:** live model invocation requires interactive browser OAuth login.
- **Claude Code:** live invocation requires an active paid Anthropic subscription or API login.
- **OpenAI Codex:** live model invocation requires an active Plus/Enterprise tier or waiting for the ChatGPT Free rate limit reset.
