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
