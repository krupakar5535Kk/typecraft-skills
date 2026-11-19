# TypeCraft Skills — Compatibility Guide

## Overview

TypeCraft is designed as a tool-independent AI Agent Skill.

Its instructions describe typography styles, design templates, creative workflows, and resource-selection rules. Actual execution depends on the capabilities of the AI agent and its available tools.

## Intended Environments

The following environments are project targets:

- Claude Code
- OpenAI Codex
- ChatGPT
- Google Antigravity
- Cursor
- Windsurf

Listing an environment here does not mean that installation or execution has been independently verified.

## Compatibility Requirements

An environment should support:

1. Discovering and loading the TypeCraft skill.
2. Reading its main SKILL.md instructions.
3. Accessing supporting reference files.
4. Following resource-selection instructions.
5. Using available tools to execute or communicate the requested design.

## Tool-Aware Execution

TypeCraft provides design direction and structured instructions. It does not guarantee that every environment can render images, produce videos, create animations, or generate production-ready web interfaces.

Execution depends on the tools available in the target environment.

## Verification Status

Platform-specific compatibility must be tested and documented independently.

Do not describe an environment as fully supported until its skill discovery, reference access, and core workflow have been verified.

## Reporting Compatibility

Future compatibility reports should identify:

- AI agent and version
- Installation method
- Skill discovery result
- Reference access result
- Workflow test result
- Known limitations
- Verification date
