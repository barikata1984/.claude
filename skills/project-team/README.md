# project-team スキル

3体のAIエージェント（Research / Engineer / Analyst）を活用し、
ロボット学習の研究・開発プロジェクトをフェーズ単位で管理するスキル。

## コマンド

| コマンド | 説明 |
| ---- | ---- |
| `/project-team init` | 新プロジェクト初期化（academic / startup モード選択） |
| `/project-team` | チェックイン: 残タスク確認、次のアクション提案 |
| `/project-team phase N` | Phase N に移行しタスクを生成 |
| `/project-team status` | 現在のフェーズ・進捗・ループ回数を表示 |

## 典型的な使い方

### プロジェクト開始

```
/project-team init
→ モード選択（academic / startup）
→ プロジェクト概要を入力
→ 状態ファイルが docs/LOGS/log_project_team.md に作成される
```

### 日常のセッション

```
/project-team
→ 状態ファイルから現在地を復元
→ 残タスクが提示される
→ タスクを選択 → エージェントが自動起動
→ 結果を確認、次のタスクへ or セッション終了
```

### フェーズ遷移

```
/project-team phase 3
→ Phase 2 の完了条件をチェック
→ Phase 3 のタスクを自動生成（実験計画書から）
→ タスクリストを確認・承認
```

## プロジェクトフェーズ

| Phase | 内容 | 主担当 |
| ----- | ---- | ------ |
| 0 | 着想・問題定義 | 人間のみ |
| 1 | 先行研究 / 市場調査 | Research |
| 2 | 仮説構築 / 実験設計 | 人間 + Analyst |
| 3 | 実装 / プロトタイプ | Engineer |
| 4 | 実験・検証 | 人間 + `/sweep run` |
| 5 | 分析・考察 | Analyst |
| 6 | 出力（論文 / 製品） | Research + Engineer |
| 7 | レビュー / 改善 | 3体で相互批評 |
| 8 | 公開・展開 | 人間のみ |

## エージェント構成

| エージェント | 実行モード | 批評モード |
| ---- | ---- | ---- |
| **Research** | 論文調査・執筆 | 論文ドラフトレビュー、コード-論文整合性 |
| **Engineer** | 実装・インフラ構築 | コードレビュー、統計コード検証 |
| **Analyst** | 実験設計・統計分析 | 統計手法・主張-証拠レビュー |

自己批評は禁止。必ず異なるエージェントが相互批評する。

## 状態管理

- 状態ファイル: `docs/LOGS/log_project_team.md`（プロジェクト側に配置）
- セッション間で永続化: フェーズ、タスクキュー、ループ回数を保持
- 承認ゲート: Phase 2→3、5→6、7→8 は人間の承認が必要

## 関連スキルとの連携

| スキル | 連携タイミング |
| ---- | ---- |
| `/literature-survey` | Phase 1 で大規模調査が必要な場合 |
| `/sweep run` / `/sweep analyze` | Phase 4-5 の実験・分析 |
| `/fault-tree-debug` | Phase 3-5 でバグ発生時 |
| `/reference-verify` | Phase 6 で引用の実在性チェック |
| `/commit` | フェーズ完了時のマイルストーンコミット |

## 設計文書

- ベストプラクティス: `skills/project-team/docs/bestpractice.md`
- 設計ログ: `docs/LOGS/log_project_team_skill.md`
