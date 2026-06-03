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
- [ ] concise 出力スタイル単体運用の効果観察（反復・冗長が抑制されるか）
  - 不足なら独自二条項（スコープ制約・反復禁止）の復活、または長さ上限 Stop フック追加
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
- [ ] 外部事実の検証節の実運用評価（検索すべき場面で実際に発火するか = 遵守率、empirical では測れない）
- [x] 批判的スタンス節の見出しを case A（タイミング主軸）に統一・目的語明確化・反証探索を削除（2026-06-03）
  - 主従不整合（土台＝役割主/増幅＝タイミング主）と導入文の二分法 vs 本文三分法を解消、目的語＝「批判」を明示
  - 「反証を最低 1 つ探す」を削除（重箱の隅の指摘で話が進まない）。empirical 2 iter で全 6 モード判定 ○・干渉課題解決・リグレッションなし、80 点で確定

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
