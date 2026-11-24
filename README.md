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

### Install with one GitHub URL

**Paste this repository URL into a compatible agent:**

`https://github.com/krupakar5535Kk/typecraft-skills.git`

The URL by itself is an installation request. The same applies when it is followed by a request such as “Install this skill.” A compatible agent should inspect this repository, read [INSTALL.md](INSTALL.md), identify its actual platform, install the complete canonical skill, and check the platform's own discovery mechanism. Do not infer the platform from the repository, operating system, or installed applications.

The flow requires repository access and, for persistent local installation, filesystem access and permission to write to the documented skill location. ChatGPT requires a ZIP upload and user confirmation. Chat-only environments without persistent installation access can use the files in the current conversation only; they must not claim a persistent installation.

When a reviewed checkout and local terminal are available, the optional router
is:

`python -m scripts.install_url --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." --agent auto`

`--agent auto` uses `TYPECRAFT_AGENT` supplied by the active runtime. If the host identity is unavailable, the command stops and asks for an explicit host ID instead of guessing. Use `--agent chatgpt --package-output /tmp/typecraft-skills.zip` to prepare a package for manual upload.

**Platform notes:**

- Claude Code local, Codex, Cursor, Gemini CLI, OpenCode, and the Antigravity App have documentation-backed routes. The Antigravity CLI path remains unestablished; do not assume the App path applies.
- GitHub Copilot's VS Code, CLI, app, and cloud-agent surfaces are separate. VS Code Agent in GitHub Codespaces and Gemini CLI user-scope installation/discovery have recorded evidence; actual skill invocation is recorded separately.
- GitHub CLI provides a preview installer for its documented host IDs. Its supported-target list does not mean TypeCraft has been installed or discovered in every host.
- ChatGPT Skills uses its own ZIP upload and workspace-eligibility flow. Upload and installation confirmation remain user actions.
- Windsurf's former skills documentation URL redirects to Devin documentation; the current Windsurf-specific route remains unverified.
- Chat-only agents without persistent installation access can use the canonical files for the current conversation only.

See [INSTALL.md](INSTALL.md) for host detection, installation, safety, and verification requirements.

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
not the same as a tested installation, and neither a file copy nor installer
inventory is proof of runtime discovery. The only recorded TypeCraft runtime
verification is GitHub Copilot Agent mode in Visual Studio Code running in
GitHub Codespaces. See the [Compatibility Guide](docs/compatibility.md) for
statuses, evidence, and remaining work.

See the [Compatibility Guide](docs/compatibility.md).

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
