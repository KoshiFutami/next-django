---
name: github-pr
description: GitHub で PR を作成する手順（gh CLI・Makefile・テンプレート）。ブランチを push したあと PR 作成するときに使う。
---

# GitHub PR 作成スキル

## 前提

- [GitHub CLI](https://cli.github.com/)（`gh`）をインストールし、`gh auth login` 済みであること
- 変更を push 済みであること（`git push -u origin <branch>`）

## 最短（このリポジトリ）

```bash
make pr
```

中身は `gh pr create --fill` です。直近コミットからタイトル・本文の下書きを埋めます。

## よく使うコマンド

| 目的 | コマンド |
|------|----------|
| エディタでタイトル・本文を書く | `make pr` のあと、または `gh pr create` |
| ブラウザで開いて作成 | `make pr-web` |
| 下書き PR | `make pr-draft` |
| ベースブランチ指定 | `gh pr create --base main --fill` |

## Cursor コマンド定義（エージェント用）

リポジトリの `.cursor/commands/` に次があります（エディタの Custom Commands から参照可能な場合があります）。

- `commit.md` — ステージ・分割コミットのガイド。`make commit` で `git commit` を起動
- `review.md` — 差分レビュー観点。`make review` → `gh pr view`
- `approve.md` — PR 承認。`make approve` → `gh pr review --approve`
- `push.md` — リモートへ push。`make push` → `git push -u origin HEAD`

## PR テンプレート

`.github/pull_request_template.md` が既定で挿入されます。ブラウザ上の「Open a pull request」でも同じテンプレートが使われます。

## トラブルシュート

- `gh: command not found` → `brew install gh`（macOS）
- 認証エラー → `gh auth login`
- リモートにブランチが無い → 先に `git push -u origin HEAD`
