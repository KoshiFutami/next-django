---
name: next-django-api-check
description: next-django の API 手動確認・Postman・CSRF・JSON エラー・スタブ認証の落とし穴。API 疎通や 403/404 の調査時に使う。
---

# next-django API 確認スキル

## Postman

- コレクション: `docs/postman/next-django-mvp.postman_collection.json`（MVP 全体の定義）
- 変数: `baseUrl`（例 `http://localhost:8000`）、`accessToken`（未実装の JWT 用。スタブ認証では空でよいことが多い）

## CSRF と POST

Django は `CsrfViewMiddleware` 有効時、ブラウザ以外からの POST で CSRF 不足だと **403** になる。

- 開発で一時的に `csrf_exempt` を付けている view がある場合は、**JWT や正規の CSRF 対応に移行したら外す**
- 同じパスに GET/POST を二重定義すると、意図しない view にルーティングされることがある。`urls.py` を確認する

## JSON エラー

- 一部のハンドラは `showcase/interface/error_handlers.py` で JSON を返す
- **`DEBUG=True` のとき、存在しない URL の 404 は Django のデバッグ用 HTML** のままになることがある。JSON 404 を確認するなら `DEBUG=False` でも試す

## レスポンスの日本語

- `json_response` は `ensure_ascii=False` で日本語をそのまま返す想定

## よくある失敗

1. **`OwnerProfile matching query does not exist`** — `seed_stub_owner` を実行していない、または `SHOWCASE_STUB_OWNER_ID` と DB の id が一致していない
2. **Empty reply / 接続エラー** — backend コンテナが落ちている、またはポート違い

## 疎通の最短

```bash
curl -s "http://localhost:8000/api/health/"
curl -s "http://localhost:8000/api/breeds/"
curl -s "http://localhost:8000/api/dogs/"
```
