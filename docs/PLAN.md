# Plan

## project-team スキル

### 目的

LLMエージェント3体（Research, Engineer, Analyst）を活用し、ロボット学習プロジェクトを
Phase 0〜8 のフェーズ駆動で推進するオーケストレーションスキルを構築する。

### 設計文書

`project-team-bestpractice.md` に全設計判断を集約済み。

### 実装方針

1. **エージェント定義** — 各エージェントは実行モード + 批評モード（相互批評のみ、自己批評禁止）
2. **フェーズ定義** — タスク生成テンプレートとして機能。固定タスクリストではなく動的生成
3. **SKILL.md** — タスクキューマネージャー。セッション・チェックイン方式で運用
4. **品質ゲート** — 相互批評 + 外部検証（pytest/ruff/pyright）の二重構造
5. **状態永続化** — `docs/LOGS/log_project_team.md` にフェーズ・タスクキューを記録

---

## ユーザーレベル設定の汎用化（完了）

### 目的

`~/.claude/` 配下のスキルと CLAUDE.md を、特定プロジェクトに依存しない汎用的な定義に整理する。

### 方針

1. **スキル** — プロジェクト固有のパスやブランチ名をハードコードしない。役割定義はスキル側に持ち、具体的なパスはプロジェクトの CLAUDE.md に委ねる
2. **CLAUDE.md** — ユーザーレベルには全プロジェクト共通のルール（コーディング規約、ワークフロー、標準ドキュメント構成）のみ残す。プロジェクト固有の内容（コマンド、参照先、注意事項）は各プロジェクトの CLAUDE.md に移動
3. **スクラッチプロジェクト** — ユーザーレベル CLAUDE.md にスクラッチプロジェクトでの標準ドキュメント構成（docs/TODO.md, docs/LOGS/, docs/ISSUES.md, docs/PLAN.md）を明記し、新規プロジェクト立ち上げ時の指針とする

---

## 挙動制御フレームワーク

### 目的

Claude の RLHF 由来デフォルト挙動（scope expansion、taxonomy ハルシネーション、
日本語スタイル違反等）を、CLAUDE.md directive と Stop hook の二段防御で抑制する。
arXiv:2511.13972 の実証では directive 単独で 56% 削減にとどまるため、
決定論的な hook で残り 44% を捕捉する設計。

### 方針

1. **層別防御** — 予防（CLAUDE.md directive）+ 事後検査（Stop hook）の組合せ。
   全会話に効くシンプルな構成を優先し、UserPromptSubmit hook や subagent
   systemPrompt override は将来の拡張として位置づける
2. **単一目的 hook** — 検出対象ごとに hook を分離（scope-check / taxonomy-check）。
   ログも分離して個別に偽陽性率を評価可能にする。共通の transcript parsing は
   3 つ目の hook が必要になるまで重複を許容（YAGNI）
3. **block mode 運用** — warn-only での試運用は精度確認時のみ。本運用では
   block JSON を返して再生成を強制し、`stop_hook_active` フラグで無限ループを防止
4. **観測駆動の改良** — 偽陽性率を `*-violation.log` から定期レビューし、
   キーワードや検出ロジックを調整。試行錯誤の根拠は `docs/LOGS/log_behavior_control.md`
   に追記
