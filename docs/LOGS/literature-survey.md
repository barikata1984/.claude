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
