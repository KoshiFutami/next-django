# Architecture Decision Records（ADR）

設計上の重要な判断を、**文脈・決定・結果**として短く残すための記録。

## 置き場所

- このディレクトリに `NNNN-kebab-case-title.md` で1判断1ファイル。
- 番号は4桁ゼロ埋め、**時系列順**（古いほど小さい番号）。

## いつ書くか

次のようなときに ADR を検討する。

- レイヤ構成・パッケージ境界を変える
- 認証・永続化・API 形式など、差し替えコストが高い選択をする
- 「なぜこの技術／このやり方か」を後から説明したくなる

## 書き方

1. [template.md](template.md) をコピーして新規ファイルを作る。
2. **Status** は `Proposed` → 合意後 `Accepted`。廃止・置換時は `Deprecated` / `Superseded by NNNN`。
3. **Context** は事実と制約。**Decision** は「何を選んだか」1つに絞る。**Consequences** はメリット・デメリット・フォローアップ。

## 一覧

| 番号 | タイトル | 状態 |
|------|----------|------|
| [0001](0001-use-architecture-decision-records.md) | ADR を採用する | Accepted |
| [0002](0002-thin-ddd-for-showcase-backend.md) | showcase バックエンドに薄い DDD を採用する | Accepted |
| [0003](0003-python-quality-via-hooks-and-ci.md) | Python 品質を pre-commit・CI・Claude Code フックで担保する | Accepted |
| [0004](0004-agent-entrypoints-as-pointers.md) | エージェント向けエントリ（AGENTS.md / CLAUDE.md）をポインタとして保つ | Accepted |
| [0005](0005-plan-then-execute-with-tests.md) | エージェント作業で計画と実行を分離し完了はテストで検証する | Accepted |

（新規 ADR を追加したらこの表を更新する。）
