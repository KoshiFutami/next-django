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
- **Claude Code** の `PreToolUse` で、Ruff / pre-commit / 関連 CI / `.claude` フック本体の編集を **exit 2 でブロック**する（[リンター設定保護](https://nyosegawa.com/posts/harness-engineering-best-practices-2026/#%E3%83%AA%E3%83%B3%E3%82%BF%E3%83%BC%E8%A8%AD%E5%AE%9A%E4%BF%9D%E8%AD%B7%3A-%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88%E3%81%AE%E3%80%8C%E3%83%AB%E3%83%BC%E3%83%AB%E6%94%B9%E7%AB%84%E3%80%8D%E3%82%92%E9%98%B2%E3%81%90)）。設定変更が必要なときは Claude 外（エディタ・別 PR）で行う。

## 結果（Consequences）

- 良い影響: エディタ非依存で一貫した Python 品質。PR でのノイズが減る。Claude Code 利用時も同じループに乗せられる。
- 負債・コスト: 初回に `pip install -r backend/requirements-dev.txt` と `pre-commit install` が必要。Claude Code フックはホストに `ruff` が PATH にある前提（dev 依存と揃える）。保護ファイルの変更は Claude Code 経由ではできないため、ルール見直しは通常の編集・PR で行う。
- フォローアップ: フロントエンドの ESLint 等は別 ADR または別タスクで検討する。
