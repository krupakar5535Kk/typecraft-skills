# TypeCraft Skills — AI Agent Installation Guide

This repository contains TypeCraft Skills, a reusable skill for typography,
graphic design direction, visual systems, and creative design workflows.

## Instructions for AI Agents

If a user asks you to install TypeCraft Skills, follow this procedure.

### 1. Inspect the repository

Repository:
https://github.com/krupakar5535Kk/typecraft-skills

Canonical skill directory:
skills/typecraft-skills/

Read these files before installation:

- skills/typecraft-skills/SKILL.md
- All Markdown files under skills/typecraft-skills/references/

Do not install only the SKILL.md file. The complete references directory
is part of the skill.

### 2. Identify your environment

Determine which AI agent, application, IDE, or CLI you are running in.

Identify its officially supported persistent skill installation mechanism.

Use the platform's documented skill directory, upload mechanism, or
installation interface.

Do not guess installation paths. Consult the platform's own documentation
when the correct location is uncertain.

### 3. Install the complete skill

Install the directory:

skills/typecraft-skills/

Preserve this structure:

typecraft-skills/
├── SKILL.md
└── references/
    ├── design-styles/
    └── design-templates/

Requirements:

- Preserve all files and directory names.
- Keep the skill folder named `typecraft-skills`.
- Do not omit reference files.
- Do not modify the canonical skill content.
- Do not execute repository scripts as part of installation.
- Do not overwrite an existing installation without user permission.
- Prefer the user's requested installation scope.
- If permissions are required, request them through the platform's
  normal approval mechanism.

### 4. Handle unsupported environments honestly

If your current environment does not support persistent custom skills,
do not claim that installation succeeded.

Explain the limitation and provide the appropriate manual installation
instructions supported by that platform.

If you can only read the repository but cannot write files, explain that
you need filesystem or installation permission.

Do not confuse temporary instructions in the current conversation with
a persistent skill installation.

### 5. Verify installation

After installation:

1. Confirm the skill directory exists in the correct location.
2. Confirm SKILL.md exists and is readable.
3. Confirm all reference Markdown files were copied.
4. Confirm the AI agent can discover or load the skill.
5. If discovery requires restarting or opening a new session, tell the user.

Report these separately:

- Installation: SUCCESS / FAILED
- File verification: SUCCESS / FAILED
- Skill discovery: VERIFIED / NOT VERIFIED / NOT SUPPORTED

Never claim discovery is verified merely because files were copied.

### 6. Report the result

Tell the user:

- Which agent or application was detected.
- Where the skill was installed.
- Whether all files were installed.
- Whether skill discovery was verified.
- Whether any user action remains.

## Important

TypeCraft Skills is the canonical skill library in this repository.

Do not create a different or modified copy for each agent. Use the
platform's supported installation mechanism while preserving the same
canonical skill content.

Repository:
https://github.com/krupakar5535Kk/typecraft-skills
