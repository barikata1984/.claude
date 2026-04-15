# Research Framing 出力: 研究・提案の方向づけ
<!-- generated: 2026-03-27 -->
<!-- mode: B -->
<!-- status: complete -->
<!-- literature-survey-report: docs/SURVEYS/explicit_physical_properties_manipulation.md -->

## A1: Take-home message

By conditioning a Transformer-based manipulation policy on interpretable physical quantities — inertia, friction, shape, and 6D pose — the policy acquires object-aware representations that generalize to unseen rigid bodies without scaling demonstration data.

## A2: Contribution statement

1. Existing approaches to object generalization in imitation learning either scale demonstration data across object instances or adapt implicitly via latent embeddings, but no prior work conditions manipulation policies on explicit, physically interpretable quantities alongside structured geometric state.
2. We propose conditioning a Transformer-based manipulation policy (ACT) on interpretable physical quantities — inertia, friction, and object shape via a point-cloud pre-encoder — together with 6D object pose in the camera frame, replacing RGB observations entirely.
3. Experiments on rigid-body pushing tasks demonstrate that explicit physical conditioning improves object generalization — measured as success rate on unseen objects pushed to target positions — compared to the pose-only baseline.
4. Analysis of Transformer self-attention maps reveals which physical input modalities are decision-relevant for pushing, providing empirical evidence for the minimum-necessary sensing requirements.

## A3: 研究ポジショニング（CARS骨格）

### Move 1: Territory
Robot manipulation policy learning has increasingly focused on object-level generalization — enabling a single policy to handle diverse objects without per-instance demonstration. Two dominant strategies have emerged: scaling demonstration data across object variations, and injecting structural priors into policy representations. The latter has split into two parallel lines: conditioning policies on physical parameters for dynamics-aware adaptation, and replacing raw image observations with structured geometric representations such as 6D pose trajectories, point clouds, or semantic keypoints for spatial generalization. Physical parameter conditioning, originating with UP-OSI and consolidated by RMA, trains policies on privileged physical quantities in simulation and distills that conditioning into online estimators. Structured geometric approaches, exemplified by SPOT and DP3, have eliminated RGB inputs entirely, achieving robust spatial and instance-level generalization.

### Move 2: Niche
However, these two lines have developed in isolation. Physical parameter methods use proprioceptive or latent embeddings but lack structured object representations, while pose-based methods capture geometry but have no mechanism for incorporating physical dynamics such as mass, friction, or inertia. No existing work conditions a manipulation policy simultaneously on interpretable physical quantities and structured 6D pose — leaving object generalization either geometrically or dynamically grounded, but never both. Bridging these two lines without resorting to data scaling is critical, as demonstration collection remains the primary bottleneck for real-world deployment.
<!-- 参照: docs/SURVEYS/explicit_physical_properties_manipulation.md → Survey Findings → Gap -->

### Move 3: Occupation
We address this gap by conditioning a Transformer-based imitation learning policy on both interpretable physical quantities — inertia, friction, and shape — and 6D object pose, demonstrating that this combination enables object-aware representations that generalize to unseen rigid bodies in pushing tasks without scaling demonstration data.

### CARS統合骨格（Introduction第1〜2段落の原型）
Robot manipulation policy learning has increasingly focused on object-level generalization — enabling a single policy to handle diverse objects without per-instance demonstration. Two dominant strategies have emerged: scaling demonstration data across object variations, and injecting structural priors into policy representations. The latter has split into two parallel lines: conditioning policies on physical parameters for dynamics-aware adaptation, and replacing raw image observations with structured geometric representations such as 6D pose trajectories, point clouds, or semantic keypoints for spatial generalization. Physical parameter conditioning, originating with UP-OSI and consolidated by RMA, trains policies on privileged physical quantities in simulation and distills that conditioning into online estimators. Structured geometric approaches, exemplified by SPOT and DP3, have eliminated RGB inputs entirely, achieving robust spatial and instance-level generalization. However, these two lines have developed in isolation. Physical parameter methods use proprioceptive or latent embeddings but lack structured object representations, while pose-based methods capture geometry but have no mechanism for incorporating physical dynamics such as mass, friction, or inertia. No existing work conditions a manipulation policy simultaneously on interpretable physical quantities and structured 6D pose — leaving object generalization either geometrically or dynamically grounded, but never both. Bridging these two lines without resorting to data scaling is critical, as demonstration collection remains the primary bottleneck for real-world deployment. We address this gap by conditioning a Transformer-based imitation learning policy on both interpretable physical quantities — inertia, friction, and shape — and 6D object pose, demonstrating that this combination enables object-aware representations that generalize to unseen rigid bodies in pushing tasks without scaling demonstration data.

## Phase Bへの引き継ぎ情報

### B1（技術アプローチの選定）で参照すべき先行研究
<!-- docs/SURVEYS/explicit_physical_properties_manipulation.md の Paper Catalogue から抽出 -->

**ベースアーキテクチャ:**
- [[Zhao2023_act]](docs/REFERENCES/MAIN.md#Zhao2023_act) — ACT: Action Chunking with Transformers (base policy)
- [[Chi2023_diffusion_policy]](docs/REFERENCES/MAIN.md#Chi2023_diffusion_policy) — Diffusion Policy (alternative backbone)

**物理パラメータ条件づけの先行手法:**
- [[Yu2017_uposi]](docs/REFERENCES/MAIN.md#Yu2017_uposi) — UP-OSI: 明示的物理パラメータ条件づけの原点
- [[Kumar2021_rma]](docs/REFERENCES/MAIN.md#Kumar2021_rma) — RMA: privileged training → online adaptation パラダイム
- [[Liang2024_rma2]](docs/REFERENCES/MAIN.md#Liang2024_rma2) — RMA2: RMAの操作への拡張
- [[Memmel2024_asid]](docs/REFERENCES/MAIN.md#Memmel2024_asid) — ASID: 能動的物理パラメータ同定

**ポーズベース / 物体中心ポリシー:**
- [[Hsu2024_spot]](docs/REFERENCES/MAIN.md#Hsu2024_spot) — SPOT: SE(3)ポーズ軌跡でRGB不使用
- [[Ze2024_dp3]](docs/REFERENCES/MAIN.md#Ze2024_dp3) — DP3: 点群入力Diffusion Policy
- [[Sun2025_prism_dp]](docs/REFERENCES/MAIN.md#Sun2025_prism_dp) — PRISM-DP: ポーズベースDiffusion Policy

**押し動作 / 物理推論:**
- [[Li2018_pushnet]](docs/REFERENCES/MAIN.md#Li2018_pushnet) — Push-Net: 物性未知での押し動作
- [[Xu2019_densephysnet]](docs/REFERENCES/MAIN.md#Xu2019_densephysnet) — DensePhysNet: 密な物理表現
- [[Li2025_pinwm]](docs/REFERENCES/MAIN.md#Li2025_pinwm) — PIN-WM: 物理情報世界モデルで押し動作

**物性推定:**
- [[Chen2025_proprioception]](docs/REFERENCES/MAIN.md#Chen2025_proprioception) — 固有覚から質量・弾性率を推定
- [[Jatavallabhula2021_gradsim]](docs/REFERENCES/MAIN.md#Jatavallabhula2021_gradsim) — gradSim: 微分可能物理+レンダリング

### ベースライン候補（比較・アブレーション設計の起点）
<!-- A2の差分記述と文献調査のGapから抽出 -->

| ベースライン | 構成 | 目的 |
|------------|------|------|
| ACT + 6D pose (RGB無し) | 提案手法から物理量を除去 | 物理量追加の効果を分離 |
| ACT + RGB | 標準ACT | ポーズベース入力 vs. RGB入力の比較 |
| ACT + 6D pose + latent embedding | 物理量を潜在ベクトルに置換 | 明示的 vs. 暗黙的物理表現の比較 |
| ACT + 6D pose + inertia only | 単一物理量のみ | 各物理量の個別貢献（アブレーション） |
| ACT + 6D pose + friction only | 同上 | 同上 |

### 未解決の問題・検討事項

1. **物理量の取得方法**: 慣性・摩擦は実験環境でどのように計測・提供するか。シミュレータのground truth使用か、推定モジュール（Chen2025等）の併用か
2. **点群プレエンコーダの設計**: 物体形状を点群NNで符号化する具体的なアーキテクチャ（PointNet, PointNet++等）の選定
3. **注意ヒートマップ分析の位置づけ**: Contribution 4としてトップティアに昇格するか、補足的な分析にとどめるか — 実験結果の質による
4. **実機転移**: シミュレーション実験のみか、実機（UR5e）での検証も含めるか
5. **デモデータの収集規模**: 押し動作のデモ数と物体バリエーション数の設計
