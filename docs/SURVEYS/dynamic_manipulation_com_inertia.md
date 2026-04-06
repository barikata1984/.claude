# Literature Survey: Dynamic Manipulation with CoM and Inertia Tensor

| | |
|---|---|
| **Date** | 2026-04-06 |
| **Scope** | マニピュレータによる push / grasp / swing-up 操作における CoM・慣性テンソルの活用（運動学ベース把持含む） |
| **Papers found** | 50 |
| **Research Questions** | RQ1: 主要なアルゴリズムアプローチの大別 / RQ2: 物体動力学の計画・制御への組み込み方 / RQ3: 評価環境と再現実装の容易さ |

## Abstract

ロボットマニピュレータによるプッシュ・把持・スイングアップ操作において、物体の重心（CoM）や慣性テンソルといった質量特性をどう活用するかは、1980 年代の Mason の pushing mechanics 以来の古典的かつ継続的な研究課題である。本サーベイでは 2010 年以降を重点に 50 本の論文を体系的に収集・分析し、5 つのアプローチカテゴリ（A. プッシュ力学・接触モデリング、B. 慣性パラメータ推定、C. 把持品質・物理情報把持、D. インハンド動的操作、E. 外的器用さ・接触活用）に整理した。主要な知見として、解析的接触モデルからデータ駆動・微分可能物理シミュレーションへの移行、CoM/慣性のオンライン推定と操作計画の統合、および重力・環境接触の積極的活用（外的器用さ）が近年の三大トレンドであることを特定した。検索は WebSearch、Semantic Scholar API、arXiv API を含む 5 つの検索角度・112 クエリで実施し、重複排除後にユーザーレビューを経て確定した。

## Research Landscape Overview

ロボット操作における物体の動力学的性質（質量、重心位置、慣性テンソル）の活用は、Mason (1986) のプッシュ力学の定式化と Goyal et al. (1991) の limit surface 理論に端を発する。これらの基盤的研究は、摩擦接触下での物体運動を幾何学的に特徴づけ、その後の quasi-static プッシュ計画（Lynch & Mason 1996）や動的非把持操作（Lynch & Mason 1999）の理論的基盤を形成した。

2010 年代には、MIT の Bauza & Rodriguez グループによる大規模プッシュデータセット（Yu et al. 2016）と確率的データ駆動モデル（Bauza & Rodriguez 2017）が、解析モデルの限界を実証的に明らかにし、学習ベースのアプローチへの転換を促した。同時期に、Ferrari & Canny (1992) の把持品質メトリクスを基盤とした物理情報付き把持計画（Dex-Net 2.0, Mahler et al. 2017）が大きな影響力を持った。

2020 年代に入り、微分可能物理シミュレーション（Song & Boularias 2020; Le Cleac'h et al. 2022）、触覚センシングによる動的スイングアップ（SwingBot, Wang et al. 2020）、および外的器用さの学習（Zhou & Held 2022）といった新しい方向性が急速に発展している。主要発表会場は ICRA、IROS、RSS、CoRL、T-RO、IJRR、RA-L である。

## Terminology and Background

| Term | Synonyms / Variants | Scope in this survey |
|------|---------------------|----------------------|
| Center of Mass (CoM) | Center of Gravity (CoG), centroid, mass center | 物体の質量中心。把持計画での安定性評価、プッシュでの回転予測に使用 |
| Inertia Tensor | Moment of inertia, rotational inertia, inertia matrix | 物体の回転慣性。スイングアップ・ピボット制御、衝突安全性評価に使用 |
| Limit Surface | Friction limit surface, motion cone boundary | プッシュ接触における力・モーメント空間の凸境界（Goyal 1991） |
| Grasp Wrench Space (GWS) | Grasp wrench set | 把持接触が生成可能なレンチの凸包。把持品質評価の基盤 |
| Non-prehensile Manipulation | Pushing, tumbling, pivoting, sliding | 把持せずに物体を操作する手法群 |
| Extrinsic Dexterity | Environmental exploitation | 重力・環境接触など手の外部リソースを活用する操作戦略 |
| Quasi-static | Slow manipulation, negligible inertia | 慣性力を無視できる低速操作の仮定。多くのプッシュ・ピボットモデルの前提 |
| Differentiable Physics | Differentiable simulation | 物理シミュレーションの勾配を解析的に計算し、パラメータ推定や計画に活用 |

## Survey Findings

### Thesis

本分野の根本的な未解決問題は、**物体の動力学パラメータ（CoM・慣性テンソル・摩擦係数）の事前知識なしに、動的操作タスクを確実に遂行する方法の確立**である。解析的モデル（Mason 1986, Goyal 1991）は既知パラメータを前提とし、データ駆動モデル（Bauza 2017, Li 2018）はパラメータ推定を回避するが汎化に限界がある。近年の微分可能物理（Song 2020）やアクティブ推定（Dutta 2023）は両者の橋渡しを試みるが、リアルタイム性と精度のトレードオフは未解決である。

### Foundation

調査対象の手法が依拠する共通の技術的基盤:

1. **Limit Surface / Motion Cone**: Goyal (1991) の limit surface 理論は、プッシュ操作における物体運動の予測基盤として Category A の大部分が依存する。楕円体近似が広く採用されるが、Yu (2016) のデータセットはその限界を実証している。

2. **Grasp Wrench Space (GWS)**: Ferrari & Canny (1992) のメトリクスは Category C の標準的品質評価基盤。Borst (2004) の Task Wrench Space によりタスク依存性が導入された。

3. **Quasi-static 仮定**: Category A, D の多くの手法が準静的仮定に依存。Hogan (2020), Moura (2022) のMPC手法、Shirai (2023) のピボット最適化がこれに該当する。

4. **Coulomb 摩擦モデル**: 接触力学の基盤として全カテゴリで使用。摩擦円錐とその相補性制約が、プッシュ計画（Moura 2022）やピボット制御（Shirai 2023）の定式化を支える。

5. **触覚センシング**: Category D, E の近年の手法（SwingBot 2020, Bi 2021, Toskov 2022）が GelSight 等の視触覚センサに依存し、物理特性の暗黙的推定を実現。

### Progress

主要な技術的進展の軌跡:

1. **解析的プッシュモデルの確立** (1986-1996): Mason (1986) が pusher-slider 系の力学を定式化、Goyal (1991) が limit surface を導入、Lynch & Mason (1996) が安定プッシュの制御可能性を証明。

2. **データ駆動プッシュモデルの台頭** (2016-2018): Yu et al. (2016) の 100万件データセットが解析モデルの仮定の限界を実証。Bauza & Rodriguez (2017) のヘテロスケダスティック GP が入力依存ノイズをモデル化し、Ajay et al. (2018) がハイブリッドモデル（解析＋ニューラル残差）を提案。

3. **微分可能物理シミュレーションの導入** (2020-2022): Song & Boularias (2020) が LCP の解析勾配を導出し、未知物体の質量・摩擦分布を効率的に推定。Le Cleac'h et al. (2022) が NeRF と微分可能物理の統合を実現。

4. **把持品質の物理情報化** (2013-2025): Kim (2013) が動力学シミュレーション＋姿勢不確実性の組み合わせの必要性を実証。Mahler (2017) の Dex-Net 2.0 が合成データ＋解析メトリクスで深層学習把持を確立。PhyGrasp (2024) が LMM による物理常識推論を導入。

5. **ピボット操作の体系化** (2014-2023): Chavan-Dafle (2014) が外的器用さの概念を体系化。Viña (2015, 2016) が重力スリップの適応制御を確立。Shirai (2023) が接触暗黙双レベル最適化で不確実性下のロバスト性を実現。

6. **触覚駆動のスイングアップ** (2020-2021): SwingBot (2020) が触覚探索から物理特徴埋め込みを学習。Bi (2021) がゼロショット sim-to-real 転移を達成。

### Gap

1. **Quasi-static 仮定の壁**

Category A（プッシュ計画）と Category D（ピボット操作）の大部分が準静的仮定に依存しているが、実際の産業応用では高速操作が求められる。Hogan (2020), Moura (2022), Shirai (2023) のいずれも明示的にこの制約を認めている。準静的から動的操作への拡張は、接触モード遷移の組合せ爆発と非滑らかな動力学のモデリングという二重の困難を伴い、高速プッシュやスイングアップの統一的な計画フレームワークは存在しない。この壁を越えることで、サイクルタイムの短縮と操作可能な物体クラスの拡大が実現する。

2. **3D 慣性パラメータの推定困難**

Category B が示すように、平面プッシュからの慣性推定は 2D パラメータ（質量、2D CoM、回転慣性）に限定される（Mavrakis 2020 survey）。3 軸すべての慣性テンソル成分を推定するには、物体を把持して 3D 運動を励起する必要があるが（Nadeau 2022, Atkeson 1986）、これは安全性と計測精度のトレードオフを生む。VLM による物理常識推論（PhyGrasp 2024）は有望だが、定量的精度は未検証である。

3. **把持品質メトリクスと実世界成功率の乖離**

Category C の Roa & Suárez (2014) のサーベイが指摘するように、既存の把持品質メトリクスは互いに矛盾する最適解を生み、実世界の把持成功率との相関が弱い。Kim (2013) は動力学＋不確実性の同時考慮が必須であることを示したが、計算コストが高い。Chen (2023) の微分可能 GWS は高速化に貢献するが、局所最適の問題を認めている。

4. **触覚ベース手法の汎化限界**

Category D の触覚駆動手法（SwingBot 2020, Bi 2021, Toskov 2022）は特定のタスク・センサ・物体クラスで実証されているが、汎化が限定的である。SwingBot は単一タスクでのみ検証、Bi は平面運動に制約、Toskov はプリズム形状に限定。触覚表現の転移可能性は未確立であり、多様なタスクに共通の物理特徴空間の構築が課題である。

5. **オンライン推定と計画の統合**

Category A と B の交差領域において、物体パラメータの推定と操作計画を同時に行うフレームワークは限定的である。Dutta (2023) のアクティブ推定は情報利得ベースの探索行動を選択するが、推定と最終タスク達成の同時最適化は行わない。推定の不確実性を直接操作計画に反映するロバスト計画（Jankowski 2024）は有望だが、非平面タスクへの拡張は未達成である。

## Paper Catalogue

### Category Overview

本サーベイの 50 論文を以下の 5 カテゴリに分類した。

| Category | Description | Count |
|----------|-------------|-------|
| A. Pushing Mechanics & Contact Modeling | プッシュ操作の物理モデル、データ駆動モデル、計画手法 | 13 |
| B. Inertial Parameter Estimation | 操作を通じた物体の質量特性推定 | 7 |
| C. Grasp Planning & Quality Metrics | 把持品質評価と物理情報に基づく把持計画 | 11 |
| D. In-hand Dynamic Manipulation | ピボット、スイングアップ、スライディング等の手内動的操作 | 13 |
| E. Extrinsic Dexterity & Contact-rich Planning | 環境接触・重力を活用した操作戦略 | 6 |

### Comparison Table

| Paper | Category | Task | Sensors | Sim/Real | CoM/Inertia Role | Code |
|-------|----------|------|---------|----------|-------------------|------|
| Mason 1986 | A | Push | None (analytical) | T | 圧力分布→回転中心 | No |
| Goyal 1991 | A | Push/Slide | None (analytical) | T | Limit surface 構成 | No |
| Lynch & Mason 1996 | A | Push | None (analytical) | B | 安定プッシュ条件 | No |
| Bauza & Rodriguez 2017 | A | Push | Vicon | B | GP で暗黙的 | No |
| Hogan & Rodriguez 2020 | A | Push | Vicon | B | 楕円体 limit surface | No |
| Song & Boularias 2020 | A | Push/Slide | RGB-D | B | 質量・摩擦の空間分布推定 | Yes |
| Moura et al. 2022 | A | Push | — | B | MPCC の接触制約 | No |
| Atkeson et al. 1986 | B | Grasp/Lift | F/T | R | 最小二乗推定 | No |
| Nadeau et al. 2022 | B | Grasp/Lift | F/T | R | PMD + 重力優位推定 | Yes |
| Dutta et al. 2023 | B | Push | Tactile+RGB-D | B | アクティブ推定 | No |
| Ferrari & Canny 1992 | C | Grasp | None (analytical) | T | GWS 内接球 | No |
| Mahler et al. 2017 | C | Grasp | Depth | B | ε品質 + 重力レンチ | Yes |
| Feng et al. 2020 | C | Grasp | Tactile+F/T | R | CoM オフセット推定→リグラスプ | No |
| Chen et al. 2023 | C | Grasp | — | S | 微分可能 GWS 境界 | Yes |
| Chavan-Dafle et al. 2014 | E | Regrasp | — | R | 重力・慣性による手内操作 | No |
| SwingBot 2020 | D | Swing-up | GelSight | R | 触覚→物理特徴埋め込み | No |
| Bi et al. 2021 | D | Swing-up | Tactile | B | Sim-to-real 触覚制御 | No |
| Shirai et al. 2023 | D | Pivot | F/T | B | 摩擦安定余裕の最大化 | No |
| PhyGrasp 2024 | C | Grasp | Point cloud | S | LMM 物理常識推論 | Yes |
| Zhou & Held 2022 | E | Grasp | — | B | RL で環境接触を学習 | Yes |

Evidence level: **R** = Real, **S** = Simulation, **B** = Both, **T** = Theoretical

### Quantitative Trends

#### Publication Count by Year

| Year | Count |
|------|-------|
| 1986 | 2 |
| 1991 | 1 |
| 1992 | 1 |
| 1996 | 1 |
| 1999 | 1 |
| 2004 | 1 |
| 2013 | 1 |
| 2014 | 2 |
| 2015 | 2 |
| 2016 | 2 |
| 2017 | 6 |
| 2018 | 5 |
| 2020 | 7 |
| 2021 | 2 |
| 2022 | 7 |
| 2023 | 6 |
| 2024 | 5 |
| 2025 | 1 |

#### Method Category Distribution

| Category | Count | % |
|----------|-------|---|
| A. Pushing Mechanics & Contact Modeling | 13 | 26% |
| B. Inertial Parameter Estimation | 7 | 14% |
| C. Grasp Planning & Quality Metrics | 11 | 22% |
| D. In-hand Dynamic Manipulation | 13 | 26% |
| E. Extrinsic Dexterity & Contact-rich Planning | 6 | 12% |

#### Experimental Setting Breakdown

| Setting | Count | % |
|---------|-------|---|
| Both (Sim + Real) | 18 | 36% |
| Real hardware only | 10 | 20% |
| Simulation only | 5 | 10% |
| Theoretical / Analytical | 6 | 12% |
| Survey | 3 | 6% |
| Dataset | 1 | 2% |
| Not classified (paywall) | 7 | 14% |

### Concept Matrix

| Concept | Mason86 | Goyal91 | Ferrari92 | Lynch96 | Bauza17 | Hogan20 | Song20 | Dutta23 | SwingBot20 | Shirai23 | PhyGrasp24 |
|---------|---------|---------|-----------|---------|---------|---------|--------|---------|------------|----------|------------|
| Limit Surface | | X | | X | | X | | | | | |
| CoM Estimation | | | | | | | X | X | | | |
| Inertia Tensor | | | | | | | X | X | X | X | |
| Grasp Wrench Space | | | X | | | | | | | | |
| Friction Model | X | X | | X | X | X | X | | | X | |
| Quasi-static | X | | | X | X | X | | | | X | |
| Differentiable Physics | | | | | | | X | X | | | |
| Tactile Sensing | | | | | | | | X | X | | |
| Deep Learning | | | | | X | | X | X | X | | X |
| Contact Mode Planning | X | | | X | | X | X | | | X | |
| Gravity Exploitation | | | | | | | | | X | X | |

### Foundational Works

| # | Paper | Year | Venue | Significance |
|---|-------|------|-------|-------------|
| A-1 | Mechanics and Planning of Manipulator Pushing Operations | 1986 | IJRR | プッシュ操作の力学的定式化の起源。圧力分布と CoM の関係を体系化 |
| A-2 | Planar Sliding with Dry Friction Part 1. Limit Surface and Moment Function | 1991 | Wear | Limit surface 理論の確立。プッシュ接触モデリングの数学的基盤 |
| A-3 | Stable Pushing: Mechanics, Controllability, and Planning | 1996 | IJRR | 安定プッシュの制御可能性証明。プッシュ計画の理論的基盤 |
| B-1 | Estimation of Inertial Parameters of Manipulator Loads and Links | 1986 | IJRR | ロボット負荷の慣性パラメータ最小二乗推定。推定分野の起源 |
| C-1 | Planning Optimal Grasps | 1992 | ICRA | ε品質メトリクスの定義。把持品質評価の事実上の標準 |
| C-2 | Grasp Planning: How to Choose a Suitable Task Wrench Space | 2004 | ICRA | Object Wrench Space による参照点不変な品質メトリクス |
| D-1 | Dynamic Nonprehensile Manipulation: Controllability, Planning, and Experiments | 1999 | IJRR | 動的非把持操作の制御可能性と計画理論 |

### A. Pushing Mechanics & Contact Modeling

プッシュ操作の物理モデルは、解析的モデル（Mason 1986, Goyal 1991, Lynch & Mason 1996）から、データ駆動モデル（Bauza 2017, Zhou 2017）、学習ベースモデル（Li 2018, Ajay 2018）、そしてモデル予測制御（Hogan 2020, Moura 2022）へと発展してきた。近年は不確実性下のロバスト計画（Heins 2024, Jankowski 2024）が新たな方向性を示す。

1. Mason1986_PushMechanics — Mason, M. T., "Mechanics and Planning of Manipulator Pushing Operations" (1986)
   - **DOI**: 10.1177/027836498600500303
   - **thesis**: プッシュ操作の力学は、支持面上の圧力分布と摩擦モデルから系統的に導出でき、pusher-slider 系の運動予測と計画に帰着する
   - **core**: 圧力分布から導かれる回転中心の位置と、プッシュ方向に対する物体の回転・並進応答の解析的関係
   - **diff**: 操作の力学を体系的に定式化した最初の研究。以前の把持中心の議論を、プッシュという非把持操作に拡張
   - **limit**: limit not available (paywall)

2. Goyal1991_LimitSurface — Goyal, S.; Ruina, A.; Papadopoulos, J., "Planar Sliding with Dry Friction Part 1. Limit Surface and Moment Function" (1991)
   - **DOI**: 10.1016/0043-1648(91)90104-3
   - **thesis**: 滑り剛体と平面間の摩擦力・モーメントは、塑性理論の limit surface と Zhukovskii のモーメント関数という二つの双対幾何構成で完全に特徴づけられる
   - **core**: 力-モーメント空間の凸境界である limit surface と、瞬間回転中心に対する摩擦トルクを与えるモーメント関数の対
   - **diff**: Zhukovskii のモーメント関数は等方 Coulomb 摩擦に限定。Limit surface はより広い摩擦法則に一般化
   - **limit**: limit not available

3. Lynch1996_StablePushing — Lynch, K. M.; Mason, M. T., "Stable Pushing: Mechanics, Controllability, and Planning" (1996)
   - **DOI**: 10.1177/027836499601500602
   - **thesis**: 安定プッシュ（プッシュ中に接触が維持される条件）は、limit surface 上の motion cone として幾何学的に特徴づけられ、この条件下でプッシュ操作は制御可能である
   - **core**: Motion cone — pusher の速度方向に対して物体が安定接触を維持する方向の集合。Limit surface の法線方向として導出
   - **diff**: Mason (1986) の力学的解析を制御可能性理論と接続。安定プッシュの必要十分条件を提供
   - **limit**: limit not available (paywall)

4. Yu2016_PushingDataset — Yu, K.-T.; Bauza, M.; Fazeli, N.; Rodriguez, A., "More than a Million Ways to Be Pushed" (2016)
   - **DOI**: 10.1109/IROS.2016.7758091 | **arXiv**: 1604.04038
   - **thesis**: 既存の解析的プッシュモデルの仮定（楕円体 limit surface、最大散逸不等式等）の精度は体系的に検証されておらず、大規模実験により重大な限界が明らかになる
   - **core**: 6 次元のプッシュパラメータを系統的に変化させ 100 万件以上の時系列データを収集する自動化リグ（ABB IRB 120 + Vicon 250Hz）
   - **diff**: 従来のプッシュデータセットは汎用性不足。動的（非準静的）プッシュを含む初の共通ベンチマーク
   - **limit**: ポリウレタンで最大散逸不等式が破綻。楕円体 limit surface 近似の精度が不良。繰り返しプッシュの結果分布は明らかに非ガウス・多峰性

5. Bauza2017_ProbabilisticPushing — Bauza, M.; Rodriguez, A., "A Probabilistic Data-Driven Model for Planar Pushing" (2017)
   - **DOI**: 10.1109/ICRA.2017.7989345 | **arXiv**: 1704.03033
   - **thesis**: プッシュ相互作用は入力依存の確率性を示し、ヘテロスケダスティック GP がこの変動する不確実性を捕捉して解析モデルを凌駕する
   - **core**: Variational Heteroscedastic Gaussian Processes (VHGPs) — 観測ノイズを入力の関数としてモデル化
   - **diff**: Lynch et al., Zhou et al. の決定論的モデルと標準 GP の定常ノイズ仮定を克服。100 サンプル未満で解析モデルを超える
   - **limit**: ガウス性・単峰性の仮定が多峰性データに不適合。物体-素材ペア固有で汎化しない。出力変数間の相関を無視

6. Zhou2017_StochasticContact — Zhou, J.; Bagnell, J. A.; Mason, M. T., "A Fast Stochastic Contact Model for Planar Pushing and Grasping" (2017)
   - **DOI**: 10.15607/RSS.2017.XIII.040 | **arXiv**: 1705.10664
   - **thesis**: 凸多項式の limit surface 表現と Wishart 分布による確率的摩擦モデルにより、プッシュと把持を統一的に扱える高速な接触モデルが実現する
   - **core**: 楕円体より高次の凸多項式 limit surface + Wishart 分布による摩擦不確実性 + LCP 定式化
   - **diff**: Lynch et al. (1992) の対角共分散行列を一般化。モード列挙の組合せ爆発を LCP で回避
   - **limit**: 準静的仮定は弾性体把持に適用不可。決定論モデルの精度は系の固有分散に制約。実験の多峰性は表面摩耗による時変摩擦に起因

7. Li2018_PushNet — Li, J.; Lee, W. S.; Hsu, D., "Push-Net: Deep Planar Pushing for Objects with Unknown Physical Properties" (2018)
   - **DOI**: 10.15607/RSS.2018.XIV.024
   - **thesis**: プッシュ相互作用の履歴を追跡する深層 RNN が、明示的な物理モデルやパラメータ推定なしに、未知物体の確実な再配置を達成できる
   - **core**: 過去のプッシュ相互作用の潜在表現を維持する LSTM モジュール + CoM 推定の補助目的関数
   - **diff**: Lynch & Mason 等の解析モデルは既知物理パラメータを要求。Push-Net は相互作用履歴からの暗黙的推定で回避
   - **limit**: limit not available

8. Ajay2018_AugmentedSim — Ajay, A.; Wu, J.; Fazeli, N.; Bauza, M.; Kaelbling, L. P.; Tenenbaum, J. B.; Rodriguez, A., "Augmenting Physical Simulators with Stochastic Neural Networks" (2018)
   - **DOI**: 10.1109/IROS.2018.8593995 | **arXiv**: 1808.03246
   - **thesis**: 解析的物理シミュレータには パラメータ調整では除去不能な系統的誤差があり、確率的ニューラルネットワークによる残差補正がより表現力豊かで効率的なモデルを生む
   - **core**: Decoupled Conditional Variational RNN (DCVRNN) — 軌跡レベルの残差補正分布を予測。単一ステップではなく軌跡全体で学習
   - **diff**: 純解析モデルの不可約接触近似誤差、Kloss et al. の決定論的残差、Fazeli et al. の GP 残差（低速・ガウス限定）を克服
   - **limit**: 物理制約を出力に強制する機構がなく、物理的に不可能な結果を予測しうる。部分観測性は未対応

9. Hogan2020_HybridMPC — Hogan, F. R.; Rodriguez, A., "Reactive Planar Non-Prehensile Manipulation with Hybrid Model Predictive Control" (2020)
   - **DOI**: 10.1177/0278364920913938
   - **thesis**: ハイブリッド接触動力学の組合せ複雑性は、接触モードスケジューリング（オフライン ML）と連続制御最適化（オンライン凸 QP）の分離により制御可能になる
   - **core**: MPC-LMS — NN 分類器がモード列を予測し、オンライン問題を凸 QP に変換。楕円体 limit surface モデル
   - **diff**: Hogan & Rodriguez (2016) の手動モード列挙、Posa et al. の連続近似、Lynch et al. の事前モード知識仮定を排除
   - **limit**: 平面操作・準静的相互作用に限定。単一接触 pusher-slider 系のみ

10. Song2020_DiffPhysics — Song, C.; Boularias, A., "Learning to Slide Unknown Objects with Differentiable Physics Simulations" (2020)
    - **DOI**: 10.15607/rss.2020.xvi.099 | **arXiv**: 2005.05456
    - **thesis**: LCP 定式化の解析勾配により、最小限の相互作用から未知物体の空間的質量・摩擦分布を効率的に推定し、安全なスライド操作を実現できる
    - **core**: キューボイドグリッドによる物体表現 + LCP の質量・摩擦パラメータに関する解析勾配の閉形式導出
    - **diff**: 標準物理エンジンは微分不能。モデルベース RL は未見の安定性イベントを予測不能。従来は摩擦のみ推定で質量は既知仮定。本手法は質量と摩擦を同時推定
    - **limit**: 帰納バイアス（摩擦上限）が必要。データ不足時に摩擦と質量分布を誤帰属。有限差分勾配ベースラインは収束せず

11. Moura2022_ComplementarityTO — Moura, J.; Stouraitis, T.; Vijayakumar, S., "Non-prehensile Planar Manipulation via Trajectory Optimization with Complementarity Constraints" (2022)
    - **DOI**: 10.1109/icra46639.2022.9811942 | **arXiv**: 2109.13145
    - **thesis**: MPCC 定式化がプッシュの軌道計画と MPC を統一し、混合整数代替より高速に収束し障害物を処理できる
    - **core**: 相補性制約 (λ_v^T φ̇_v + ε = 0) による接触モード遷移の符号化 + 楕円体 limit surface モデル
    - **diff**: MINLP より高速収束。Hogan & Rodriguez (2020) の MIQP より大外乱への追従改善。ロボット MPC への初の MPCC 適用
    - **limit**: 同時接触数へのスケーラビリティ未検証。非準静的シナリオ不可。MPC 水平線（1秒）が短い

12. Heins2024_ForcePush — Heins, A.; Schoellig, A. P., "Force Push: Robust Single-Point Pushing With Force Feedback" (2024)
    - **DOI**: 10.1109/LRA.2024.3414180 | **arXiv**: 2401.17517
    - **thesis**: 接触力計測のみで、視覚フィードバック・姿勢計測・スライダモデルなしに安定プッシュが達成できる
    - **core**: 接触力方向誤差と経路横偏差に基づく比例制御則 θ_p = θ_d + (k_f+1)Δ_f + k_cΔ_c
    - **diff**: 従来は視覚/触覚フィードバックと安定線接触を仮定。単一接触点の力ベクトルのみで動作する初の手法
    - **limit**: 理論的安定性証明が欠如。学習・適応的手法との統合が未達。狭い通路・乱雑環境未対応

13. Jankowski2024_RobustPushing — Jankowski, J.; Brüdermüller, L.; Hawes, N.; Calinon, S., "Robust Pushing: Exploiting Quasi-static Belief Dynamics and Contact-informed Optimization" (2024)
    - **DOI**: 10.1177/02783649251318046 | **arXiv**: 2404.02795
    - **thesis**: 準静的接触動力学の解析的不確実性伝播により、外部センサなしのロバストなオープンループプッシュ計画を合成できる
    - **core**: 分散予測の閉形式 V+ = Var_b[f(q^o,u)] + E_b[η]V_w + 接触事前分布による最適化バイアス
    - **diff**: Lynch & Mason (1995) の事前プログラム行動、Pang et al. (2023) の正確モデル仮定、Jankowski et al. (2023) のサンプリング最適化を克服。事前定義プリミティブなしの初のモデルベース計画
    - **limit**: 高剛性ロボット仮定は包囲把持で破綻。分散が 0 に収束しうる。ガウス近似は非ガウス信念の簡略化

### B. Inertial Parameter Estimation

物体の慣性パラメータ推定は、Atkeson et al. (1986) の最小二乗法から、プッシュベースの 2D 推定（Mavrakis 2020, Gao 2023）、協調ロボットの形状活用推定（Nadeau 2022）、アクティブ推定（Dutta 2023）、微分可能シミュレーション（Chen 2024）へと多様化している。

1. Atkeson1986_InertialID — Atkeson, C.; An, C.; Hollerbach, J., "Estimation of Inertial Parameters of Manipulator Loads and Links" (1986)
   - **DOI**: 10.1177/027836498600500306
   - **thesis**: マニピュレータの逆動力学方程式を慣性パラメータの線形系として定式化し、最小二乗法でロボットリンクおよび負荷の全慣性パラメータを推定できる
   - **core**: ニュートン-オイラー逆動力学の慣性パラメータに関する線形性を活用した最小二乗推定
   - **diff**: 操作対象の慣性パラメータ推定を系統的に定式化した最初の研究
   - **limit**: limit not available (paywall)

2. Mavrakis2020_InertialSurvey — Mavrakis, N.; Stolkin, R., "Estimation and Exploitation of Objects' Inertial Parameters in Robotic Grasping and Manipulation: A Survey" (2020)
   - **DOI**: 10.1016/j.robot.2019.103374 | **arXiv**: 1911.04397
   - **thesis**: 慣性パラメータは操作にとって重要だが過小利用されており、推定方法をロボット-物体相互作用レベルで分類することで相補的強みが明らかになる
   - **core**: 3 カテゴリ分類 — 視覚的（形状＋密度仮定）、探索的（プッシュ/傾斜＋力/運動計測）、固定物体（把持負荷＋動力学方程式）
   - **diff**: ロボティクスにおける慣性パラメータ推定の初のサーベイ
   - **limit**: 探索的手法は 2D パラメータに限定。視覚的手法は未知密度分布で精度低下。ロボット自己同定は対象外

3. Mavrakis2020_PushEstimation — Mavrakis, N.; Stolkin, R.; Ghalamzan Esfahani, A., "Estimating An Object's Inertial Parameters By Robotic Pushing: A Data-Driven Approach" (2020)
   - **DOI**: 10.1109/IROS45743.2020.9341112
   - **thesis**: 単一の準静的プッシュから、データ駆動回帰モデルにより物体の 2D 慣性パラメータを正確に予測できる
   - **core**: Multi-Output Regression Random Forest — 力・モーメント・速度特徴から慣性パラメータへの非線形写像を学習
   - **diff**: Yu et al. (2005) 等の解析手法が要求する対称性・既知摩擦・非滑り接触仮定を緩和
   - **limit**: 2D パラメータのみ。大規模学習データ（48,000 シミュレーション）が必要。力/トルクセンシング品質に依存

4. Nadeau2022_FastInertialID — Nadeau, P.; Giamou, M.; Kelly, J., "Fast Object Inertial Parameter Identification for Collaborative Robots" (2022)
   - **DOI**: 10.1109/ICRA46639.2022.9916213 | **arXiv**: 2203.00830
   - **thesis**: 協調ロボットの安全な低速動作でも、重力優位の力/トルク信号を活用すれば物体慣性パラメータを迅速かつ正確に推定できる
   - **core**: Point Mass Discretization (PMD) — 物体形状を固定位置の点質量に離散化し凸最適化で重みを回復 + 動的度に基づく重力/動力学モデル混合
   - **diff**: Atkeson et al. (1986) と Kubus et al. (2008) は低速で誤差大。Traversaro et al. (2016) は事前知識要求。PMD は形状情報と重力優位分析で克服
   - **limit**: 物体形状の知覚が必要。ハイパーパラメータの per-robot チューニングが必要

5. Gao2023_ZeroMomentPush — Gao, Z.; Elibol, A.; Chong, N. Y., "Zero Moment Two Edge Pushing of Novel Objects With Center of Mass Estimation" (2023)
   - **DOI**: 10.1109/TASE.2022.3208739
   - **thesis**: 推定 CoM を通る力線を生成する二辺接触プッシュにより、摩擦係数の知識なしに物体を回転なく並進できる
   - **core**: DL 運動予測 + Mason の Voting Theorem による CoM 推定 + ZMTEP アルゴリズム（接触間距離最大化で CoM 推定誤差への耐性確保）
   - **diff**: 従来の単一点プッシュ（Lynch & Mason 1996）は既知摩擦を仮定。二指法（Yu et al. 2005）は CoM 間のプッシュ線を要求。ZMTEP は表面摩擦・pusher 摩擦とも不要
   - **limit**: 純並進のみ（回転制御は今後の課題）。高速プッシュ（非準静的）への拡張が必要

6. Dutta2023_PushToKnow — Dutta, A.; Burdet, E.; Kaboli, M., "Push to Know! — Visuo-Tactile Based Active Object Parameter Inference with Dual Differentiable Filtering" (2023)
   - **DOI**: 10.1109/IROS55552.2023.10341832 | **arXiv**: 2308.01001
   - **thesis**: 双対微分可能フィルタリングとアクティブ情報利得最大化により、非把持プッシュを通じた物理パラメータ推定のサンプル効率を大幅に改善できる
   - **core**: Active Dual Differentiable Filter (ADDF) — 時不変パラメータと時変姿勢の分離推定 + N-step KL ダイバージェンス情報利得による行動選択
   - **diff**: Mavrakis et al. (2020) のランダムプッシュよりサンプル効率 ~20% 改善。視覚のみ/触覚のみの手法を統合
   - **limit**: 新規物体には VisNet の再学習が必要。RGB-D と 2D 姿勢推定に依存。学習に真値が必要

7. Chen2024_DiffInteraction — Chen, P. Y.; Liu, C.; Ma, P.; Eastman, J.; Rus, D.; Randle, D.; Ivanov, Y.; Matusik, W., "Learning Object Properties Using Robot Proprioception via Differentiable Robot-Object Interaction" (2024)
   - **DOI**: 10.1109/ICRA55743.2025.11127955 | **arXiv**: 2410.03920
   - **thesis**: ロボットの関節エンコーダ信号のみから — 外部センサなしに — 操作対象の質量・弾性率等の物体特性を推定できる
   - **core**: Nvidia Warp による微分可能ロボット-物体相互作用シミュレーション。固有受容損失（シミュレーション-実機関節位置 MSE）の勾配を全結合動力学に逆伝播
   - **diff**: 従来の微分可能シミュレーションはロボット特性推定またはビジョンベースの物体追跡に焦点。ロボットデータのみで物体特性を推定する初の手法
   - **limit**: 物体の初期位置の知識を仮定。非現実的な初期推定は局所最適に陥る。複雑なロボット系・非一様分布・ソフトロボットへの拡張が今後の課題

### C. Grasp Planning & Quality Metrics

Ferrari & Canny (1992) の GWS メトリクスを基盤に、タスク依存品質（Borst 2004）、動力学考慮（Kim 2013）、深層学習統合（Mahler 2017）、CoM/慣性活用（Mavrakis 2017, Kanoulas 2018, Feng 2020）、微分可能品質（Chen 2023）、物理常識推論（PhyGrasp 2024, Trupin 2025）へと発展。

1. Ferrari1992_GraspQuality — Ferrari, C.; Canny, J., "Planning Optimal Grasps" (1992)
   - **DOI**: 10.1109/ROBOT.1992.219918
   - **thesis**: 把持品質は抵抗可能な最悪ケースレンチと要求指力の比として厳密に定量化でき、L∞ と L1 の二つの最適性基準が幾何学的に解釈可能な品質メトリクスを与える
   - **core**: 品質 Q = プリミティブ接触レンチ凸包に内接する最大球の半径。L∞ では Minkowski 和、L1 では和集合の凸包
   - **diff**: Kirkpatrick et al. は L∞ のみ。Markenskoff & Papadimitriou は指力強度和最小化のみ。両基準を統一し O(n) 計画アルゴリズムを提供
   - **limit**: 提示された計画アルゴリズムは 2D 物体に限定。力とトルクの次元非比較性を認め、異なるノルムでの内接球探索を示唆

2. Borst2004_TaskWrench — Borst, C.; Fischer, M.; Hirzinger, G., "Grasp Planning: How to Choose a Suitable Task Wrench Space" (2004)
   - **DOI**: 10.1109/ROBOT.2004.1307170
   - **thesis**: タスクが未知の場合、Object Wrench Space から導出した物理的に動機づけられた Task Wrench Space が、力-トルク次元の非一様性を自動的に解決し、参照点不変な品質メトリクスを与える
   - **core**: OWS（物体表面への単位外乱力が生む全レンチ集合）の 6D 楕円体近似。品質 Q_MBF = OWS 楕円体が GWS に内接する最大スケーリング係数
   - **diff**: Ferrari & Canny のメトリクスはスケール不変でなくトルク参照点に依存。Pollard の OWS は品質メトリクスを直接提供しない。OWS 楕円体は参照点不変で 10-20ms で計算
   - **limit**: OWS 楕円体は包囲楕円体の近似（保守的）。動的効果は未考慮

3. Kim2013_PhysicsGraspEval — Kim, J.; Iwamoto, K.; Kuffner, J. J.; Ota, Y.; Pollard, N. S., "Physically Based Grasp Quality Evaluation Under Pose Uncertainty" (2013)
   - **DOI**: 10.1109/TRO.2013.2273846
   - **thesis**: 物体動力学と姿勢不確実性は把持品質評価において同時に考慮する必要があり、いずれか単独では実際の把持成功率予測が改善しない
   - **core**: 指閉鎖中の 3D 剛体物体運動をシミュレートする物理ベース動的把持シミュレーション + 姿勢不確実性の Monte Carlo サンプリング
   - **diff**: GraspIt! 等の運動学シミュレーションは静的物体仮定で誤判断。Weisz & Allen は姿勢不確実性のみ追加。動力学＋不確実性の同時考慮で初めて改善
   - **limit**: 手の動力学モデルが高度に簡略化。単純なペナルティベース接触モデル。開ループ把持のみ検証。把持コントローラ間のデータ移植性が未検証

4. Roa2014_GraspQualitySurvey — Roa, M. A.; Suárez, R., "Grasp Quality Measures: Review and Performance" (2014)
   - **DOI**: 10.1007/s10514-014-9402-3
   - **thesis**: 単一の把持品質メトリクスは万能ではなく、異なるメトリクスは異なる把持特性を優先して矛盾する最適解を生むため、タスク依存の選択と多基準アプローチが必要
   - **core**: 接触位置ベース（把持行列の代数的性質、幾何学的関係、力/トルク制限メトリクス）と手構成ベース（特異点距離、操作性）の体系的分類 + 共通ベンチマーク評価
   - **diff**: Suárez et al. (2006) はメトリクスを列挙したが比較評価なし。共通ベンチマークでの初の定量的性能比較を提供
   - **limit**: 最適化アルゴリズムの計算複雑性。劣駆動・パワー把持への適用が限定的。動的効果の考慮不足。多基準結合戦略の不足。理論と実世界性能の乖離

5. Mahler2017_DexNet2 — Mahler, J.; Liang, J.; Niyaz, S.; Laskey, M.; Doan, R.; Liu, X.; Ojea, J. A.; Goldberg, K., "Dex-Net 2.0: Deep Learning to Plan Robust Grasps with Synthetic Point Clouds and Analytic Grasp Metrics" (2017)
   - **DOI**: 10.15607/RSS.2017.XIII.058 | **arXiv**: 1703.09312
   - **thesis**: 大規模合成データ＋解析的把持ロバスト性メトリクスで学習した GQ-CNN が、物理的試行ゼロで単一深度画像から高精度把持計画を実現する
   - **core**: Dex-Net 2.0 データセット（670 万合成点群 + Monte Carlo ε品質）＋ Grasp Quality CNN + 深度画像勾配からの対蹠点把持候補サンプリング
   - **diff**: 自己教師あり手法（Pinto & Gupta: 4万物理試行）やマルチロボット手法（Levine et al.: 80万データ点）と異なり物理データ不要。登録ベース（Dex-Net 1.0: 3.4s）より高速（0.8s）
   - **limit**: 平面上の分離物体を仮定。剛体または弱変形物のみ。単一深度カメラ。薄い形状の欠損データや狭い領域での衝突誤分類で失敗

6. Mavrakis2017_SafeGrasp — Mavrakis, N.; Ghalamzan E., A. M.; Stolkin, R., "Safe Robotic Grasping: Minimum Impact-Force Grasp Selection" (2017)
   - **DOI**: 10.1109/IROS.2017.8206258 | **arXiv**: 1707.08150
   - **thesis**: 把持姿勢の選択は把持後の衝突安全性に大きく影響し、拡張ロボット-物体有効質量を最小化する把持を選択することで衝撃力を約 30% 低減できる
   - **core**: 操作空間慣性行列と物体慣性テンソル（把持姿勢変換済み）を結合した拡張動力学モデル。軌道速度方向の有効質量 M_tot が衝撃力を直接予測
   - **diff**: 従来の把持計画は指配置安定性のみ。タスク指向把持もタスクレンチのみ考慮。把持後の衝撃力最小化を把持選択基準に導入した初の研究
   - **limit**: 衝撃力最小化のみ（衝撃後安定性は未考慮）。ロボット動力学と物体慣性は既知仮定。Baxter のみで実験。産業用マニピュレータでの検証が今後の課題

7. Kanoulas2018_CoMGrasp — Kanoulas, D.; Lee, J.; Caldwell, D. G.; Tsagarakis, N. G., "Center-of-Mass-Based Grasp Pose Adaptation Using 3D Range and Force/Torque Sensing" (2018)
   - **DOI**: 10.1142/S0219843618500135 | **arXiv**: 1802.06392
   - **thesis**: 重い物体を CoM 近傍で把持することで手首トルクを最小化でき、視覚 CoM 推定＋固有受容リグラスプの 2 段階反復法により通常 1 回のリグラスプで達成できる
   - **core**: Stage I: 3D レンジデータからボクセル化幾何重心推定＋円筒フィット。Stage II: 手首力/トルクから CoM 線までの変位 d を計算し、||d_h × f|| 最小化ハンドルを選択
   - **diff**: 深層学習視覚把持は形状のみで質量分布を無視。力/トルクベース CoM 推定は視覚統合なし。3D レンジと手首力/トルクの反復統合は初
   - **limit**: 支配的支持面を仮定。等方材料・一定密度仮定。円筒形把持領域に限定。手首トルクのみ最小化（関節負荷無視）。単腕のみ

8. Feng2020_CoMGraspPlanning — Feng, Q.; Chen, Z.; Zhang, J.; Knoll, A., "Center-of-Mass-based Robust Grasp Planning for Unknown Objects Using Tactile-Visual Sensors" (2020)
   - **DOI**: 10.1109/ICRA40945.2020.9196815 | **arXiv**: 2006.00906
   - **thesis**: 触覚によるスリップ検出と力/トルクデータからの CoM オフセット推定に基づくリグラスプ計画が、視覚のみのベースライン（Dex-Net 4.0）を 31% 上回る
   - **core**: 3 段パイプライン — 対蹠点把持サンプラ + スリップ検出器（SVM、F-score 76.88%）+ リグラスププランナ（並列 LSTM）
   - **diff**: Dex-Net 4.0 は画像中心付近を把持し非対称物体で失敗（49% 成功率）。Calandra et al. は静的物体接触のみ。持ち上げ中のスリップ予測に基づくリグラスプは初
   - **limit**: リグラスプ方向が 1 軸のみ。実験物体セット・データセット規模が限定的。一部テスト物体で精度低下（LEGO: 57% F-score）

9. Chen2023_DiffGWS — Chen, J.; Chen, Y.; Zhang, J.; Wang, H., "Task-Oriented Dexterous Grasp Synthesis via Differentiable Grasp Wrench Boundary Estimator" (2023)
   - **arXiv**: 2309.13586
   - **thesis**: GWS 境界はサポート写像と Minkowski 和分解により、反復最適化や凸包計算なしに正確・高速・微分可能に推定でき、勾配ベースのタスク指向把持合成を実現する
   - **core**: 微分可能 GWS 境界推定器 s_{W_g}(u) = Σ_i G_i s_{F_i}(G_i^T u)。O(mK) 計算量 + 6D hyper-fan Task Wrench Space + メッシュ上の微分可能最近点計算
   - **diff**: Ferrari & Canny の凸包は 3 桁以上低速で微分不能。Liu et al., Turpin et al. はタスク非対応 force closure のみ。非 force closure 把持も含むタスク指向合成を実現（57.1% vs 37.0%）
   - **limit**: 勾配最適化は局所最適に陥る。GWS サンプリングの一様性が不十分。手の接触点は手動割当

10. PhyGrasp2024_Guo — Guo, D.; Xiang, Y.; Zhao, S.; Zhu, X.; Tomizuka, M.; Ding, M.; Zhan, W., "PhyGrasp: Generalizing Robotic Grasping with Physics-informed Large Multimodal Models" (2024)
    - **DOI**: 10.1109/IROS60139.2025.11246481 | **arXiv**: 2402.16836
    - **thesis**: 材料特性・脆弱性・密度・摩擦などの物理常識推論を言語条件付きマルチモーダル学習で統合することで、形状のみのアプローチより物理的に困難な物体への把持が大幅に改善する
    - **core**: PointNeXt 3D 視覚特徴と Llama 2 言語特徴（GPT-3.5 生成の物理特性記述）を融合するブリッジネットワーク + PhyPartNet（195K 物体、16 材料タイプ）
    - **diff**: GraspNet, VGN は 3D 形状のみで物理的に困難な物体で性能低下。PhyGrasp は物理記述の統合で一般→困難テストセットの性能劣化を最小化（61.5% vs 59.7%）
    - **limit**: 特異形状（細首ランプ等）で困難。PartNet のパーツセグメンテーションが不十分。埋め込み分類器の誤マッチが発生

11. Trupin2025_PhysicsGrasp — Trupin, N.; Wang, Z.; Qureshi, A. H., "Physics-Conditioned Grasping for Stable Tool Use" (2025)
    - **arXiv**: 2505.01399
    - **thesis**: 準静的・動的・乱雑タスクにわたるロバストなツール使用には、VLM による意味理解と物理ペナルティネットワークの両方が必要
    - **core**: Stable Dynamic Grasp Network (SDG-Net) — 相互作用トルク・スリップペナルティ・法線整列の 3 物理メトリクスを学習。GPT-4o VLM によるツール/接触点選択パイプライン
    - **diff**: CoPa は準静的タスクのみ。SDG-Net はハンマリングでのネットトルクを 17.6% 低減。実世界成功率 76.67% vs CoPa 60%
    - **limit**: 3 物理メトリクスに限定（完全動力学モデルではない）。VLM は 2D 表現で 3D 空間接地が欠如。VLM 出力品質に依存。軌道計画に衝突回避なし

### D. In-hand Dynamic Manipulation

重力・摩擦を活用したインハンド操作は、Lynch & Mason (1999) の動的非把持操作理論を基盤に、ピボット（Holladay 2015, Viña 2015/2016, Costanzo 2021, Toskov 2022, Shirai 2023）、スライディング（Shi 2017）、スイングアップ（SwingBot 2020, Bi 2021）、フリッピング（Kolathaya 2018）、および motion cone 一般化（Chavan-Dafle 2018）へと展開。

1. Lynch1999_DynamicNonprehensile — Lynch, K. M.; Mason, M. T., "Dynamic Nonprehensile Manipulation: Controllability, Planning, and Experiments" (1999)
   - **DOI**: 10.1177/027836499901800105
   - **thesis**: 動的（慣性効果を利用する）非把持操作は制御可能であり、接触モード遷移を含む軌道計画が可能である
   - **core**: 動的操作における制御可能性の証明と、接触/非接触フェーズを含む軌道計画アルゴリズム
   - **diff**: Lynch & Mason (1996) の準静的プッシュを動的領域に拡張。投げ、転がし、叩き等の動的プリミティブの計画可能性を初めて示す
   - **limit**: limit not available (paywall)

2. Holladay2015_OpenLoopPivoting — Holladay, R.; Paolini, R.; Mason, M. T., "A General Framework for Open-Loop Pivoting" (2015)
   - **DOI**: 10.1109/ICRA.2015.7139709
   - **thesis**: ピボット操作（接触点まわりの回転）はオープンループでも実行可能であり、重力と摩擦の相互作用を幾何学的に解析することで一般的な計画フレームワークを構築できる
   - **core**: ピボット接触における摩擦錐と重力モーメントの幾何学的解析によるオープンループ計画
   - **diff**: 従来のピボット研究は特定物体・特定タスクに限定。一般的な物体形状と把持構成に適用可能なフレームワークを提供
   - **limit**: limit not available (paywall)

3. Vina2015_GravitySlip — Viña, F. E.; Karayiannidis, Y.; Pauwels, K.; Smith, C.; Kragic, D., "In-Hand Manipulation Using Gravity and Controlled Slip" (2015)
   - **DOI**: 10.1109/IROS.2015.7354177
   - **thesis**: 重力と制御されたスリップを活用することで、指の再配置や複雑な接触力制御なしにインハンドでの物体再配向を実現できる
   - **core**: グリッパの把持力を意図的に緩め、重力トルクによる制御されたスリップ（回転）を誘発する機構
   - **diff**: 従来のインハンド操作は指ガイトと複雑な接触力制御に依存。重力補助スリップ戦略は機械的・計算的複雑性を大幅に低減
   - **limit**: 操作ワークスペースと物体形状に制約。重力トルクを効果的に利用できない大型物体や不利な質量分布では適用困難

4. Vina2016_AdaptivePivoting — Viña, F. E.; Karayiannidis, Y.; Smith, C.; Kragic, D., "Adaptive Control for Pivoting with Visual and Tactile Feedback" (2016)
   - **DOI**: 10.1109/ICRA.2016.7487159
   - **thesis**: 視覚と触覚のフィードバックを統合した適応制御により、物体パラメータの事前知識なしにピボット操作の精度と堅牢性を大幅に向上できる
   - **core**: 視覚フィードバック（物体角度追跡）と触覚フィードバック（スリップ検出/把持力調整）の統合適応制御器
   - **diff**: Viña et al. (2015) のオープンループ重力スリップを、センサフィードバックによるクローズドループ制御に拡張。未知物体パラメータへの適応能力を付与
   - **limit**: limit not available (paywall)

5. Shi2017_DynamicSliding — Shi, J.; Woodruff, J. Z.; Umbanhowar, P.; Lynch, K., "Dynamic In-Hand Sliding Manipulation" (2017)
   - **DOI**: 10.1109/TRO.2017.2693391
   - **thesis**: アーム運動による慣性力を活用した動的インハンドスライディングにより、準静的手法では到達不能な把持再構成を実現できる
   - **core**: 把持物体に対するアーム加速度が生む慣性力を利用し、指と物体間の制御されたスライディングを誘発する動力学ベースの計画・制御
   - **diff**: 従来のインハンド操作は準静的（重力のみ）。動的アーム運動による慣性効果の積極的活用でスライディング方向と量を制御する初のフレームワーク
   - **limit**: limit not available (paywall)

6. Kolathaya2018_DirectCollocation — Kolathaya, S.; Guffey, W.; Sinnet, R.; Ames, A., "Direct Collocation for Dynamic Behaviors With Nonprehensile Contacts: Application to Flipping Burgers" (2018)
   - **DOI**: 10.1109/LRA.2018.2854910
   - **thesis**: Direct collocation による軌道最適化が、非把持接触を伴う動的行動（バーガーフリッピング等）の計画に適用可能であり、接触力と運動を同時最適化できる
   - **core**: Direct collocation 定式化 — 接触力を最適化変数に含め、摩擦錐制約と相補性制約を離散時間点で強制
   - **diff**: 従来の非把持操作計画は準静的または特定プリミティブに限定。動的な投げ上げ・キャッチを含む接触リッチな軌道の汎用最適化
   - **limit**: limit not available (paywall)

7. Chavan-Dafle2018_MotionCones — Chavan-Dafle, N.; Holladay, R.; Rodriguez, A., "In-Hand Manipulation via Motion Cones" (2018)
   - **DOI**: 10.15607/RSS.2018.XIV.058 | **arXiv**: 1810.00219
   - **thesis**: Motion cone は水平面プッシュから、重力が動力学に影響する一般的な平面タスク（prehensile push によるインハンド操作を含む）に一般化できる
   - **core**: 力バランスと楕円体 limit surface モデルの連立求解 — pusher の全摩擦錐方向にわたる実現可能物体運動の計算
   - **diff**: Mason (1986) と Lynch & Mason (1996) は重力なし水平プッシュの点接触に限定。重力下の prehensile タスクとグリッパ-物体-pusher の複雑な相互作用に拡張
   - **limit**: 準静的仮定（低速操作）。既知物体形状・質量・摩擦係数が必要。pusher 位置は事前定義

8. Ruggiero2018_NonprehensileSurvey — Ruggiero, F.; Lippiello, V.; Siciliano, B., "Nonprehensile Dynamic Manipulation: A Survey" (2018)
   - **DOI**: 10.1109/LRA.2018.2801939
   - **thesis**: 非把持動的操作は投げ、打撃、プッシュ、ピボット等の多様なプリミティブから構成され、各プリミティブの動力学モデルと制御手法の体系的分類が分野の進展に不可欠
   - **core**: 非把持動的操作プリミティブの分類体系 — 投げ（throwing）、打撃（batting）、プッシュ（pushing）、ピボット（pivoting）、転がし（rolling）等
   - **diff**: 非把持操作の初の包括的サーベイ。個別プリミティブの研究を統一的フレームワークで整理
   - **limit**: limit not available (paywall)

9. SwingBot2020_Wang — Wang, C.; Wang, S.; Romero, B.; Veiga, F.; Adelson, E., "SwingBot: Learning Physical Features from In-hand Tactile Exploration for Dynamic Swing-up Manipulation" (2020)
   - **DOI**: 10.1109/IROS45743.2020.9341006 | **arXiv**: 2101.11812
   - **thesis**: 傾けと振りの触覚探索から学習した低次元物理特徴埋め込みにより、未見物体の動的スイングアップを平均誤差 17.2 度で達成できる
   - **core**: マルチアクション融合モデル — 傾け（CNN 処理触覚信号）と振り（LSTM 処理時系列）を 40 次元物理埋め込み空間に統合
   - **diff**: 視覚ベース手法（Xu et al., Agrawal et al.）は構造化環境と傾斜路が必要。GelSight 触覚による直接接触変形観測で環境制約を排除
   - **limit**: ロボットプラットフォームの高いアクチュエーションノイズ。GelSight のレイテンシでスイングアップ全運動を観測不能。単一タスクのみ検証。埋め込みの他タスク転移可能性は未実証

10. Bi2021_SwingUpSimToReal — Bi, T.; Sferrazza, C.; D'Andrea, R., "Zero-Shot Sim-to-Real Transfer of Tactile Control Policies for Aggressive Swing-Up Manipulation" (2021)
    - **DOI**: 10.1109/LRA.2021.3084880 | **arXiv**: 2101.02680
    - **thesis**: 視覚ベース触覚センサの精密なシミュレータにより、物体物理特性の事前知識なしに 180° スイングアップのクローズドループ制御ポリシーをゼロショットで sim-to-real 転移できる
    - **core**: 軟質センサ表面と剛体棒の相互作用を正確にモデル化する新規触覚シミュレータ（有限要素法＋接触解決）。現実的な学習データ生成を可能にする
    - **diff**: Wang et al. (SwingBot) はセンシングと操作を 2 段階に分離し事前探索が必要。Karayiannidis et al., Senoo et al. は視覚追跡やマルチセンサ融合に依存。本手法は触覚データのみのクローズドループ制御を事前探索なしで実現
    - **limit**: 単一タスク・単一ロボットのみ実証。平面運動制約。触覚観測から手動設計特徴を抽出（エンドツーエンド学習ではない）。非平面タスクと 6-DOF 制御への拡張が必要

11. Costanzo2021_PivotingTactile — Costanzo, M., "Control of Robotic Object Pivoting Based on Tactile Sensing" (2021)
    - **DOI**: 10.1016/j.mechatronics.2021.102545
    - **thesis**: 触覚センシングに基づくフィードバック制御により、物体の幾何学的・物理的パラメータの事前知識なしにロバストなピボット操作を実現できる
    - **core**: 触覚センサからの滑り検出と接触力推定に基づくピボット角度のフィードバック制御
    - **diff**: モデルベースのピボット手法（Holladay 2015 等）が物体形状・質量・摩擦の既知を仮定するのに対し、触覚フィードバックによりパラメータフリーな制御を実現
    - **limit**: limit not available (paywall)

12. Toskov2022_GravitationalPivoting — Toskov, J.; Newbury, R.; Mukadam, M.; Kulić, D.; Cosgun, A., "In-Hand Gravitational Pivoting Using Tactile Sensing" (2022)
    - **arXiv**: 2210.05068
    - **thesis**: 触覚センシングとグリップ力調整のみで、物体の形状・質量・摩擦の事前知識なしに重力ピボットによる目標角度への回転が可能
    - **core**: RSE-LSTM ニューラルネットワーク — 触覚データのみから角度位置・速度を予測し、グリップコントローラがリアルタイム調整
    - **diff**: Viña et al., Cruciani & Smith のモデルベース手法は物体情報を要求。Chen et al. のスライディングウィンドウ MLP を回転スリップに拡張し LSTM の隠れ状態で記憶
    - **limit**: 重力駆動のため一方向のみ（エラー回復困難）。グリッパコマンド遅延 ~0.83s が速度予測誤差を増幅。未見物体での性能低下。プリズム形状に限定

13. Shirai2023_PivotingBilevel — Shirai, Y.; Jha, D. K.; Raghunathan, A., "Robust Pivoting Manipulation Using Contact Implicit Bilevel Optimization" (2023)
    - **DOI**: 10.1109/TRO.2024.3422053 | **arXiv**: 2303.08965
    - **thesis**: 摩擦は接触操作において計測可能な安定余裕を提供し、この「摩擦安定性」を活用することで質量・CoM・摩擦の不確実性にロバストな軌道を計画できる
    - **core**: Contact Implicit Bilevel Optimization (CIBO) — 下位問題が最大安定余裕を計算し上位問題が軌跡上の最小余裕を最大化。下位 LP の KKT 条件で効率的に解く
    - **diff**: 従来のピボット研究はスティッキング接触（本質的に安定）を仮定。制御されたスリッピングでの不確実性ロバスト性保証を提供。オンライン触覚フィードバック（参照 [8]）に依存しない軌道レベルのロバスト性
    - **limit**: 質量と CoM の同時不確実性は非線形結合で下位問題が非凸化。非凸物体はドメイン知識に基づくモード別逐次最適化が必要。オープンループ実装で力追跡フィードバックなし

### E. Extrinsic Dexterity & Contact-rich Planning

単純なグリッパでも、重力・環境接触・慣性力という外部リソースを活用することで高度な操作が可能であるという「外的器用さ」の概念（Chavan-Dafle 2014）に基づくカテゴリ。

1. Chavan-Dafle2014_ExtrinsicDexterity — Chavan-Dafle, N.; Rodriguez, A.; Paolini, R.; Tang, B.; Srinivasa, S.; Erdmann, M.; Mason, M. T.; Lundberg, I.; Staab, H.; Fuhlbrigge, T., "Extrinsic Dexterity: In-hand Manipulation with External Forces" (2014)
   - **DOI**: 10.1109/ICRA.2014.6907062
   - **thesis**: 単純なグリッパでも、重力・環境接触・動的アーム運動という手の外部リソースを活用することで、豊かなインハンド操作が実現できる
   - **core**: 12 のオープンループリグラスプ プリミティブの分類体系（準静的外部接触、受動動的重力駆動、能動動的慣性駆動）+ 把持グラフによるプリミティブ連鎖
   - **diff**: Salisbury (1982) の「内的器用さ」は多指巧緻ハンドを要求。単一アクチュエータ 3 指コンプライアントグリッパで同等の把持遷移を、環境・重力・アーム動力学に複雑性を移譲して実現
   - **limit**: 全行動がオープンループ・手動コーディング。誤差蓄積で長シーケンスは成功率低下（11 ステップで 15/30）。~2g のアーム加速度は一般的研究用マニピュレータの能力を超過

2. LeClreach2022_DANOs — Le Cleac'h, S.; Yu, H.-X.; Guo, M.; Howell, T.; Gao, R.; Wu, J.; Manchester, Z.; Schwager, M., "Differentiable Physics Simulation of Dynamics-Augmented Neural Objects" (2022)
   - **DOI**: 10.1109/LRA.2023.3257707 | **arXiv**: 2210.09420
   - **thesis**: ニューラル密度場（NeRF 等）に物理特性を直接付加し、メッシュ抽出なしに微分可能物理エンジンでシミュレーションできる
   - **core**: 2 物体のニューラル密度場の積から Monte Carlo 積分で貫入体積・接触重心・接触力を計算する確率的接触モデル + Dojo 微分可能物理エンジン
   - **diff**: マーチングキューブによるメッシュ抽出はアーティファクト生成と凸分解が必要。DANOs は連続密度場上で直接動作しレベルセット選択とメッシュ前処理を排除
   - **limit**: 接触力は単一重心に適用（分散なし）。剛体のみ。RGB ビデオからの姿勢軌跡抽出は局所最適に陥る。微分可能トルク-ピクセルの完全ループは未達成

3. Zhou2022_EmergentExtrinsic — Zhou, W.; Held, D., "Learning to Grasp the Ungraspable with Emergent Extrinsic Dexterity" (2022)
   - **arXiv**: 2211.01500
   - **thesis**: 単純な平行グリッパでも、壁への押し付け等の接触リッチな外的器用さ行動をモデルフリー強化学習で学習でき、明示的な報酬設計なしにゼロショット sim-to-real 転移が可能
   - **core**: 目標条件付き RL + Operational Space Control によるコンプライアンス + オクルージョンペナルティ + マルチグラスプカリキュラム + Automatic Domain Randomization
   - **diff**: Chavan-Dafle et al. (2014) は手動コーディングのオープンループ。本手法はモデルフリー RL でクローズドループポリシーを学習し、物体固有チューニング不要
   - **limit**: ボックス形状のみで学習。物体姿勢のみでは新規形状の変動に不十分。正確なロボット・グリッパモデルを仮定

4. Nazir2022_RockAndWalk — Nazir, A.; Xu, P.; Seo, J., "Rock-and-Walk Manipulation: Object Locomotion by Passive Rolling Dynamics and Periodic Active Control" (2022)
   - **DOI**: 10.1109/tro.2021.3140147
   - **thesis**: 把持やプッシュが困難な大型・重量物体を、周期的な左右揺動と受動的重力転がり動力学により前方移動させる rock-and-walk 歩行で運搬できる
   - **core**: 物体の力学的エネルギーと姿勢を周期的揺動中に制御するフィードバック戦略。環境接触点での受動的転がり動力学を活用
   - **diff**: 従来の物体運搬（把持、プッシュ）は大型・重量物体に適用困難。Lynch & Mason (1996) のプッシュは持続接触力と平面物体を要求。3D 転がり動力学を活用した歩行は最小限の能動制御で実現
   - **limit**: limit not available

5. Cheng2023_HiDex — Cheng, X.; Patil, S.; Temel, Z.; Kroemer, O.; Mason, M. T., "Enhancing Dexterity in Robotic Manipulation via Hierarchical Contact Exploration" (2023)
   - **DOI**: 10.1109/LRA.2023.3333699 | **arXiv**: 2307.00383
   - **thesis**: 内的・外的器用さを統一する階層的フレームワーク — 環境接触モード選択、ロボット接触計画、経路評価の 3 レベル分解 — が、タスク固有学習なしに効率的な大域的接触空間探索を実現する
   - **core**: 3 レベル MCTS 階層 — L1: 環境接触モード＋RRT 物体軌道計画、L2: 接触再配置計画（各タイムステップではなく再配置タイミング）、L3: 準静的力解析＋軌道最適化
   - **diff**: CMGMP 等は特定タスクに限定で問題タイプ間の転移不能。HiDex は外的器用さ、インハンド操作、マルチロボット協調を統一的に解き、数秒で 100% 成功率
   - **limit**: 剛体・既知モデル・固定環境を仮定。オープンループ実行。接触力精度は実行時に未検証

6. Oller2024_TactileExtrinsic — Oller, M.; Berenson, D.; Fazeli, N., "Tactile-Driven Non-Prehensile Object Manipulation via Extrinsic Contact Mode Control" (2024)
   - **DOI**: 10.15607/RSS.2024.XX.135 | **arXiv**: 2405.18214
   - **thesis**: 把持ツールを通じた非把持操作は、微分可能接触モード制約上の勾配最適化とコンプライアント触覚センサで精密に制御できる
   - **core**: cvxpylayers による微分可能 QP（静的平衡＋Coulomb 摩擦）+ SEED 弾性モデル（センサ変形→外力レンチ）+ Contact Particle Filter
   - **diff**: 位置制御のみの手法と異なり、4 体接触チェーン（グリッパ-センサ-ツール-物体）を明示的に推論し力と姿勢を同時最適化。サンプルベース手法（MPPI, iCEM）より力精度と軌道滑らかさで優位
   - **limit**: 局所最適化で大域最適を逃しうる。ロボットワークスペース・関節限界を無視。弾性モデルは特にトルクで簡略化。連続スティッキング接触を仮定。平面準静的剛体動力学に限定

## Survey Methodology

### Search Review Checkpoint

- Papers presented to user: 50
- User additions: 0
- User removals: 0
- Target count adjustment: none
- Duplicates removed before checkpoint: 10

### Search Log

#### Search Angle 1: Dynamic Pushing Manipulation

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | WebSearch | "planar pushing manipulation center of mass inertia robot manipulator" | 10 | Found survey, Force Push, mode-aware pushing |
| 2 | WebSearch | "non-prehensile manipulation pushing dynamics center of mass estimation robot" | 10 | Found Lynch, ZMTEP, Dutta framework |
| 3 | Semantic Scholar | "planar pushing center of mass inertia robotic manipulation" (2020-2026) | 10 | Direct hits on CoM estimation via pushing |
| 4 | Semantic Scholar | "non-prehensile pushing manipulation dynamics planning" (2020-2026) | 30 | Many relevant + tangential |
| 5 | Semantic Scholar | "quasi-static pushing model contact mechanics robot" (2010-2026) | 30 | Jankowski, Halm/Posa, Zhou/Mason |
| 6-30 | Various | Multiple follow-up queries | ~200 | 34 unique papers from this angle |

#### Search Angle 2: Grasp Planning with Dynamics

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | Semantic Scholar | "grasp quality metric dynamics wrench space robot" (2020-2026) | 31 | Qiu2022, Zechmair2021, Chen2023, Park2020 |
| 2 | Semantic Scholar | "force closure grasp planning robot foundational" (1990-2009) | 261 | Ferrari1992, foundational papers |
| 3-29 | Various | Multiple queries for CoM-based grasping, physics-informed | ~300 | 29 unique papers from this angle |

#### Search Angle 3: Swing-up, Pivoting, Tumbling

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | Semantic Scholar | "swing-up manipulation robot manipulator dynamics" (2010+) | 2104 | SwingBot, Bi et al. |
| 2 | Semantic Scholar | "pivoting manipulation robot object reorientation" (2010+) | 136 | Shirai, Costanzo, Holladay, Chavan-Dafle |
| 3-15 | Various | Extrinsic dexterity, dynamic regrasping, rocking | ~200 | 23 unique papers from this angle |

#### Search Angle 4: Surveys & Foundational Works

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1-21 | Semantic Scholar | Targeted queries for Ferrari, Mason, Lynch, Bicchi, etc. | ~100 | 17 unique papers (8 surveys, 9 foundational) |

#### Search Angle 5: Inertia Estimation for Manipulation

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1-17 | Semantic Scholar + WebSearch | Inertial parameter estimation, interactive perception | ~150 | 14 unique papers |

**Source summary**: Google via WebSearch (~20 queries), Semantic Scholar API (~80 queries), arXiv API (indirect via WebSearch), ar5iv (~30 papers for full-text). Total ~112 search actions across 5 search angles.

### DOI Resolution Log

- Papers with publisher DOI resolved: 4 / 8
- Papers remaining arXiv-only: 3 (CoRL/arXiv proceedings: 2, preprint: 0, DOI not found: 1)
- Preprint (no DOI): 1 (Trupin 2025)
- Resolution sources used: DBLP (7 queries)

| Paper | arXiv ID | Publisher DOI | Source | Notes |
|-------|----------|---------------|--------|-------|
| Mavrakis 2017 | 1707.08150 | 10.1109/IROS.2017.8206258 | DBLP | IROS 2017 |
| Oller 2024 | 2405.18214 | 10.15607/RSS.2024.XX.135 | DBLP | RSS 2024 |
| Le Cleac'h 2022 | 2210.09420 | 10.1109/LRA.2023.3257707 | DBLP | RA-L 2023 |
| SwingBot 2020 | 2101.11812 | 10.1109/IROS45743.2020.9341006 | DBLP | IROS 2020 |
| Zhou & Held 2022 | 2211.01500 | — | — | CoRL 2022 (arXiv DOI only) |
| Toskov 2022 | 2210.05068 | — | — | CoRL 2022 (arXiv DOI only) |
| Chen 2023 | 2309.13586 | — | — | arXiv DOI only |
| Trupin 2025 | 2505.01399 | — | — | Preprint |

### Hallucination Check Results

- Papers checked: 50 (all via Semantic Scholar metadata during Phase 2)
- Passed: 50
- Failed and re-searched: 0
- Removed (unverifiable): 0

### Limit Field Coverage

- Papers with limit recorded: 36 / 50 (72%)
- Papers marked "limit not available": 14, breakdown:

| Category | Count | Papers | Action taken |
|----------|-------|--------|-------------|
| Paywall (IEEE, not extracted) | 5 | Holladay2015, Vina2016, Shi2017, Kolathaya2018, Ruggiero2018 | PDF fetched but binary extraction failed |
| Paywall (SAGE, 403) | 4 | Mason1986, Atkeson1986, Lynch1996, Lynch1999 | HTTP 403 |
| Paywall (Elsevier, 403) | 1 | Costanzo2021 | HTTP 403 |
| OA but no explicit section | 2 | Li2018, Goyal1991 | No Limitations section in paper |
| Partial OA extraction | 2 | Nazir2022, Chavan-Dafle2018 | Key sections extracted, no explicit limits |

### Threats to Validity

- **Search scope**: WebSearch (Google) と Semantic Scholar API を主要ソースとし、Scopus・Web of Science は未使用。英語論文のみ。2010 年以降を重点とし、それ以前は高被引用論文に限定。
- **Publication bias**: arXiv プレプリント（Trupin 2025, Chen 2023 等）を含めることで査読済み会場の肯定的結果偏向を部分的に緩和。ただし否定的結果の論文は系統的に探索していない。
- **Selection bias**: マニピュレータ（アーム/ハンド）ベースに限定し、移動ロボットロコモーションと航空操作を除外。これにより関連する制御理論やロコモーション-操作統合研究が欠落している可能性がある。
- **Analysis limitations**: AI 支援の単一レビューア分析。Paywall 論文 10 本（20%）はアブストラクト・メタデータのみで limit フィールドが欠損。IEEE PDF のテキスト抽出失敗により、5 本の全文分析が実施できなかった。

## Conclusion

1. **RQ1 (主要アルゴリズムアプローチの大別)**: 5 カテゴリに大別される — (A) プッシュ力学・接触モデリング（解析→データ駆動→微分可能物理の進化軸）、(B) 慣性パラメータ推定（力/トルクベース→アクティブ探索→固有受容ベースの進化軸）、(C) 把持品質・物理情報把持（GWS メトリクス→深層学習→LMM 物理推論の進化軸）、(D) インハンド動的操作（ピボット・スイングアップ・スライディング、モデルベース→触覚学習の進化軸）、(E) 外的器用さ・接触活用（環境接触のプリミティブ設計→RL 学習の進化軸）。

2. **RQ2 (物体動力学の計画・制御への組み込み方)**: 物体動力学の組み込み方は大きく 3 つ — (a) 明示的パラメータとして解析モデルに組み込む（Mason 1986, Goyal 1991, Shirai 2023）、(b) 学習モデルで暗黙的に捕捉する（Li 2018, SwingBot 2020, Zhou & Held 2022）、(c) 微分可能シミュレーションの最適化変数とする（Song 2020, Le Cleac'h 2022, Chen 2024）。(a) は解釈性が高いが既知パラメータを仮定、(b) は柔軟だが汎化が課題、(c) は両者の利点を狙うが計算コストと局所最適の問題がある。

3. **RQ3 (評価環境と再現実装の容易さ)**: 全 50 論文中 36% が sim+real の両方で評価、20% が実機のみ。プッシュ分野は Yu et al. (2016) の MIT データセットが共通ベンチマークとして機能。把持分野は Dex-Net が広く参照される。コード公開は限定的で、Song 2020, Mahler 2017, Chen 2023, PhyGrasp 2024, Zhou & Held 2022 が公開。再現実装に最も適したエントリポイントは、カテゴリ別に (A) Hogan 2020 の hybrid MPC、(B) Nadeau 2022 の PMD、(C) Chen 2023 の微分可能 GWS、(D) Shirai 2023 の CIBO、(E) Zhou & Held 2022 の RL extrinsic dexterity である。
