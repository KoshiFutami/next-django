# HTTP API 一覧（案）

ベース URL は `http(s)://{host}/api`（本番では HTTPS）。  
認証が必要なエンドポイントは `Authorization: Bearer <access_token>` を想定（未実装の場合は「予定」とする）。

---

## 共通

| メソッド | パス | 認証 | 説明 |
|---------|------|------|------|
| GET | `/health/` | 不要 | ヘルスチェック（200、`{"status":"ok"}` 想定） |

---

## 認証・利用者（Owner）

Django `User` + `OwnerProfile` と整合させる。

| メソッド | パス | 認証 | 説明 |
|---------|------|------|------|
| POST | `/auth/register/` | 不要 | メール・パスワード・ニックネーム等で登録し、Owner を作成 |
| POST | `/auth/login/` | 不要 | ログイン、アクセストークン（＋必要ならリフレッシュ）を返す |
| POST | `/auth/logout/` | 要 | トークン失効（方式による） |
| GET | `/auth/me/` | 要 | 現在の Owner 情報（ニックネーム・メール・プロフィール画像キー等） |
| PATCH | `/auth/me/` | 要 | プロフィール更新（ニックネーム・画像など） |

---

## 犬種マスタ（Breed）

検索 UI のセレクトとタイムラインの `breed_code` フィルタ用。

| メソッド | パス | 認証 | 説明 |
|---------|------|------|------|
| GET | `/breeds/` | 不要 | `sort_order` 順の一覧（`code`, `name`, `sort_order`） |
| GET | `/breeds/{code}/` | 不要 | 単一取得（`code` は整数 PK） |

管理用に POST/PATCH/DELETE を付ける場合は **スタッフのみ**などポリシーを別途明記。

---

## 愛犬（Dog）

閲覧（GET）は認証なしの公開 API とし、作成・更新・削除（POST / PATCH / DELETE）はオーナー文脈が必要（現状は `SHOWCASE_STUB_OWNER_ID` のスタブ）。本番では公開範囲・個人情報の取り扱いを別途決めること。

| メソッド | パス | 認証 | 説明 |
|---------|------|------|------|
| GET | `/dogs/` | 不要 | 登録済み犬の一覧（オーナーで絞らない） |
| POST | `/dogs/` | 要 | 犬の登録（`breed_code` はマスタ参照。スタブ Owner に紐づく） |
| GET | `/dogs/{dog_id}/` | 不要 | 詳細（ID が存在すれば返す） |
| PATCH | `/dogs/{dog_id}/` | 要 | 更新（本人の犬のみ。スタブ Owner） |
| DELETE | `/dogs/{dog_id}/` | 要 | 削除（本人の犬のみ。スタブ Owner） |

**DELETE `/dogs/{dog_id}/`**

- 成功時は **204 No Content**（**レスポンス本文なし**）。該当しない ID や他人の犬は **404**、`{"code":"not_found","message":"..."}` 形式の JSON。

**GET `/dogs/`（実装済み・認証不要）**

- **POST / PATCH / DELETE** のみ、現在の Owner を `SHOWCASE_STUB_OWNER_ID`（環境変数、未設定時は `00000000-0000-0000-0000-000000000001`）で固定。JWT 導入後に差し替え。
- レスポンス例:

```json
{
  "items": [
    {
      "id": "uuid",
      "name": "ポチ",
      "birth_date": "2021-05-01",
      "weight": 8.0,
      "color": "茶",
      "gender": "male",
      "breed_code": 1,
      "profile_image_key": null,
      "created_at": "2024-06-01T00:00:00+00:00"
    }
  ]
}
```

---

## アピール投稿・タイムライン（予定）

`ShowcasePost` 等を追加するときの置き場（仕様は未実装なら「案」のまま）。

| メソッド | パス | 認証 | 説明 |
|---------|------|------|------|
| GET | `/posts/` | 不要または任意 | 公開タイムライン。クエリ `breed_code`（必須要件なら仕様で固定） |
| POST | `/posts/` | 要 | 自分の犬に紐づく投稿作成（画像 multipart 等） |
| GET | `/posts/{post_id}/` | 不要または任意 | 投稿詳細 |

---

## メモ

- **バージョン**: 将来 `/api/v1/` に切り出す場合は、上記パスを `v1` 配下に移す。
- **エラー形式**: 統一 JSON（例: `{"detail": "..."}` または `{"code": "...", "message": "..."}`）を別紙で決めるとフロントと相性がよい。
- **画像**: アップロードは `POST /uploads/` のように分離するか、各リソースの `multipart` に含めるかを実装時に決定。
