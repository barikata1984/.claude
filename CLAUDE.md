# Claude Code ユーザーレベル設定

## ワークフロー

- 3ステップ以上のタスクは Plan Mode から開始せよ
- 調査・分析タスクはサブエージェントに委譲し、メインコンテキストを保護せよ
- 実装完了を自己宣言するな。テスト実行・差分確認・ログ確認で動作を実証せよ
- バグ報告を受けたらまずログ・エラー・テストから自力調査せよ。質問は調査後に
- セッション終了時は /log-progress で進捗を記録せよ

## モデル・effort・context の使い分け

Max サブスク前提。タスク種別ごとに適切なモデル/effort/context を選択し、Opus 枠と週次制限を浪費しない。

- **デフォルト**: Opus 4.7 + effort `xhigh`
- **Plan → 実装の二段構え**: `/model opusplan`（Plan 時 Opus、実行時 Sonnet 自動切替）
- **通常の実装タスク**: Sonnet 4.6 + `medium`（既知パターン・明確な仕様の場合）
- **単純タスク**（型チェック・機械的置換・ログ解析・分類）: Haiku 4.5 + `low`
- **難問と確認済みの場合のみ**: `/effort max`（効用逓減に注意）
- **1M context**: 大規模リファクタ・全体設計の開始時のみ `/model opus[1m]` で明示有効化。短時間タスクは 200K で十分（切替時のキャッシュ再構築コストを避ける）
- **コンテキスト 600K 超過**: `/compact` で要約圧縮
- **トピック切替時**: `/clear` で完全リセット
- `/context` で残量を定期確認。Opus 枠超過時は Sonnet へ自動フォールバックされるため、意図せぬモデル降格に注意

## 調査・回答ポリシー

- ユーザーの質問・要求に回答する際、内部知識だけで即答するな。必ず WebSearch / WebFetch で最新の一次情報を取得せよ
- 検索結果をそのまま転記するな。論理構造の把握 → 推論・演繹 → ベストプラクティスの導出 のプロセスを経て回答せよ
- 回答の根拠となるソース（URL・文献）を明示せよ
- 「可能性がある」「疑いがある」と感じた時点で、報告せず先に検証せよ。コード挙動なら実行・ログ確認、仕様ならドキュメント参照、エラー原因なら該当コード読み込みと再現で確定させる。検証手段が尽きた場合のみ、仮説であることを明示して報告してよい

## コーディング規約

- **Formatter**: `ruff format`
- **Linter**: `ruff check`
- **Type hints**: Python 3.10+ annotations required
- **Line length**: 100 characters
- **Import order**: stdlib → third-party → local (enforced by ruff isort)
- **Docstrings**: Google style, only for non-obvious functions

## Git Workflow

- **Commit format**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`)
- **Main branch**: `main`

## 標準ドキュメント構成

スクラッチプロジェクトでは以下の構成を `docs/` 配下に作成する。
フォーク・既存プロジェクトでは、既存の構成に従う。

| ファイル | 役割 | 運用ルール |
|---|---|---|
| `docs/TODO.md` | タスクリスト | 完了項目は `[x]` に。新規タスクを追記 |
| `docs/LOGS/` | 作業・実験記録（トピック別 `log_<topic>.md`） | append-only。過去の記録は編集しない |
| `docs/ISSUES.md` | 未解決の技術課題 | 解決済みは削除（アーカイブしない） |
| `docs/PLAN.md` | 設計方針・ロードマップ | 設計判断が変わった場合のみ更新 |
