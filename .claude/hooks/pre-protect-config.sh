#!/usr/bin/env bash
# Claude Code PreToolUse: Ruff / pre-commit / CI / フック設定の「ルール改竄」編集をブロックする（exit 2）。
# 参考: https://nyosegawa.com/posts/harness-engineering-best-practices-2026/#%E3%83%AA%E3%83%B3%E3%82%BF%E3%83%BC%E8%A8%AD%E5%AE%9A%E4%BF%9D%E8%AD%B7%3A-%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88%E3%81%AE%E3%80%8C%E3%83%AB%E3%83%BC%E3%83%AB%E6%94%B9%E7%AB%84%E3%80%8D%E3%82%92%E9%98%B2%E3%81%90
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

input_json="$(cat)"
export _PRE_PROTECT_HOOK_JSON="$input_json"
python3 - "$REPO_ROOT" <<'PY'
import json
import os
import sys
from pathlib import Path

# リポジトリルートからの相対パス（POSIX）。人間が意図して変える場合はエディタや PR 外で対応する。
PROTECTED = frozenset(
    {
        ".pre-commit-config.yaml",
        "backend/pyproject.toml",
        "backend/requirements-dev.txt",
        ".github/workflows/backend-ruff.yml",
        ".claude/settings.json",
        ".claude/hooks/pre-protect-config.sh",
        ".claude/hooks/post-ruff.sh",
    }
)

repo = Path(sys.argv[1]).resolve()
raw = os.environ.get("_PRE_PROTECT_HOOK_JSON", "")
try:
    data = json.loads(raw) if raw.strip() else {}
except json.JSONDecodeError:
    sys.exit(0)
finally:
    os.environ.pop("_PRE_PROTECT_HOOK_JSON", None)

ti = data.get("tool_input") or {}
raw = ti.get("file_path") or ti.get("path") or ""
if not str(raw).strip():
    sys.exit(0)

path = Path(str(raw))
try:
    target = path.resolve() if path.is_absolute() else (repo / path).resolve()
    rel = target.relative_to(repo)
except (ValueError, OSError):
    sys.exit(0)

key = rel.as_posix()
if key in PROTECTED:
    print(
        f"BLOCKED: 「{key}」は品質ハーネス用の保護対象です。\n"
        "リンター・pre-commit・CI の設定を弱めてパスさせず、コード側を修正してください。\n"
        "参考: docs/adr/0003-python-quality-via-hooks-and-ci.md\n"
        "背景: https://nyosegawa.com/posts/harness-engineering-best-practices-2026/",
        file=sys.stderr,
    )
    sys.exit(2)
sys.exit(0)
PY
