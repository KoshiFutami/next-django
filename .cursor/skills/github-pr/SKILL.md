---
name: github-pr
description: GitHub で PR を作成・更新する手順（gh CLI・Makefile）。テンプレに沿ったタイトル・本文。既存 PR では未反映コミットを追記。push 後に使う。
---

# GitHub PR 作成スキル

## 前提

- [GitHub CLI](https://cli.github.com/)（`gh`）をインストールし、`gh auth login` 済みであること
- 変更を push 済みであること（`git push -u origin <branch>`）

## PR のベースブランチ（マージ先）

**feature ブランチをどこから切ったか**と、GitHub の PR の **Base（マージ先）を一致**させる。`main` から切ったなら `main`、`release/owner-api` など別ブランチから切ったなら **そのブランチ**を `--base` に指定する。いきなり `main` を指定しない。

**派生元の確認の例**

- 分岐時に決めているなら、そのブランチ名をそのまま使う。
- `git reflog -n 20` に `checkout: moving from <元ブランチ> to <feature>` が残っていることがある。
- `git log --oneline --graph --decorate -20` で、どのリモートブランチ系列に乗っているかを見る。
- 迷う場合はユーザーに「マージ先はどのブランチか」を確認する。

**コマンド**

```bash
gh pr create --base <派生元ブランチ名> --title "feat: …" …
```

既存 PR の更新フローでは、`gh pr view` の `baseRefName` がすでに設定されたマージ先なので、**新規作成時**に特に `--base` を誤らないこと。

## タイトル・説明文（テンプレート準拠）

[`.github/pull_request_template.md`](../../.github/pull_request_template.md) の見出しに沿って書く。`--fill` は直近コミットの寄せ集めに過ぎないため、**レビューに出す前に**テンプレに合わせて埋め直す。

### タイトル

- **Conventional Commits 風の接頭辞**（`feat:` / `fix:` / `chore:` / `docs:` / `refactor:` など）＋ **一行で変更要約**（目安 50〜72 文字以内）。
- 複数領域にまたがる場合は、最も重要な変更か「なぜ」を表す語を選ぶ。

### 本文（各セクションの役割）

| 見出し | 書くこと |
|--------|----------|
| 概要 | **なぜ**この PR が必要か。背景・目的を 1〜3 文。 |
| 変更内容 | **何を**どう変えたか。箇条書き。ファイル名の羅列だけにしない。 |
| テスト | 実施した確認にチェックを入れる（pytest / curl / 手動など）。未実施なら理由を一言。 |
| チェックリスト | 該当項目にチェック。マイグレーションがあれば説明に手順を書く。 |
| 関連 | Issue や議論へのリンク。なければ「なし」。`Closes #123` はここで。 |

### 改行・余白（読みやすさ）

GitHub の Markdown は**空行がないと**段落やリストがつながって読みにくくなる。

- **見出し（`##`）の直後**に本文を書くときは、見出しと本文のあいだに空行を 1 行入れる。
- **複数段落の概要**は、段落と段落のあいだに空行を入れる。
- **変更内容**でトピックが変わる単位（例: ドメインと CI）ごとに、箇条書きのブロックのあいだに空行を入れてもよい。
- `gh pr create --body` や `--body-file` では、文字列内に `\n\n`（空行）を明示して段落を分ける。

### 作成の流れ（推奨）

1. 差分を踏まえて、上記の内容を**頭の中またはメモで**埋める。
2. **どちらか**:
   - **A**: `make pr`（`--fill`）→ すぐ `gh pr edit` でタイトル・本文をテンプレ構造に差し替える。
   - **B**: `gh pr create --base <派生元> --title "feat: …" --body-file .github/pull_request_template.md` で、エディタで各セクションを埋めてから保存（テンプレの HTML コメントは説明用・GitHub 上では非表示）。`<派生元>` は上記「PR のベースブランチ」を満たすこと。
3. ブラウザでプレビューし、箇条書きとチェックが揃っているか確認。

エージェントが PR を作るときは、**先に派生元ブランチを特定して `--base` を付ける**こと。あわせて**テンプレの見出しごとに**概要・変更点・テスト・関連を埋めた `--body` を渡すか、`--body-file` 用に一時ファイルへ整形してから `gh pr create` すること。

### 既存 PR がある場合（追 push 後もタイトル・説明を最新にする）

`make pr` / `gh pr create` は**新規作成専用**。同じブランチに PR が既にあるときは、**説明文やタイトルにまだ載っていないコミット**を拾って反映する。

1. **PR の有無とベースブランチを取得**

   ```bash
   gh pr view --json number,title,body,baseRefName,url
   ```

   エラーなら PR なし → 新規作成フローへ。成功なら `baseRefName`（マージ先＝派生元に揃えたブランチ名）を控える。

2. **ベース…HEAD のコミット一覧**（PR に含まれる差分の全体）

   ```bash
   git fetch origin
   BASE=<上記 baseRefName>
   git log "origin/$BASE"..HEAD --oneline
   ```

   `origin/$BASE` が無い場合は `git merge-base HEAD "origin/$BASE"` や `gh pr view --json mergeCommit` は使わず、まず `git fetch origin "$BASE"` を試す。

3. **未反映コミットの判定（目安）**

   各コミットの件名（`git log` の行）について、**現在の PR タイトル・本文に、その件名または言い換えが含まれているか**を見る。含まれないものは「変更内容」に追記する候補。マージコミットや `fixup!` はまとめて書いてよい。

4. **本文の更新**

   - **変更内容**に、未反映分を箇条書きで足す（コミット件名をそのまま並べるだけでも可。必要なら人間向けに言い換え）。
   - 新しいコミットで**目的やテスト状況が変わったら**、**概要**・**テスト**・**チェックリスト**も更新。
   - 「（追記）」のようなラベル付けや、追記部分だけの太字強調は不要。既存の箇条書きへ自然に統合する。

5. **タイトルの更新**

   - まだブランチ名のまま・古い主題のままなら、**差分全体**を表す一行に直す。
   - 後から `fix:` や `docs:` だけが増えた場合は、接頭辞を `chore:` などに揃えるか、**最もレビュー上重要な変更**を表す語を残す。

6. **反映**

   ```bash
   gh pr edit --body-file /path/to/edited-body.md
   # または gh pr edit --title "feat: …" --body "…"
   ```

エージェントは **push のあと必ず** `gh pr view` で既存 PR を確認し、あれば **2→3→4→6** を実行してから新規 `gh pr create` を試みないこと。

## 最短（このリポジトリ）

```bash
make pr
```

中身は `gh pr create --fill` です。下書き用。**公開前に**上記「タイトル・説明文」に沿って `gh pr edit` で整える。

既に同じブランチに PR がある場合は `gh pr create` が失敗する。**既存 PR がある場合**の手順で `gh pr edit` により追記する。

## よく使うコマンド

| 目的 | コマンド |
|------|----------|
| 既存 PR の確認（番号・ベース・本文） | `gh pr view --json number,title,body,baseRefName,url` |
| 作成後にタイトル・本文を編集 | `gh pr edit`（現在ブランチの PR） |
| エディタでタイトル・本文を書く | `make pr` のあと、または `gh pr create` |
| ブラウザで開いて作成 | `make pr-web` |
| 下書き PR | `make pr-draft` |
| ベースブランチ指定 | `gh pr create --base <派生元> --fill`（`main` 固定にしない） |

## Cursor コマンド定義（エージェント用）

リポジトリの `.cursor/commands/` に次があります（エディタの Custom Commands から参照可能な場合があります）。

- `commit.md` — ステージ・分割コミットのガイド。`make commit` で `git commit` を起動
- `review.md` — 差分レビュー観点。`make review` → `gh pr view`
- `approve.md` — PR 承認。`make approve` → `gh pr review --approve`
- `push.md` — リモートへ push。`make push` → `git push -u origin HEAD`

## PR テンプレート

[`.github/pull_request_template.md`](../../.github/pull_request_template.md) が GitHub 上の「Open a pull request」で既定挿入される。CLI だけでは自動では入らないため、**本文は手動でテンプレ構造に合わせる**（上記「タイトル・説明文」参照）。

## トラブルシュート

- `gh: command not found` → `brew install gh`（macOS）
- 認証エラー → `gh auth login`
- リモートにブランチが無い → 先に `git push -u origin HEAD`
