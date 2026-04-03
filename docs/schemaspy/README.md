# SchemaSpy（DB スキーマ可視化）

`public` スキーマを HTML（ER 図・テーブル一覧）に出力します。**生成ファイルは Git に含めず**、GitHub Actions が **GitHub Pages** に公開します（リポジトリの差分を膨らませないため）。

## 公開 URL（GitHub Pages）

1. リポジトリの **Settings → Pages**
2. **Build and deployment** で **Source** を **GitHub Actions** にする（初回のみ）
3. デプロイ後、画面上に表示される URL（例: `https://<owner>.github.io/<repo>/`）から `index.html` に相当するトップを開く

ワークフロー: `.github/workflows/schemaspy.yml`（`main` へマイグレーション関連の push、または手動 **Run workflow**）。

`main` への **push** でデプロイが終わると、マージコミットや squash メッセージから拾った **PR に GitHub Pages の URL をコメント**します（直接 `main` へ push しただけで PR が無い場合はコメントしません）。

## ローカル

- 前提: `make up` などで `db` が起動していること（マイグレーション済み推奨）。
- 実行: ルートで `make schemaspy` → `docs/schemaspy/index.html` をブラウザで開く（生成物は `.gitignore` 対象）。

接続値は `docker-compose.yml` の `db` サービス（`showcase` / `showcase` / DB 名 `showcase`）に合わせています。PostgreSQL 16 互換のため **`-t pgsql11`** を使っています。
