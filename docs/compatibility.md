# TypeCraft Skills — Platform Compatibility

## Status definitions

The registry separates installer support from platform compatibility and
runtime discovery:

- **Compatible:** current official platform documentation describes Agent
  Skills support and a documented installation route. This is not a TypeCraft
  end-to-end test.
- **Verified:** TypeCraft installation and runtime discovery were actually
  tested on the named platform and version.
- **Research required:** TypeCraft has not established a safe supported route
  for that platform.
- **Unsupported:** no persistent skill installation mechanism is available.

No platform is marked `verified` merely because a directory exists or an
installer returned success.

## Supported installation routes

| Platform | Route | What can be verified by the TypeCraft router |
|---|---|---|
| Claude Code | Native `~/.claude/skills/` or `.claude/skills/` | File tree; runtime discovery must be checked with `/skills` |
| OpenAI Codex | Native `~/.agents/skills/` or `.agents/skills/` | File tree; runtime discovery must be checked in Codex |
| Cursor | Native `~/.cursor/skills/` or `.cursor/skills/` | File tree; runtime discovery must be checked in Cursor |
| Gemini CLI | Native `~/.gemini/skills/` or `.gemini/skills/` | File tree and, when available, `gemini skills list --all` |
| OpenCode | Native `~/.config/opencode/skills/` or `.opencode/skills/` | File tree; runtime discovery must be checked in OpenCode |
| Google Antigravity App | Native `~/.gemini/config/skills/` or `.agents/skills/` | File tree; runtime discovery must be checked in the App |
| GitHub CLI registered hosts | GitHub CLI preview `gh skill install` adapter | CLI inventory and reference files; not runtime discovery |
| ChatGPT Skills | ZIP upload in the product UI | ZIP contents only; upload, scan, and installation require user action |
| Chat-only environment | Current-conversation use, if all files are readable | No persistent installation or discovery |

The native paths are sourced from the platform documentation linked in
[`registry/agents.yaml`](../registry/agents.yaml). Antigravity App and
Antigravity CLI are separate hosts; no CLI-specific path is asserted here.

GitHub CLI currently documents 48 supported host IDs. That list means the
installer can route a skill to those host integrations; it does not mean each
host has been independently tested with TypeCraft. The registry keeps
`installation_verified` and `skill_discovery_verified` false until an actual
test is performed.

## Platforms requiring further research

Windsurf, Zed, Aider, custom agent frameworks, and any host without a documented
TypeCraft adapter remain `research_required` in the registry. Do not copy to an
assumed path or claim compatibility based on a shared skill format alone.

## Tool-aware execution

TypeCraft provides design direction and structured resources. Rendering images,
video, animation, or production-ready web interfaces depends on the tools
available in the active environment.

## Verification report

For each real platform test, record:

- Agent, version, operating system, and installation scope.
- Adapter and resulting destination.
- Complete source-file and reference verification.
- Platform-native skill discovery result.
- Core workflow and reference access result.
- User action, reload requirement, and limitations.
- Verification date.

Until that evidence exists, report file installation and runtime discovery as
separate results.
