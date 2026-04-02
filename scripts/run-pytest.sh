#!/usr/bin/env bash
# backend で venv を有効にし pytest を実行する。
# 使い方:
#   ./scripts/run-pytest.sh
#   ./scripts/run-pytest.sh showcase/domain/tests/
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT/backend"

if [[ ! -f .venv/bin/activate ]]; then
  echo "backend/.venv が見つかりません。backend で python -m venv .venv と pip install を実行してください。" >&2
  exit 1
fi

# shellcheck source=/dev/null
. .venv/bin/activate
exec pytest "$@"
