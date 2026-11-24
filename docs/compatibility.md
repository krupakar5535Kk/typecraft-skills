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
| OpenAI Codex CLI | verified | Codex plugin marketplace from this repository or `$skill-installer` / native directories | Codex CLI 0.172.0 installed the repo plugin in isolated `CODEX_HOME`; complete tree SHA-256 matched | `codex plugin list --json` confirmed it installed and enabled; model invocation not tested |
| OpenAI Codex IDE extension | compatible | Native `~/.agents/skills/` or project `.agents/skills/` | Not tested with the IDE extension | Not tested |
| GitHub Copilot, VS Code Agent in Codespaces | verified | GitHub CLI managed; user scope | Verified: `SKILL.md` and 20 references | Verified in one fresh VS Code Agent session |
| GitHub Copilot CLI | verified | `~/.copilot/skills/` or project `.github/skills/` | Verified at both scopes; 20 reference files match the canonical tree | Verified with `copilot skill list --json`; one actual CLI invocation exercised Swiss International Typographic Style and Cinematic Title Poster |
| GitHub Copilot app | compatible | Skills configured for repositories or Copilot CLI; manage in app UI | Not tested | Not tested |
| GitHub Copilot cloud agent and code review | compatible | Project skill in the repository | Not tested | Not tested in a fresh cloud task |
| Cursor local Agent | compatible | Shared `~/.agents/skills/` or `.agents/skills/` | Not tested | Not tested. Local user skills do not automatically sync to Cloud Agents. |
| Gemini CLI | verified | Native local-directory install; user or workspace scope | Verified: all files and 20 references matched by SHA-256 in user scope | Verified by `gemini skills list --all` in Gemini CLI 0.70.0; no model invocation |
| Claude.ai | compatible | Upload ZIP through **Plugins → Skills → Create → Upload from your computer**; **Create with chat** is another official route | Package integrity tests pass locally; no Claude upload test | Not verified; user must upload and enable. Free plans support custom skills when file creation is enabled. |
| Claude Cowork | compatible | Same account-managed ZIP upload via **Customize → Skills** | Package integrity tests pass locally; no Cowork upload test | Not verified; paid-plan and rollout requirements apply. |
| Google Antigravity App | compatible | Global `~/.gemini/config/skills/` or workspace `.agents/skills/` | Not tested | Not tested in the App |
| Google Antigravity IDE | compatible | Global `~/.gemini/config/skills/` or workspace `.agents/skills/`; legacy `~/.gemini/antigravity/skills/` | Not tested | Not tested; official docs name the Customizations menu in the agent side panel |
| Antigravity CLI | compatible | CLI-only global `~/.gemini/antigravity-cli/skills/` or workspace `.agents/skills/`; it also reads `~/.gemini/config/skills/` and `~/.gemini/skills/` | Not tested | Not tested; CLI supports skill slash commands and `/skills reload` |
| OpenCode | verified | Shared `~/.agents/skills/` or `.agents/skills/` | Verified: 1.2.0 manifest and all 20 references matched by SHA-256 | Verified with `opencode --pure debug skill` in OpenCode 1.19.6; pure mode skips external project plugins; invocation not tested without provider authentication |
| Cline | compatible | Native `~/.cline/skills/` or `.cline/skills/` | Not tested | Not tested; confirm the skill in the Skills panel and a fresh chat |
| Roo Code | compatible | Native `~/.roo/skills/` or `.roo/skills/` | Not tested | Not tested; official docs also support the shared `.agents/skills/` path |
| Kilo Code | compatible | Native `~/.kilo/skills/` or `.kilo/skills/` | Not tested | Not tested; official docs also support the shared `.agents/skills/` path |
| Continue CLI | research_required | No Agent Skills install route established | Not tested | CLI exists, but official Agent Skills installation and native discovery were not established |
| ChatGPT Skills (web) | compatible | **Plugins → Skills → Create → Upload from your computer**; **Create with chat** is also documented | Package integrity tests pass locally; no ChatGPT upload test | Not verified; upload, scan, and install/enable confirmation require the user and an eligible workspace |
| ChatGPT desktop app | compatible | Repo-local OpenAI plugin marketplace in this repository; plugin points at the canonical skill directory | Manifest and marketplace structure validated locally; no desktop app install test | Not verified; if the app exposes local/repo marketplaces, user must add the marketplace and install from Plugins |
| Windsurf | research_required | No route advertised here | Not tested | Not tested; the former Windsurf skills URL redirects to Devin documentation |

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
| `codex` | OpenAI Codex | compatible | Native directory; isolated installer/file-integrity tests | Official route documented; TypeCraft runtime not tested |
| `gemini-cli` | Gemini CLI | verified | Native CLI; isolated installer/file-integrity test | Native installation and discovery; see evidence below |
| `antigravity` | Google Antigravity App | compatible | Native directory; isolated installer/file-integrity tests | Official route documented; TypeCraft runtime not tested |
| `antigravity-cli` | Antigravity CLI | compatible | Native directory; isolated installer/file-integrity tests | Official route documented; TypeCraft runtime not tested |
| `antigravity2.0` | Antigravity 2.0 | research_required | GitHub CLI target; preview only | Installer host ID only |
| `adal` | AdaL | research_required | GitHub CLI target; preview only | Installer host ID only |
| `amp` | Amp | research_required | GitHub CLI target; preview only | Installer host ID only |
| `augment` | Augment | research_required | GitHub CLI target; preview only | Installer host ID only |
| `bob` | IBM Bob | research_required | GitHub CLI target; preview only | Installer host ID only |
| `cline` | Cline | compatible | Native `.cline/skills`; isolated installer/file-integrity tests | Official docs establish path; TypeCraft runtime not tested |
| `codebuddy` | CodeBuddy | research_required | GitHub CLI target; preview only | Installer host ID only |
| `command-code` | Command Code | research_required | GitHub CLI target; preview only | Installer host ID only |
| `continue` | Continue | research_required | GitHub CLI target; preview only | Installer host ID only; CLI exists but official Agent Skills route not established |
| `cortex` | Cortex Code | research_required | GitHub CLI target; preview only | Installer host ID only |
| `crush` | Crush | research_required | GitHub CLI target; preview only | Installer host ID only |
| `deepagents` | Deep Agents | research_required | GitHub CLI target; preview only | Installer host ID only |
| `devin` | Devin | research_required | GitHub CLI target; preview only | Installer host ID only |
| `droid` | Droid | research_required | GitHub CLI target; preview only | Installer host ID only |
| `firebender` | Firebender | research_required | GitHub CLI target; preview only | Installer host ID only |
| `goose` | Goose | research_required | GitHub CLI target; preview only | Native route/compatibility not confirmed |
| `grok` | Grok | research_required | GitHub CLI target; preview only | Installer host ID only |
| `iflow-cli` | iFlow CLI | research_required | GitHub CLI target; preview only | Installer host ID only |
| `junie` | Junie | research_required | GitHub CLI target; preview only | Installer host ID only |
| `kilo` | Kilo Code | compatible | Native `.kilo/skills`; isolated installer/file-integrity tests | Official docs establish native and shared paths; TypeCraft runtime not tested |
| `kimi-cli` | Kimi Code CLI | research_required | GitHub CLI target; preview only | Installer host ID only |
| `kiro-cli` | Kiro CLI | research_required | GitHub CLI target; preview only | Installer host ID only |
| `kode` | Kode | research_required | GitHub CLI target; preview only | Installer host ID only |
| `mcpjam` | MCPJam | research_required | GitHub CLI target; preview only | Installer host ID only |
| `mistral-vibe` | Mistral Vibe | research_required | GitHub CLI target; preview only | Installer host ID only |
| `mux` | Mux | research_required | GitHub CLI target; preview only | Installer host ID only |
| `neovate` | Neovate | research_required | GitHub CLI target; preview only | Installer host ID only |
| `openclaw` | OpenClaw | research_required | GitHub CLI target; preview only | Installer host ID only |
| `opencode` | OpenCode | verified | Native `.agents/skills`; OpenCode 1.19.6 project install and integrity test | `opencode --pure debug skill` confirmed exact path with external plugins disabled; invocation not tested |
| `openhands` | OpenHands | research_required | GitHub CLI target; preview only | Native route/compatibility not confirmed |
| `pi` | Pi | research_required | GitHub CLI target; preview only | Installer host ID only |
| `pochi` | Pochi | research_required | GitHub CLI target; preview only | Installer host ID only |
| `qoder` | Qoder | research_required | GitHub CLI target; preview only | Installer host ID only |
| `qwen-code` | Qwen Code | research_required | GitHub CLI target; preview only | Native route/compatibility not confirmed |
| `replit` | Replit | research_required | GitHub CLI target; preview only | Installer host ID only |
| `roo` | Roo Code | compatible | Native `.roo/skills`; isolated installer/file-integrity tests | Official docs establish native and shared paths; TypeCraft runtime not tested |
| `trae` | Trae | research_required | GitHub CLI target; preview only | Installer host ID only |
| `trae-cn` | Trae CN | research_required | GitHub CLI target; preview only | Installer host ID only |
| `universal` | Universal | research_required | GitHub CLI target; preview only | Installer host ID only |
| `warp` | Warp | research_required | GitHub CLI target; preview only | Installer host ID only |
| `zencoder` | Zencoder | research_required | GitHub CLI target; preview only | Installer host ID only |

### Actual GitHub Copilot evidence

On November 23, 2026, TypeCraft **1.1.0** was installed at user scope in
GitHub Copilot for Visual Studio Code running in GitHub Codespaces:

`/home/codespace/.copilot/skills/typecraft-skills/`

The fresh Agent session discovered the skill, read `SKILL.md`, and exercised
four references: Art Deco Typographic Style, Swiss International Typographic
Style, E-commerce Product Showcase Layout, and Cinematic Title Poster. The
installation record reports all 20 reference files present.

This evidence applies only to the named VS Code + Codespaces environment. It
does not verify the Copilot app, cloud agent, other editors, or other install
scopes. It is historical evidence for TypeCraft 1.1.0; the current repository
registry version is `1.2.0`.

### Actual GitHub Copilot CLI evidence

GitHub Copilot CLI 1.0.105 installed TypeCraft 1.2.0 through the router in
isolated Linux project and user directories. Both installs matched the
canonical manifest and all 20 reference files, and `copilot skill list --json`
returned the skill at the exact installed path in each scope. A fresh
project-scope regression repeated installation and discovery. In a separate
authenticated, isolated one-shot session, `/typecraft-skills` produced the
requested Swiss International Typographic Style and Cinematic Title Poster
direction: asymmetric modular grid, sans-serif title hierarchy, generous
whitespace, image and information zones, restrained color, and no invented
credits. Installation and discovery used no account credentials; the model
invocation used the configured Copilot account. This proves only the Copilot
CLI surface, not the Copilot app or cloud agent.

### Actual Gemini CLI evidence

Gemini CLI 0.70.0 installed the canonical local skill into an isolated
user-scope directory on Ubuntu, then listed `typecraft-skills` with
`gemini skills list --all`. SHA-256 tree verification confirmed the manifest and all 20 reference files.
The Ubuntu CI job is configured to repeat the check without account
credentials or a model session. Gemini CLI's native consent option was used
only in the isolated test. Workspace discovery was not claimed because the
CLI requires project trust; actual skill invocation was not attempted.

### Actual OpenCode evidence

OpenCode CLI 1.19.6 installed TypeCraft 1.2.0 through the URL-first router in
an isolated Linux project at
`/tmp/typecraft-opencode-edAbKa/project/.agents/skills/typecraft-skills/`.
The router verified the complete tree, including `SKILL.md` and all 20
references, by SHA-256. OpenCode's native `opencode --pure debug skill` command
listed TypeCraft at the exact installed manifest path. Pure mode skips external
project plugins; the integration test includes a project plugin probe and
confirms it is not executed during discovery. Invocation was not attempted:
the isolated environment had no provider account or credential. This verifies
installation and discovery only, not model invocation.

### Actual Codex CLI evidence

Codex CLI 0.172.0 added the repository's local plugin marketplace, listed
`typecraft-skills@typecraft-skills` as available, installed the plugin in a
temporary isolated `CODEX_HOME`, and listed it as installed and enabled.
SHA-256 tree verification confirmed the installed plugin's canonical
`skills/typecraft-skills/` directory, including `SKILL.md` and all 20
references, matches the repository exactly. No OpenAI credential or model
session was used; invocation remains untested. This verifies Codex CLI only,
not the separate Codex IDE extension or ChatGPT desktop app.

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
  to account-managed skills. Claude Code v2.1.273+ can sync enabled Claude.ai
  skills for supported account sign-ins; that route is distinct from a local
  directory install and does not mean TypeCraft was tested in Cowork.
- **Claude.ai and Cowork:** the current help center documents ZIP upload via
  Customize → Skills. Claude.ai lists Free, Pro, Max, Ultra, Team, and
  Enterprise availability subject to Code execution/file creation and
  organization policy; Cowork is available on eligible paid plans. The
  TypeCraft package is verified locally, but neither platform upload nor
  runtime discovery has been tested.
- **GitHub Copilot:** VS Code, CLI, app, and cloud agent/code review have
  different management and persistence behavior. VS Code Agent and CLI have
  separate TypeCraft installation/discovery evidence; only the named surfaces
  and versions above are verified. This evidence does not extend to the app or
  cloud agent/code review.
- **Cursor:** a local user skill is not automatically synced to Cloud Agents;
  project skills and Cloud Agent synchronization are separate.
- **Gemini CLI:** supports native `gemini skills install`, user/workspace scope,
  discovery listing, and consent during installation. The router uses the native
  command only when the installed CLI advertises scoped installation. User
  scope has automated file and discovery evidence; workspace discovery and
  model invocation remain unverified.
- **Antigravity App, standalone IDE, and CLI:** the official skills page
  documents three separate product surfaces. All read workspace
  `.agents/skills/`; the App and IDE global directory is
  `~/.gemini/config/skills/`. The CLI additionally reads
  `~/.gemini/antigravity-cli/skills/` and `~/.gemini/skills/`. Its `/skills
  reload` command refreshes skill slash commands. TypeCraft installation,
  discovery, and invocation have not been tested in any Antigravity surface.
- **OpenCode:** discovers its own and shared skill directories. TypeCraft's
  tested project install uses `.agents/skills/`; `opencode --pure debug skill`
  confirmed discovery without loading external project plugins. Restart
  existing sessions after installation. No provider-authenticated invocation
  was available in this environment.
- **Cline, Roo Code, and Kilo Code:** current official docs establish their
  native installation directories, so they are marked `compatible`. Only
  isolated router/file-integrity tests were run; each product's own runtime
  discovery and invocation remain untested.
- **Continue:** the official CLI quickstart confirms the `cn` runtime, but an
  official Agent Skills installation route was not established. Continue
  remains `research_required`; no directory is guessed.
- **ChatGPT Skills:** creating a ZIP is only packaging. The user must upload,
  wait for scanning, and confirm product installation.
- **OpenAI plugin marketplace:** this repository contains a portable
  `plugin.json` and `.agents/plugins/marketplace.json` that point to the
  existing canonical skill, without another `SKILL.md` copy. Codex CLI
  installation/discovery was tested. ChatGPT desktop local-marketplace UI and
  ChatGPT web persistent upload/activation remain separate, untested actions.
- **Windsurf:** its former documentation URL redirects to Devin docs, which
  mention legacy Windsurf paths. This alone does not establish present
  Windsurf-specific TypeCraft support.

GitHub CLI currently advertises 48 host IDs in the locally inspected
`gh 2.103.3` preview command. CI's `--dry-run` and registry checks exercise
installer routing; neither an installer preview nor an inventory item proves
that TypeCraft was installed, discovered, or invoked in the target agent.

## Remaining verification

The following are explicitly blocked on environments or account actions not
available to this run:

- **Claude.ai, Cowork, and ChatGPT:** a user with an eligible account must
  upload the generated ZIP, confirm the product's scan/install step, enable the
  skill, and verify it in a fresh session. Packaging tests are not product
  installation tests.
- **Claude Code, Codex IDE, Cursor, Antigravity App, Antigravity IDE, and
  Antigravity CLI:** their native runtimes were not installed in this
  environment. Their documented directory install paths were exercised by
  isolated file-integrity tests, but product-native discovery and invocation
  remain untested.
- **Codex CLI invocation:** native installation and discovery passed; no
  authenticated model session was available for an actual design prompt.
- **ChatGPT desktop app:** the repo marketplace was validated and Codex
  consumed its plugin structure, but the desktop app UI was unavailable for
  native installation or discovery testing.
- **OpenCode:** installation integrity and native discovery passed on CLI
  1.19.6. A provider-authenticated skill invocation remains untested.
- **Cline, Roo Code, and Kilo Code:** official routes and isolated adapter
  file-integrity tests are recorded, but their product-native discovery and
  invocation remain untested.
- **Gemini CLI:** install and discovery run without account credentials; no
  Gemini model invocation was attempted.
- **GitHub Copilot app and cloud agent/code review:** these separate surfaces
  need product UI/repository access and a fresh product session; CLI and VS
  Code evidence does not transfer to them.
- **Other GitHub CLI host IDs:** the installer preview passed, but these IDs
  are not compatibility claims. Research and test each native runtime before
  advertising support.

Before upgrading any remaining surface to `verified`, capture its exact
product/version, operating system, scope/path, complete source-file comparison,
native discovery result, and actual invocation when the host permits one.
