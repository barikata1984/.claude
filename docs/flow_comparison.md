# フロー比較: 我々のワークフロー vs AutoResearchClaw vs AI-Researcher

## 3システムのステージ構成一覧

### AutoResearchClaw（23ステージ / 8フェーズ）

| フェーズ | ステージ | 内容 |
|----------|---------|------|
| A: Research Scoping | 1. TOPIC_INIT | トピックの初期化 |
| | 2. PROBLEM_DECOMPOSE | 研究課題の分解（構造化された課題ツリーの生成） |
| B: Literature Discovery | 3. SEARCH_STRATEGY | 検索戦略の設計 |
| | 4. LITERATURE_COLLECT | 文献収集（OpenAlex, Semantic Scholar, arXiv API） |
| | 5. LITERATURE_SCREEN [gate] | 文献のスクリーニング（人間承認 or auto-approve） |
| | 6. KNOWLEDGE_EXTRACT | 知識の抽出 |
| C: Knowledge Synthesis | 7. SYNTHESIS | 知識の統合 |
| | 8. HYPOTHESIS_GEN | 仮説生成（マルチエージェント議論） |
| D: Experiment Design | 9. EXPERIMENT_DESIGN [gate] | 実験設計（人間承認 or auto-approve） |
| | 10. CODE_GENERATION | 実験コードの生成 |
| | 11. RESOURCE_PLANNING | 計算資源の計画 |
| E: Experiment Execution | 12. EXPERIMENT_RUN | 実験の実行 |
| | 13. ITERATIVE_REFINE | 反復的改良（自己修復） |
| F: Analysis & Decision | 14. RESULT_ANALYSIS | 結果の分析（マルチエージェント） |
| | 15. RESEARCH_DECISION | 研究判断（PROCEED / REFINE → 13 / PIVOT → 8） |
| G: Paper Writing | 16. PAPER_OUTLINE | 論文アウトライン |
| | 17. PAPER_DRAFT | 論文ドラフト |
| | 18. PEER_REVIEW | 査読（エビデンスチェック） |
| | 19. PAPER_REVISION | 論文修正 |
| H: Finalization | 20. QUALITY_GATE [gate] | 品質ゲート（人間承認 or auto-approve） |
| | 21. KNOWLEDGE_ARCHIVE | 知識のアーカイブ（自己学習） |
| | 22. EXPORT_PUBLISH | LaTeXエクスポート |
| | 23. CITATION_VERIFY | 引用検証（関連性チェック） |

### AI-Researcher（5段階、Tang et al., NeurIPS 2025）

| 段階 | 内容 |
|------|------|
| 1. Literature Exploration | Knowledge Acquisition Agent が参考論文（10-15本）を処理し、関連リポジトリを検索・フィルタリング |
| 2. Idea Generation | Idea Generator Agent が文献と実装のギャップ・矛盾・新興パターンからアイデアを生成 |
| 3. Algorithm Design & Implementation | Resource Analyst が概念を原子的コンポーネントに分解し数式⇔コードの双方向マッピングを構築。Implementation Framework が専門エージェント間の構造化フィードバックサイクルで反復的に実装を改善 |
| 4. Experimental Validation | Docker環境で自動実行。結果の統計的分析 |
| 5. Scientific Documentation | Documentation Agent が階層的合成アプローチで研究成果物を出版品質の原稿に変換 |

### 我々のワークフロー（17アイテム / 4フェーズ）

| フェーズ | ステージ |
|----------|---------|
| A: 研究の方向づけ | A1 Take-home message, A2 Contribution statement, A3 研究ポジショニング |
| B: 技術的実現 | B1 技術アプローチの選定, B2 手法の設計・実装・記述, B3 実験の実行と結果取得, B4 図表の作成, B5 実験の動的再設計 |
| C: 論文化 | C1 ストーリーライン設計, C2 セクション別ドラフト, C3 統合・推敲ループ, C4 ページ予算の調整 |
| D: 品質保証と投稿 | D1 クロスモデル査読, D2 引用検証・反捏造, D3 テンプレート適用・最終整形, D4 投稿前チェックリスト |
| 横断 | 関連研究リストと評価, 先行研究との差分の明示, 比較・アブレーション設計, 査読基準の内部化 |

---

## ステージの対応関係

| 我々のステージ | AutoResearchClaw | AI-Researcher | 備考 |
|---------------|-----------------|---------------|------|
| **Phase A: 研究の方向づけ** | | | |
| A1 Take-home message | 1. TOPIC_INIT | — (入力として与えられる) | AutoResearchClawはトピック文から自動生成。AI-Researcherは参考論文10-15本を入力とする。我々は人間が定義。 |
| A2 Contribution statement | 2. PROBLEM_DECOMPOSE | 2. Idea Generation | AutoResearchClawは課題ツリーに分解。AI-Researcherはギャップからアイデアを生成。我々は人間が貢献を定義。 |
| A3 研究ポジショニング | — (明示的ステージなし) | 2. Idea Generation (部分的) | CARS 3ムーブに相当するステージは両システムとも持たない。 |
| **Phase B: 技術的実現** | | | |
| B1 技術アプローチの選定 | — (明示的ステージなし) | 3. Algorithm Design (部分的) | AutoResearchClawは仮説生成（8）から直接実験設計（9）に進み、技術選定を独立ステージとしない。AI-Researcherも概念分解の中で暗黙に行う。我々のみが独立ステージ。 |
| B2 手法の設計・実装・記述 | 10. CODE_GENERATION | 3. Algorithm Design & Implementation | AutoResearchClawはコード生成に特化。AI-Researcherは数式⇔コードの双方向マッピングと反復的改善を含む。 |
| B3 実験の実行と結果取得 | 12. EXPERIMENT_RUN + 13. ITERATIVE_REFINE | 4. Experimental Validation | AutoResearchClawは自己修復（13）を分離。AI-ResearcherはDocker実行。 |
| B4 図表の作成 | FigureAgentサブシステム (v0.2.0) | 5. Documentation (部分的) | AutoResearchClawはFigureAgentが独立サブシステム。AI-Researcherは文書化段階に含む。 |
| B5 実験の動的再設計 | 15. RESEARCH_DECISION | — (明示的ステージなし) | AutoResearchClawのPIVOT(→8)/REFINE(→13)に対応。AI-Researcherは反復改善を3段階内部で処理。 |
| **横断アイテム** | | | |
| 関連研究リストと評価 | 3〜6 (B: Literature Discovery全体) | 1. Literature Exploration | AutoResearchClawは4ステージに分解（戦略→収集→スクリーニング→抽出）。AI-Researcherは入力論文ベース。我々は横断的に段階更新。 |
| 先行研究との差分の明示 | 7. SYNTHESIS (部分的) | 2. Idea Generation (部分的) | 両システムとも独立ステージとしない。 |
| 比較・アブレーション設計 | 9. EXPERIMENT_DESIGN | — | AutoResearchClawは実験設計に含む。AI-Researcherは明示的に扱わない。 |
| 査読基準の内部化 | 18. PEER_REVIEW + 20. QUALITY_GATE | — | AutoResearchClawは査読と品質ゲートを分離。AI-Researcherは自動査読ステージを持たない。 |
| **Phase C: 論文化** | | | |
| C1 ストーリーライン設計 | 16. PAPER_OUTLINE | 5. Documentation (部分的) | AutoResearchClawはアウトライン生成を分離。AI-Researcherは階層的合成の一部。 |
| C2 セクション別ドラフト | 17. PAPER_DRAFT | 5. Documentation | |
| C3 統合・推敲ループ | 19. PAPER_REVISION | 5. Documentation (部分的) | AutoResearchClawは査読(18)→修正(19)のループ。 |
| C4 ページ予算の調整 | — | — | 両システムとも明示的ステージなし。ジャーナル固有の制約。 |
| **Phase D: 品質保証と投稿** | | | |
| D1 クロスモデル査読 | 18. PEER_REVIEW | — | AutoResearchClawはエビデンスチェック付き査読。AI-Researcherは自動査読を持たない。 |
| D2 引用検証・反捏造 | 23. CITATION_VERIFY + VerifiedRegistry | — | AutoResearchClawは4層検証 + 反捏造。AI-Researcherは明示的な引用検証ステージなし。 |
| D3 テンプレート適用・最終整形 | 22. EXPORT_PUBLISH | 5. Documentation (部分的) | |
| D4 投稿前チェックリスト | 20. QUALITY_GATE | — | |

---

## 比較から得られる知見

### 我々にあって他にないもの

1. **A3 研究ポジショニング（CARS 3ムーブ）**: AutoResearchClawもAI-Researcherも、Territory→Niche→Occupationの学術的フレーミングに相当するステージを持たない。完全自律前提のシステムでは省略されるが、RA-Lの査読プロセスではIntroductionの論理構造が厳しく評価されるため、我々のフローでは不可欠。

2. **B1 技術アプローチの選定**: 両システムとも技術選定を独立ステージとしない。AutoResearchClawは仮説生成から直接実験設計に進み、AI-Researcherは概念分解の中で暗黙に技術選択を行う。完全自律システムではエージェントが自ら選ぶため独立ステージにする必要がないが、Human-in-the-Loopの我々のフローでは人間の意思決定として明示が必要。

3. **C4 ページ予算の調整**: 両システムとも持たない。NeurIPS/ICMLはページ制限が緩いが、RA-Lの6+2ページ制約は厳格であり、ジャーナル固有の要件として必要。

### 他にあって我々にないもの

1. **文献検索の戦略設計（AutoResearchClaw 3. SEARCH_STRATEGY）**: 我々は関連研究リストを横断アイテムとしているが、検索戦略の設計（どのデータベースをどのクエリで検索するか）を明示的に扱っていない。スキル設計時に検討の余地あり。

2. **問題の分解（AutoResearchClaw 2. PROBLEM_DECOMPOSE）**: 我々のA2（Contribution statement）は貢献の定義だが、AutoResearchClawは研究課題を構造化された課題ツリーに分解する。課題の分解と貢献の定義は関連するが同一ではない。

3. **知識のアーカイブ / 自己学習（AutoResearchClaw 21. KNOWLEDGE_ARCHIVE）**: ラン間の知識蓄積。我々のフローは単一の論文執筆を想定しており、クロスプロジェクト学習は範囲外だが、将来的な拡張として有望。

4. **計算資源の計画（AutoResearchClaw 11. RESOURCE_PLANNING）**: GPU/MPS/CPU自動検出と適応。実機実験を含む我々のケースでは、計算資源に加えてロボット可用性やラボアクセスの計画も必要になりうる。

5. **数式⇔コードの双方向マッピング（AI-Researcher）**: 概念を原子的コンポーネントに分解し、数式とコード実装の双方向対応を明示する。幻覚リスクの低減に有効とされ、B2（手法の設計・実装・記述）のスキル設計時に参考にすべき手法。

### 構造的な差異

1. **フェーズの粒度**: AutoResearchClawは8フェーズ/23ステージと細かく、AI-Researcherは5段階で粗い。我々の4フェーズはAI-Researcherに近い粒度だが、ステージ数（13 + 横断4）はAutoResearchClawとAI-Researcherの中間。

2. **文献調査の扱い**: AutoResearchClawはPhase B（4ステージ）として独立フェーズ化。AI-Researcherは入力段階として1段階。我々は横断アイテムとして分散配置。この設計差は、文献調査を一括で行うか段階的に行うかの設計思想の違いを反映している。

3. **査読・品質保証の配置**: AutoResearchClawはPhase G内（18. PEER_REVIEW）とPhase H（20. QUALITY_GATE, 23. CITATION_VERIFY）に分散。AI-Researcherは品質保証ステージを持たない。我々はPhase Dとして集約。AutoResearchClawの「執筆中に査読→修正」のループは、我々のPhase C（C3推敲ループ）とPhase D（D1クロスモデル査読）の間に位置する設計であり、参考になる。

4. **戻りループ**: AutoResearchClawはステージ15で明示的にPIVOT(→8)/REFINE(→13)を定義。AI-Researcherは段階3内部の反復改善のみ。我々はB5で4段階の判断（→Phase C / →B3 / →B1 / Phase A再検討の提案）を定義しており、最も柔軟。

5. **横断アイテムの扱い**: AutoResearchClawとAI-Researcherは全ステージを直線的パイプラインで配置。我々のみが4つのアイテムを明示的に「横断」として分離しており、これは文献調査や査読基準が特定フェーズに閉じない実態を反映した設計。
