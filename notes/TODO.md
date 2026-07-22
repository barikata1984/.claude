# TODO

## Skills の汎用化

- [x] commit/SKILL.md — `ros-o` ハードコードを削除
- [x] push/SKILL.md — `ros-o` ハードコードを削除
- [x] log-progress/SKILL.md — パスのハードコードをやめ、役割定義 + CLAUDE.md からのパス解決に書き換え
- [x] log-progress/SKILL.md — `.claude/rules/references.md` 参照を「存在する場合のみ」に緩和
- [x] wrap-up-session/SKILL.md — log-progress 変更に伴う調整（不要と確認）

## CLAUDE.md の整理

- [x] ユーザーレベル CLAUDE.md からプロジェクト固有の内容を分離
  - 移動対象: 注意事項、コンテナ環境、参照先、検証コマンド、学習・評価コマンド
  - 退避先: ~/_CLAUDE.md
- [x] ユーザーレベル CLAUDE.md にスクラッチプロジェクトの標準ドキュメント構成を明記

## 挙動制御フレームワーク

- [x] ドキュメント事前参照 (Doc-First) ハーネス導入 (2026-06-06)
  - `~/.claude/CLAUDE.md` に Doc-First 節追加, `~/.claude/doc-registry.md` 新規作成
  - EPT 検証 (2 iter + hold-out, 6/6 subagent が自発的に手順を実行, 精度 100% 収束)
  - 修正 2 件適用 (doc-registry のサンプル分離, 手順 3 の「1 回」削除)
- [ ] Doc-First の実運用評価 (実セッションで遵守されるか, EPT では測れない顕著性リスク)
- [ ] doc-registry.md にエントリを追加 (実際に使うハードウェア/ライブラリの参照先を登録)
- [x] CLAUDE.md 剪定 (153 → 124 行、2026-05-04)
- [x] `## 応答スコープ規約` セクション追加 (2026-05-04)
- [x] 日本語スタイル自己点検 directive を `## 日本語スタイル規約` に追加 (2026-05-04)
- [x] `~/.claude/hooks/stop-scope-check.sh` 実装、block mode で稼働 (2026-05-04)
- [x] `~/.claude/hooks/stop-taxonomy-check.sh` を warn-only から block へ昇格 (2026-05-04)
- [ ] 1-2 週間運用後、`scope-violation.log` と `taxonomy-warn.log` の偽陽性率レビュー
- [ ] レビュー結果に応じて scope-check のキーワード調整、または検出ロジック改良
- [x] 和文タイポグラフィ正規化フック実装（マスク方式、24 テスト全通過、2026-05-22）
  - `hooks/format_ja_typography.py` + `.sh` + テスト、`settings.json` PostToolUse 登録
  - 全角約物→半角・ASCII 不可侵・コード/数式/URL 保護、global 適用
- [x] 応答制御を concise 出力スタイルへ移行（2026-05-22）
  - 「1-3 文/preamble 禁止の組み込み既定」は非存在と確認（公式ドキュメント）
  - `output-styles/concise.md` 作成、応答スコープ規約から独自二条項を削除
- [x] concise 出力スタイル単体運用の効果観察（2026-07-02）
  - Opus 4.7/4.8 で Output style（システムプロンプト常駐）だけでは冗長ドリフトを抑止しきれないと判明
  - 対策: `/concise` スキル新規作成（recency bias を利用した会話内リマインダー、EPT 3 iter で応答プロトコルを 4 分岐に精緻化・unclear points 0 に収束）
  - 二段構え化: CLAUDE.md に `@~/.claude/skills/concise/SKILL.md` を常時ルールとして追加、settings.json から `outputStyle: "Concise"` を削除。`/concise` はドリフト時の明示リマインド用に維持
- [ ] 二段構え（CLAUDE.md 常時ルール + `/concise` 明示リマインド）の実運用評価（冗長ドリフトが実際に抑制されるか）
- [x] 反迎合「批判的スタンス」節を CLAUDE.md に追加（2026-05-29）
  - Web ベストプラクティス調査（役割再定義・問題先出し・立場表明・過剰補正の安全弁）
  - empirical-prompt-tuning で A/B 検証（4 シナリオ × 2 群、過剰補正なし・解除条項機能を確認）
- [ ] 批判的スタンス節の実運用での体感評価（迎合が出やすい主観判断の局面で効くか）
- [x] 過剰応答（未要求出力・喋りすぎ）への予防層導入（2026-05-30）
  - 機構検証: Stop hook の block=継続（撤回不可）、prompt/agent hook の実在、旧 stop-scope-check の機構的破綻を実証
  - 編集 A: concise.md にスコープ条項、編集 B: 批判的スタンス節を最優先ゲート化（構造改修）
  - A/B 3 iteration: ルーブリック汚染を発見しブラインド化、構造改修で S2/S3 改善・S1 残留（SQLi 指摘）はプロンプト層の天井
- [x] 批判的スタンス節を 3 層構成（土台/増幅/抑制）に再設計（2026-05-30）
  - 全面抑制をやめ「欠陥は指摘・展開はしない」へ。karpathy §1/§3 と整合確認
  - ブラインド A/B（独立判定者 + hold-out S2）: T-S1 漏れ（無問題の自発報告）を発見→土台 bullet を「気づいたときだけ・無ければ言わない」に修正し解消
  - S4 の指摘どまり/指摘+修正のブレは prompt 層の天井として 80 点で確定
- [ ] 予防層の実運用評価（未要求の批判・分析・蛇足が減るか、S1/S4 型の残留が許容範囲か）
- [x] under-retrieval 対策「外部事実の検証」節を CLAUDE.md に新設（段階 1、2026-05-30）
  - hallucination でなく under-retrieval と切り分け、批判的スタンス（対ユーザー態度）とは別軸（対・事実）で独立節化
  - 既存実装調査（Aedelon の classifier-gated injection、blueprint research-protocol、Anthropic 公式）
  - 設計: 強制は原理不可、事後ゲート却下、デーモン不採用、段階導入（指示 → 測定 → 必要なら軽量 hook）
  - empirical-prompt-tuning 5 シナリオ（検索すべき/不要/境界 ×2/under-trigger hold-out）全て意図通り・収束・文面修正不要
- [x] under-retrieval 対策「参照情報の検証」節を段階 1 → 段階 3 に強化（5 iter + hold-out, 収束, 2026-06-08）
  - 段階 1 の問題: トリガーが出力時（「述べるとき」）のため、内部知識で回答構成後に追認検索になる
  - 段階 2: 入力時トリガー + 免除条項を限定列挙化 + deep-research 閾値を「1–2 回」に具体化
  - 段階 3: 「**最初の行動: 検索**」に強化。行動順序で規定（思考順序の曖昧さを回避）
  - EPT 5 iter: 免除境界曖昧→解消、「構成する」曖昧→「書き始める」→「考える前に」→「最初の行動として」に収束
  - hold-out（asyncio.TaskGroup）: 精度 100%, 過適合なし
- [x] 「1–2 回の検索」計数単位の明確化（EPT 3 iter + hold-out, 収束, 2026-06-09）
  - 「1–2 回の検索」→「検索クエリを 1–2 回試みて」に変更 (参照情報の検証節 + Doc-First 節)
  - 「クエリ」の語義から WebSearch = 1 回, WebFetch = カウント外が自然導出される
- [x] 造語禁止ルールを CLAUDE.md に新設 (EPT 4 iter + hold-out, 全シナリオ精度 100% 収束, 2026-06-10)
  - 問題: エージェントが既存語で足りるのに独自造語を作り, 定義も共有せず対話が成立しない
  - iter 2: 「造語」の定義を明確化 (学術文献ヒット基準), 「〜性」禁止範囲を限定
  - iter 3: ブレスト局面でも解除しない旨を明示
  - hold-out (命名要求シナリオ): 仮称提案の escape hatch が正しく機能
- [ ] 造語禁止ルールの実運用評価 (ブレスト・研究議論で造語が抑制されるか, 正当な仮称提案は可能か)
- [x] 参照情報の検索規則を「全技術・科学的問い」に拡張 + 信頼度バイアス警告追加（2026-06-19）
  - カテゴリ列挙方式から「技術的・科学的な問いはすべて対象」に書き換え
  - EPT iter 1: 全 3 シナリオ 100% — ルール文面は明瞭、実問題は顕著性（salience）と判明
- [x] 顕著性対策: UserPromptSubmit + SubagentStart フック追加（2026-06-19）
  - `~/.claude/hooks/search-first-reminder.sh` — 毎ターン検索優先リマインダーを注入
  - `~/.claude/hooks/search-first-reminder-subagent.sh` — サブエージェント起動時にも注入
  - `settings.json` に UserPromptSubmit / SubagentStart フックとして登録
- [ ] 参照情報の検証節の実運用評価（検索すべき場面で実際に発火するか = 遵守率、empirical では測れない）
- [ ] request-source Sources ブロック自動付与の実運用評価（付与/非付与の判断精度、Sources の粒度が適切か）
- [x] 批判的スタンス節の見出しを case A（タイミング主軸）に統一・目的語明確化・反証探索を削除（2026-06-03）
  - 主従不整合（土台＝役割主/増幅＝タイミング主）と導入文の二分法 vs 本文三分法を解消、目的語＝「批判」を明示
  - 「反証を最低 1 つ探す」を削除（重箱の隅の指摘で話が進まない）。empirical 2 iter で全 6 モード判定 ○・干渉課題解決・リグレッションなし、80 点で確定
- [x] japanese-tech-writing スキル登録・常時読み込み化 + EPT (2026-06-17)
  - k16shikano gist をスキルとして登録, CLAUDE.md に @include 追加
  - EPT 2 iter + hold-out, 全シナリオ 100%, description 修正のみで収束
- [x] argument-gap-edit スキル登録 (2026-06-17)
- [x] CLAUDE.md 圧縮・統合 132 → 84 行 (2026-06-17)
  - Git Workflow + 標準ドキュメント構成を rules/workflow.md に移動
  - 「参照情報の検証」+「Doc-First」を「外部ソース事前参照」に統合
  - 統合節 EPT 3 シナリオ 100% 収束

## project-team スキル

### 設計（完了）

- [x] チーム構成の調査・設計（人間2名 + エージェント3体）
- [x] プロジェクトフェーズ構造の設計（Phase 0-8 + ループ A/B/C/D）
- [x] 運用モデルの決定（セッション・チェックイン方式 = モデルC）
- [x] ベストプラクティス文書の作成（`project-team-bestpractice.md`）
- [x] 既存エージェントSE rule of thumb との整合性検証・修正反映

### 実装

- [x] Step 1: エージェント定義 — `agents/pt-research.md`, `pt-engineer.md`, `pt-analyst.md`
- [x] Step 2: リファレンス — `references/handoff_protocol.md`, `phase_transitions.md`
- [x] Step 3: フェーズ定義 — `phases/phase1-research.md` 〜 `phase7-review.md`（6ファイル）
- [x] Step 4: `skills/project-team/SKILL.md`
- [x] Step 5: `settings.json` パーミッション更新（Step 4 で実施済み — `Edit/Write(~/.claude/skills/**)` 追加）

### 廃止・後継（2026-07-04）

- project-team スキル本体（フェーズ管理・ハンドオフ・状態ファイル）は `abff630` で未使用として削除済み。フェーズ/ハンドオフを伴う重量級設計自体が使われなかったのが敗因
- `agents/pt-engineer.md` / `pt-analyst.md` / `pt-research.md` のロール定義（実装・分析・調査の内容）は再利用価値ありと判断し、project-team 依存部分（Critique Mode, Phase, Handoff Notes）を除去して独立サブエージェント化
  - [x] `agents/engineer.md`（model: opus）, `agents/analyst.md`（model: opus）, `agents/researcher.md`（model: sonnet）を新規作成、pt-*.md は削除
  - [x] `rules/delegation.md` を新規作成 — ロール別ルーティング表 + 報告前レビュー方針
  - [x] `agents/writer.md`（model: sonnet）を追加、`researcher` から論文/提案書執筆タスクを分離（Opus 4.8 のライティング品質低下を確認したため文書作成用ロールを新設。他ロールと同じ frontmatter 機構であり「固定」という特別な機構ではない点は誤記を訂正済み）
  - [x] EPT iteration 1 実施（2026-07-04） — 実装/執筆/些細な修正の3シナリオで検証。些細な修正(100%)は正しく委譲回避、実装(33%)・執筆(63%)は委譲されず実行エージェントが自力完結。決定的診断: `rules/delegation.md` が本セッション中に作成されたファイルであるため、セッション開始時静的スナップショットの `~/.claude/rules/*.md` ロードに反映されておらず、今回の精度はルール文言の有効性を測るデータになっていない（詳細: `log_delegation_roles.md`）
  - [x] delegation.md ロード済み環境で EPT 再実行（2026-07-04） — 同じ3シナリオを iteration 1・2 で実行、6/6 シナリオとも正しいロールに委譲され精度100%、delegation.md 起因の新規 unclear points は2 iteration 連続で0件。収束と判定し文言修正なしで確定（詳細: `log_delegation_roles.md`）。副産物として Write ガードが `summary.md` のような正当な成果物パスもブロックする問題を再確認し ISSUES.md に追記
  - [x] Write ガード問題の深掘り調査・恒久対策（2026-07-04） — GitHub issues/Reddit/HN・公式ドキュメント・`settings.json` hooks を調査したが公開報告なし、PreToolUse ブロックの明示定義も未検出。モデル自身がファイル名パターンから「サブエージェントは所見をテキストで返すべき」という規範を内面化している可能性が高いと判断。調査過程で EPT シナリオB設計自体がユーザー想定の運用思想（出口はインターフェースエージェント＝メインループが検証してから保存）と食い違っていたと判明し、`agents/writer.md` の tools を Read/Grep のみに制限、`rules/delegation.md` の報告前レビュー条項に writer の制約を追記（詳細: `log_delegation_roles.md`）
  - [x] 再検証1（scenB4）で多段階委譲時の新問題を発見（2026-07-04） — writer 自身は Write を試みなくなったが、委譲元（代理メインループ役のサブエージェント）自身が同じ Write ガードでブロックされることが判明。中間委譲元も真のメインループの権限を持たないという構造的限界（詳細: `log_delegation_roles.md`）
  - [x] 再検証2（scenB5）でシナリオをテキスト完結型に再設計し再実行（2026-07-04） — ファイル保存を求めないシナリオに変更した結果、Write ガードに一切遭遇せず、委譲判断・報告前レビューとも精度100%で確認（詳細: `log_delegation_roles.md`）
  - [x] `agents/engineer.md`・`agents/analyst.md` の `model` を `opus` から `fable` に変更（2026-07-08） — fable のエイリアス有効性、無効値のサイレントフォールバック仕様、使用制限時の非フォールバック挙動を公式ドキュメントで確認（詳細: `log_delegation_roles.md`）
  - [ ] fable 運用後の使用制限到達頻度を観察（頻発する場合は `model:` 指定を opus/sonnet へ見直し）
  - [ ] 次回 EPT では `run_in_background: false` の逐次実行、または usage meta 取得手段を確保してから定量指標（tool_uses/duration_ms）を測定する（今回は並列実行のため両 iteration とも未測定）
  - [ ] 多段階委譲を検証する EPT は、成果物のファイル保存を求めずテキスト完結型のシナリオ設計にして Write ガードとの交絡を避ける
  - [x] `rules/delegation.md` を除外リスト方式から allow-list/default-deny 方式に改訂（2026-07-09） — メインループの自力実行によるトークン浪費対策、EPT 4 iteration で収束（詳細: `log_delegation_roles.md`）
  - [ ] allow-list/default-deny 方式の実運用評価（メインループの自力実行が実際に減るか、(a)/(b) の境界判断で EPT 未検証のエッジケースが顕在化しないか）

## Agent Teams

- [x] Agent Teams 機能の調査・検証（環境変数、TeamCreate スキーマ、公式ドキュメント）
- [x] `~/.claude/rules/agent-teams.md` 作成（トリガー条件・ワークフロー・ベストプラクティス）
- [x] empirical-prompt-tuning による検証（4 iter + hold-out、精度 100% 収束、修正 2 件適用）
- [x] サブエージェント完了報告ルール追加（2026-07-02） — spawn 時プロンプトに「完了時 SendMessage で報告せよ」を含める旨を明記、催促の往復を削減
- [ ] 実運用での効果観察（TeamCreate が適切な場面で自動発火するか）

## Literature Survey

- [x] Robotic Pick-and-Place: Grasping and Stable Object Placement (2026-04-06)
  - 48論文収録、6カテゴリ、Survey Findings (thesis/foundation/progress/gap) 完了
  - 出力: `docs/SURVEYS/robotic_pick_and_place.md`, `docs/REFERENCES/MAIN.md`

## academic-search MCP サーバー

- [x] クレデンシャル隔離ベストプラクティス文書作成
- [x] academic-search MCP サーバー実装 (search_semantic_scholar + resolve_oa_url)
- [x] SKILL.md 更新 (MCP ツール参照 + OA パイプライン)
- [x] クレデンシャル隔離検証
- [x] `pass insert api/unpaywall-email` で Unpaywall 用メールアドレス登録
- [x] Phase 3a/3b 分割 (OA 論文を先行処理、ペイウォール論文を出版社グループ単位でバッチ処理)

- [x] Dynamic Manipulation with CoM and Inertia Tensor (2026-04-06)
  - 50論文収録、5カテゴリ (Pushing/Estimation/Grasping/In-hand Dynamic/Extrinsic Dexterity)
  - Survey Findings (thesis/foundation/progress/gap) 完了
  - 出力: `docs/SURVEYS/dynamic_manipulation_com_inertia.md`

- [x] robotic_pick_and_place.md レビュー・修正 (2026-04-07)
  - 用語統一（サブミリメートル→1mm以下）
  - 6-DoFusion limit/Gap 精密化（ground-truth SDF前提、推定SDFロバスト性未検証）
  - Nadeau & Kelly limit/Gap 精密化（CAD形状+一律密度仮定、推定慣性パラメータ感度分析未実施）
  - UOP-Net/AnyPlace limit 追加（訓練データの物理特性ランダマイズ未報告、幾何重心/質量重心乖離への非対応）
  - Gap 4 再構成（事前知識の種類と推定困難度の区別を明確化）

- [x] F/Tセンサ × 安定配置計画 文献調査 (2026-04-07)
  - 55論文収録、7カテゴリ (Classical/Online/Consistency/Cobot/Placement/Adjacent/Survey)
  - 新規性確認: F/T推定×配置計画の統合研究は存在しない
  - Seed 3件提案 (End-to-end pipeline, Uncertainty-aware placement, Active CoM refinement)
  - 出力: `docs/SURVEYS/ft_estimation_placement.md`
- [ ] literature-survey スキル改善 (ISSUES 反映)
  - [x] Subagent Model Policy 追加（ミドルクラスモデル指定）
  - [x] Issue #5 (Paywall 判断): OA カバレッジ分析 + 推奨生成を SKILL.md に適用 → Issue 解消
  - [x] Issue #3 (コンテキスト予算): Fix を「コンテキスト保護設計」に書き直し（ISSUES.md）
  - [x] Issue #4 (DOI 検証遅延): Fix を実態に合わせて書き直し（ISSUES.md）
  - [x] 出力パスを `literature/` 配下に統合 (2026-04-21)
  - [ ] `rules/references.md` の `docs/REFERENCES/MAIN.md` パスを `literature/references/main.md` に更新
  - [ ] Issue #2 (並列サブエージェント): Phase 2 への最大3並列制限を SKILL.md に適用
  - [ ] Issue #3: 対策案を SKILL.md に適用
  - [ ] Issue #4: Phase 6 の失敗モード調査（ログ・中間ファイルへのアクセスが必要）

## スキルエイリアス

- [x] ラッパースキル方式でエイリアス作成 (`/fta` → `/fault-tree-debug`, `/ept` → `/empirical-prompt-tuning`)
- [ ] エイリアス経由での呼び出しが本体スキルを正しく転送するか実運用確認

## plan-to-implement スキル

### 設計（完了）

- [x] チーム分割 vs 単一サブエージェントのトリアージ判断のギャップ特定（`agent-teams.md` はチーム編成の機構のみ定義）
- [x] 置き場所をスキルに決定（ルールでなくスキル、`/implement` から起動可能・合成可能なことを理由に）
- [x] トリアージゲート設計（2問: 広さ/深さ、継ぎ目の名指し可否）
- [x] 機能主導のインターフェース交渉フロー設計（星型トポロジ、ハブ=インターフェース担当、≤3ラウンド収束、非収束時のエスカレーション）
- [x] ロードマップ策定（v1=Stage1+/implement、Stage2=critical、Stage3/4/agent-teams一行=条件付き）

### 実装

- [x] Stage 1（交渉フロー）の起草（2026-07-02） — `plan-to-implement/SKILL.md`（本体オーケストレータ）+ `implement/SKILL.md`（薄いラッパ、wrap-up-session と同じ委譲パターン）を新規作成
- [x] 起草後、ept（empirical-prompt-tuning）で検証（2026-07-02） — 5 iteration・8 シナリオ全て accuracy 100%、6 failure pattern を検出・修正、実質収束（詳細は `log_plan-to-implement.md`）
- [x] 探索フェーズ扱い（明示フェーズか暗黙の下準備か）の決定（2026-07-02） — 明示フェーズ（Phase 0）に決定、read-only は Explore agent type で実現
- [ ] Stage 2（トリアージ・非収束処理の硬化） — 使いながら判断（保留、実運用での必要性次第で着手）
- [ ] Stage 3（大 N の再帰的メタ分割） — 使いながら判断（保留、同上）

## Literature Survey スキル改善 (2026-04-06)

- [x] ベストプラクティス文献に基づく乖離分析
- [x] コンテクスト・実行時間のコスト分析
- [x] Step 1: SKILL.md リファクタリング (references/ 分離)
- [x] Step 2: コンテクスト流入制御 (P2/P4/P5 統合)
- [x] Step 3: 乖離改善追加 (RQ, キーワード, 比較表, 用語, Threats to Validity 等)
- [x] Step 4: `scripts/resolve_dois.py` 新設
- [x] `scripts/extract_sections.py` 新設 + Phase 3 改訂
- [x] テストケースでの実行評価 → empirical prompt tuning で代替 (2026-04-21)
- [x] empirical prompt tuning による SKILL.md 堅牢化 (2026-04-21, 8 iterations, 精度 100% 収束)

## log-progress 再設計 (2026-07-20)

- [ ] 新 log-progress の実運用観察: 議事録の質・発動の安定性。特に短い依頼 (「議事録書いて」「DECISIONS に反映」) ([議事録](LOGS/2026-07-20_log-progress-redesign.md))

## サブエージェント実行モード (2026-07-20)

- [ ] 実行モード則 + log-progress wrap-up 例外の実運用観察: standalone/wrap-up で background/同期が正しく分岐するか ([議事録](LOGS/2026-07-20_subagent-execution-mode.md))

## japanese-tech-writing 会話応答適用 (2026-07-22)

- [ ] 試験投入の実運用観察: メイン (Fable/Opus) で失敗モード (長文化・メタ文・整形滲み) が出ないか、である調転換を許容するか。sonnet 系サブエージェント (writer 等) の原稿化滲みも監視 ([議事録](LOGS/2026-07-22_japanese-tech-writing-conversational.md))
- [ ] 論点が溜まれば再設計版 EPT: 判定型指標で床効果回避、対象 Fable/Opus、OFF/静的のみ/静的+注入の 3 腕 ([議事録](LOGS/2026-07-22_japanese-tech-writing-conversational.md))
