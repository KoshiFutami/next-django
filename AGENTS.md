# next-django — エージェント向け（ポインタ）

モノレポ: **Django（`backend/showcase`）+ Next.js（`frontend`）**。HTTP API は `/api/` 配下。

詳細な「現状説明」やスタイルの重複は書かない。**コード・テスト・ADR・リンター設定が真実**。[ポインタ型 AGENTS の意図](https://nyosegawa.com/posts/harness-engineering-best-practices-2026/#3%3A-agents.md-%2F-claude.md%E3%82%92%E3%83%9D%E3%82%A4%E3%83%B3%E3%82%BF%E3%81%A8%E3%81%97%E3%81%A6%E8%A8%AD%E8%A8%88%E3%81%99%E3%82%8B)

## まず読む

- **設計の「なぜ」**: [docs/adr/](docs/adr/)（有効は `Accepted`。[薄い DDD](docs/adr/0002-thin-ddd-for-showcase-backend.md)）
- **Python 品質・Claude Hooks**: [ADR 0003](docs/adr/0003-python-quality-via-hooks-and-ci.md)
- **エントリポイント方針（本ファイルの短さ）**: [ADR 0004](docs/adr/0004-agent-entrypoints-as-pointers.md)
- **API 一覧**: [docs/api.md](docs/api.md) / Postman は [docs/postman/](docs/postman/)

## ルーティング（よく使うコマンド）

| 目的 | コマンド |
|------|----------|
| 起動 | `make up` |
| ログ | `make logs` / `docker compose logs -f backend` |
| テスト | `make test` |
| DB | `make psql` / `make migrate` |
| Backend lint | `pip install -r backend/requirements-dev.txt` → `make lint-backend` |
| pre-commit | `make pre-commit-install` |

シード（コンテナ起動後）: `docker compose exec backend python manage.py seed_breeds` / `seed_stub_owner`

## レイヤー（置き場所だけ）

`showcase/` のディレクトリと ADR 0002 が境界の真実。**domain** → **application** → **infrastructure** → **interface**。ORM は `showcase/models.py`。

## 禁止・落とし穴

- リンター・pre-commit・関連 CI・`.claude` フックを弱めて赤を消さない（Claude Code は PreToolUse でブロック。変更はエディタ・通常 PR）。
- `OwnerProfile matching query does not exist` → 先に `seed_stub_owner`（スタブ ID は `config/settings.py`）。

## PR / スキル / ルール

- `gh` + `make pr` / `make push`。手順: [.cursor/skills/github-pr/SKILL.md](.cursor/skills/github-pr/SKILL.md)
- 開発フロー全体: [.cursor/skills/next-django-dev/SKILL.md](.cursor/skills/next-django-dev/SKILL.md)
- コミットメッセージは **日本語**: [.cursor/commands/commit.md](.cursor/commands/commit.md)
- Python の細目: **`.cursor/rules/*.mdc`**（配置されていれば。なければ既存コードに合わせる）

**Claude Code** 利用時はルートの [CLAUDE.md](CLAUDE.md) も読む。
