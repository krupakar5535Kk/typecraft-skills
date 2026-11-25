# TypeCraft Skills

**ONE URL. ONE SKILL. EVERY COMPATIBLE AI AGENT.**

TypeCraft Skills is an open-source AI Agent Skill for typography, visual design direction, and creative composition.

It helps AI agents select and apply typography styles and design templates across five creative domains.

## What Is TypeCraft?

TypeCraft provides a structured creative resource library and reusable design instructions for AI agents.

It separates two important design concepts:

- **Typography Style:** Defines the visual personality and treatment of typography.
- **Design Template:** Defines the structural arrangement of content and composition.

A style controls how typography looks. A template controls how content is arranged. They can be used independently or combined.

## Resource Library

The current fixed library contains exactly 20 resources:

- **10 typography styles**
- **10 design templates**

There is one canonical installable Agent Skill at `skills/typecraft-skills/`.
All 20 library resources have been editorially reviewed and are approved for
production use.

### Typography Styles

| ID | Style |
|---|---|
| TCS-STYLE-001 | Swiss International Typographic Style |
| TCS-STYLE-002 | Art Deco Typographic Style |
| TCS-STYLE-003 | Bauhaus Typographic Style |
| TCS-STYLE-004 | Punk Typographic Style |
| TCS-STYLE-005 | Constructivist Typographic Style |
| TCS-STYLE-006 | De Stijl Typographic Style |
| TCS-STYLE-007 | Art Nouveau Typographic Style |
| TCS-STYLE-008 | Psychedelic Typographic Style |
| TCS-STYLE-009 | Brutalist Typographic Style |
| TCS-STYLE-010 | Kinetic Typographic Style |

### Design Templates

| ID | Template |
|---|---|
| TCS-TEMPLATE-001 | Swiss Grid Editorial Poster |
| TCS-TEMPLATE-002 | Cinematic Title Poster |
| TCS-TEMPLATE-003 | Swiss Editorial Magazine Spread |
| TCS-TEMPLATE-004 | Corporate Annual Report Layout |
| TCS-TEMPLATE-005 | Modern Business Presentation Deck |
| TCS-TEMPLATE-006 | E-commerce Product Showcase Layout |
| TCS-TEMPLATE-007 | Creative Portfolio Case Study Layout |
| TCS-TEMPLATE-008 | Event and Conference Promotional Layout |
| TCS-TEMPLATE-009 | Social Media Campaign Carousel Layout |
| TCS-TEMPLATE-010 | Data Visualization and Infographic Storytelling Layout |

**Resource lifecycle:** All 10 typography styles and 10 design templates are approved production resources.

## Creative Domains

1. **Static Graphics** — Posters, advertisements, banners, covers, and social media graphics.
2. **Motion Graphics** — Kinetic typography, animated text, and motion compositions.
3. **Video** — Opening titles, closing credits, lower thirds, captions, and title sequences.
4. **Web and UI** — Websites, landing pages, application interfaces, and responsive typography.
5. **Editorial** — Magazines, books, reports, brochures, and publication layouts.

## Selection Modes

- **Automatic:** The agent selects suitable styles and templates based on the creative brief.
- **Manual:** The agent respects the user's explicitly selected resources.
- **Mixed:** The agent preserves explicit choices and automatically selects unspecified components.

Explicit user choices must never be silently overridden.

## Installation

### 1. Install with one URL (Autonomous AI Coding Agents)

**Paste this repository URL into your AI agent:**

```text
https://github.com/krupakar5535Kk/typecraft-skills.git
Install this skill.
```

The URL by itself is an installation request. The same applies when it is followed by a request such as “Install this skill.” A compatible agent should inspect this repository, read [BOOTSTRAP.md](BOOTSTRAP.md) and [INSTALL.md](INSTALL.md), identify its actual platform, install the complete canonical skill using TypeCraft's safe installer, and check the platform's own discovery mechanism. Do not infer the platform from the repository, operating system, or installed applications.

### 2. Local-Agent Installation Route (CLI & Terminal Agents)

When a reviewed checkout and local terminal are available, the authoritative installer is:

```bash
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent auto \
  --scope user
```

`--agent auto` uses `TYPECRAFT_AGENT` or unambiguous host runtime signals. If the host identity is unavailable, the command stops and asks for an explicit host ID instead of guessing. You can also specify an agent explicitly (`--agent claude-code`, `--agent gemini-cli`, `--agent codex`, `--agent cursor`, `--agent antigravity`, etc.) or choose an installation engine: `--engine auto`, `--engine native`, `--engine vercel`, or `--engine gh`.

**Collision & Overwrite Safety:**
TypeCraft enforces automated pre-installation collision detection. It will never silently overwrite modified local files or unrelated skills. Raw commands like `npx skills add ... --yes` bypass collision protection and are strictly prohibited in the default workflow. Use `--force` only when you explicitly intend to overwrite an existing installation after review.

### 3. Browser-Based Platform Route (ChatGPT, Claude.ai, Gemini Web)

Browser-based chat platforms operate in sandboxed browser environments without local terminal or filesystem access. For these platforms, download the official release package and upload it directly:

- **Latest Downloadable Asset:** [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip)
- **Checksum Verification:** [SHA256SUMS](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/SHA256SUMS)

You can also package the canonical skill locally:

```bash
python -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git" \
  --agent chatgpt \
  --package-output ./typecraft-skills.zip
```

**Platform Upload Steps:**
- **ChatGPT:** Open **Plugins → Plugin Directory → Skills → Create → Upload from your computer** (or attach to **Custom GPT → Knowledge**).
- **Claude.ai / Claude Cowork:** Open **Customize → Skills → Create skill → Upload a skill** (or add `typecraft-skills/SKILL.md` to **Project Knowledge**).
- **Gemini Web:** Open **Customize → Skills** (or **More → Customize → Skills**), select **Upload a skill**, and upload `typecraft-skills.zip`. Availability requires a Gemini Advanced subscription or an eligible Google Workspace (Business/Enterprise/Edu) account with custom skills enabled. Once saved, invoke via `@typecraft-skills` or `/typecraft-skills`. (For personal accounts or environments without Custom Skills upload access, paste `typecraft-skills/SKILL.md` into a **Custom Gem** or attach it to the conversation as a fallback).

### Platform Evaluation Stages & Compatibility

TypeCraft strictly distinguishes between four lifecycle stages:
- **Installation:** Files copied to a documented native directory or archive uploaded.
- **Discovery:** The platform's native skill catalog affirmatively indexes TypeCraft (`copilot skill list`, `gemini skills list`, `/skills` in Claude Code, `$skill-installer` in Codex).
- **Invocation:** The agent model actually accesses and applies TypeCraft typography styles or design templates in a real task.
- **Persistence:** Availability across fresh, independent conversations without reinstallation.

| Surface | Status | Route | Verified Evidence |
|---|---|---|---|
| **GitHub Copilot CLI** | **verified** | Native directory (`~/.copilot/skills/`) | Full installation, discovery (`copilot skill list`), and model invocation verified on CLI 1.0.105 & 1.0.114. |
| **GitHub Copilot VS Code Agent** | **verified** | GitHub CLI managed (`~/.copilot/skills/`) | Historical installation, discovery, and invocation verified in GitHub Codespaces (v1.1.0). |
| **Gemini CLI** | **verified** | Native directory (`~/.gemini/skills/`) | User-scope installation and native discovery verified via `gemini skills list --all`; live model invocation blocked by headless OAuth requirement. |
| **OpenAI Codex** | **compatible** | Native directories (`~/.agents/skills/`, `~/.codex/skills/`) | Native paths and bundled `$skill-installer` registered; live invocation blocked by upstream ChatGPT account usage limit. |
| **Claude Code CLI** | **compatible** | Native directory (`~/.claude/skills/`) | Route documented; user-reported discovery observed; end-to-end model invocation unverified in CI. |
| **Cursor IDE** | **compatible** | Shared directory (`~/.agents/skills/`) | Route documented; local user skills do not automatically sync to Cloud Agents. |
| **Google Antigravity App / CLI** | **compatible** | Native directories (`~/.gemini/config/skills/`, `~/.gemini/antigravity-cli/skills/`) | Documented native routes; App catalog & CLI `/skills reload` supported. |
| **OpenCode** | **compatible** | Shared directory (`~/.agents/skills/`) | Documented native routes across multiple directories. |
| **ChatGPT / Claude.ai / Cowork / Gemini Web** | **compatible** | Release ZIP upload | Verified local packaging; upload, scan, and confirmation require user action and account eligibility (Gemini Advanced/Workspace for Skills upload; Custom Gems fallback). |
| **Windsurf** | **research_required** | Unconfirmed | Former documentation URL redirects to Devin; native route unconfirmed. |

See the complete [Compatibility Guide](docs/compatibility.md) and [Installation Guide](docs/installation.md) for full audit records and evidence.

### Maintainer: install for GitHub CLI targets

TypeCraft includes a registry-driven installer for 48 GitHub CLI-supported agent targets.

**Prerequisites:** Git, Python 3.12 or compatible, and GitHub CLI with `gh skill` support.

Clone the repository:

`git clone https://github.com/krupakar5535Kk/typecraft-skills.git`

`cd typecraft-skills`

Create the Python environment:

`python3.12 -m venv .venv`

Install dependencies:

`.venv/bin/python -m pip install -r requirements-installer.txt`

Preview all targets:

`.venv/bin/python -m scripts.install --all --scope user --dry-run`

Install all targets:

`.venv/bin/python -m scripts.install --all --scope user`

Install selected agents:

`.venv/bin/python -m scripts.install --agent claude-code --agent cursor`

Use `--version v1.0.0` to select a specific release. Existing installations are skipped by default. Use `--force` only when you explicitly intend to overwrite an installation.

Some agents share physical installation directories. Therefore, 48 agent targets do not necessarily mean 48 separate folders.

ChatGPT uses a separate installation route and is not included in these 48 GitHub CLI targets.

See [INSTALL.md](INSTALL.md) for AI-agent installation instructions.

### Install manually


TypeCraft is distributed as a single Agent Skill.

Clone the repository:

```bash
git clone https://github.com/krupakar5535Kk/typecraft-skills.git
cd typecraft-skills
```

The installable skill directory is:

`skills/typecraft-skills/`

See the [Installation Guide](docs/installation.md) for installation instructions.

## Compatibility

TypeCraft uses a tool-independent architecture with tool-aware execution.

Compatibility is surface-specific. Official documentation-backed routes are
distinct from tested installations, and neither a file copy nor installer
inventory is proof of runtime discovery or model invocation. TypeCraft
independently tracks Installation, Discovery, Invocation, and Persistence.
See the [Compatibility Guide](docs/compatibility.md) for complete statuses,
recorded evidence, and evaluation matrices.

## Usage

Describe the creative brief and intended output.

The agent will:

1. Identify the creative domain.
2. Determine whether a typography style or design template is needed.
3. Select resources using Automatic, Manual, or Mixed mode.
4. Apply the selected design direction.
5. Adapt the result to the target medium and available tools.

You can request a style, a template, or both.

**Examples:**

- Create a poster using the Swiss International Typographic Style.
- Use the Cinematic Title Poster template for a film announcement.
- Automatically choose a style and template for a technology conference.
- Combine an explicitly selected style with an automatically selected template.

See the [Usage Guide](docs/usage.md).

## Documentation

- [Architecture](docs/architecture.md)
- [Authoring Standard](docs/authoring-standard.md)
- [Resource Schema](docs/resource-schema.md)
- [Installation Guide](docs/installation.md)
- [Compatibility Guide](docs/compatibility.md)
- [Design Guidelines](docs/design-guidelines.md)
- [Usage Guide](docs/usage.md)
- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## License

Released under the [MIT License](LICENSE).
