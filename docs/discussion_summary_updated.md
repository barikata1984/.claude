# エージェントによる論文執筆の自律化に向けた調査と議論のまとめ（更新版）

## 1. 調査の目的

Claude Codeを用いてIEEE RA-Lに投稿する論文を書かせることを最終目標とし、その前段階として、LLMエージェントに論文を書かせる試みを調査した。初版では、エージェントによる論文執筆それ自体を研究として論文化しているものに限定していたが、本更新版では**論文化されていないが実用に供されているツール・ワークフロー・プラットフォーム**まで調査範囲を拡大した。

---

## 2. 先行研究の調査結果（論文化されたもの）

### 2.1 完全自律型（アイデア→実験→論文生成）

**The AI Scientist (v1)** — Lu et al., 2024 (arXiv:2408.06292, Sakana AI)
- 初の完全自動科学発見フレームワーク。アイデア生成・コード実装・実験実行・結果の可視化・論文全文の執筆・自動査読までを一貫して実行する。
- 1本あたり$15以下のコストで論文を生成。自動レビュアーがほぼ人間レベルの精度でスコアリングを行う。
- ただしv1は人間が書いたコードテンプレート（NanoGPT, 2D Diffusion, Grokking）に依存する制約があった。
- 参照: https://arxiv.org/abs/2408.06292

**The AI Scientist-v2** — 2025 (arXiv:2504.08066, Sakana AI)
- v1の制約を解消。人間のコードテンプレートへの依存を排除し、experiment managerエージェントとagentic tree searchによる深い仮説探索を導入。
- ICLRワークショップに3本を投稿し、うち1本が人間の平均採択閾値を超えるスコアを獲得。完全AI生成論文の査読通過の初事例。
- 参照: https://arxiv.org/abs/2504.08066

### 2.2 Human-in-the-Loop型研究支援

**Agent Laboratory** — Schmidgall et al., 2025 (arXiv:2501.04227, EMNLP 2025 Findings)
- 人間が提供した研究アイデアを入力とし、文献レビュー→実験→論文執筆の3フェーズをPhD・Postdoc・ML Engineerの各役割エージェントが遂行する。
- o1-previewが最良の成果を出し、人間のフィードバックが品質を向上させ、先行手法比で研究コスト84%削減を達成。
- 参照: https://arxiv.org/abs/2501.04227, https://aclanthology.org/2025.findings-emnlp.320/

**AgentRxiv** — Schmidgall & Moor, 2025 (arXiv:2503.18102)
- Agent Laboratoryの拡張。複数の自律研究エージェントが互いの論文をアップロード・参照・蓄積しながら累積的に研究を進めるフレームワーク。
- MATH-500ベンチマークで逐次実行より並列エージェント間知識共有が有効であることを示した。
- 参照: https://agentrxiv.github.io/

### 2.3 サーベイ論文・長文学術文書の自動生成

**AutoSurvey** — Wang et al., 2024 (arXiv:2406.10252)
- RAGベースのアウトライン生成→専門LLMによる並列セクション執筆→統合・推敲の段階的手法。64kトークン規模の長文生成に対応。
- 参照: https://arxiv.org/abs/2406.10252

**AutoSurvey2** — 2025 (arXiv:2510.26012)
- リアルタイム検索と段階的精緻化、マルチLLM評価フレームワークを追加した後継版。
- 参照: https://arxiv.org/pdf/2510.26012

**IterSurvey** — 2025 (arXiv:2510.21900)
- 人間の反復的読解プロセスに着想を得て、静的なアウトラインではなく逐次的にアウトラインを更新しながら文献を探索・統合する。
- 参照: https://arxiv.org/html/2510.21900

**Agentic AutoSurvey** — Liu et al., 2025 (arXiv:2509.18661)
- Paper Search・Topic Mining・Academic Writer・Quality Evaluatorの4専門エージェントが協調。AutoSurveyの4.77/10に対して8.18/10のスコアを達成。
- 参照: https://arxiv.org/html/2509.18661

### 2.4 論文の部分的自動生成

**PaperRobot** — Wang et al., 2019 (arXiv:1905.07870)
- 背景知識グラフから新アイデアのリンク予測を行い、タイトル→アブストラクト→結論→次論文タイトルを段階的に生成。Turing Testで人間執筆と比較して最大30%の選好率を獲得。
- 参照: https://arxiv.org/abs/1905.07870

### 2.5 長文記事生成（学術論文の前段階）

**STORM** — Shao et al., 2024 (NAACL 2024, arXiv:2402.14207)
- 多視点質問シミュレーションとWeb検索を組み合わせてアウトラインを構築し、Wikipedia品質の長文記事をゼロから生成。
- 直接的に学術論文を書くものではないが、後続の論文生成システムの多くがSTORMの設計思想を参照。
- 参照: https://arxiv.org/abs/2402.14207

---

## 3. 論文化されていない実用的な試み（本更新で追加）

### 3.1 プラットフォーム型：統合的な研究支援環境

#### 3.1.1 OpenAI Prism（2026年1月公開）

- GPT-5.2を統合したクラウドベースのLaTeXネイティブ科学論文執筆ワークスペース。OpenAIがCrixet（LaTeXコラボレーションプラットフォーム）を買収し、AI統合を施した製品。
- ChatGPTアカウントがあれば無料で利用可能。プロジェクト数・共同編集者数に制限なし。
- **主要機能**: ドキュメント全体のコンテキストを理解したAI支援（セクション横断的な一貫性チェック）、arXiv等からの文献検索と引用挿入、ホワイトボード手書き数式・図のLaTeX変換、リアルタイム共同編集、音声ベース編集。
- **位置づけ**: 論文を自律的に書くシステムではなく、研究者の既存ワークフローにAIを深く統合するアプローチ。OpenAI VP Kevin Weillは「2026年はAIと科学にとって、2025年がAIとソフトウェアエンジニアリングにとってそうであったような年になる」と発言。
- **課題**: 学術出版社・査読者からのAI支援研究の透明性への懸念が指摘されている。IクラスタCLR等が求める透明性方針との整合が今後の論点。
- 参照: https://openai.com/index/introducing-prism/, https://openai.com/prism/

#### 3.1.2 FutureHouse Platform（2025年5月公開）

- Eric Schmidt支援の非営利研究機関FutureHouseが構築した、科学研究の自動化を目指すAIエージェントプラットフォーム。「公的に利用可能な初の超知能科学エージェント」を標榜。
- **エージェント群**:
  - **Crow**: PaperQA2ベースの一般目的文献Q&Aエージェント
  - **Falcon**: 大規模深層文献レビュー用エージェント（Crowより多くのソースを合成）
  - **Owl**: 先行研究の存在確認エージェント（特定の実験や仮説が過去に試みられたかを検出）
  - **Phoenix**: 化学実験設計支援エージェント
  - **Finch**: データ解析エージェント
  - **Robin**: 上記エージェントを統合したエンドツーエンド発見エージェント（2025年にripasudilを加齢黄斑変性の候補治療薬として同定する実績）
- **ベンチマーク**: LitQA（大学院レベルの生物学文献問題約250問）でPhD研究者の約67%に対し約90%の精度を達成。
- **商業展開**: 2025年11月にEdison Scientificとして営利子会社をスピンアウトし、製薬・バイオ企業向けに$70Mを調達。
- **論文執筆との関連**: 直接的に論文を書くツールではないが、文献検索・合成・仮説生成の自動化は論文執筆パイプラインの第3層（文脈情報）に直結する。
- 参照: https://www.futurehouse.org/, https://platform.futurehouse.org

#### 3.1.3 PaperQA2（FutureHouse, オープンソース）

- 科学文献に特化した高精度RAGエージェント。PDFからメタデータ（被引用数、撤回チェック含む）を自動取得し、全文検索インデックスを構築、反復的にクエリを精緻化して引用付きの回答を生成。
- 複数のタスク（文献Q&A、要約、矛盾検出）でPhD・ポスドクレベルの研究者を超える性能を実証（2024年論文）。
- WikiCrow（Wikipedia品質の科学記事自動生成）、ContraCrow（論文間矛盾検出）などの応用エージェントの基盤。
- オープンソースでカスタマイズ可能。LiteLLM対応で任意のLLMプロバイダを利用可能。
- 参照: https://github.com/Future-House/paper-qa, https://arxiv.org/abs/2409.13740

#### 3.1.4 Elicit（Research Agent, 2025年12月〜）

- 1億3800万件以上の論文を検索可能なAI研究ツール。2025年12月にResearch Agentを導入し、単純な文献検索から競合分析、研究ランドスケープマッピング等の複合的ワークフローへ拡張。
- **Systematic Review機能**: スクリーニング精度94%、データ抽出精度94-99%を達成（自社評価）。ただし外部評価（Cochrane, 2025）では感度が平均39.5%と限定的で、補完ツールとして位置づけるのが適切。
- 2026年にはAPI公開、200論文対応レポート、スケーラブルなシステマティックレビュー機能を追加。
- **論文執筆との関連**: 文献レビュー・データ抽出の自動化に強く、5層15アイテム体系の第3層（関連研究リスト、先行研究との差分）の作成を大幅に効率化できる。ただし論文執筆自体の機能は限定的。
- 参照: https://elicit.com/, https://elicit.com/blog/introducing-research-agent-workflows

#### 3.1.5 Gemini Deep Research / Deep Think（Google DeepMind）

- **Deep Research**: Gemini 2.0以降で提供される自律的リサーチエージェント。100以上のソースを分析し、構造化されたレポートを生成。Google Scholar連携。APIも公開（2026年にInteractions API経由で利用可能に）。
- **Deep Think**: 推論特化モード。IMO 2025で金メダル水準、物理・化学オリンピック2025でも金メダルレベルを達成。2026年には研究レベル数学でBirdős予想4問の自律的解決に貢献。STOC'26のCS理論論文査読にも活用。
- **論文執筆との関連**: Deep Researchは文献調査・構造化レポート生成に、Deep Thinkは証明支援・仮説検証に活用可能。ただし論文執筆の直接的なワークフローは提供していない。
- 参照: https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/

### 3.2 コーディングエージェント型：Claude Code / Codexベースのワークフロー

論文化されていないが、GitHubで急速にエコシステムが成長しているカテゴリ。Claude Codeのスキルシステムを活用し、研究ライフサイクル全体をMarkdownベースのスキルファイルで制御するアプローチが共通する。

#### 3.2.1 ARIS（Auto-Research-In-Sleep）

- 「寝ている間にClaude Codeが研究を進める」コンセプトのML研究自動化ワークフロー。GitHub: wanshuiyin/Auto-claude-code-research-in-sleep
- **アーキテクチャ**: Claude Code（実行者）+ 外部LLM（GPT-5.4等、Codex MCP経由のレビュアー）のクロスモデル対抗協調。単一モデルの自己レビューによる盲点を回避する設計。
- **4ワークフロー構成**:
  1. 文献サーベイ→アイデア発見→新規性チェック
  2. 実験実行→自動改善ループ（最大ラウンド数・スコア閾値・GPU制限を設定可能）
  3. 論文執筆パイプライン（/paper-plan → /paper-figure → /paper-write → /paper-compile）、ICLR/NeurIPS/ICMLテンプレート対応
  4. リバッタル・ポスター生成
- **実績**: 一晩の自律実行で20以上のGPU実験を実施し、borderline rejectからsubmission-readyへ改善した事例。ARISパイプラインで完成した論文がAAAI 2026に採択。
- **特筆点**: フレームワーク非依存（純粋なMarkdownスキルファイル）。Claude Code、Codex CLI、Cursor、OpenClaw等で動作。Zotero/Obsidian連携、Feishu/Lark通知機能も。
- 参照: https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep

#### 3.2.2 claude-scholar

- Galaxy-Dawn/claude-scholar。Claude Code / Codex CLI / OpenCode対応の半自律研究アシスタント。
- **設計思想**: 「完全自動科学者ではなく、半自動研究アシスタント」を明示。重い反復作業（文献整理、ノートテイキング、実験分析、レポーティング、執筆支援）を自動化しつつ、判断は人間に留める。
- **主要機能**: Zoteroコレクション経由の文献インポート、構造化リーディングノート生成、実験後の結果分析（統計・科学的図表生成）、ML論文執筆支援（/mine-writing-patternsで強い論文から執筆パターンを抽出）、査読対応。
- **2026年3月の更新**: 結果レポーティングの分離（results-analysisとresults-report）、グローバルなwriting memoryの導入。
- 参照: https://github.com/Galaxy-Dawn/claude-scholar

#### 3.2.3 academic-research-skills

- Imbad0202/academic-research-skills。Claude Code用の包括的学術研究スキルスイート。
- **13エージェント体制のDeep Research**: ソクラテス式対話モード + 系統的レビュー/PRISMA + SCRループ。
- **12エージェント体制の論文執筆**: LaTeX出力、可視化、リビジョンコーチング、引用変換。
- **マルチ視点査読**: EIC + 3名の動的レビュアー + Devil's Advocateによる0-100品質ルーブリック。
- **10ステージ学術パイプライン**: アダプティブチェックポイント、主張検証、material passportを含む完全パイプライン。
- **推奨環境**: Claude Opus 4.6 + Maxプラン（1回のend-to-end実行で200K入力 + 100K出力トークン以上を消費する場合あり）。
- 参照: https://github.com/Imbad0202/academic-research-skills

#### 3.2.4 Sibyl Research System（AutoResearch-SibylSystem）

- 20以上の専門AIエージェントが議論・実験・論文執筆・査読を行う完全自律型研究システム。AI Scientist、FARS、AutoResearchに触発されつつ、Claude Codeのエコシステム（スキル、プラグイン、MCPサーバー、マルチエージェントチーム）をネイティブに活用。
- **Inner Loop（研究反復）**: 仮説→実験→論文を品質が出版水準に達するまで自動反復。
- **Outer Loop（自己進化）**: 研究プロセス自体から学習し、8カテゴリの問題分類、再利用可能な教訓の蓄積、エージェントプロンプト・スケジューリング戦略の自動更新を実行。
- tmuxベースの永続セッションとSentinel watchdogによる無人自律運用を実現。
- 参照: https://github.com/Sibyl-Research-Team/AutoResearch-SibylSystem

#### 3.2.5 claude-scientific-writer / claude-scientific-skills（K-Dense-AI）

- **claude-scientific-writer**: 20スキルを含む科学論文執筆ツール。Perplexity Sonar Pro Searchによるリアルタイム文献検索、Nano Banana Proによる科学図の自動生成、ScholarEval（8次元スコアリング）による査読フレームワーク。Claude Codeプラグイン、Pythonパッケージ、CLI として利用可能。
- **claude-scientific-skills**: 170以上の科学・研究スキルを収録。生物学、化学、医学を中心に、配列解析、単細胞解析、薬物ターゲット結合、分子動力学など広範な領域をカバー。Agent Skillsオープン標準準拠で、Cursor、Claude Code、Codex等のエージェントで自動検出・利用可能。
- 参照: https://github.com/K-Dense-AI/claude-scientific-writer, https://github.com/K-Dense-AI/claude-scientific-skills

#### 3.2.6 clo-author（Hugo Sant'Anna, UAB）

- 論文（Paper/main.tex）を single source of truth とし、発表スライドや補足資料を論文から派生させるワークフロー。
- **対抗的worker-criticエージェントペア**: すべての創作エージェントに専任の批評エージェントを配置し、「批評者は創作せず、創作者は自己評価しない」という権力分立を厳格に実施。
- 文献レビュー→ジャーナル投稿→revise-and-resubmitまでのフルライフサイクルをカバー。
- 参照: https://github.com/hsantanna88/clo-author, https://psantanna.com/claude-code-my-workflow/workflow-guide.html

#### 3.2.7 Karpathy's autoresearch（2026年3月公開）

- Andrej Karpathy（元Tesla AI責任者、OpenAI共同創設者）が公開した自律的ML実験ループ。GitHub: karpathy/autoresearch。公開後数日で21,000以上のGitHubスター、X上で860万ビューを記録。
- **コンセプト**: AIエージェントに訓練スクリプト（train.py, 約630行）と固定計算予算（GPU 5分間）を与え、コードの読解→仮説形成→コード修正→実験実行→結果評価→改善/棄却のループを人間の介入なしで無限に繰り返す。
- **3ファイルアーキテクチャ**: prepare.py（不変のデータ準備・評価メトリクス）、train.py（エージェントが修正する唯一のファイル）、program.md（エージェントへの指示・制約・終了条件を記述する「スキル」ファイル）。
- **実績**: 2日間で約700実験を実行し、20の有効な最適化を発見。QKNormのスケーラー欠落、Value Embeddingsの正則化など、人間の研究者が8年かけて定式化したMLのマイルストーンを17時間で再発見。Shopify CEO Tobias Lütkeは一晩で37実験を実行し、0.8Bパラメータモデルが手動チューニングした1.6Bモデルを上回る19%の改善を達成。
- **Karpathyのビジョン**: 「目標は単一のPhD学生をエミュレートすることではなく、PhD学生の研究コミュニティをエミュレートすること」。非同期的に大規模協調する分散エージェントスウォームを次のステップとして構想。
- **留意点**: Claude Opus 4.6は12時間以上・118実験を安定して実行できた一方、GPT-5.4は「LOOP FOREVER」指示に追従できず失敗したとの報告があり、エージェントの長時間安定性はモデル依存。
- 参照: https://github.com/karpathy/autoresearch

#### 3.2.8 AutoResearchClaw（AIMING Lab, UNC-Chapel Hill, 2026年3月公開）

- 「Chat an Idea. Get a Paper.」を標榜する完全自律型23ステージ研究パイプライン。GitHub: aiming-lab/AutoResearchClaw。2026年3月15日にv0.1.0公開、3月22日にv0.3.2でクロスプラットフォーム対応。8,800+スター（2026年3月時点）。
- **23ステージパイプライン**: Research Scoping → Literature Discovery → Knowledge Synthesis → Hypothesis Generation → Experiment Design → Self-Healing Execution → Analysis & Decision → Paper Writing → Citation Verificationの7フェーズで構成。
- **マルチエージェントシステム**: Innovator・Pragmatist・Contrarianの3エージェントが仮説を議論するマルチエージェント議論、adversarial analysis panelによる結果レビュー。
- **自己修復実行器**: 実験がクラッシュした場合の自動診断・コード修復、仮説が成立しない場合のPivot/Refine/Proceed自律判断（ステージ15: RESEARCH_DECISION）。
- **MetaClaw統合（v0.3.0）**: クロスラン知識転移機能。パイプライン実行時の失敗・警告を構造化レッスンに変換し、再利用可能なスキルとして次回実行の全23ステージに注入。制御実験で+18.3%のロバスト性向上を報告。
- **反捏造システム（v0.3.2）**: VerifiedRegistryが実験データのground-truthを強制。未検証の数値は自動消去。失敗した実験を自動診断・修復してから論文に反映。
- **引用検証**: arXiv、DOI、Semantic Scholar、LLM関連性チェックの4層パイプライン。
- **クロスプラットフォーム**: Claude Code、Codex CLI、Copilot CLI、Gemini CLI、Kimi CLIのACP互換エージェントで動作。Discord/Telegram/Lark/WeChatからの実行も可能。
- **ショーケース**: 8分野（数学、統計、生物学、計算、NLP、RL、ビジョン、ロバスト性）で8本の論文を人間の介入なしで完全自律生成。NeurIPS/ICML/ICLRフォーマット対応。
- 参照: https://github.com/aiming-lab/AutoResearchClaw

#### 3.2.9 FARS（Fully Automated Research System, Analemma, 2026年2月）

- Analemma社が構築したエンドツーエンドの完全自動研究システム。2026年2月12日に公開ライブ実験を開始し、228時間28分33秒の連続無人運転で100本の短報論文を自律的に生成。
- **4モジュール構成**: Ideation（文献調査・仮説生成）→ Planning → Experiment → Writingの各モジュールが複数の研究タスクを並列処理。
- **インフラ**: 160枚のGPUクラスタ、オープンソース・クローズドソース問わず任意のLLMを呼び出し可能。大学研究室の実験条件を大幅に上回る規模。
- **実績**: 平均約2時間17分で1本の論文を完成。1論文あたり平均コスト約$1,000、1億トークン以上を消費。Stanford大学のAgentic Reviewer（paperreview.ai）による評価で平均スコア5.05/10を達成（ICLR 2026人間投稿の平均4.21を上回るが、採択平均5.39には未達）。
- **課題**: 「計算力を知能に変換する」段階にあり、アルゴリズム効率の最適化にはまだ工学的余地が大きい。arXivのポリシー上、生成AIを著者として記載できないため、品質基準を通過した論文の配信チャネルを模索中。
- **意義**: 無人科学研究「組立ライン」がスループットの点で実現可能であることを初めて大規模に実証。
- 参照: https://analemma.ai/fars, https://github.com/fars-analemma

### 3.3 論文化された完全自律型研究システム（本更新で追加）

#### 3.3.1 AI-Researcher（Tang et al., HKU, NeurIPS 2025 Spotlight）

- 完全自律型研究システム。文献探索→仮説生成→アルゴリズム実装→実験検証→出版品質の原稿準備までを最小限の人間介入で統合的にオーケストレーション。
- **3つの革新**: (1) Resource Analystエージェントが複雑な研究概念を原子的コンポーネントに分解し、数式とコード実装の間の双方向マッピングを明示（幻覚リスクの大幅低減）。(2) 構造化フィードバックサイクルでの専門エージェント間協調（人間のメンター-学生関係を模倣）。(3) 階層的合成アプローチによるDocumentation Agentが研究成果物を出版品質の原稿に変換。
- **Scientist-Bench**: 多様なAI研究ドメインの最先端論文から構成される初の包括的ベンチマーク。ガイド付き革新シナリオとオープンエンド探索タスクの両方を含む。
- **発見**: ガイド付き実装よりもオープンエンド探索でより優れた性能を発揮。自律的研究システムは指示的なディレクティブに従うよりも内部知識合成を活用する方が得意である可能性を示唆。
- 参照: arXiv:2505.18705, https://github.com/HKUDS/AI-Researcher

#### 3.3.2 AlphaEvolve（Google DeepMind, 2025年5月公開）

- Gemini LLMを用いた進化的コーディングエージェント。汎用的なアルゴリズム発見・最適化のための自律的パイプライン。
- **アーキテクチャ**: LLMアンサンブル（Gemini Flash: 探索の広さ、Gemini Pro: 洞察の深さ）がコード変異を生成→自動評価器がスコアリング→進化アルゴリズムが最も有望な解を選択→次世代の変異に活用するループ。
- **実績**: 56年間改善されなかったStrassen行列乗算アルゴリズムを更新（4×4複素行列を48回のスカラー乗算で実行）。Google データセンタースケジューリングで全世界の計算資源の0.7%を回復。GeminiトレーニングのFlashAttentionカーネルで32.5%の高速化。50以上の数学問題で75%は最先端解を再発見、20%でそれを超える解を発見。
- **論文執筆との関連**: 直接的に論文を書くシステムではないが、Karpathyのautoresearchと同様の「自律的実験ループ+進化的探索」パラダイムの先駆者。「評価可能な問題であれば何でもautoresearchできる」というKarpathyの主張の理論的基盤を提供。
- 参照: arXiv:2506.13131, https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/

### 3.4 エージェントインフラストラクチャ：OpenClaw

- Peter Steinberger（オーストリア）が2025年11月にClawdbotとして公開。2026年1月にOpenClawに改名。2026年2月時点でGitHub 100,000スター超、2026年3月時点で250,000スター超（史上最速級のオープンソースプロジェクト成長）。
- **本質**: チャットアプリ（WhatsApp, Telegram, Discord, Signal等）をインターフェースとし、ローカルマシン上でLLMエージェントにファイル操作・ブラウザ制御・シェルコマンド実行等のタスクを自律的に実行させるフレームワーク。
- **研究との関連**: OpenClawそのものは研究ツールではないが、AutoResearchClawがOpenClaw互換サービスとして設計されており、チャットメッセージ1つで23ステージの研究パイプラインを起動できるインフラを提供。NVIDIA GTC 2026でJensen Huangが「OpenClawはパーソナルAIのオペレーティングシステム」と宣言。
- **スキルシステム**: Markdownベースのスキルファイル（SKILL.md）による拡張。ARISやAutoResearchClawのスキルはOpenClawで直接利用可能。
- **セキュリティ懸念**: Gartnerが「デフォルトでセキュアでない」と評価、Ciscoがデータ流出・プロンプトインジェクションの脆弱性を指摘。中国政府は国営企業での使用を制限。研究用途ではセキュリティリスクの認識が必要。
- 参照: https://github.com/open-claw/open-claw（OpenClawリポジトリ）

### 3.5 プラットフォーム型とコーディングエージェント型の比較

| 観点 | プラットフォーム型（Prism, Elicit等） | コーディングエージェント型（ARIS, claude-scholar等） |
|---|---|---|
| ユーザー層 | 幅広い研究者（非技術者含む） | コード操作に慣れた研究者 |
| カスタマイズ性 | 限定的（提供機能の範囲内） | 高い（スキルファイルの追加・改変で自由に拡張） |
| 実験の自動実行 | なし（文献調査・執筆支援に特化） | GPU実験の自律実行が可能（ARIS, Sibyl等） |
| LaTeX対応 | Prismが直接対応 | 多くがLaTeXパイプラインを内蔵 |
| オフライン/ローカル実行 | 不可（クラウド依存） | 可能（ローカルGPU・ファイルシステム直接操作） |
| 査読シミュレーション | Elicitの品質評価程度 | クロスモデル対抗レビューが標準化 |
| 再現性・透明性 | プラットフォーム依存 | Gitベースで完全な再現性 |
| コスト | Prism無料、Elicit有料プランあり | LLM API費用のみ（1論文で$15-100程度） |

---

## 4. 論文執筆に必要な情報の体系化（更新）

### 4.1 情報源

初版の情報源に加え、以下の実践知見を統合した。

- **初版の情報源**（変更なし）: Swales CARSモデル、PLOS 15-Step Guide、PMC Successful Scientific Writing、Michael Black CVPR執筆指南、IEEE RA-L Author Guidelines、Bates Scientific Writing Guide、ACS Scientific Writing Resources
- **新規追加**:
  - ARISの実践知見: クロスモデル対抗レビュー（executor≠reviewer）によるブラインドスポット回避
  - claude-scholarの設計原則: 「半自動アシスタント」としての境界設計（判断は人間、反復作業はエージェント）
  - clo-authorの対抗的worker-criticペア: 創作と批評の分離原則
  - academic-research-skillsのSCR（State-Challenge-Reflect）プロトコル: ソクラテス式対話による研究仮説の精緻化

### 4.2 5層16アイテムの体系（更新）

#### 4.2.1 「層」の意味

本体系が「層」という表現を用いるのは、以下の2つの軸が同じ方向に整列しているためである。

1. **意味的深度**: 上位層ほど研究の意味構造（what, why, so what）に近く、下位層ほど表層的な形式に近い。第1層のtake-home messageは研究の存在意義そのものであり、第5層のLaTeXテンプレート適用は内容に依存しない機械的作業である。
2. **人間関与の不可欠性**: 上位層ほど人間の知的判断が代替不可能であり、下位層ほどエージェントによる自動化が容易である。

この2軸が整列しているため、層番号が上がるにつれて「人間主導→共同作業→エージェント主導」へと連続的に移行する構造が自然に生じる。逆に言えば、もしこの2軸が分離するアイテム（意味的に深いがエージェントで自動化可能、あるいは表層的だが人間の判断が必要）が現れた場合、層の割り当てを再検討すべきシグナルとなる。

#### 4.2.2 初版からの変更点

今回の調査に基づき、以下の構造的変更を行う。

- **追加**: 「技術アプローチの選定」（第2層）、「実験の動的再設計」（第2層）、「引用検証・反捏造」（第5層）
- **統合**: 旧第3層「分野の慣習とジャーナル要件」を第5層「LaTeXテンプレートとスタイル適用」に統合
- 結果: 5層**17**アイテム（旧15 + 追加3 − 統合1）

「分野の慣習とジャーナル要件」を第3層から第5層に移動する理由は、IEEE RA-Lの6ページ制限やキーワード要件等のルールベースの制約は、Prismのテンプレート自動適用やARISの学会テンプレート内蔵により完全に自動化される領域であり、「文脈情報」として人間が共同作業すべきアイテムではなく、第5層のフォーマット制約に属するためである。

#### 第1層：研究の核心

意味的深度が最も高く、研究の存在意義と独自性を定義するアイテム群。人間の知的判断が代替不可能。

| アイテム | 説明 | エージェント負担 | 人間負担 | 負担分担の根拠 |
|---|---|---|---|---|
| Take-home message | 論文全体の主張を1〜2文で表現した核心メッセージ。全セクションの生成を制御するアンカー。 | 🟡 草案の提示・選択肢の生成（対話的に抽出）。ARISの自動レビューループはtake-home messageと実験結果の整合性を検証し矛盾する主張を排除できるが、メッセージの生成自体は支援にとどまる。 | 🔴 最終決定・承認 | 研究の意義判断は著者固有の知的行為。AI-ResearcherのNeurIPS 2025での発見（オープンエンド探索の方がガイド付き実装より優れる）も、出発点としての人間の意図設定の重要性を裏付ける。 |
| Contribution statement | 研究の貢献を3〜5文で明示したもの。レビュアーが最初に評価する対象。 | 🟡 既存研究との差分分析を支援、表現の推敲。PaperQA2/FutureHouse Owlによる先行研究の存在確認が新規性検証を効率化。 | 🔴 貢献の定義・優先順位付け | 何が貢献かは研究者のドメイン判断。Michael Blackの執筆指南で「key ideas, experimental validation, significanceをレビュアーに明示せよ」と強調。 |
| 研究ポジショニング (CARS 3ムーブ) | Territory（領域の重要性）→ Niche（ギャップの特定）→ Occupation（本研究の位置）の3段構造。 | 🟡 関連研究の検索・分類によるギャップ候補の提示。Elicit Research AgentやFalconによりギャップ候補の自動同定精度が向上。academic-research-skillsのSCRプロトコルはソクラテス式対話でギャップの妥当性を検証。 | 🔴 ギャップの選択とフレーミング | エージェントの寄与度は増しているが、フレーミングの最終判断は人間に留まる。 |

#### 第2層：技術的内容

研究の実体をなす技術的判断・データ・手法・図表。内容の正確性は著者の責任だが、整形・可視化・MLタスクの実験実行はエージェントへの委譲が進行中。

| アイテム | 説明 | エージェント負担 | 人間負担 | 負担分担の根拠 |
|---|---|---|---|---|
| 技術アプローチの選定 **[新規]** | 研究課題の実現に求められる技術的要件の定義、候補アプローチの要件に対する評価、および評価に基づく選択。ポリシーアーキテクチャ、状態・行動表現、学習フレームワーク等が対象。論文上ではMethodの冒頭で要件・候補・選定根拠の順に記述される。 | 🟡 候補アプローチの文献ベースでの列挙、要件に対する各候補の長所短所の比較表作成。PaperQA2やElicitによる候補技術の網羅的調査。 | 🔴 技術的要件の定義、プロジェクト固有の制約（計算資源、実機制約、投稿締切、チームのスキルセット等）を踏まえた最終選定 | 要件定義と最終選定は研究者のドメイン知識とプロジェクト固有の状況判断に依存する。候補の網羅的な比較はエージェントが効率的だが、要件の優先順位付けと制約下での選択は人間の責任。 |
| 手法の詳細記述 | アルゴリズム、アーキテクチャ、ハイパーパラメータ、実験セットアップ等。他者が再現可能な粒度が必要。 | 🟡 構造化された記述の生成、数式のLaTeX化、擬似コード生成。claude-scientific-writerのIMRAD構造化やclo-authorの対抗的worker-criticペアが記述の品質検証を自動化。 | 🔴 技術的正確性の保証、設計判断の説明 | ロボティクスの実機実験記述は著者の責任。 |
| 実験結果（定量データ＋解釈） | 数値テーブル、学習曲線、成功率等の生データと、各結果が何を意味するかの解釈。 | 🟢 データの整形・可視化、統計処理、表の自動生成。ARIS/Sibylは一晩で20以上のGPU実験を自律完了。claude-scholarのresults-analysisは統計処理と科学的図表生成を自動化。 | 🔴 実験実施（実機）、結果の解釈と意義付け | MLタスクではデータ取得から可視化まで自動化が実現。ロボティクスの実機データ取得は人間限定。 |
| 図表の設計と素材 | 実験写真、システム構成図、比較グラフ等の視覚素材と、各図が伝えるべきメッセージ。 | 🟡 ARISの/paper-figureがClaims-Evidence Matrixに基づく図表を自動生成。Prismはホワイトボードスケッチからのダイアグラム変換を実現。 | 🔴 写真撮影、図の設計意図の指定 | 実機ロボット写真やハードウェア図は自動生成不可。 |
| 実験の動的再設計 **[新規]** | 実験結果がtake-home messageを十分に支持しない場合に、次に取るべき行動を判断する。実験条件の調整（→再実験）、技術アプローチの再選定、または研究方向性の再検討の提案を含む。 | 🟡 結果の分析に基づき、実験条件の調整や技術アプローチの再選定を判断。研究方向性の再検討が必要な場合は人間に提案。AutoResearchClawのステージ15（RESEARCH_DECISION）やARISの/ablation-plannerが参考実装。 | 🔴 研究方向性の再検討の最終判断（特に実機実験を伴う場合の技術アプローチ再選定も人間判断） | 初版の体系は「一度設計したら実行する」静的な想定だったが、自律実行パラダイムでは実験結果に基づく動的再設計が本質的要素。 |

#### 第3層：文脈情報

研究を既存の学術的文脈に位置づけるためのアイテム群。文献検索・合成はエージェント主導に移行しつつある。

| アイテム | 説明 | エージェント負担 | 人間負担 | 負担分担の根拠 |
|---|---|---|---|---|
| 関連研究リストと評価 | 引用すべき先行研究のリストと、各論文の位置づけ（何が重要/何が限界か）。 | 🟢 PaperQA2がPhDレベル超の文献検索・合成性能を実証。Elicitはデータ抽出精度94-99%。FutureHouse Falconは数十本の論文を合成するdeep literature reviewを提供。 | 🟡 論文の選定基準、評価の最終判断 | エージェント主導に近づいているが、引用の適切性判断は人間が必要。 |
| 先行研究との差分の明示 | 既存手法と提案手法の定性的・定量的な違いを整理した対照表やディスカッション。 | 🟡 FutureHouse Owlの先行研究存在確認、Elicitの構造化データ抽出により差分の網羅的把握が効率化。対照表の自動生成。 | 🟡 比較軸の選定、技術的判断 | 比較軸の設計は研究者の判断。 |

#### 第4層：メタ情報

論文の構成・論理・品質を制御するアイテム群。ナラティブ設計は人間主導だが、査読シミュレーションと実験設計の検証はエージェントの能力が急速に向上。

| アイテム | 説明 | エージェント負担 | 人間負担 | 負担分担の根拠 |
|---|---|---|---|---|
| ストーリーライン（narrative arc） | 読者にどういう順序で何を理解させるかの設計。セクション間の論理的接続を決定する。 | 🟡 ナラティブ案の複数提示、一貫性チェック。ARISの自動レビューループがナラティブの書き直しを実行し根拠のない主張を排除した事例あり。claude-scholarの/mine-writing-patternsは強い論文からナラティブパターンを抽出。 | 🔴 物語構造の最終決定 | ストーリー設計の最終決定は人間。 |
| 査読基準の内部化 | 想定されるレビュー観点（新規性、再現性、実験の信頼性等）を事前に組み込んだ自己評価。 | 🟢 ARISのクロスモデル対抗レビュー（Claude実行→GPT-5.4査読）、academic-research-skillsのマルチ視点査読（EIC + 3レビュアー + Devil's Advocate）、clo-authorの対抗的worker-criticペアにより、査読シミュレーションの精度と多様性が大幅に向上。 | 🟡 ドメイン固有の評価基準の定義（ロボティクス固有の安全性・実機検証の信頼性等） | AI Scientistの自動レビュアーを超える実用的な査読支援が実現しつつある。 |
| 比較・アブレーションの設計論理 | なぜこのベースラインを選んだか、何を除くと何が失われるかの因果構造。 | 🟡 ARISの/ablation-plannerが実験設計を支援。Sibylのマルチエージェント議論がベースライン選定の論理を検討。アブレーション結果の表・グラフ自動生成。 | 🔴 比較設計の論理構築 | 何と比較すべきかは研究仮説に直結し、著者の知的判断が不可欠。 |

#### 第5層：フォーマット・制約・検証

表層的な形式に関するアイテム群。ルールベースの作業と反復的な品質改善はエージェントの最も得意とする領域。

| アイテム | 説明 | エージェント負担 | 人間負担 | 負担分担の根拠 |
|---|---|---|---|---|
| テンプレート適用・ジャーナル要件の充足 **[統合]** | IEEE RA-L用LaTeXテンプレート、BibTeXフォーマット、著者情報、キーワード設定、6+2ページ制約、IEEE 2カラムフォーマット等。旧第3層「分野の慣習とジャーナル要件」を統合。 | 🟢 テンプレート適用、コンパイル、エラー修正、制約充足の自動検証。Prismのクラウドコンパイル環境、ARISのICLR/NeurIPS/ICMLテンプレート内蔵、claude-scientific-writerのvenue-templatesスキル。 | 低 初期テンプレート選択のみ | ルールベースの制約でありエージェントが最も得意とする領域。人間の関与は初期選択と最終確認のみ。 |
| ページ予算の配分 | 6ページ制約下での各セクションへの配分計画（例：Intro 0.75p, Method 1.5p 等）。 | 🟢 同分野論文の統計分析、配分最適化、文字数調整 | 🟡 配分方針の承認・調整指示 | RA-Lの6+2ページ制約は厳格。過去論文の構成比率の統計分析と提案はエージェント向き。 |
| 文章の推敲と品質改善ループ | 文法・表現の改善、冗長性の除去、セクション間の整合性チェック。 | 🟢 ARISの自動改善ループ（スコア閾値に達するまで反復）、clo-authorの対抗的批評、PrismのGPT-5.2によるドキュメント全体のコンテキストを理解した推敲。 | 🟡 最終承認、技術的正確性の確認 | 言語的推敲はエージェントの強み。PMCガイドの「20〜25語を文の最大長の目安」等のルールは自動適用可能。 |
| 引用検証・反捏造 **[新規]** | 引用の実在性検証、引用内容と本文の整合性チェック、実験データの出所追跡、未検証数値の検出・消去。 | 🟢 AutoResearchClawの4層引用検証パイプライン（arXiv, DOI, Semantic Scholar, LLM関連性チェック）とVerifiedRegistry（実験データのground-truth強制、未検証数値の自動消去）。ARISの/paper-writeはDLBP/CrossRefから実BibTeXを取得しLLM生成エントリを排除。 | 🟡 最終確認、ドメイン固有の引用適切性判断 | 自律生成パイプラインでは引用の捏造（hallucinated references）が構造的リスク。FARSの100本の論文でarXivが著者記載を拒否した事例が示すように、引用検証は推敲の一部ではなく独立した品質ゲートとして機能すべき。 |

### 4.3 分担の全体構造（更新）

| 層 | アイテム数 | 主な担当 | 更新された評価 |
|---|---|---|---|
| 第1層：研究の核心 | 3 | 🔴 人間主導 | 変更なし。検証の自動化（整合性チェック等）は進展するが、意味構造の決定は人間固有 |
| 第2層：技術的内容 | 5 (+2) | 🔴 人間主導（整形・ML実験はエージェント） | 「技術アプローチの選定」「実験の動的再設計」を追加。MLタスクではデータ取得→可視化→動的再設計の自動化が実現。ロボティクス実機実験は人間限定 |
| 第3層：文脈情報 | 2 (−1) | 🟢寄りの共同作業 | 「分野の慣習」を第5層に統合。PaperQA2/Elicit/Falconにより文献検索・合成がエージェント主導に移行 |
| 第4層：メタ情報 | 3 | 🟡寄りの人間主導 | クロスモデル対抗レビューにより査読シミュレーションがエージェント主導に。ナラティブ設計は人間主導 |
| 第5層：フォーマット・制約・検証 | 4 (+1) | 🟢 エージェント主導 | 「引用検証・反捏造」を追加、「ジャーナル要件」を統合。Prism/ARISによりほぼ完全自動化 |

凡例: 🔴 人間が主担当 / 🟡 共同作業 / 🟢 エージェントが主担当

---

## 5. 初版からの主要な知見の変化

### 5.1 クロスモデル対抗レビューの標準化

初版ではAI Scientistの単一モデル自動レビュアーのみを参照していたが、ARISやclo-authorが実証したクロスモデル対抗レビュー（実行モデル≠査読モデル）は、単一モデルの自己レビューによるブラインドスポットを体系的に回避する。これは5層15アイテム体系の第4層（査読基準の内部化）の実効性を大きく変える知見である。

### 5.2 一晩自律実行パラダイムの同時多発的確立

「夜間にエージェントが実験→査読→改稿を自律的に反復し、朝に結果を確認する」パラダイムは、2026年2〜3月の極めて短い期間に複数のプロジェクトが独立して可視化された。時系列は以下の通り:

- **2025年5月**: AlphaEvolve公開（進化的アルゴリズム探索の自律ループ、直接の影響源の一つ）
- **2025年5月〜**: AI-Researcher（HKU）開発、NeurIPS 2025 Spotlightに採択
- **2026年2月12日**: FARS公開ライブ実験開始（228時間で100本の論文を自律生成）
- **2026年3月7日**: Karpathy autoresearch公開（8.6M views、「Karpathyループ」として広く認知）
- **2026年3月12日**: ARIS初回リリース（ただしAAI 2026採択論文はautoresearch公開前に完成）
- **2026年3月15日**: AutoResearchClaw v0.1.0公開
- **2026年3月〜**: Sibyl公開（「Inspired by The AI Scientist, FARS, and AutoResearch」と明記）

Karpathyのautoresearchが最も広く認知されたが、ARIS・AutoResearchClaw等は独立に開発が進行しており、「Karpathyの後続」ではなく**同一パラダイムの同時多発的出現**と捉えるべきである。これは技術的条件（Claude Code / Codexの長時間安定動作、MCP対応）が成熟し、パラダイムの実現可能性閾値を超えたタイミングの一致として理解できる。

人間の役割は「実行者」から「研究方針の定義者・承認者」へシフトしている。ただしこの恩恵はGPU実験で完結するMLタスクに限定され、ロボティクスの実機実験には直接適用できない点に注意が必要。

### 5.3 Markdownスキルベースの「軽量エージェントOS」

ARIS、claude-scholar、academic-research-skills等に共通するアーキテクチャは、フレームワークやデータベースに依存せず、純粋なMarkdownスキルファイルでエージェントの行動を制御する「軽量エージェントOS」パターンである。これにより、特定のLLMプロバイダやツールにロックインされず、Claude Code、Codex CLI、Cursor等の間でワークフローを移植可能になっている。この標準化は、我々のClaude Codeベースの論文執筆ワークフロー設計にも直接適用可能な設計パターンである。

### 5.4 プラットフォーム型の台頭と「AI for Science」の産業化

OpenAI Prism（無料）、FutureHouse/Edison Scientific（$70M調達）、Elicit（APIの公開）など、研究支援のプラットフォーム化・商業化が急速に進展している。OpenAI VP Kevin Weillの「2026年はAIと科学にとって、2025年がAIとソフトウェアエンジニアリングにとってそうであったような年になる」という発言は、この産業化の方向性を端的に示している。一方で、学術出版社・査読者からの「AI slop」（低品質AI生成論文の氾濫）への懸念も強まっており、透明性と品質保証の両立が今後の重要な課題である。

### 5.5 自己進化・反捏造メカニズムの実装

AutoResearchClawのMetaClaw（クロスラン知識転移）やSibylのOuter Loop（8カテゴリの問題分類→再利用可能スキル化）は、「研究パイプライン自体が実行から学習して改善する」自己進化パラダイムを実装している。これはAI Scientist v2のagentic tree searchをさらに推し進めたものであり、長期的には研究のメタ最適化を可能にする。

同時に、AutoResearchClawのVerifiedRegistry（実験データのground-truth強制、未検証数値の自動消去）やFARSのAI slop検出・7次元レビュースコアリングは、自律研究における「捏造」リスクに対する具体的な技術的対策を提示している。品質保証なき大量生産への懸念が高まる中、こうした反捏造メカニズムは今後のワークフロー設計で必須の要素となる。

### 5.6 進化的アルゴリズム探索の台頭

AlphaEvolve（Google DeepMind, 2025年5月）は、LLMの創造的問題解決能力と進化的計算を組み合わせた自律的アルゴリズム発見エージェントとして、Karpathyのautoresearchの理論的基盤を先行的に提供した。「評価関数さえ定義できれば任意の問題を自律的に最適化できる」というAlphaEvolveの設計原則は、Karpathyの「*any* metric you care about that is reasonably efficient to evaluate can be autoresearched by an agent swarm」という主張と本質的に同一であり、この設計パターンの汎用性が独立に検証されている。

### 5.7 RA-Lワークフローへの示唆（更新）

上記の動向を踏まえ、Claude Codeを用いたRA-L投稿ワークフローについて以下の更新された示唆が得られる。

1. **第3層はエージェント主導で設計可能**: PaperQA2やElicit APIを統合することで、関連研究リストの自動生成と差分分析をClaude Codeのスキルとして実装できる。
2. **クロスモデル対抗レビューを組み込むべき**: ARISが実証したexecutor-reviewer分離パターンを採用し、Claude CodeでドラフトしたセクションをGPT-5.x等で査読するループを構築する。
3. **第2層のロボティクス固有制約は変わらない**: UR5e実機実験のデータ取得・解釈は引き続き人間の責任。ARISの自律実験パラダイムはシミュレーション（MuJoCo等）には適用可能だが、実機実験には直接適用できない。
4. **Prismは補完ツールとして検討**: LaTeXコラボレーション環境としてPrismの活用は有望だが、カスタマイズ性の観点からClaude Codeベースのスキルアプローチとの使い分けが必要。
5. **ARISのWorkflow 3（論文執筆パイプライン）を参考設計として検討**: Claims-Evidence Matrix → 図表生成 → セクション別LaTeX → コンパイルの流れは、我々のワークフロー設計に直接参考にできる。

---

## 参考文献一覧

### 論文執筆エージェントに関する先行研究

1. Lu, C., Lu, C., Lange, R.T., Foerster, J., Clune, J., & Ha, D. (2024). The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery. arXiv:2408.06292. https://arxiv.org/abs/2408.06292
2. Sakana AI (2025). The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search. arXiv:2504.08066. https://arxiv.org/abs/2504.08066
3. Schmidgall, S., et al. (2025). Agent Laboratory: Using LLM Agents as Research Assistants. EMNLP 2025 Findings. arXiv:2501.04227. https://aclanthology.org/2025.findings-emnlp.320/
4. Schmidgall, S. & Moor, M. (2025). AgentRxiv: Towards Collaborative Autonomous Research. arXiv:2503.18102. https://agentrxiv.github.io/
5. Wang, Y., et al. (2024). AutoSurvey: Large Language Models Can Automatically Write Surveys. arXiv:2406.10252. https://arxiv.org/abs/2406.10252
6. Shao, Y., et al. (2024). Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models (STORM). NAACL 2024. arXiv:2402.14207. https://arxiv.org/abs/2402.14207
7. Wang, Q., et al. (2019). PaperRobot: Incremental Draft Generation of Scientific Ideas. arXiv:1905.07870. https://arxiv.org/abs/1905.07870

### 学術論文執筆のベストプラクティス

8. Swales, J.M. (1990). Genre Analysis: English in Academic and Research Settings. Cambridge University Press. CARSモデル解説: https://libguides.usc.edu/writingguide/CARS
9. PLOS Computational Biology (2025). How to write a scientific paper in fifteen steps. https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1013505
10. Cals, J.W.L. & Kotz, D. (2013). Successful Scientific Writing and Publishing: A Step-by-Step Approach. PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC6016396/
11. Black, M. (2024). Writing a good scientific paper. https://medium.com/@black_51980/writing-a-good-scientific-paper-c0f8af480c91
12. IEEE RA-L Information for Authors. https://www.ieee-ras.org/publications/ra-l/information-for-authors-ra-l
13. Bates College. How to Write a Paper in Scientific Journal Style and Format. https://www.bates.edu/biology/files/2010/06/How-to-Write-Guide-v10-2014.pdf
14. ACS Scientific Writing Resources. https://researcher-resources.acs.org/publish/scientific_writing

### 論文化されていないツール・プラットフォーム（本更新で追加）

15. OpenAI (2026). Introducing Prism. https://openai.com/index/introducing-prism/
16. FutureHouse (2025). Launching FutureHouse Platform: AI Agents for Scientific Discovery. https://www.futurehouse.org/research-announcements/launching-futurehouse-platform-ai-agents
17. FutureHouse (2024). PaperQA2: Superhuman Scientific Literature Search. https://www.futurehouse.org/research-announcements/wikicrow, arXiv:2409.13740
18. Elicit (2025). New in Elicit: Research Agents. https://elicit.com/blog/introducing-research-agent-workflows
19. Google DeepMind (2026). Accelerating Mathematical and Scientific Discovery with Gemini Deep Think. https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/
20. ARIS (Auto-Research-In-Sleep). https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep
21. claude-scholar. https://github.com/Galaxy-Dawn/claude-scholar
22. academic-research-skills. https://github.com/Imbad0202/academic-research-skills
23. Sibyl Research System. https://github.com/Sibyl-Research-Team/AutoResearch-SibylSystem
24. claude-scientific-writer / claude-scientific-skills. https://github.com/K-Dense-AI/claude-scientific-writer, https://github.com/K-Dense-AI/claude-scientific-skills
25. clo-author. https://github.com/hsantanna88/clo-author
26. Karpathy, A. (2026). autoresearch: AI agents running research on single-GPU nanochat training automatically. https://github.com/karpathy/autoresearch
27. Liu, J., Xia, P., Han, S., et al. (2026). AutoResearchClaw: Fully Autonomous Research from Idea to Paper. https://github.com/aiming-lab/AutoResearchClaw
28. Analemma (2026). FARS: Fully Automated Research System. https://analemma.ai/fars, https://github.com/fars-analemma
29. Tang, J., Xia, L., Li, Z., & Huang, C. (2025). AI-Researcher: Autonomous Scientific Innovation. NeurIPS 2025 Spotlight. arXiv:2505.18705. https://github.com/HKUDS/AI-Researcher
30. Novikov, A. et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery. Google DeepMind. arXiv:2506.13131. https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
31. OpenClaw (2025-2026). https://github.com/open-claw/open-claw（旧Clawdbot/Moltbot）
32. Sibyl Research System (AutoResearch-SibylSystem). https://github.com/Sibyl-Research-Team/AutoResearch-SibylSystem
