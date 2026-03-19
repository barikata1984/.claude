# Skills 汎用化ログ

## 2026-03-19: スキル定義の調査と修正開始

### 調査対象
- commit, push, commit-and-push, log-progress, wrap-up-session

### 発見した問題

1. **commit/push に `ros-o` がハードコード** — 特定プロジェクトのメインブランチ名が埋め込まれており、汎用スキルとして不適切
2. **log-progress にファイルパスがハードコード** — `docs/TODO.md`, `docs/LOGS/`, `docs/ISSUES.md`, `docs/PLAN.md` が固定。フォークプロジェクト等で成立しない
3. **log-progress の参照処理ルール** — `.claude/rules/references.md` は研究プロジェクト固有
4. **ユーザーレベル CLAUDE.md にプロジェクト固有の内容が混在** — 検証コマンド、コンテナ環境、参照先、注意事項が osx_ose_for_learning_manipulation 固有

### 実施した修正
- commit/SKILL.md: `ros-o` への警告ルールを削除
- push/SKILL.md: `ros-o` への特別処理（警告・確認・force push 禁止）を削除

### 議論と方針決定
- ブランチ保護は必要なプロジェクトでプロジェクトレベルの CLAUDE.md に個別定義する
- log-progress は役割定義をスキルに残しつつ、パス解決は CLAUDE.md に委ねる方針に
- ユーザーレベル CLAUDE.md を汎用化し、スクラッチプロジェクトの標準ドキュメント構成を明記する

### 追加修正
- log-progress/SKILL.md: パスのハードコードを除去。CLAUDE.md からのパス解決 + ファイルが存在しなければスキップする設計に変更。参照処理は `.claude/rules/references.md` が存在する場合のみ適用に緩和
- CLAUDE.md: プロジェクト固有の内容（コマンド、コーディング規約の一部、注意事項、コンテナ環境、参照先）を `~/_CLAUDE.md` に退避。汎用的な内容のみ残し、「標準ドキュメント構成」セクションを新設
- wrap-up-session/SKILL.md: 確認の結果、変更不要

### 残作業
- `~/_CLAUDE.md` の内容を対象プロジェクトの CLAUDE.md に配置する（対象プロジェクトでの作業時に実施）
