# ロボット学習プロジェクト: チーム構成・運用ベストプラクティス

本文書は、LLMエージェントを活用したロボット学習プロジェクトの推進に関する
ベストプラクティスを、Web調査・先行事例分析・技術的制約の検証に基づき編纂したものである。

---

## 1. チーム構成

### 1.1 設計原則

- エージェント数は **3〜5体** が最適。超えると協調オーバーヘッドが支配的になる
  （出典: [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), [Google ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/), [Cemri et al. NeurIPS 2025](https://arxiv.org/abs/2503.13657)）
- マルチエージェントの失敗率は **41〜86.7%**。非構造的なネットワークはエラーを **17.2倍** に増幅する（[同上](https://arxiv.org/abs/2503.13657)）
- マルチエージェントはシングルエージェントの **約15倍** のトークンを消費する（[Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)）
- Claude Code のサブエージェントは **1階層のみ**（ネスト不可、[公式ドキュメント](https://code.claude.com/docs/en/sub-agents)で明示）
- 独立した「レビュー専門職」は現実に存在しない。批評はドメイン専門家が兼任するのが自然
- LLMの自己修正は外部フィードバックなしでは**信頼できない**。自己批評（同一エージェントが自分の出力をレビュー）は避け、必ず**異なるエージェントによる相互批評**か**外部検証ツール**（pytest, ruff, pyright等）の実行結果を用いる
  （出典: [Kamoi et al. TACL 2025](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177), [Snorkel AI](https://snorkel.ai/blog/the-self-critique-paradox-why-ai-verification-fails-where-its-needed-most/)）
- 品質ゲートには必ず**客観的検証**（テスト実行結果、linter出力等）を含める。エージェントの主観的判断のみに依存しない
  （出典: [GitHub Blog](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/)）

### 1.2 人間チーム（最小構成: 1〜2名）

| 役割 | 人数 | 説明 |
| ---- | ---- | ---- |
| リード | 1名（必須・常駐） | PM/PI + 研究者を兼ねる全フェーズの意思決定者。学術モードでは研究責任者(PI)、スタートアップモードではプロダクトマネージャー(PM)として機能。問題定義・仮説構築・結果解釈・公開判断など、エージェントに委譲できない判断を担う |
| オペレーター | 1名（Phase 3-4のみ） | 実機ロボットの操作・テレオペレーション・物理データ収集。エージェントでは原理的に代替不可能な身体的作業を担当。実機を使わないプロジェクト（シミュレーションのみ）では不要 |

> **注**: PM/PI と研究者を分離するのはチームが3名以上に拡大した段階で初めて意味を持つ。
> 最小構成では区別しないほうが現実的である。

#### スケール時の人員追加順序

先行事例の調査（Physical Intelligence, Skild AI, Covariant 等）に基づく優先順:

| 順序 | 追加役割 | トリガー |
| ---- | ---- | ---- |
| 1 | 追加研究者 | リードの研究負荷が Phase 2-5 のボトルネックになった時 |
| 2 | ドメインエキスパートCEO | スタートアップとして市場投入を目指す時（学術のみなら不要） |
| 3 | プロダクトエンジニア | 顧客向けUIやAPI、デプロイが必要になった時 |
| 4 | 追加オペレーター | データ収集のスループットがボトルネックになった時 |

### 1.3 エージェントチーム（3体）

各エージェントは **実行モード** と **批評モード** の2つの動作モードを持つ。
批評モードでは、**他のエージェントの出力**を自身のドメイン知識に基づいて検証する。
自分自身の出力を自己批評することは行わない（LLMの自己修正は外部フィードバックなしでは
信頼できないため。出典: [Kamoi et al. TACL 2025](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177)）。

| エージェント | 実行モード | 批評モード |
| ---- | ---- | ---- |
| **Research** | 論文調査・要約・分類、競合/特許/市場調査、論文執筆・提案書作成 | 論文ドラフトのレビュー（新規性・引用妥当性・論理構成）、関連研究の網羅性チェック |
| **Engineer** | アルゴリズム実装・テスト作成・リファクタリング、CI/CD・Docker・wandb・GPU環境構築 | コードレビュー（正確性・テストカバレッジ・型安全性・セキュリティ）、インフラ構成の検証 |
| **Analyst** | 実験マトリクス設計・統計検定計画・コスト見積、結果の統計処理・図表生成・効果量算出 | 統計手法のレビュー（検定の妥当性・サンプルサイズ・多重比較補正）、実験設計の欠陥検出 |

#### エージェント統合の根拠

| 統合 | 理由 |
| ---- | ---- |
| Literature + Writing → **Research** | 調査と執筆は「学術テキストを扱う」同一能力の表裏。文脈を保持したまま処理するほうが品質が高く、ハンドオフのオーバーヘッドも消える |
| Code + Infra → **Engineer** | Dockerfile を書くのも model.py を書くのもコーディング。分離すると「Code が書いたコードを Infra が動かせない」問題が起きる |
| Experiment → **Analyst** | 名称変更のみ。エージェントは実験を実行できない（物理世界の制約）ため、実態（分析）に合わせた |
| Review → **廃止・各エージェントに統合** | 批評にはドメイン知識が必要。独立した Critic は全ドメインの知識が必要で肥大化する。査読・コードレビューの現実と一致する相互批評構造を採用 |

---

## 2. プロジェクトフェーズ

### 2.1 フェーズ別作業分担表

凡例: **★** 主担当 / **◆** 積極的に関与 / **△** 必要時に支援 / 空欄 = 関与なし

| Phase | 内容 | リード | Oper. | Research | Engineer | Analyst |
| ----- | ---- | ----- | ----- | -------- | -------- | ------- |
| 0 | 着想・問題定義 | ★ | | | | |
| 1 | 先行研究/市場調査 | ◆ | | ★ | | |
| 2 | 仮説構築/実験設計 | ★ | | ◆ | | ★ |
| 3 | 実装/プロトタイプ | △ | △ | ◆ 批評 | ★ 実装 | △ |
| 4 | 実験・検証 | ◆ | ★ | | △ | |
| 5 | 分析・考察 | ★ | | | ◆ 批評 | ★ 分析 |
| 6 | 出力(論文/製品) | ◆ | | ★ 執筆 | ◆ | ◆ 批評 |
| 7 | レビュー/改善 | ★ | | ◆ 批評 | ◆ 批評 | ◆ 批評 |
| 8 | 公開・展開 | ★ | | △ | ◆ | |

### 2.2 各フェーズの詳細

#### Phase 0: 着想・問題定義

| 項目 | 内容 |
| ---- | ---- |
| 目的 | 解くべき問題を明確化し「何が面白いか/何に価値があるか」を言語化する |
| 担当 | リード（意思決定）のみ |
| エージェント | **不使用**。問題設定の質がプロジェクト全体の価値を決定するため、人間の直感と判断が不可欠 |
| 成果物 | 問題定義文書（1ページ以内） |
| 完了条件 | 「何を解くか」「なぜそれが重要か」が1文で説明できる状態 |

#### Phase 1: 先行研究/市場調査

| 項目 | 内容 |
| ---- | ---- |
| 目的 | 問題の既知/未知の境界を特定する |
| 担当 | Research（★ 調査実行）、リード（◆ 結果評価・差別化判断） |
| 学術モード | 論文網羅・研究ギャップ特定。`/literature-survey` に委譲可 |
| スタートアップモード | 競合調査・特許検索・市場レポート分析 |
| 成果物 | 先行研究/競合分析レポート |
| 完了条件 | 「既存研究/製品との差分」が明確に言語化できている |

#### Phase 2: 仮説構築/実験設計

| 項目 | 内容 |
| ---- | ---- |
| 目的 | 検証可能な仮説を立て、実験計画を策定する |
| 担当 | リード（★ 仮説策定）、Analyst（★ 実験設計）、Research（◆ ベースライン評価条件収集） |
| 成果物 | 実験計画書（独立/従属変数、対照条件、評価指標、統計検定計画、計算コスト見積） |
| 承認ゲート | リードが実験計画を承認（コスト・期間のトレードオフ判断） |

#### Phase 3: 実装/プロトタイプ

| 項目 | 内容 |
| ---- | ---- |
| 目的 | 仮説検証に必要なコードとインフラを構築する |
| 担当 | Engineer（★ 実装 + 環境構築） |
| 外部検証 | `pytest`, `ruff check`, `pyright` の実行（客観的品質ゲート） |
| 相互批評 | Research が批評モードでコードレビュー（論文記述との整合性、引用の正確性） |
| 人間の役割 | 実機統合はリード + Oper.（エージェント不可） |
| 成果物 | 実行可能なコード + テスト + 実験環境 |

#### Phase 4: 実験・検証

| 項目 | 内容 |
| ---- | ---- |
| 目的 | 実験計画に従いデータを収集する |
| 担当 | Oper.（★ 実機実験）、リード（◆ 実行監視・判断）、Engineer（△ ジョブ管理） |
| エージェント活用 | 限定的。実験の実行自体は計算資源と物理ロボットの問題 |
| 既存スキル連携 | `/sweep run` でハイパーパラメータ探索を自動化 |
| 成果物 | 実験データ（wandb ログ、CSV、動画等） |

#### Phase 5: 分析・考察

| 項目 | 内容 |
| ---- | ---- |
| 目的 | 実験データから結論を引き出す |
| 担当 | Analyst（★ 統計処理）、リード（★ 解釈・考察） |
| 相互批評 | Engineer が批評モードで統計処理コードの正確性を検証 |
| 既存スキル連携 | `/sweep analyze` で結果分析を自動化 |
| 判定分岐 | 仮説支持 → Phase 6 / 仮説否定 → Phase 2 / 不明瞭 → Phase 4 |
| 成果物 | 分析レポート（統計表、図、考察） |

#### Phase 6: 出力（論文 or 製品）

| 項目 | 内容 |
| ---- | ---- |
| 目的 | 成果物を形にする |
| 担当 | Research（★ 執筆）、Engineer（◆ 再現コード/プロダクションコード） |
| 相互批評 | Analyst が批評モードで主張と証拠の対応を検証 |
| リードの役割 | ストーリー構成判断、主張の最終決定 |
| 学術モード | 論文草稿（Introduction〜Conclusion） |
| スタートアップモード | 技術ドキュメント、投資家向け資料、デプロイ準備 |
| 成果物 | 論文ドラフト or リリース可能なプロダクト |

#### Phase 7: レビュー/改善ループ

| 項目 | 内容 |
| ---- | ---- |
| 目的 | 相互批評 + 外部検証により成果物の品質を担保する |
| 担当 | 3体すべてが批評モードで稼働（相互チェック） |
| 外部検証 | `pytest`（テスト通過）、`ruff check`（lint）、`pyright`（型チェック）の実行結果を判定材料に含める |
| 判定 | 各エージェントが PASS / REVISE / BLOCK を判定。外部検証が FAIL の場合は自動的に REVISE 以上 |
| リードの役割 | レビュー結果の優先度判断、対応方針決定 |
| 成果物 | 品質保証済みの最終成果物 |

相互批評の具体的なディスパッチ:

| 批評者 | 批評対象 | 検証観点 |
| ---- | ---- | ---- |
| Engineer | Research の論文草稿 | Method 節のコード記述が実装と一致するか |
| Research | Engineer の実装 | 論文の記述と実装の整合性、引用の正確性 |
| Analyst | 全体 | 実験結果の統計処理に誤りがないか、主張と証拠の対応 |

#### Phase 8: 公開・展開

| 項目 | 内容 |
| ---- | ---- |
| 目的 | 成果を世に出す |
| 担当 | リード（★ 意思決定・実行）、Engineer（◆ リポジトリ公開/デプロイ） |
| エージェント活用 | 最小限。公開の意思決定は人間が行う |
| 成果物 | 投稿済み論文 or リリース済み製品 |

### 2.3 フェーズ進行フロー

```text
 ┌─────────────────────────────────────────────────────────────────────┐
 │   Phase 0: 着想・問題定義                                           │
 │   [リード ★]  エージェント介入なし                                  │
 └──────────────────────┬──────────────────────────────────────────────┘
                        ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │   Phase 1: 先行研究 / 市場調査                                      │
 │   [Research ★]  →  リードが結果を評価                              │
 │   学術: /literature-survey に委譲可  ┃  startup: 競合・特許・市場    │
 └──────────────────────┬──────────────────────────────────────────────┘
                        ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │   Phase 2: 仮説構築 / 実験設計                                      │
 │   [リード ★ + Analyst ★ + Research ◆]                              │
 │   ──────────────────── 承認ゲート ────────────────────              │
 └──────────────────────┬──────────────────────────────────────────────┘
                        ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │   Phase 3: 実装 / プロトタイプ                                      │
 │   [Engineer ★] 実装 + 環境構築 → 外部検証(pytest/ruff/pyright)     │
 │   → [Research ◆批評] コードレビュー → 実機統合(人間)               │
 └──────────────────────┬──────────────────────────────────────────────┘
                        ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │   Phase 4: 実験・検証                                               │
 │   [Oper. ★ + リード ◆]                                             │
 │   シミュレーション: /sweep run  ┃  実機: テレオペ・データ収集       │
 └──────────────────────┬──────────────────────────────────────────────┘
                        ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │   Phase 5: 分析・考察                                               │
 │   [Analyst ★ + リード ★]  /sweep analyze に委譲可                  │
 │                                                                     │
 │   ┌──────────── 判定分岐 ────────────┐                              │
 │   │ 仮説支持   → Phase 6 へ         │                              │
 │   │ 仮説否定   → Phase 2 へ ─────────┼──── (A) 仮説修正ループ      │
 │   │ 結果不明瞭 → Phase 4 へ ─────────┼──── (B) 追加実験ループ      │
 │   └─────────────────────────────────┘                              │
 └──────────────────────┬──────────────────────────────────────────────┘
                        ▼  (仮説支持の場合)
 ┌──────────────────────────────────────────────────────────────────────┐
 │   Phase 6: 出力                                                     │
 │   [Research ★ + Engineer ◆]                                        │
 │   学術: 論文草稿           ┃  startup: ドキュメント・デプロイ準備   │
 └──────────────────────┬──────────────────────────────────────────────┘
                        ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │   Phase 7: レビュー / 改善ループ                                    │
 │   外部検証(pytest/ruff/pyright) + 相互批評:                        │
 │   [Research ◆批評 + Engineer ◆批評 + Analyst ◆批評]               │
 │                                                                     │
 │       BLOCK  ──→ Phase 3/4 へ ───────────── (C) 重大欠陥ループ     │
 │       REVISE ──→ 該当 Agent が修正 → 再レビュー                    │
 │       PASS   ──→ Phase 8 へ                                         │
 └──────────────────────┬──────────────────────────────────────────────┘
                        ▼  (PASS の場合)
 ┌──────────────────────────────────────────────────────────────────────┐
 │   Phase 8: 公開・展開                                               │
 │   [リード ★ + Engineer ◆]                                          │
 │   学術: 投稿・OSS公開     ┃  startup: デプロイ・リリース           │
 └─────────────────────────────────────────────────────────────────────┘
```

### 2.4 ループ構造

| ループ | 経路 | トリガー | 想定回数 | 上限超過時の対応 |
| ------ | ---- | -------- | -------- | ---------------- |
| (A) 仮説修正 | Ph.5 → Ph.2 → Ph.3 → Ph.4 → Ph.5 | 実験結果が仮説を否定 | 1-3回 | Phase 0 の問題設定を見直す |
| (B) 追加実験 | Ph.5 → Ph.4 → Ph.5 | 結果が不明瞭（有意差なし、サンプル不足） | 1-2回 | 実験設計の根本的再検討 |
| (C) 重大欠陥 | Ph.7 → Ph.3/4 → Ph.5 → Ph.6 → Ph.7 | レビューで BLOCK 判定 | 0-1回 | 設計の根本問題を示唆 |
| (D) 軽微修正 | Ph.7 内で完結 | レビューで REVISE 判定 | 1-3回 | — |

---

## 3. エージェントシステム設計

### 3.1 アーキテクチャ: 二層構造

| 層 | 駆動方式 | 責務 | 実装 |
| ---- | ---- | ---- | ---- |
| フェーズ層 | フェーズ駆動 | 「今どのフェーズにいるか」を管理し、フェーズ遷移とループ判定を行う | SKILL.md（タスクキューマネージャー）+ フェーズ定義ファイル |
| タスク層 | タスク駆動 | フェーズ内で同一エージェントを異なるプロンプトで複数回呼ぶ | Agent tool による呼び出し |

フェーズ駆動はプロジェクト全体の状態管理（どこにいて、次にどこへ行くか）を担い、
タスク駆動はフェーズ内の具体的な作業分配を担う。

#### タスク駆動のみが適する場合（フェーズ管理不要）

- 数日〜1週間で完結する小規模タスク
- 1〜3セッションで完了
- 仮説修正ループが0〜1回
- エージェント1〜2体で足りる

#### フェーズ駆動が必要な場合

- 数週間〜数ヶ月の中大規模プロジェクト
- 10+セッションにまたがる
- 仮説修正ループ2回以上
- 3体以上のエージェントが同一プロジェクトに関与

### 3.2 運用モデル: セッション・チェックイン方式

スキルの呼び出し単位は**作業セッションの開始時**。1回の呼び出しで進めるのは
**1〜2タスク**。フェーズ全体を一気に進めるのではなく、タスク単位で段階的に
進行する。

```text
 ユーザーの1セッション
 ──────────────────────────────────────────────────

 作業開始: /project-team
   ↓
 スキルが状態ファイルを読む
   ↓
 ┌─ タスクリストが存在する → 残タスクを提示、ユーザーが選択
 │
 └─ タスクリストが存在しない（新フェーズ進入時）
      ↓
    フェーズ定義ファイル（テンプレート）を読む
      ↓
    前フェーズの成果物を入力としてタスクリストを自動生成
      ↓
    ユーザーに提示 → 承認ゲート
      ↓
    状態ファイルに書き込み
   ↓
 選択されたタスクに応じてエージェントを起動
   ↓
 エージェントの結果を受け取り、タスクを完了にマーク
   ↓
 次のアクションを提案（続けるか、今日はここまでか）
   ↓
 終了時: 状態ファイルに現在地を書き込み
```

このモデルを選択した理由:

| 観点 | フェーズ単位で呼ぶ方式 | セッション・チェックイン方式 |
| ---- | ---- | ---- |
| スキルの付加価値 | 低い（直接エージェントを呼ぶのと同じ） | 高い（状態管理 + 次の一手の提案） |
| コンテキスト消費 | フェーズ全体分を1セッションで消費 | 1〜2タスク分のみ |
| セッション跨ぎ | 状態が消える | 状態ファイルに永続化される |
| 人間の負荷 | 高い（フェーズ管理は自力） | 低い（現在地と残タスクをスキルが提示） |

### 3.3 タスク生成: フェーズ進入時に動的生成

各フェーズのタスクリストは**事前に固定できない**。Phase 3 のタスクは Phase 2 の
実験計画が決まるまで定義できない。

| フェーズ | タスク生成に必要な入力 | その入力が生まれるフェーズ |
| ---- | ---- | ---- |
| Phase 1 | 問題定義（何を調べるか） | Phase 0 |
| Phase 2 | 先行研究の全体像（何が未解決か） | Phase 1 |
| Phase 3 | 実験計画書（何を実装するか） | Phase 2 |
| Phase 4 | 実装済みコード（何を動かすか） | Phase 3 |
| Phase 5 | 実験データ（何を分析するか） | Phase 4 |
| Phase 6 | 分析結果（何を書くか） | Phase 5 |
| Phase 7 | 成果物ドラフト（何をレビューするか） | Phase 6 |
| Phase 8 | レビュー済み成果物 | Phase 7 |

したがって、フェーズ定義ファイルは固定タスクリストではなく
**タスク生成テンプレート**として機能する。

#### フェーズ定義ファイルの構造（例: phase3-implement.md）

```text
## タスク生成ルール

入力: Phase 2 の実験計画書

以下のカテゴリでタスクを生成せよ:

1. ベースライン実装（実験計画の「比較対象」から各1タスク）
   - Agent: Engineer (execute)
   - 依存: なし

2. 提案手法実装（提案手法の主要コンポーネントごとに1タスク）
   - Agent: Engineer (execute)
   - 依存: なし

3. 実験インフラ構築（1タスク、カテゴリ1-2と並行実行可）
   - Agent: Engineer (execute)
   - 依存: なし

4. コードレビュー（1タスク）
   - Agent: Engineer (critique)
   - 依存: カテゴリ1, 2 の全タスク完了

5. 実機統合（実機を使う場合のみ。人間タスク）
   - Agent: (人間)
   - 依存: カテゴリ1, 2, 3 の全タスク完了

## タスク粒度ガイドライン

- 1タスク = 1回のエージェント呼び出しで完了する単位
- 目安: コード実装なら1ファイル〜1モジュール程度
- 大きすぎる場合はユーザーに分割を提案
```

### 3.4 モード分岐の配置

モード（academic / startup）の分岐は**エージェント内ではなくフェーズ定義ファイルに配置**する。
エージェントのシステムプロンプトはモード非依存に保ち、モード固有の指示はフェーズ定義ファイルが
タスク生成時のプロンプトとして組み立てる。

| モード分岐が大きいフェーズ | 学術 | スタートアップ |
| ---- | ---- | ---- |
| Phase 1 | 論文網羅・ギャップ特定 | 競合・特許・市場調査 |
| Phase 2 | 有意差検定・ablation設計 | A/Bテスト・実用的有意差 |
| Phase 6 | 論文草稿 | 技術ドキュメント・投資家資料・デプロイ |
| Phase 8 | 学会投稿・OSS公開 | プロダクトデプロイ・リリース |

| モード分岐が小さいフェーズ | 共通の動作 |
| ---- | ---- |
| Phase 0, 3, 4, 5, 7 | モードによる動作の差異はほぼない |

### 3.5 ファイル構成

```text
~/.claude/
├── agents/
│   ├── pt-research.md          # Research Agent（調査 + 執筆 + 論文批評）
│   ├── pt-engineer.md          # Engineer Agent（実装 + インフラ + コード批評）
│   └── pt-analyst.md           # Analyst Agent（実験設計 + 統計分析 + 統計批評）
│
├── skills/
│   └── project-team/
│       ├── SKILL.md             # タスクキューマネージャー + タスク生成器 + 外部検証実行
│       ├── phases/
│       │   ├── phase1-research.md      # タスク生成テンプレート
│       │   ├── phase2-hypothesis.md    # タスク生成テンプレート
│       │   ├── phase3-implement.md     # タスク生成テンプレート
│       │   ├── phase5-analysis.md      # タスク生成テンプレート
│       │   ├── phase6-output.md        # タスク生成テンプレート
│       │   └── phase7-review.md        # タスク生成テンプレート（相互批評）
│       └── references/
│           ├── handoff_protocol.md     # エージェント間ハンドオフ形式
│           └── phase_transitions.md    # フェーズ遷移条件・ループ判定基準
│
└── docs/
    └── LOGS/
        └── log_project_team.md         # フェーズ状態 + タスクキューの永続化
```

Phase 0, 4, 8 にフェーズ定義ファイルがない理由:

| Phase | 理由 |
| ---- | ---- |
| Phase 0（着想） | エージェント不使用。スキルの管轄外 |
| Phase 4（実験実行） | 人間と計算資源の作業。`/sweep run` に委譲 |
| Phase 8（公開） | 人間の意思決定。`/commit-and-push` 等に委譲 |

### 3.6 SKILL.md の責務

スキルの本質は**タスクキューマネージャー + タスク生成器**である。

1. 状態ファイル（`docs/LOGS/log_project_team.md`）から現在フェーズとタスクキューを読む
2. タスクリストが未生成なら、フェーズ定義ファイル + 前フェーズ成果物からタスクを生成し承認を得る
3. 残タスクを提示し、ユーザーの選択に応じてエージェントを起動する
4. エージェント完了後、外部検証ツール（`pytest`, `ruff check`, `pyright`）を実行し結果を記録する
5. 外部検証の結果とエージェント出力を合わせてタスクを完了/差し戻しにマークし、状態ファイルを更新する
6. フェーズ内の全タスク完了時、フェーズ遷移判定を行い次フェーズを提案する

想定するインターフェース:

```text
/project-team                    → 状態を読み、残タスクを提示（チェックイン）
/project-team phase 3            → Phase 3 に移行しタスクを生成
/project-team status             → 現在のフェーズ・タスク進捗を表示
```

### 3.7 状態ファイルの構造

```markdown
# プロジェクト状態

- モード: academic
- 現在フェーズ: 3
- ループ回数: (A)0 (B)0 (C)0 (D)0

## Phase 3 タスクキュー

| ID | タスク | エージェント | モード | 依存 | 状態 | 完了日 |
| -- | ------ | ------------ | ------ | ---- | ---- | ------ |
| 3.1 | ベースラインPPO実装 | Engineer | execute | - | 完了 | 2026-03-22 |
| 3.2 | ドメインランダム化実装 | Engineer | execute | - | 作業中 | |
| 3.3 | Docker+wandb環境構築 | Engineer | execute | - | 完了 | 2026-03-22 |
| 3.4 | コードレビュー | Engineer | critique | 3.1,3.2 | 待ち | |
| 3.5 | 実機統合 | (人間) | - | 3.1,3.2,3.3 | 待ち | |
```

### 3.5 既存スキルとの連携

| 既存スキル | 連携ポイント |
| ---- | ---- |
| `/literature-survey` | Phase 1 で本格的な調査（30+本）が必要な場合に委譲 |
| `/sweep` (plan/config/run/analyze) | Phase 4 で実験実行、Phase 5 で結果分析を委譲 |
| `/fault-tree-debug` | Phase 3-5 でバグ発生時に委譲 |
| `/reference-verify` | Phase 6 で引用の実在性チェックに委譲 |
| `/commit`, `/commit-and-push` | フェーズ完了時のマイルストーンコミットに使用 |
| `/log-progress` | Phase 完了時にプロジェクト進捗を記録 |
| `/daily-report` | 独立して呼び出し可。マルチエージェント作業の日次サマリー |

### 3.6 ハンドオフプロトコル

各エージェントの出力は以下の形式で統一する:

```markdown
## [Agent名] Report
**Phase**: [現在のフェーズ番号]
**Mode**: [execute | critique]
**Status**: [complete | partial | blocked]

### 成果
[実行結果の詳細]

### 生成/変更したファイル
| ファイル | 操作 | 説明 |
| ---- | ---- | ---- |

### 後続への引き継ぎ
- [次のエージェントまたはフェーズへの申し送り事項]

### 問題・懸念
- [発見した問題点、リードへのエスカレーション事項]
```

---

## 4. 学術/スタートアップモードの差異一覧

| 観点 | 学術モード | スタートアップモード |
| ---- | ---- | ---- |
| リードの役割 | 研究責任者(PI) | プロダクトマネージャー(PM) |
| Phase 1 の焦点 | 論文・研究ギャップ | 競合製品・特許・市場 |
| 仮説の性質 | 「Xは既存手法Yより汎化性能が高い」 | 「Xでタスク完遂率が実用水準に達する」 |
| 比較対象 | 発表済みベースライン | 自社現行システム or 競合製品 |
| 実験設計 | 有意差検定・ablation | A/Bテスト・実用的有意差 |
| 品質基準 | 新規性 + 再現性 | 信頼性 + ユーザー影響 |
| Phase 6 の出力 | 論文草稿 | 技術ドキュメント・投資家資料 |
| Phase 8 の出力 | 学会投稿・OSS公開 | デプロイ・リリース |
| 成功の定義 | 採択された論文 | 売上・顧客数・PMF |

---

## 5. 技術的制約と設計判断の根拠

| 制約/知見 | 出典 | 設計への影響 |
| ---- | ---- | ---- |
| サブエージェントのネスト不可 | [Claude Code Sub-agents](https://code.claude.com/docs/en/sub-agents) | フラットな3体構成を採用。サブチーム構造は不可 |
| 最適エージェント数: 3〜5体 | [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system), [Google ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) | 6体 → 3体に統合 |
| マルチエージェント失敗率: 41〜86.7% | [Cemri et al., NeurIPS 2025](https://arxiv.org/abs/2503.13657) | エージェント数を最小化し、ハンドオフを削減 |
| 非構造ネットワークのエラー増幅: 17.2倍 | [同上](https://arxiv.org/abs/2503.13657) | フェーズ駆動による構造化されたディスパッチ |
| トークン消費: シングルの約15倍 | [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system) | フェーズ定義ファイルで呼び出し回数を最適化 |
| SOP をプロンプトに組み込むと品質向上 | [MetaGPT](https://openreview.net/forum?id=VtmBAGCN7o) | フェーズ定義ファイルに SOP を記述 |
| ツール説明の精度が品質に40%影響 | [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | エージェントのツール数を3〜5に制限 |
| Agent Teams（実験的機能） | [Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams) | 現時点では非推奨。安定化後に再検討 |
| LLM自己修正は外部フィードバックなしで不可 | [Kamoi et al. TACL 2025](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713/125177) | 自己批評を廃止、相互批評 + 外部検証に変更 |
| 自己批評は簡単なタスクで性能を劣化させる | [Snorkel AI](https://snorkel.ai/blog/the-self-critique-paradox-why-ai-verification-fails-where-its-needed-most/) | 同一エージェントによる自己レビューを禁止 |
| 独立批評者 + 3-5ラウンドで問題の90%+を除去 | [Actor-Critic Adversarial Coding](https://understandingdata.com/posts/actor-critic-adversarial-coding/) | 相互批評のラウンド数上限を3-5に設定 |
| 品質ゲートは全エージェント境界に配置 | [GitHub Blog](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/) | ハンドオフ時に型付きスキーマで検証 |
| SRP（単一責任原則）はエージェントにも適用 | [arxiv 2512.08769](https://arxiv.org/html/2512.08769v1) | 1エージェント = 1専門領域の設計を維持 |
| ルーティングが if/else で書けるならコード駆動 | [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/multi_agent/) | SKILL.md をタスクキューマネージャーとして実態に合わせて記述 |

---

## 6. 調査に使用した主要情報源

### ロボティクススタートアップのチーム構成

- [Salesforce Ventures: Guide to Investing in Robotics](https://salesforceventures.com/perspectives/salesforce-ventures-guide-to-investing-in-robotics/) — 5つの必須ロール定義
- [Robot & Chisel: Some Thoughts on Robotics Startups (2024)](https://www.robotandchisel.com/2024/10/01/robotics-startups/) — ドメインエキスパートCEOの重要性
- [Cemri et al.: Why Do Multi-Agent LLM Systems Fail? (NeurIPS 2025)](https://arxiv.org/abs/2503.13657) — 150+トレースの失敗分析
- [Kyle Vedder: State of Robot Learning (Dec 2025)](https://vedder.io/misc/state_of_robot_learning_dec_2025.html) — データキュレーションと評価の不可分性
- [Brad Porter: This Business of Robotics Foundation Models](https://medium.com/@bp_64302/this-business-of-robotics-foundation-models-cb4bdede1444) — 垂直統合戦略
- [Christian & Timbers: Robotics Recruiting in 2026](https://www.christianandtimbers.com/insights/robotics-recruiting-in-2026-key-strategies-trends-and-hiring-top-talent) — ロボティクス人材市場分析
- [Contrary Research: Skild AI](https://research.contrary.com/company/skild-ai) — Skild AI のチーム・事業分析
- [Physical Intelligence Overview (Grishin Robotics)](https://www.grishinrobotics.com/post/physical-intelligence-company-overview) — Pi の創業チーム・資金調達分析
- [Sankaet Pathak Interview (Sacra)](https://sacra.com/research/sankaet-pathak-foundation-humanoids-robotics/) — 資本効率とリーンチーム

### 学術ラボの構造

- [Berkeley RAIL Lab](https://rail.eecs.berkeley.edu/people.html) — ラブレット構造と学生パイプライン
- [Stanford IRIS Lab (Chelsea Finn)](https://irislab.stanford.edu/) — メタ学習からスタートアップへの移行パターン
- [CMU Deepak Pathak Lab](https://www.cs.cmu.edu/~dpathak/) — 教授兼CEOモデル（Skild AI）
- [MIT Improbable AI Lab (Pulkit Agrawal)](https://improbableai.com/members.html) — 研究エンジニアの役割
- [ETH Zurich RSL](https://rsl.ethz.ch/the-lab/people.html) — 研究エンジニア18名体制の生産性
- [TU Darmstadt IAS Lab (Jan Peters)](https://www.ias.informatik.tu-darmstadt.de/Team/Members) — 多拠点ラボ運営
- [TRI University Collaboration](https://www.tri.global/news/toyota-research-institute-invests-over-100m-collaborative-research-program-us-universities) — 共同研究者モデル（$100M+投資）
- [CMU-NVIDIA Joint Research Center](https://www.cmu.edu/news/stories/archives/2024/october/cmu-and-nvidia-to-lead-joint-research-center-for-robotics-autonomy-ai) — 産学連携モデル

### マルチエージェント設計

- [Anthropic: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) — オーケストレーター・ワーカーパターン
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — スケーリングルール、ツール記述の重要性
- [Google ADK: Developer's Guide to Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) — 8つの協調パターン
- [Claude Code Sub-agents](https://code.claude.com/docs/en/sub-agents) — ネスト不可の制約
- [Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams) — 実験的な並列エージェント通信
- [MetaGPT (OpenReview)](https://openreview.net/forum?id=VtmBAGCN7o) — SOPエンコーディングによる品質向上
- [Multi-Agent System Reliability (Maxim)](https://www.getmaxim.ai/articles/multi-agent-system-reliability-failure-patterns-root-causes-and-production-validation-strategies/) — 失敗パターンと検証戦略
- [MongoDB: Why Multi-Agent Systems Need Memory Engineering](https://medium.com/mongodb/why-multi-agent-systems-need-memory-engineering-153a81f8d5be) — メモリ管理の重要性

### オープンソースロボティクスプロジェクト

- [ALOHA / Mobile ALOHA (Stanford)](https://mobile-aloha.github.io/) — 2-3名コアチーム、商業化パス
- [Octo (UC Berkeley + Stanford + CMU + Google DeepMind)](https://octo-models.github.io/) — 15+著者の分散協調
- [OpenVLA (Stanford + TRI + UC Berkeley)](https://openvla.github.io/) — 18著者のクロス機関構成
- [Physical Intelligence (pi0)](https://www.physicalintelligence.company/) — 研究ラボ型スタートアップの人員構成
- [Trossen Robotics ALOHA Project](https://www.trossenrobotics.com/the-aloha-project) — 学術成果の商業化パス
- [UMI Gripper (Columbia/Stanford)](https://umi-gripper.github.io/) — データ収集と実装の分離設計
