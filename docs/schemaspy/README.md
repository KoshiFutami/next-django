# SchemaSpy（DB スキーマ可視化）

`public` スキーマを HTML（ER 図・テーブル一覧）に出力します。**このディレクトリの生成物は Git で管理**し、`.github/workflows/schemaspy.yml` がマイグレーション後に SchemaSpy を実行します。

## ローカル

- 前提: `make up` などで `db` が起動していること（マイグレーション済み推奨）。
- 実行: ルートで `make schemaspy` → `docs/schemaspy/index.html` を開く。

接続値は `docker-compose.yml` の `db` サービス（`showcase` / `showcase` / DB 名 `showcase`）に合わせています。DB 種別は PostgreSQL 16 互換のため **`-t pgsql11`** を使っています（従来の `pgsql` だと `datlastsysoid` などでエラーになります）。

## CI（GitHub Actions）

**`push` / `pull_request` は** `backend/**/migrations/**/*.py` または `.github/workflows/schemaspy.yml` に差分があるときだけ起動します（それ以外の PR ではジョブ自体が走りません）。**`workflow_dispatch`** は常に手動実行できます。

- **push 先が `main` のとき**: 生成結果に差分があれば `github-actions[bot]` がコミットしてプッシュします。
- **pull request のとき**: 生成結果がブランチ上の `docs/schemaspy` と一致しないと失敗します。マイグレーションを変えたらローカルで `make schemaspy` してからコミットしてください。
- 手動再実行: Actions タブから **SchemaSpy** を **Run workflow**。ブランチが **`main`** のときは、差分があれば bot がコミット・プッシュします。
