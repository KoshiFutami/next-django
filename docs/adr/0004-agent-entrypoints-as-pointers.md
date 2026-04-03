# 0004. エージェント向けエントリ（AGENTS.md / CLAUDE.md）をポインタとして保つ

日付: 2026-04-03

## 状態

Accepted

## 文脈（Context）

- エージェントはリポジトリ内テキストを等しく権威ある情報として読むため、**長い説明は腐敗しやすく、コンテキストも浪費**する。
- [AGENTS.md / CLAUDE.md をポインタとして設計する](https://nyosegawa.com/posts/harness-engineering-best-practices-2026/#3%3A-agents.md-%2F-claude.md%E3%82%92%E3%83%9D%E3%82%A4%E3%83%B3%E3%82%BF%E3%81%A8%E3%81%97%E3%81%A6%E8%A8%AD%E8%A8%88%E3%81%99%E3%82%8B) に沿い、**ルーティング・禁止の参照・最低限のコマンド**に絞る。
- Cursor は `AGENTS.md`、Claude Code は `CLAUDE.md` を読みやすいが、**重複を避け**共通部分は `AGENTS.md` に一本化する。

## 決定（Decision）

- **AGENTS.md** をリポジトリ共通の短いポインタとする（目安 **50 行前後**）。詳細は ADR、`.cursor/skills/`、`.cursor/rules/`、`docs/api.md` へリンクする。
- **CLAUDE.md** は Claude Code 専用の数行にし、**必ず AGENTS.md を読む**旨と Hooks（`.claude/`）・ ADR 0003 へのポインタのみを書く。
- 技術スタックの解説や冗長なスタイルガイドはエントリに書かない（`package.json` / Ruff / ルールファイルに委ねる）。

## 結果（Consequences）

- 良い影響: 指示の先頭バイアスを減らし、真実のソース（コード・テスト・ADR）へ誘導しやすい。
- 負債: エントリを更新し忘れるとリンク切れになるが、**壊れたポインタは操作で気づきやすい**（記事の副次効果）。
- フォローアップ: ドメイン別に `backend/showcase/AGENTS.md` などを足す場合は、ルートからリンクする。
