# Development Workflow Rules

- Test after code changes: `python -m pytest tests/ -v -k "relevant_keyword"`
- Commit only after passing tests
- Session records: run `/log-progress` (or `/wrap-up-session` at session end) — it writes session minutes to `<notes>/LOGS/YYYY-MM-DD_<topic>.md` and syncs `TODO.md` / `ISSUES.md`
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
| `<notes>/LOGS/YYYY-MM-DD_<topic>.md` | セッション議事録 (一次記録): Topic / History / Decisions / Changes / Open Items. History は因果順の散文, 決定の理由・却下案・失敗はここに載る | メインエージェントが /log-progress で執筆. 当該セッション中は更新可, セッション終了後は凍結 |
| `<notes>/TODO.md` | 薄い状態インデックス: 未完了タスク | 1 項目 1–2 行 + 発生元議事録へのリンク. 完了は `[x]` |
| `<notes>/ISSUES.md` | 薄い状態インデックス: 未解決課題 | 1 項目 1–2 行 + リンク. 解決済みは削除 (アーカイブしない) |
| `<notes>/DECISIONS.md` | 決定台帳: 全決定を 1 行ずつ蓄積 | 行 = 日付 + 採用案 / 却下: 案名 — 承認区分 + 議事録リンク. 覆された決定は行を更新 (削除しない) |
| `<notes>/LOGS/log_*.md` | 旧トピック別ログ (凍結) | 追記・編集禁止. 参照のみ. スキル固有台帳 (`log_sweep.md`, `gpu_monitor_*.csv` 等) は各スキルの管轄で対象外 |
| `<notes>/PLAN.md` | 廃止 | 既存ファイルは残置. 更新しない |
