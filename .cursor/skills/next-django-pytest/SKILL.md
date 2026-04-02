---
name: next-django-pytest
description: next-django の pytest / pytest-django テスト規約。命名・fixture・APIテスト・DBテストの実践ルール。
---

# next-django pytest スキル

## いつ使うか

- `backend/` のテストを新規追加・修正するとき
- API テストの書き方を揃えたいとき
- バグ修正時に再発防止テストを追加するとき

## 基本方針

- テストは **振る舞い** を検証する（実装詳細への過剰依存を避ける）
- 1 テスト 1 意図。失敗理由がすぐ分かる粒度に分ける
- 既存の JSON エラー仕様（`code` / `message`）を優先して assert する

## 命名ルール

- ファイル名: `test_*.py`
- 関数名: `test_<対象>_<条件>_<期待結果>`
  - 例: `test_dogs_post_invalid_birth_date_returns_400`
- 用語は API 仕様に合わせる（`method_not_allowed`, `bad_request` など）

## テスト構造（AAA）

- Arrange: データ準備（Owner/Breed など）
- Act: API 呼び出し / UseCase 実行
- Assert: ステータス、レスポンス、DB 反映

必要なら空行で 3 ブロックを分ける。コメントは最小限でよい。

## pytest-django の使い方

- DB を触るテストには `@pytest.mark.django_db` を付ける
- スタブ認証前提のテストでは `@override_settings(SHOWCASE_STUB_OWNER_ID=...)` を使う
- 時刻・UUID はテスト内で明示して不安定さを避ける

## API テストの作法（このリポジトリ向け）

- Django `Client()` で `/api/...` を叩く
- JSON POST は `data=json.dumps(body)` と `content_type="application/json"`
- 最低限、次を検証する
  - HTTP ステータス（200/201/400/403/404/405 など）
  - `res.json()["code"]`（エラー時）
  - 主要フィールド（`name`, `breed_code` など）
  - 必要なら DB 反映（`Model.objects.filter(...).exists()`）

## fixture / ヘルパー

- 同一ファイル内で複数テストに使う準備処理は小さなヘルパー関数へ
  - 例: `_stub_owner_and_breed()`
- 複数ファイルで共通化したくなったら `conftest.py` に fixture 化
- fixture は「作るデータ」を返す。副作用が分かりにくい抽象化は避ける

## parametrize の目安

- 入力バリエーションが同じ検証ロジックを共有する場合に使う
- 失敗時に何ケース目か分かる値を入れる

## 避けること

- 実装内部（private 関数、途中変数）を直接 assert する
- 1 テストで複数シナリオをまとめる
- 不要なモックを多用する（DB/API レイヤでは実データ優先）
- 期待値に `datetime.now()` など非決定的な値をそのまま使う

## 最低テスト観点（PR 時）

変更タイプごとに最低 1 ケースを追加する。

- 機能追加: 正常系 + 代表的な異常系
- バグ修正: 再現テスト + 修正後成功テスト（または失敗しないこと）
- バリデーション変更: 境界値 / 不正値

## 実行コマンド

ローカル（Docker）:

```bash
make test
# または
cd backend && pytest -q
```

CI は `.github/workflows/backend-tests.yml` で `pytest -q` を実行。

## レビュー時チェックリスト

- [ ] テスト名で意図が分かる
- [ ] DB 利用時に `django_db` が付いている
- [ ] API エラー時に `code` を検証している
- [ ] 変更の主目的に対して、正常系と異常系のどちらかが欠けていない
- [ ] テストが順序依存・時刻依存になっていない
