
# TYPECRAFT SKILLS

## Technical Architecture v1.2.0

**Status:** Current release
**Project Type:** Open-Source, Tool-Independent AI Agent Skill
**License:** MIT

## 1. Product Vision

**ONE URL. ONE SKILL. EVERY COMPATIBLE AI AGENT.**

TypeCraft Skills is a tool-independent AI typography and text-design skill for creative professionals.

It provides reusable typography knowledge, creative direction and design execution instructions to compatible AI agents.

Its goal is to make professional typography and visual design workflows more accessible, consistent and adaptable across creative domains.

## 2. Core Product

- One installable AI Agent Skill.
- Exactly 10 typography design styles.
- Exactly 10 design templates.
- Automatic, manual and mixed design selection.
- Static and animated typography guidance.
- Video and motion-graphics design guidance.
- Web and UI typography guidance.
- Editorial and publication design guidance.

## 3. Creative Domains

1. Static graphics and posters.
2. Motion graphics and animated typography.
3. Video titles, overlays and lower thirds.
4. Websites and UI design.
5. Editorial and publication design.

## 4. Design System

Typography styles define visual appearance, type treatments, effects and visual language.

Design templates define composition, layout, text positioning and hierarchy.

Styles and templates are independent resources and can be combined according to the creative requirements.

Users may combine multiple styles and templates when the task requires it.

A selected style must not automatically dictate the layout, and a selected template must not unnecessarily restrict typography choices.

## 5. Selection System

### Automatic Selection

The agent selects appropriate typography styles and design templates based on the user's creative request.

### Manual Selection

Users explicitly specify their preferred styles and templates. The agent must respect those selections.

### Mixed Selection

Users specify one design dimension and allow the agent to select the other.

For example, a user may select a typography style while allowing the agent to choose a suitable layout template.

### Selection Integrity

Explicit user choices, content requirements and design constraints must never be silently overridden.

When selected resources conflict with technical or visual requirements, the agent should explain the conflict and propose an alternative.

## 6. Single Skill Architecture

The repository maintains one primary installable skill:

`skills/typecraft-skills/`

Its required entry point is:

`skills/typecraft-skills/SKILL.md`

Supporting resources are organized into:

- `references/` — Detailed typography styles, design templates and supporting knowledge.
- `examples/` — Practical examples demonstrating resource applications.
- `assets/` — Reusable project assets where applicable.

The core skill coordinates the workflow and loads supporting resources when relevant.

## 7. Progressive Disclosure

`SKILL.md` contains the core workflow and operating instructions.

Detailed typography knowledge belongs in `references/`.

Examples and reusable resources belong in `examples/` and `assets/`.

Supporting resources should be loaded only when relevant to the user's request.

This keeps the primary skill focused. This release candidate preserves the
fixed resource scope of 10 styles and 10 templates; expanding that library is
out of scope.

## 8. Technical Foundation

- Open Agent Skills specification.
- Markdown-based instructions.
- YAML frontmatter.
- Single source of truth.
- Git-based version control.
- MIT licensing for project code and documentation, subject to applicable third-party asset licenses.

## 9. AI Agent Compatibility

Platform integrations are recorded by product surface in
[`registry/agents.yaml`](../registry/agents.yaml). A documented route is not
proof that TypeCraft has been installed; file verification is not runtime
discovery, and discovery is not skill invocation. Runtime discovery evidence
exists for GitHub Copilot Agent mode in Visual Studio Code running in GitHub
Codespaces and Gemini CLI user scope. Only the Copilot record includes actual
skill-invocation evidence. Copilot CLI, app, and cloud agent are separate
surfaces. Claude Code local sessions are not equivalent to Cowork or remote
cloud sessions. Windsurf and Antigravity CLI remain unverified.

Platform-specific installation instructions must accurately describe the requirements and limitations of each environment.

## 10. Tool-Aware Execution

TypeCraft provides creative direction, typography knowledge, design specifications and execution instructions.

Actual image, video, animation or code generation depends on the capabilities and tools available to the connected AI agent.

The skill must identify available capabilities before promising or attempting tool-dependent operations.

When a requested operation cannot be performed directly, the agent should provide the most useful practical instructions supported by the environment.

Unsupported capabilities must never be claimed.

## 11. Quality Standards

Every applicable design should be evaluated for:

- Typography hierarchy.
- Legibility.
- Composition and spacing.
- Color consistency.
- Visual balance.
- Domain suitability.
- Motion and timing where applicable.
- Accessibility and readability.
- Platform-specific output quality.
- Asset licensing and attribution.

Quality evaluation should reflect the intended medium and the user's requirements.

## 12. Distribution

Maintain one canonical skill implementation.

Platform-specific installation methods must reuse the same core skill without creating separate implementations or divergent versions.

The project is intended for public distribution through GitHub.

Public availability does not automatically guarantee installation or execution compatibility across every AI platform.

Documentation must distinguish verified installation methods from intended or unverified integrations.

## 13. Core Philosophy

One library.

One installable skill.

10 typography styles.

10 design templates.

Multiple creative domains.

Multiple compatible AI agents.

Independent and flexible design combinations.

One consistent design philosophy.

**TYPECRAFT SKILLS — ONE URL. ONE SKILL. EVERY COMPATIBLE AI AGENT.**
