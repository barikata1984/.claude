# project-team スキル 設計ログ

## 2026-03-22: 設計フェーズ完了

### 成果物

- `project-team-bestpractice.md` — チーム構成・運用ベストプラクティス文書（全6章）
- `project-team-phases.md` — フェーズ別作業分担表・進行フロー（中間成果物、bestpractice に統合済み）

### 調査実施内容

Web調査を3回（各3並列、計9サブエージェント）実施:

1. **チーム構成調査**: ロボット学習スタートアップのチーム編成（Physical Intelligence, Skild AI, Covariant, Figure AI 等）、学術ラボの構造（Berkeley RAIL, Stanford IRIS, CMU, MIT, ETH Zurich RSL, TU Darmstadt IAS）、産学連携モデル（TRI, NVIDIA, Google DeepMind）
2. **マルチエージェント設計調査**: オーケストレーションパターン（CrewAI, AutoGen, LangGraph, MetaGPT）、失敗モード分析（Cemri et al. NeurIPS 2025）、Anthropic/Google/OpenAI のベストプラクティス
3. **検証調査**: エージェントSEのrule of thumb（SRP、粒度、オーケストレーター設計）、批評パターン（Generator-Critic、自己修正の限界）、運用モデル（セッション管理、状態永続化）

### 設計判断の経緯

1. **エージェント数**: 6体 → 4体 → 3体に段階的に統合
   - Literature + Writing → Research（調査と執筆は同一能力の表裏）
   - Code + Infra → Engineer（分離するとハンドオフ問題発生）
   - Experiment → Analyst（名称変更、実態に合わせ）
   - Review → 廃止（各エージェントの批評モードに統合）

2. **批評構造の修正**: 自己批評 → 相互批評 + 外部検証
   - Kamoi et al. TACL 2025: LLM自己修正は外部フィードバックなしで不可
   - Snorkel AI: 自己批評は簡単なタスクで性能を劣化させる
   - 修正: 同一エージェントの自己レビューを禁止、pytest/ruff/pyright による客観的検証を必須化

3. **運用モデル**: 3案を比較し、モデルC（セッション・チェックイン方式）を採用
   - モデルA（フェーズ単位）: スキルの付加価値が低い
   - モデルB（セッション全体）: コンテキスト消費が過大
   - モデルC: 状態永続化 + タスク単位の段階的進行

4. **アーキテクチャ**: 二層構造（フェーズ駆動 + タスク駆動）
   - フェーズ層: プロジェクト全体の状態管理
   - タスク層: フェーズ内の作業分配
   - タスクリスト: 事前固定ではなくフェーズ進入時に動的生成

5. **SKILL.md の位置づけ**: 「薄いルーター」→「タスクキューマネージャー + タスク生成器 + 外部検証実行」に修正（OpenAI Agents SDK の知見に基づく）

### 次のステップ

実装フェーズ（docs/TODO.md 参照）:
Step 1 → 2 → 3 → 4 → 5 の依存順序で作成

## 2026-03-22: Step 1 完了 — エージェント定義3体

### 作成ファイル

| ファイル | 内容 |
| ---- | ---- |
| `agents/pt-research.md` | Research Agent — 調査 + 執筆 + 論文批評 |
| `agents/pt-engineer.md` | Engineer Agent — 実装 + インフラ + コード批評 |
| `agents/pt-analyst.md` | Analyst Agent — 実験設計 + 統計分析 + 統計批評 |

### 設計判断

- 各エージェントに **execute / critique** の2モード構造を定義
- 批評モードでは「自分自身の出力をレビューしない」制約を全エージェントに明記
- Engineer には外部検証（pytest/ruff/pyright）の実行と結果報告を義務付け
- Analyst には統計的厳密性チェックリスト（検定前提、多重比較補正、効果量等）を組み込み
- 出力形式はハンドオフプロトコル（bestpractice §3.6）に準拠
- コーディング規約は CLAUDE.md のルールをそのまま Engineer に転記（DRY 違反だが、サブエージェントは CLAUDE.md を自動で読まないため明示が必要）

## 2026-03-22: Step 1 英語化 + Step 2 完了 — リファレンス2ファイル

### エージェント定義の英語化

前セッションで日本語で作成した3体のエージェント定義を英語に書き直し。
Memory ルール（`feedback_agent_definitions_english.md`）に従い、エージェント定義は英語で記述する。

### Step 2 作成ファイル

| ファイル | 内容 |
| ---- | ---- |
| `skills/project-team/references/handoff_protocol.md` | レポート形式、Status/Mode/Verdict 定義、相互批評ディスパッチ表 |
| `skills/project-team/references/phase_transitions.md` | フェーズ完了条件、承認ゲート、ループ構造(A/B/C/D)、状態ファイル形式 |

### 補足: VSCode 設定変更

`git.autoRepositoryDetection: "openEditors"` を VSCode user settings に追加。
シンボリックリンク経由で `~/workspace/dotfiles` が Source Control に表示される問題を解消。

## 2026-03-22: Step 3 完了 — フェーズ定義6ファイル

### Step 3 作成ファイル

| ファイル | 内容 |
| ---- | ---- |
| `skills/project-team/phases/phase1-research.md` | 先行研究/市場調査のタスク生成テンプレート。academic: 論文網羅+ギャップ分析、startup: 競合/特許/市場分析 |
| `skills/project-team/phases/phase2-hypothesis.md` | 仮説構築/実験設計のタスク生成テンプレート。academic: 有意差検定+ablation、startup: A/Bテスト+実用的有意差 |
| `skills/project-team/phases/phase3-implement.md` | 実装のタスク生成テンプレート。ベースライン・提案手法・インフラ・外部検証・コードレビューの5カテゴリ |
| `skills/project-team/phases/phase5-analysis.md` | 分析のタスク生成テンプレート。前処理→主分析→ablation→図表→統計コードレビュー→仮説判定 |
| `skills/project-team/phases/phase6-output.md` | 出力のタスク生成テンプレート。academic: 論文セクション別、startup: 技術文書/投資家資料/本番コード |
| `skills/project-team/phases/phase7-review.md` | レビューのタスク生成テンプレート。Round 1 外部検証→Round 2 相互批評→Round 3 判定+Loop D修正 |

### Step 3 設計判断

- 全ファイル英語で記述（Memory ルール準拠）
- タスク生成テンプレートとして機能（固定タスクリストではない）— bestpractice §3.3 準拠
- モード分岐（academic/startup）はフェーズファイル側に配置、エージェントはモード非依存 — §3.4 準拠
- `handoff_protocol.md` / `phase_transitions.md` は参照のみ、内容の重複なし
- 全フェーズに承認ゲートまたは人間タスクを明示的に配置（SKILL.md の自動進行を防止）
- クロスチェック実施済み: エージェント名/モード、批評ディスパッチ、完了条件、ループ参照すべて整合

## 2026-03-22: Step 4 完了 — SKILL.md

### Step 4 作成ファイル

| ファイル | 内容 |
| ---- | ---- |
| `skills/project-team/SKILL.md` | タスクキューマネージャー。状態ファイル読み込み→タスク生成→エージェントディスパッチ→外部検証→状態更新の8ステップ |

### インターフェース

| コマンド | 動作 |
| ---- | ---- |
| `/project-team` | チェックイン: 状態読み込み、残タスク提示、次アクション提案 |
| `/project-team init` | 新プロジェクト初期化（モード選択、状態ファイル作成） |
| `/project-team phase N` | Phase N に遷移しタスク生成 |
| `/project-team status` | 現在のフェーズ・タスク進捗・ループ回数を表示 |

### SKILL.md の責務（bestpractice §3.6 準拠）

1. 状態ファイル読み込み（現在フェーズ + タスクキュー）
2. コマンドルーティング（init / phase / status / チェックイン）
3. タスク生成（フェーズ定義テンプレート + 前フェーズ成果物 → タスクキュー）
4. エージェントディスパッチ（Agent tool 経由、プロンプト構築）
5. エージェント報告の解析（Status / Verdict の処理）
6. 外部検証（pytest / ruff / pyright の実行）
7. 状態ファイル更新（タスク完了、ループカウント、History）
8. 次アクション提案（残タスク / フェーズ遷移 / ブロッカー報告）

### 補足: settings.json パーミッション

- `Edit(~/.claude/skills/**)` + `Write(~/.claude/skills/**)` をユーザー設定に追加
- 個別スキルごとのルール（literature-survey, project-team）を統合ワイルドカードに置換

### ユーザー向けドキュメント

- `skills/project-team/README.md` を作成: コマンド一覧、典型的な使い方フロー、フェーズ表、エージェント構成、関連スキル連携
