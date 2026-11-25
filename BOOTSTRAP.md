# TypeCraft Skills v1.4.0 — Universal AI Agent Bootstrap Protocol

> **For AI Agents:** You are receiving this instruction because the user provided the TypeCraft repository URL (`https://github.com/krupakar5535Kk/typecraft-skills.git` or `https://github.com/krupakar5535Kk/typecraft-skills`) and requested: **"Install this skill"** (or supplied the standalone URL).

---

## 1. Zero-Friction Installation Mandate

A user pasting this URL into their AI agent expects the agent to handle the installation natively:

- **DO NOT** instruct the user to open a terminal or run commands manually.
- **DO NOT** ask the user to clone the repository manually.
- **DO NOT** create dummy files, mock directories, or install to all agents on the machine.
- **DO NOT** execute untrusted third-party scripts.
- **DO NOT** run raw `npx skills add ... --yes` without pre-installation collision checks.

When the active agent has terminal and filesystem permissions, **the agent must perform the installation autonomously using TypeCraft's authoritative safe installer.**

---

## 2. Authoritative Safe Installation Workflow

TypeCraft provides an authoritative, collision-protected installer at `scripts/install_url.py`.

### Primary Execution Pattern

```bash
python3 -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent auto \
  --scope user
```

`--agent auto` detects the running agent from active environment variables (`TYPECRAFT_AGENT` or unambiguous host signals). If running in a specific known agent, pass its exact ID (e.g. `--agent antigravity` or `--agent claude-code`).

### External Engine Support (with Mandatory Pre-Collision Check)

If your platform specifically uses Vercel Skills CLI or GitHub CLI, use TypeCraft's engine flags:

```bash
# Vercel Skills CLI with TypeCraft collision protection
python3 -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope user \
  --engine vercel

# GitHub CLI with TypeCraft collision protection
python3 -m scripts.install_url \
  --request "https://github.com/krupakar5535Kk/typecraft-skills.git Install this skill." \
  --agent <ACTIVE_AGENT_ID> \
  --scope user \
  --engine gh
```

---

## 3. Critical Collision & Overwrite Protection

**WARNING:** Raw `npx skills add ... --yes` silently overwrites modified or existing files on disk, destroying local customizations without warning.

TypeCraft's installer enforces strict pre-execution collision checks before modifying the filesystem or invoking external tools:

| Existing Target State | Required System Behavior |
|---|---|
| **No installation** | Installs all 21 canonical files cleanly. |
| **Identical installation** | Reports already installed and verified; skips overwriting. |
| **Modified TypeCraft copy** | Safely blocks with `ExistingInstallationError`; protects user modifications. |
| **Different skill with same name** | Safely blocks with `ExistingInstallationError`; refuses to clobber. |
| **Explicit overwrite requested** | Requires the explicit `--force` flag with clear user authorization. |

This protection covers all native directories, external installer invocations (`npx` and `gh`), and shared locations like `~/.agents/skills/typecraft-skills`.

---

## 4. Evaluated Target Agents & Mappings

| Agent Target ID | Product Surface | User-Scope Persistent Directory | Project-Scope Directory | Runtime Discovery Check |
|---|---|---|---|---|
| **`antigravity`** | Google Antigravity App / IDE | `~/.gemini/config/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | App skill catalog inspection |
| **`antigravity-cli`** | Google Antigravity CLI | `~/.gemini/antigravity-cli/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | `/skills reload` command |
| **`claude-code`** | Claude Code CLI | `~/.claude/skills/typecraft-skills/` | `.claude/skills/typecraft-skills/` | `/skills` command in session |
| **`codex`** | OpenAI Codex | `~/.agents/skills/typecraft-skills/` or `~/.codex/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | Native `~/.agents/skills/` index or `$CODEX_HOME/skills` |
| **`cursor`** | Cursor IDE | `~/.agents/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | Cursor Features > Skills panel |
| **`gemini-cli`** | Gemini CLI | `~/.gemini/skills/typecraft-skills/` | `.gemini/skills/typecraft-skills/` | `gemini skills list --all` |
| **`opencode`** | OpenCode | `~/.agents/skills/typecraft-skills/` | `.agents/skills/typecraft-skills/` | `opencode skills list` |
| **`github-copilot`** | GitHub Copilot Agent (VS Code) | `~/.copilot/skills/typecraft-skills/` | `.github/skills/typecraft-skills/` | Copilot Agent Skills inventory |

### Surface Disambiguation
- **Antigravity App vs Antigravity CLI:** Distinct targets. Antigravity App/IDE reads `~/.gemini/config/skills/`; CLI-specific target is `~/.gemini/antigravity-cli/skills/`. Both support workspace `.agents/skills/`.
- **Claude Code vs Claude Web:** Claude Code has a local terminal and persistent directory (`~/.claude/skills/`). Claude Web runs in the browser and requires account-level upload or Project Knowledge.
- **OpenAI Codex vs ChatGPT Web:** Codex uses `~/.agents/skills/`. ChatGPT web requires workspace skill upload.
- **Gemini CLI vs Gemini Web/Mobile:** Gemini CLI is a terminal agent. Gemini Web and mobile apps do not have persistent filesystem access.

---

## 5. Five-Stage Verification Protocol

Never claim successful installation based solely on process exit code `0`. Complete all five stages:

### Stage 1: Files Installed
Confirm that the installed directory contains all 21 canonical files:
- Manifest: `SKILL.md` (root of skill directory)
- 10 Typography Styles: `references/design-styles/*.md`
- 10 Design Templates: `references/design-templates/*.md`

### Stage 2: SHA-256 Integrity Verified
Verify that every installed file matches the canonical source SHA-256 hash. No files truncated, omitted, or altered.

### Stage 3: Runtime Discovery Verified
Query the host agent's native discovery mechanism (e.g. `gemini skills list --all`, `gh skill list`, or `/skills reload`) to ensure the runtime indexes `typecraft-skills`. Report `NOT_VERIFIED` honestly if the platform's discovery cannot be checked programmatically.

### Stage 4: Invocation Tested
Verify that your active context understands the TypeCraft system:
- 5 creative domains (Static Graphics, Motion Graphics, Video, Web/UI, Editorial).
- Typography Styles (personality) vs. Design Templates (structure).
- 3 selection modes (Automatic, Manual, Mixed).

### Stage 5: Session Persistence Verified
Confirm that files reside in a global user-level location (not an ephemeral `/tmp` directory) so TypeCraft remains available across restarts.

---

## 6. Chat-Only Platform Handoff Protocol

If your runtime is a browser or mobile chat without persistent filesystem access:

1. **Be Honest:** Do not claim you wrote files or installed TypeCraft persistently.
2. **Provide Official Platform Handoff:**
   - **ChatGPT Web Skills:** Direct the user to **Settings > Skills > Upload from your computer**. Use `--package-output` to create the ZIP.
   - **Claude Free / Pro Web:** Instruct the user to attach or paste `skills/typecraft-skills/SKILL.md` into Project Knowledge or the active conversation context.
   - **Gemini Web / Mobile:** Instruct the user to create a Custom Gem using `skills/typecraft-skills/SKILL.md`.

---

## 7. Zero-Context Bootstrap Discovery

> **Important Architectural Reality:** `AGENTS.md` and repository instruction files only become active after the repository or workspace is accessible to the agent. A remote URL pasted into a blank conversation does not automatically load `AGENTS.md` before the repository is fetched.

For a fresh agent in a zero-context conversation with just the URL:
1. The agent fetches/inspects the repository from the provided URL.
2. The agent reads `README.md` and `BOOTSTRAP.md`.
3. The agent resolves its host identity and executes `python3 -m scripts.install_url`.
4. The installer performs collision checking, installs atomically, verifies SHA-256 hashes, and checks discovery.
5. The agent reports the final status using the standard report format.

---

## 8. Standard Installation Report Format

```text
TypeCraft Skills Installation Report
====================================
Platform:             <Platform Name> (<agent-id>)
Version:              1.4.0
Installation:         SUCCESS (or ALREADY_INSTALLED / UPDATED)
Location:             <Installed Path>
File verification:    SUCCESS (21/21 files verified by SHA-256)
Skill discovery:      VERIFIED (or NOT_VERIFIED)
User action:          None (or platform-specific remaining action)
Details:              <Summary of action taken>
```
