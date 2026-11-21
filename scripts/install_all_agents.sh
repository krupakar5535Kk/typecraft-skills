#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

if [[ -x "$ROOT/.venv/bin/python" ]]; then
    PYTHON="$ROOT/.venv/bin/python"
else
    PYTHON="$(command -v python3 || true)"
fi

if [[ -z "$PYTHON" ]]; then
    echo "ERROR: Python 3 is required."
    exit 1
fi

if ! "$PYTHON" -c "import strictyaml" >/dev/null 2>&1; then
    echo "ERROR: Missing dependency: strictyaml"
    echo "Install dependencies with: $PYTHON -m pip install -r $ROOT/requirements-installer.txt"
    exit 1
fi

ARGS=(--all)

if [[ -n "${TYPECRAFT_SCOPE:-}" ]]; then
    ARGS+=(--scope "$TYPECRAFT_SCOPE")
fi

exec "$PYTHON" "$ROOT/scripts/install.py" "${ARGS[@]}" "$@"
