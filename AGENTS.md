# next-django — エージェント向けメモ

このリポジトリは **Django（backend）+ Next.js（frontend）** のモノレポ。API は `/api/` 配下。

## 構成

- `backend/` — Django 5 + DRF 利用可。アプリ本体は `showcase/`
- `frontend/` — Next.js（App Router）
- `docker-compose.yml` — `db`（Postgres）、`backend`、`frontend`

## アーキテクチャ（薄い DDD）

- **リポジトリ境界**: `showcase/domain/repositories.py`（Protocol）→ `showcase/infrastructure/django_repositories.py`（実装）
- **ユースケース**: `showcase/application/`（オーケストレーションを薄く）
- **HTTP 境界**: `showcase/interface/`（views、urls、serializers 的な JSON 整形、`responses.py`）
- **ドメイン**: `showcase/domain/` — ルールが増えたところから厚くする。最初からフルDDDにしない

ORM モデルは `showcase/models.py`。

## ローカル運用

- 起動: `make up`
- backend ログ: `docker compose logs -f backend`（または `make logs` で全体）
- DB: `make psql`（コンテナ内 `psql`）
- マイグレーション: `make migrate`
- テスト: `make test`（コンテナ内 `pytest`）

コード変更は backend がボリュームマウントされているため、通常 **コンテナ再起動不要**（依存追加や Dockerfile 変更時は再ビルド）。

## データ投入（管理コマンド）

コンテナ起動後、backend 内で実行:

- `python manage.py seed_breeds` — 犬種マスタ
- `python manage.py seed_stub_owner` — スタブ Owner（`SHOWCASE_STUB_OWNER_ID` に対応する `OwnerProfile`）

例: `docker compose exec backend python manage.py seed_stub_owner`

## 開発用スタブ認証

`config/settings.py` 参照:

- `SHOWCASE_STUB_OWNER_ID` — 現在の Owner として扱う UUID（環境変数で上書き可）
- `SHOWCASE_STUB_OWNER_EMAIL` — スタブ用ユーザーのメール（`seed_stub_owner` で使用）

犬の登録などで `OwnerProfile matching query does not exist` が出たら、先に `seed_stub_owner` を実行する。

## API / ドキュメント

- 人向け一覧: `docs/api.md`
- Postman: `docs/postman/`（`next-django-mvp.postman_collection.json` など）

## GitHub / PR

- [GitHub CLI](https://cli.github.com/)（`gh`）を入れ、`gh auth login` 済みであること
- ブランチを push したあと: `make pr`（`gh pr create --fill`）。下書きは `make pr-draft`、ブラウザは `make pr-web`
- ローカル: `make commit`（ステージ済みのみ `git commit`）、`make push`（`git push -u origin HEAD`）
- コミットメッセージは **日本語**（詳細は `.cursor/commands/commit.md`）
- `gh` 利用: `make review`（`gh pr view`）、`make approve`（`gh pr review --approve`）
- PR の本文テンプレート: `.github/pull_request_template.md`
- Cursor 用コマンド定義: `.cursor/commands/commit.md` など（4 ファイル）
- エージェント向け手順: `.cursor/skills/github-pr/SKILL.md`

## 細かいコーディング規約

エディタ・エージェント向けの詳細ルールは **`.cursor/rules/`** の `.mdc` に置く。ここは要約のみ。
