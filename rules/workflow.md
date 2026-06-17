# Development Workflow Rules

- Test after code changes: `python -m pytest tests/ -v -k "relevant_keyword"`
- Commit only after passing tests
- When completing a task: update `notes/TODO.md` (or `docs/TODO.md` if the project uses legacy `docs/`; check off item)
- When completing a topic: append results to relevant `notes/LOGS/log_*.md` (or `docs/LOGS/log_*.md` for legacy)
- When discovering a new issue: add entry to `notes/ISSUES.md` (or `docs/ISSUES.md` for legacy)
- When resolving an issue: delete the entry from `notes/ISSUES.md` (or `docs/ISSUES.md` for legacy)
- Directory resolution (`notes/` default vs `docs/` legacy): see「標準ドキュメント構成」below
- Commit message: English, imperative mood, Conventional Commits format
- Main branch: `main`

## 標準ドキュメント構成

ドキュメント基底ディレクトリ `<notes>` の解決順序:

1. `notes/` が存在 → `notes/` (デフォルト)
2. `docs/` が存在 → `docs/` (legacy / フォーク)
3. どちらも無し → project-level CLAUDE.md の指定, なければ `notes/` を新規作成

| ファイル | 役割 | 運用ルール |
|---|---|---|
| `<notes>/TODO.md` | タスクリスト | 完了項目は `[x]` に. 新規タスクを追記 |
| `<notes>/LOGS/` | 作業・実験記録 (トピック別 `log_<topic>.md`) | append-only. 過去の記録は編集しない |
| `<notes>/ISSUES.md` | 未解決の技術課題 | 解決済みは削除 (アーカイブしない) |
| `<notes>/PLAN.md` | 設計方針・ロードマップ | 設計判断が変わった場合のみ更新 |
