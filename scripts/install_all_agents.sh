#!/usr/bin/env bash
set -u

REPOSITORY="krupakar5535Kk/typecraft-skills"
SKILL="typecraft-skills"
SCOPE="${TYPECRAFT_SCOPE:-user}"

AGENTS=(
  github-copilot claude-code cursor codex gemini-cli
  antigravity antigravity-cli antigravity2.0 adal amp augment bob
  cline codebuddy command-code continue cortex crush deepagents
  devin droid firebender goose grok iflow-cli junie kilo kimi-cli
  kiro-cli kode mcpjam mistral-vibe mux neovate openclaw opencode
  openhands pi pochi qoder qwen-code replit roo trae trae-cn
  universal warp zencoder
)

MODE="${1:-install}"

if ! command -v gh >/dev/null 2>&1 || ! gh skill --help >/dev/null 2>&1; then
  echo "ERROR: GitHub CLI with gh skill support is required."
  exit 1
fi

echo "TYPECRAFT UNIVERSAL INSTALLER"
echo "Repository: $REPOSITORY"
echo "Skill: $SKILL"
echo "Scope: $SCOPE"
echo "Agent targets: ${#AGENTS[@]}"
echo

if [[ "$MODE" == "--dry-run" ]]; then
  for agent in "${AGENTS[@]}"; do
    echo "[PREVIEW] $agent"
  done
  echo
  echo "Preview only. Nothing was installed."
  exit 0
fi

SUCCESS=0
FAILED=0

for agent in "${AGENTS[@]}"; do
  echo
  echo "Installing: $agent"

  if gh skill install "$REPOSITORY" "$SKILL" \
      --agent "$agent" --scope "$SCOPE"; then
    echo "SUCCESS: $agent"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "FAILED: $agent"
    FAILED=$((FAILED + 1))
  fi
done

echo
echo "INSTALLATION SUMMARY"
echo "Successful targets: $SUCCESS"
echo "Failed targets: $FAILED"
echo "Some agents share installation directories."
echo "ChatGPT requires its separate distribution route."

[[ "$FAILED" -eq 0 ]]
