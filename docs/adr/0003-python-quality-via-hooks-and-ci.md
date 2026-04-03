# 0003. Python 品質を pre-commit・CI・Claude Code フックで担保する

日付: 2026-04-03

## 状態

Accepted

## 文脈（Context）

- エディタ（Cursor 等）のルールやエージェント指示だけでは、**コミット前に同じチェックが必ず走る保証がない**。別ツール（Claude Code 等）で編集した場合も同様。
- スタイル・未使用 import などは機械的に揃えられる領域であり、レビューと人の注意を節約したい。
- [フィードバックループの設計（Hooks の活用）](https://nyosegawa.com/posts/harness-engineering-best-practices-2026/#%E3%83%95%E3%82%A3%E3%83%BC%E3%83%89%E3%83%90%E3%83%83%E3%82%AF%E3%83%AB%E3%83%BC%E3%83%97%E3%81%AE%E8%A8%AD%E8%A8%88%3A-hooks%E3%81%AE%E6%B4%BB%E7%94%A8) のように、**ツール実行直後に短い診断を返す**と、エージェントが自己修正しやすい。

## 決定（Decision）

- **Ruff** で `backend/` 配下の Python を lint・format する。設定は `backend/pyproject.toml` に集約する。
- **pre-commit**（リポジトリルートの `.pre-commit-config.yaml`）でコミット前に Ruff を実行する。開発者は `pre-commit install` で有効化する。
- **GitHub Actions** で `ruff check` と `ruff format --check` を別ジョブとして実行し、リモートでも同じ基準を強制する。
- **Claude Code** 向けに `.claude/settings.json` の `PostToolUse` で、Write / Edit / MultiEdit 後に `backend/**/*.py` へ Ruff をかけるシェルフックを置く。失敗時は `hookSpecificOutput.additionalContext` で診断を返す（ツール自体の成否とは切り離し、修正のヒントとして渡す）。

## 結果（Consequences）

- 良い影響: エディタ非依存で一貫した Python 品質。PR でのノイズが減る。Claude Code 利用時も同じループに乗せられる。
- 負債・コスト: 初回に `pip install -r backend/requirements-dev.txt` と `pre-commit install` が必要。Claude Code フックはホストに `ruff` が PATH にある前提（dev 依存と揃える）。
- フォローアップ: フロントエンドの ESLint 等は別 ADR または別タスクで検討する。
