# Literature Survey Execution Log

## 2026-04-06: Robotic Pick-and-Place — Grasping and Stable Object Placement

### Scope
- トピック: 物体の把持と安定配置（pick-and-place）
- 対象期間: 2020年以降
- 対象媒体: トップ会議・ジャーナル（CoRL, RSS, ICRA, IROS, NeurIPS, ICML, ICLR, T-RO, RA-L, Science Robotics等）
- Seed提案: 不要

### Search Process
- 5つの検索角度で並列サブエージェントを実行:
  1. Core pick-and-place (Semantic Scholar ×5, WebSearch ×3, OpenAlex ×2)
  2. Grasp planning + placement (Semantic Scholar ×7, WebSearch ×3)
  3. Sim-to-real + manipulation (Semantic Scholar ×4, WebSearch ×3)
  4. Foundation models + manipulation (Semantic Scholar ×4, WebSearch ×4)
  5. Object rearrangement + pose (Semantic Scholar ×7, WebSearch ×4)
- 合計約280件の候補を収集、重複約60件を排除、関連性フィルタリング後48本に絞込

### Output Files
- Survey report: `docs/SURVEYS/robotic_pick_and_place.md`
- Reference database: `docs/REFERENCES/MAIN.md` (48 entries)
- Survey index: `docs/SURVEYS/README.md`

### Key Findings
- **根本的未解決問題**: 汎化性・配置精度・物理的安定性の三要素を同時に満たすpick-and-placeシステムの実現
- **主要ギャップ**:
  1. 把持-配置の結合計画が多くの手法で未統合
  2. VLA/基盤モデルが物理的安定性の保証を欠く
  3. 閉ループ触覚フィードバックによる配置制御が未成熟
  4. 未知物理特性を持つ新規物体への安定配置汎化
  5. 安定中間配置を伴う長期多段再配置

### Categories
- A: Stable Placement Prediction (11 papers)
- B: Integrated Pick-and-Place (9 papers)
- C: Relational Object Rearrangement (10 papers)
- D: Generalist Robot Policies (8 papers)
- E: SE(3) Grasp & Motion Optimization (5 papers)
- F: Task Planning & Benchmarks (5 papers)

## 2026-04-07: F/T Sensor-Based Inertial Parameter Estimation and Placement Planning

**Scope**: F/Tセンサベース慣性パラメータ推定と安定配置計画への応用。全年次（1986-2026）、Tier分けで重み付け。Seed提案あり（3件）。

**Search**:

- 検索角度: 5（F/T推定主要, 安定配置+物理, サーベイ+引用, 動的励起手法, 隣接領域）
- 検索クエリ総数: ~130
- 重複除去前: ~130 → 重複除去後: 55
- OA論文32本は ar5iv/MDPI経由で全文分析、ペイウォール23本はアブストラクトベースで注釈

**Output**:

- レポート: `docs/SURVEYS/ft_estimation_placement.md` (55 papers, 7 categories, ~760 lines)
- MAIN.md: 48エントリ追加（412→828行）、DOI検証で6件の修正
- 中間データ: `docs/SURVEYS/_ft_estimation_placement_papers.json`, `_ft_estimation_placement_annotations.json`

**Key Findings**:

- **RQ2（新規性）確認**: F/Tベース慣性推定と安定配置計画を直接統合した先行研究は存在しない
- 最も近い研究: Nadeau et al. (2022, 推定) + Nadeau & Kelly (2025, 配置) — 同一グループだが未統合
- Lerner et al. (2024): F/Tフィードバック配置を実現するがCoM推定を含まない
- 3つのSeed提案: (1) End-to-end pipeline, (2) Uncertainty-aware placement, (3) Active CoM refinement

**Implications**:

- 研究提案の新規性が文献調査により裏付けられた
- Seed 1（Nadeau推定+Nadeau配置の統合）が最も直接的で実現可能性の高い出発点
- 推定精度→配置安定性の感度分析が最初の学術的貢献となりうる
- 非均一密度物体のベンチマーク作成も付随的貢献

---

## 2026-04-08: Deformable Object Physical Property Recovery from Observation and Robotic Manipulation

### Scope
- トピック: ビデオ・観察記録からの柔軟物物性復元（弾性率、粘性等）を含む3D再構築、F/Tセンサからの柔軟物物性推定、復元物性に基づくロボット操作
- 対象期間: 2020年以降（基盤的論文は2019年まで遡及）
- 除外: 剛体慣性パラメータ同定（前回サーベイで網羅済み）、外科手術応用（ユーザリクエスト）
- Seed提案: あり（3 seeds）

### Search Process
- 5つの検索角度で並列サブエージェントを実行:
  1. 視覚ベース物性復元（NeRF/3DGS + 微分可能物理）: ~38 WebSearch queries
  2. F/T・触覚ベース柔軟物物性推定: ~15 WebSearch queries
  3. 物性活用柔軟物操作: ~10 WebSearch queries
  4. サーベイ論文: ~13 WebSearch queries
  5. 特定手法・会場検索: ~16 WebSearch queries
- 合計約130クエリで92件の候補を収集、重複約35件を除去、52本に絞込
- ユーザレビューで外科手術系3本を除外 → 最終49本（後の整理で48本に確定）

### Output Files
- `docs/SURVEYS/deformable_physics_reconstruction.md` — メインレポート（48本、6カテゴリ）
- `docs/REFERENCES/MAIN.md` — Category G として48エントリ追加
- `docs/SURVEYS/README.md` — エントリ追加

### Key Findings

**RQ1（視覚観察からの物性復元）**: 2020年のFEM逆問題から2025年の3DGS+MPMデジタルツインへ急速に発展。MPMが支配的物理バックボーン、表現はNeRF→3DGSへ移行。フィードフォワード予測（VoMP, Vid2Sim）やVideo Diffusion蒸留（Physics3D, DreamPhysics）が2025年の新潮流。

**RQ2（F/T・力覚からの物性推定）**: 剛体慣性パラメータ同定と対照的に、**標準的な定式化が存在しない**。Hunt-Crossley（Patni2024）、VSF（Yao2023）、微分可能シミュレーション逆問題（Chen2025, DPSI）等が散発的に存在するのみ。

**RQ3（復元物性のロボット操作活用）**: **極めて少ない**。明示的物性同定→操作計画の完全パイプラインはDPSI（Yang et al., IJRR 2025）のみ。AdaptiGraph, RoboPack, RoboCraft, RAPiDはlatent動力学適応で間接的に物性を活用。

**RQ4（未解決ギャップ）**: (a) 視覚物性復元→操作の断絶、(b) F/Tベース柔軟物物性同定の標準定式化不在、(c) 不均一材料への未対応、(d) sim-to-real検証の不足、(e) 構成則自動選択のメタ問題。

### Reference Verification
- 48本中47本 PASS、1本 DOI typo修正（Liu2022_DiffRope: 3264749→3264766）
- Fan2025_PhysWorld のキー名を修正（lead author は Yang）

### Implications for Project

- **前回サーベイ（ft_estimation_placement）との接続**: 剛体の慣性パラメータ同定の知見（回帰行列、励起軌道、物理整合性制約）を柔軟物に移植する研究方向が、本サーベイのSeed 1として独立に導出された。これは前回サーベイのGap 2（推定→配置の接続不在）の柔軟物版に相当する。
- **Seed 1（F/Tベース構成則パラメータ回帰）**: 剛体のτ=Y(q,q̇,q̈)πに相当する柔軟物版の標準的回帰定式化は前例がなく、学術的新規性が高い
- **Seed 2（推定→操作パイプライン）**: DPSIが唯一の先行事例だが5分の推定時間はリアルタイム操作に不十分。高速化が実用上の鍵
- **Seed 3（不均一物性＋操作）**: Yao2023のVSFと前回サーベイのNadeau配置計画の統合が有望
