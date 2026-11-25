# TypeCraft Skills

**ONE URL. ONE SKILL. EVERY COMPATIBLE AI AGENT.**

TypeCraft Skills is the open-source Agent Skill for professional typography, visual design direction, and creative composition across modern AI coding agents.

It equips AI agents with deep typographic knowledge, historical style rules, and structural composition templates across five creative domains.

---

## What Is TypeCraft?

TypeCraft provides a structured creative resource library and reusable design instructions for AI agents.

It separates two fundamental design concepts:

- **Typography Style:** Defines the visual personality, era, font direction, tracking, leading, and hierarchy treatment.
- **Design Template:** Defines the modular grid, content regions, structural layout, and compositional zones.

A style controls how typography looks. A template controls how content is arranged. They can be used independently or combined.

---

## Resource Library (20 Locked Canonical Resources)

The canonical library contains exactly 20 production-approved design resources inside one installable Agent Skill at `skills/typecraft-skills/`:

### 10 Typography Styles
| ID | Style | Key Characteristics |
|---|---|---|
| `TCS-STYLE-001` | Swiss International Typographic Style | Mathematical grids, neutral grotesque sans-serif, asymmetrical balance, objective clarity |
| `TCS-STYLE-002` | Art Deco Typographic Style | Geometric elegance, high-contrast display letterforms, verticality, decorative symmetry |
| `TCS-STYLE-003` | Bauhaus Typographic Style | Functional geometric purity, elemental forms, primary colors, typography as structural element |
| `TCS-STYLE-004` | Punk Typographic Style | Raw DIY energy, xerox textures, distressed ransom-note cutouts, anti-grid rebelliousness |
| `TCS-STYLE-005` | Constructivist Typographic Style | Bold diagonal dynamism, heavy rules, solid geometric slabs, agitprop urgency |
| `TCS-STYLE-006` | De Stijl Typographic Style | Neoplastic reduction, horizontal/vertical orthogonal grid, primary colors, non-decorative |
| `TCS-STYLE-007` | Art Nouveau Typographic Style | Organic whiplash curves, floral rhythm, handcrafted aesthetic, decorative integration |
| `TCS-STYLE-008` | Psychedelic Typographic Style | Vibrating optic colors, curvilinear distorted letterforms, concert poster counterculture |
| `TCS-STYLE-009` | Brutalist Typographic Style | Raw digital utilitarianism, system defaults, dense information, unadorned frankness |
| `TCS-STYLE-010` | Kinetic Typographic Style | Temporal motion behaviors, variable weights, directional velocity, spatial typography |

### 10 Design Templates
| ID | Template | Purpose & Structure |
|---|---|---|
| `TCS-TEMPLATE-001` | Swiss Grid Editorial Poster | 6-column modular grid poster with clear 5-zone information hierarchy |
| `TCS-TEMPLATE-002` | Cinematic Title Poster | High-impact entertainment visual hierarchy with standardized credit block billing |
| `TCS-TEMPLATE-003` | Swiss Editorial Magazine Spread | Balanced multi-column editorial spread with headline, pull quote, and margin system |
| `TCS-TEMPLATE-004` | Corporate Annual Report Layout | Polished corporate publication layout balancing narrative, metrics, and tables |
| `TCS-TEMPLATE-005` | Modern Business Presentation Deck | 16:9 widescreen presentation slides with strong slide title hierarchy and data cards |
| `TCS-TEMPLATE-006` | E-commerce Product Showcase Layout | Commercial product merchandising layout with hero visual, specs, and price hierarchy |
| `TCS-TEMPLATE-007` | Creative Portfolio Case Study Layout | Multi-section design case study layout showcasing project context, deliverables, and impact |
| `TCS-TEMPLATE-008` | Event and Conference Promotional Layout | Action-oriented conference promotional poster with speaker lineup and schedule zones |
| `TCS-TEMPLATE-009` | Social Media Campaign Carousel Layout | Multi-slide storytelling sequence with progressive hooks and swipe momentum |
| `TCS-TEMPLATE-010` | Data Visualization Storytelling Layout | Information graphics architecture combining statistical figures, charts, and annotations |

---

## Creative Domains

1. **Static Graphics** — Posters, advertisements, banners, covers, and promotional graphics.
2. **Motion Graphics** — Kinetic typography, animated text sequences, and title animations.
3. **Video** — Opening titles, closing credits, lower thirds, captions, and information overlays.
4. **Web and UI** — Responsive typographic scales, hero sections, editorial web pages, and product UI.
5. **Editorial** — Magazines, books, annual reports, whitepapers, and exhibition catalogs.

---

## Installation

### 1. Zero-Context URL Installation (AI Coding Agents)

To install TypeCraft in a fresh conversation with any compatible AI coding agent, provide the repository URL:

```text
https://github.com/krupakar5535Kk/typecraft-skills.git
Install this skill.
```

The agent autonomously inspects the repository, reads [BOOTSTRAP.md](BOOTSTRAP.md), identifies its active platform ID, and executes the standard Skills CLI installation command globally.

---

### 2. Standard Skills CLI Route (Terminal & CLI Agents)

TypeCraft adopts the standard Agent Skills distribution ecosystem via the official Vercel Skills CLI (`skills`).

#### Install for your active agent globally (Default):
```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --global \
  --agent <ACTIVE_AGENT_ID> \
  --yes
```

#### Install across all supported local agents:
```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --global \
  --agent '*' \
  --yes
```

#### Install into current project/workspace only:
```bash
npx --yes skills add https://github.com/krupakar5535Kk/typecraft-skills.git \
  --skill typecraft-skills \
  --agent <ACTIVE_AGENT_ID> \
  --yes
```

#### Supported Agent Identifiers:
- `antigravity` — Google Antigravity App / IDE (`~/.gemini/config/skills/typecraft-skills/`)
- `antigravity-cli` — Google Antigravity CLI (`~/.gemini/antigravity-cli/skills/typecraft-skills/`)
- `claude-code` — Claude Code CLI (`~/.claude/skills/typecraft-skills/`)
- `cursor` — Cursor IDE (`~/.agents/skills/typecraft-skills/`)
- `codex` — OpenAI Codex CLI (`~/.agents/skills/typecraft-skills/`)
- `opencode` — OpenCode (`~/.agents/skills/typecraft-skills/`)
- `gemini-cli` — Gemini CLI (`~/.gemini/skills/typecraft-skills/`)
- `github-copilot` — GitHub Copilot Agent / VS Code (`~/.copilot/skills/typecraft-skills/`)

---

### 3. Offline / Maintainer Python Fallback Route

If Node.js or `npx` is unavailable in the environment, use TypeCraft's bundled Python installer:

```bash
python3 -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope user
```

*(Use `--force` to authorize replacing an existing installation).*

---

### 4. Browser-Based Platforms (ChatGPT Web, Claude.ai, Gemini Web)

Browser-based chat platforms operate in sandboxed browser environments without local filesystem or terminal access. For these platforms, download the official release package and upload it directly:

- **Verified Release Package:** [typecraft-skills.zip](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/typecraft-skills.zip)
- **SHA-256 Checksums:** [SHA256SUMS](https://github.com/krupakar5535Kk/typecraft-skills/releases/latest/download/SHA256SUMS)

#### Platform Upload Steps:
- **Gemini Web:** Open **Customize → Skills** (or **More → Customize → Skills**), select **Upload a skill**, and upload `typecraft-skills.zip`. Availability requires a Gemini Advanced subscription or an eligible Google Workspace (Business/Enterprise/Edu) account with custom skills enabled. Once saved, invoke via `@typecraft-skills` or `/typecraft-skills`. (For personal accounts without custom skills access, paste `typecraft-skills/SKILL.md` into a **Custom Gem** or attach it to the conversation as a fallback).
- **Claude.ai / Claude Cowork:** Open **Customize → Skills → Create skill → Upload a skill** and upload `typecraft-skills.zip` (or attach `typecraft-skills/SKILL.md` to **Project Knowledge**).
- **ChatGPT Web:** Open **Plugins → Plugin Directory → Skills → Create → Upload from your computer** (or attach to **Custom GPT → Knowledge**).

---

## Platform Verification Matrix

TypeCraft strictly evaluates platform readiness across four lifecycle stages:
1. **Installation:** Files copied to a documented native directory or archive uploaded.
2. **Discovery:** The platform's native skill catalog affirmatively indexes TypeCraft (`copilot skill list`, `gemini skills list`, `/skills` in Claude Code, `$skill-installer` in Codex).
3. **Invocation:** The agent model actually accesses and applies TypeCraft typography styles or design templates in a real task.
4. **Persistence:** Availability across fresh, independent conversations without reinstallation.

| Surface | Status | Route | Verified Evidence |
|---|---|---|---|
| **GitHub Copilot CLI** | **verified** | Native directory (`~/.copilot/skills/`) | Full installation, discovery (`copilot skill list`), and model invocation verified on CLI 1.0.105 & 1.0.114. |
| **GitHub Copilot VS Code Agent** | **verified** | GitHub CLI managed (`~/.copilot/skills/`) | Historical installation, discovery, and invocation verified in GitHub Codespaces (v1.1.0). |
| **Gemini CLI** | **verified** | Native directory (`~/.gemini/skills/`) | User-scope installation and native discovery verified via `gemini skills list --all`; live model invocation blocked by headless OAuth requirement. |
| **Google Antigravity App / CLI** | **compatible** | Standard CLI (`~/.gemini/config/skills/`, `~/.gemini/antigravity-cli/skills/`) | Live installation and catalog inspection verified; `/skills reload` supported. |
| **Claude Code CLI** | **compatible** | Standard CLI (`~/.claude/skills/`) | Route documented and verified with `skills add`; user-reported discovery observed; model invocation unverified in CI. |
| **Cursor IDE** | **compatible** | Standard CLI (`~/.agents/skills/`) | Route documented and verified with `skills add`; local user skills do not automatically sync to Cloud Agents. |
| **OpenAI Codex** | **compatible** | Standard CLI (`~/.agents/skills/`, `~/.codex/skills/`) | Route documented and verified with `skills add`; live invocation blocked by upstream account usage limit. |
| **OpenCode** | **compatible** | Standard CLI (`~/.agents/skills/`) | Route documented and verified with `skills add`. |
| **ChatGPT / Claude.ai / Cowork / Gemini Web** | **compatible** | Release ZIP upload | Verified local packaging; upload, scan, and confirmation require user action and account eligibility. |
| **Windsurf** | **research_required** | Unconfirmed | Former documentation URL redirects to Devin; native route unconfirmed. |

See the complete [Compatibility Guide](docs/compatibility.md) and [Installation Guide](docs/installation.md) for full audit records and evidence.

---

## Usage

After installing TypeCraft, describe your creative brief to your AI agent.

The agent will:
1. Identify the creative domain (Static, Motion, Video, Web/UI, Editorial).
2. Determine whether a typography style or design template is needed.
3. Select resources using **Automatic**, **Manual**, or **Mixed** mode.
4. Apply the canonical typographic rules, scale ratios, and layout zones.

### Selection Modes:
- **Automatic:** The agent chooses the optimal style and template for the brief.
- **Manual:** The agent strictly follows the style and template named by the user.
- **Mixed:** The agent preserves explicit user choices and selects unspecified components automatically.

**Example Prompts:**
- *"Design a poster for a technology conference using TypeCraft. Apply Swiss International Typographic Style and the Swiss Grid Editorial Poster template."*
- *"Create a film announcement title treatment using the Cinematic Title Poster template."*
- *"Suggest typography direction and font pairings for a luxury fashion brand editorial spread."*

---

## Documentation

- [Authoritative Agent Directives](AGENTS.md)
- [Universal Bootstrap Protocol](BOOTSTRAP.md)
- [Installation Guide](INSTALL.md)
- [Platform Installation Deep-Dive](docs/installation.md)
- [Platform Compatibility Guide](docs/compatibility.md)
- [Architecture](docs/architecture.md)
- [Usage Guide](docs/usage.md)
- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)

---

## License

Released under the [MIT License](LICENSE).
