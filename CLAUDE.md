# Claude Code

共通のルーティング・禁止事項は **[AGENTS.md](AGENTS.md)** に集約している（短いポインタ）。**先に AGENTS.md を読んでから**タスクに入ること。

## Claude 専用

- **Hooks**: `.claude/settings.json`（PreToolUse: 品質設定の編集ブロック、PostToolUse: `backend/**/*.py` に Ruff）
- **詳細**: [ADR 0003](docs/adr/0003-python-quality-via-hooks-and-ci.md)

## 参考

- [AGENTS.md / CLAUDE.md をポインタとして設計する](https://nyosegawa.com/posts/harness-engineering-best-practices-2026/#3%3A-agents.md-%2F-claude.md%E3%82%92%E3%83%9D%E3%82%A4%E3%83%B3%E3%82%BF%E3%81%A8%E3%81%97%E3%81%A6%E8%A8%AD%E8%A8%88%E3%81%99%E3%82%8B)（理想はエントリ各 ~50 行以下）
