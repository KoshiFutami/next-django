---
name: next-django-dev
description: next-django モノレポの開発手順・薄いDDD・Docker/Makefile・シードコマンド。backend/frontend の変更時に参照する。
---

# next-django 開発スキル

## いつ使うか

- このリポジトリで機能追加・バグ修正・リファクタをするとき
- レイヤー配置や「どこに何を書くか」を揃えたいとき

## アーキテクチャ（薄い DDD）

1. **永続化の抽象**: `backend/showcase/domain/repositories.py`（`Protocol`）
2. **実装**: `backend/showcase/infrastructure/django_repositories.py` と `mappers.py`
3. **ユースケース**: `backend/showcase/application/*.py` — リポジトリを組み合わせるだけに近づける
4. **HTTP**: `backend/showcase/interface/` — view、URL、JSON 用の dict 整形（`serializers.py` 的な関数）、`responses.py` の `json_response`
5. **ドメイン**: `backend/showcase/domain/` — ルールが複雑になったら factory メソッド・値オブジェクト・例外を足す

View にビジネスロジックを溜めない。ORM を直接 view から触らない方針を基本とする。

## Docker / Make

- ルートで `make up` → `make psql` / `make test` / `make migrate`
- backend のログ: `docker compose logs -f backend`
- DB ホスト名は **コンテナ間で `db`**（ホストマシンからは `localhost:5432`）

## シード

```bash
docker compose exec backend python manage.py seed_breeds
docker compose exec backend python manage.py seed_stub_owner
```

犬 API を試す前にスタブ Owner が無いと DB エラーになる。`SHOWCASE_STUB_OWNER_ID` は `config/settings.py` で定義。

## 変更時の注意

- `requirements.txt` や `Dockerfile` を変えたらイメージ再ビルドが必要
- Python の import は `showcase.` から（`backend.showcase` のような誤パスにしない）

## PR を出すとき

- `git push` 後に `make pr`（要 `gh`）。詳細は `github-pr` スキル参照。
