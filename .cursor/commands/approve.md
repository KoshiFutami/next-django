---
description: 現在のブランチの PR を承認する（gh pr review）
---

# approve

## 前提

- [GitHub CLI](https://cli.github.com/)（`gh`）が入り、`gh auth login` 済み。
- レビュー完了し、マージしてよいと判断したときだけ使う。

## 手順

1. オープンな PR が現在ブランチに存在することを確認: `gh pr status` または `gh pr view`。
2. 承認: 次のいずれか。

```bash
gh pr review --approve --body "LGTM"
```

コメント付きで承認:

```bash
gh pr review --approve --body "内容の説明..."
```

## Makefile ショートカット

```bash
make approve
```

`gh pr review --approve` を実行する（コメントは空でよい場合は `--body` なしで可。`gh` の仕様に合わせて調整）。

## 注意

- **自分の PR には通常は不要**（他者レビュー前提のワークフローのときはルールに従う）。
- チームで必須レビュー数がある場合は、それを満たしてからマージする。
