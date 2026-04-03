#!/usr/bin/env bash
# Claude Code PostToolUse: backend の .py を Ruff で検査し、失敗時は additionalContext を返す。
# 前提: `pip install -r backend/requirements-dev.txt` などで ruff が PATH にあること。
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if ! command -v ruff >/dev/null 2>&1; then
  python3 - "$REPO_ROOT" <<'PY'
import json, sys
root = sys.argv[1]
msg = (
    "ruff が PATH にありません。リポジトリルートで次を実行してください:\n"
    f"  pip install -r {root}/backend/requirements-dev.txt\n"
    "（または pre-commit の仮想環境内の ruff を PATH に通す）"
)
print(
    json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": msg,
            }
        },
        ensure_ascii=False,
    )
)
PY
  exit 0
fi

input_json="$(cat)"
rel="$(
  printf '%s' "$input_json" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
ti = d.get('tool_input') or {}
p = ti.get('file_path') or ti.get('path') or ''
print(p or '', end='')
")"

[[ -z "$rel" ]] && exit 0
[[ "$rel" == *.py ]] || exit 0

if [[ "$rel" == /* ]]; then
  case "$rel" in
    "$REPO_ROOT"/*) rel="${rel#"$REPO_ROOT"/}" ;;
    *) exit 0 ;;
  esac
else
  rel="${rel#./}"
fi

[[ "$rel" == backend/*.py ]] || exit 0

target="$REPO_ROOT/$rel"
[[ -f "$target" ]] || exit 0

diag_file="$(mktemp)"
trap 'rm -f "$diag_file"' EXIT
ec=0
if ! (cd "$REPO_ROOT" && ruff check "$rel") >>"$diag_file" 2>&1; then
  ec=1
fi
if ! (cd "$REPO_ROOT" && ruff format --check "$rel") >>"$diag_file" 2>&1; then
  ec=1
fi

if [[ "$ec" -eq 0 ]]; then
  exit 0
fi

python3 - "$diag_file" <<'PY'
import json, sys

path = sys.argv[1]
with open(path, encoding="utf-8", errors="replace") as f:
    msg = f.read().strip()
if not msg:
    msg = "Ruff が失敗しました（詳細なし）。ターミナルで ruff check / ruff format --check を実行してください。"
print(
    json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": msg,
            }
        },
        ensure_ascii=False,
    )
)
PY
exit 0
