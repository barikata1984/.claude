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

## Literature Survey スキル改善 (2026-04-06)

- [x] ベストプラクティス文献に基づく乖離分析
- [x] コンテクスト・実行時間のコスト分析
- [x] Step 1: SKILL.md リファクタリング (references/ 分離)
- [x] Step 2: コンテクスト流入制御 (P2/P4/P5 統合)
- [x] Step 3: 乖離改善追加 (RQ, キーワード, 比較表, 用語, Threats to Validity 等)
- [x] Step 4: `scripts/resolve_dois.py` 新設
- [x] `scripts/extract_sections.py` 新設 + Phase 3 改訂
- [ ] テストケースでの実行評価
