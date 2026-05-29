# Claude Code ユーザーレベル設定

<!-- 実験中: karpathy ガイドライン + Git/ドキュメント構成のみ試用。他セクションは一旦解除。
     復元する場合は `git checkout CLAUDE.md`（直前コミットに従来版あり）。 -->

@~/.claude/plugins/marketplaces/karpathy-skills/CLAUDE.md

## Git Workflow

- **Commit format**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`)
- **Main branch**: `main`

## 標準ドキュメント構成

ドキュメント基底ディレクトリ `<notes>` の解決順序:

1. `notes/` が存在 → `notes/`（デフォルト）
2. `docs/` が存在 → `docs/`（legacy / フォーク）
3. どちらも無し → project-level CLAUDE.md の指定、なければ `notes/` を新規作成

| ファイル | 役割 | 運用ルール |
|---|---|---|
| `<notes>/TODO.md` | タスクリスト | 完了項目は `[x]` に。新規タスクを追記 |
| `<notes>/LOGS/` | 作業・実験記録（トピック別 `log_<topic>.md`） | append-only。過去の記録は編集しない |
| `<notes>/ISSUES.md` | 未解決の技術課題 | 解決済みは削除（アーカイブしない） |
| `<notes>/PLAN.md` | 設計方針・ロードマップ | 設計判断が変わった場合のみ更新 |
