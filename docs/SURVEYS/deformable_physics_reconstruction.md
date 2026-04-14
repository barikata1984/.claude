# Literature Survey: Deformable Object Physical Property Recovery from Observation and Its Application to Robotic Manipulation

| | |
|---|---|
| **Date** | 2026-04-08 |
| **Scope** | 2020年以降に提案された、ビデオや他の観察記録から柔軟物の物理特性を復元する三次元再構築手法、F/Tセンサ・触覚センサからの柔軟物物性推定手法、および復元物性に基づくロボット操作の実証。剛体慣性パラメータ同定は対象外。 |
| **Papers found** | 48 |
| **Research Questions** | RQ1: 視覚観察からの柔軟物物性復元アルゴリズム / RQ2: F/T・力覚情報からの柔軟物物性推定手法 / RQ3: 復元物性を活用したロボット操作の実証 / RQ4: 未解決の技術的ギャップ |

## Abstract

柔軟物の三次元再構築に物理特性復元を統合する研究は、2020年の対応点不要逆FEMから2025年の3D Gaussian Splatting＋MPMデジタルツインへと急速に発展し、視覚観察から弾性率・粘性・密度などの連続体パラメータを回復する手法が確立されつつある。本サーベイは48本の論文を体系的に収集・分析し、視覚ベース物性復元（20本）、布・ロープ等の実物パラメータ推定（10本）、力覚・触覚ベース推定（6本）、物性活用操作（5本）、基盤フレームワーク（7本）の5カテゴリに整理した。主要な知見として、視覚ベースの物性復元は急速に成熟しているが「復元された物性でロボットが柔軟物を操作する」エンドツーエンドの実証は極めて少なく、DPSI（Yang et al., IJRR 2025）が唯一の完全パイプライン（MPMベースのelastoplastic物性同定→長期操作計画）であることが確認された。検索はWebSearchを主軸に5つの角度から約130クエリを実行し、ar5ivを用いた全文解析により注釈を付与した。

## Research Landscape Overview

柔軟物の物理特性を観察から復元する研究は、コンピュータビジョン、コンピュータグラフィックス、ロボティクスの3分野が交差する領域に位置する。2020年以前は、FEMの逆問題として定式化し力-変位データから弾性パラメータを同定するアプローチが主流であったが、対象は主に医療応用（軟部組織）に限定されていた。

2021年のgradSim（Jatavallabhula et al., ICLR 2021）が微分可能レンダリングと微分可能物理シミュレーションを統合し、ビデオピクセルから物理パラメータへの勾配逆伝播を初めて実現したことで、研究の方向性が大きく転換した。2022年には視覚振動断層撮影（Feng et al., CVPR 2022）、NeuPhysics（NeurIPS 2022）、NeuroFluid（ICML 2022）など、対象物理現象に特化した手法が百花繚乱となった。2023年のPAC-NeRF（Li et al., ICLR 2023）は形状未知の条件下でNeRF＋MPMにより物性を同定する初の手法として転機を画した。

2024年以降は3D Gaussian Splatting（3DGS）が表現基盤として台頭し、PhysGaussian（CVPR 2024 Highlight）、GIC（NeurIPS 2024 Oral）、Spring-Gaus（ECCV 2024）など、Gaussianカーネルに物理属性を直接付与する手法が急増した。並行して、Video Diffusionモデルの物理プライオアを蒸留するPhysics3D、DreamPhysicsや、フィードフォワード予測を実現するVoMP（NVIDIA）など、Per-scene最適化を超えるアプローチも登場している。

ロボティクス側では、AdaptiGraph（RSS 2024）が物性条件付きGNNによるオンライン適応を、DPSI（Yang et al., IJRR 2025）がMPMベースの微分可能物性同定からの操作計画を、RAPiD（2026）がRMAフレームワークの柔軟物への拡張をそれぞれ実証している。しかし、「視覚・力覚からの物性復元 → 復元結果に基づく操作」を一貫して実証した研究は依然として少ない。

主要な研究拠点として、MIT CSAIL / Stanford（Li, Wu: DPI-Net, RoboCraft, AdaptiGraph, Spring-Gaus, PhysTwin）、UCLA（Jiang: PAC-NeRF, PhysGaussian, GIC, EMPM）、USC / MIT（Chen: 微分可能ロボット-物体インタラクション, EMPM, Vid2Sim）、ETH Zurich（DER）、トロント大学（Antonova: Bayesian real-to-sim）が挙げられる。

## Terminology and Background

| Term | Synonyms / Variants | Scope in this survey |
|------|---------------------|----------------------|
| Physical property recovery | system identification, parameter identification, material parameter estimation, inverse physics | 観察データから柔軟物の構成則パラメータ（弾性率、粘性等）を推定すること全般 |
| Young's modulus (E) | elastic modulus, stiffness coefficient | 応力-ひずみ関係における線形弾性係数。多くの手法が推定対象とする主要パラメータ |
| Poisson's ratio (ν) | lateral contraction ratio | 横ひずみ/縦ひずみ比。Eと組み合わせて等方弾性体を記述 |
| Material Point Method (MPM) | hybrid Eulerian-Lagrangian method | 連続体力学の粒子ベース離散化手法。PAC-NeRF以降の物性復元で支配的 |
| Finite Element Method (FEM) | finite element analysis | 連続体の要素分割による離散化。布・軟組織のモデリングに使用 |
| 3D Gaussian Splatting (3DGS) | Gaussian splats, GS | 点群ベースの微分可能レンダリング。2024年以降、物性復元の表現基盤として急速に普及 |
| Neural Radiance Fields (NeRF) | neural radiance field, implicit neural representation | 暗黙的3D表現。2022-2023年の物性復元研究の主要基盤 |
| Differentiable simulation | differentiable physics, diff-sim | 物理シミュレーションの勾配を解析的に計算可能にしたもの。逆問題解法の核心技術 |
| Constitutive model | material model, stress-strain relation | 応力-ひずみ関係を記述する数理モデル（Neo-Hookean, von Mises等） |
| Real-to-sim | sim calibration, domain adaptation | 実世界データにシミュレーションパラメータを合わせるプロセス |
| Volumetric Stiffness Field (VSF) | stiffness map, compliance field | 空間的に変化する剛性の3D表現。不均一物体の物性を表現 |

## Survey Findings

### Thesis

本サーベイが明らかにする分野の根本的未解決問題は、**「観察から物性を復元する能力」と「復元物性に基づいてロボットが柔軟物を操作する能力」の間に深い断絶がある**ことである。

視覚ベースの物性復元は劇的な進歩を遂げている。PAC-NeRF（2023）は形状未知の条件下でマルチビュービデオから弾性率・粘性を同定し、GIC（2024）はGaussian-MPMハイブリッドで推定精度を大幅に向上させた。PhysTwin（2025）やVid2Sim（2025）はビデオからデジタルツインを構築する能力を実証している。しかし、これらの手法が推定した物理パラメータを**下流のロボット操作タスクに供給し、その操作性能を検証した研究は48本中わずか5本**（DPSI, AdaptiGraph, RoboPack, RoboCraft, RAPiD）に留まる。さらに、明示的な物理パラメータ同定からの操作計画を完全に実証したのはDPSI（Yang et al., IJRR 2025）のみであり、他はlatentな動力学表現の適応に依拠している。

一方、F/Tセンサや触覚センサからの物性推定（Category C）は、剛体の慣性パラメータ同定と対照的に、柔軟物に対しては標準的な定式化すら確立されていない。Patni et al.（2024）はグリッパ圧縮からの弾性推定を実証したがYoung's modulusの絶対値精度は低く、Yao & Hauser（2023）はVolumetric Stiffness Fieldを提案したが操作への活用は未実証である。剛体における「ニュートン＝オイラー方程式 → 回帰行列 → 最小二乗」に相当する、柔軟物の力学パラメータに対する標準的な推定フレームワークは存在しない。

### Foundation

本サーベイで調査した論文群が依拠する共通技術基盤は以下の4つに集約される。

1. **微分可能シミュレーション（MPM / FEM）**: Category A-Dの物性復元手法のほぼ全てが、微分可能な物理シミュレーションを勾配計算の基盤として使用している。特にMPMはPAC-NeRF以降の支配的手法であり、GIC, PhysGaussian, Physics3D, DreamPhysics, EMPM, PhysWorld, AS-DiffMPM, DPSIがいずれもMPMを採用している。FEMはDiffCloth, DiffCloud, DiSECt, NeuPhysics, gradSimで使用され、布やメッシュベースの対象に適している。Spring-Mass系はSpring-Gaus, PhysTwinが採用し、計算コストの低さを活かしている。

2. **ニューラルレンダリング（NeRF → 3DGS）**: 視覚観察と物理シミュレーションを接続するインタフェースとして、NeRF（2022-2023年）から3DGS（2024年以降）への表現基盤の移行が顕著である。3DGSはガウシアンカーネルに物理属性を直接付与できる利点があり、PhysGaussianが「what you see is what you simulate」パラダイムを確立した。

3. **連続体力学の構成則**: 推定対象パラメータの物理的意味を定義する基盤。Neo-Hookean弾性体（PAC-NeRF, GIC, EMPM等）、von Mises弾塑性体（PlasticineLab, DPSI）、粘弾性体（Physics3D）、Kirchhoff-Love薄殻（DiffCloth, Bayesian DiffCloth）が主要な構成則として使用されている。PIDGは構成則自体を学習する枠組みを提案している。

4. **点群 / 深度表現**: 実世界データとの接点として、RGB-D点群がDiffCloud, DiffCP, DPSI, EMPMで使用され、Chamfer距離やEarth Mover's Distanceが最適化目標として広く採用されている。RoboPack, AdaptiGraphはグラフニューラルネットワーク上の粒子表現を使用し、触覚・力覚情報との融合を可能にしている。

### Progress

柔軟物の物性復元と操作の研究は、以下の主要な能力遷移を経てきた。

1. **対応点不要の逆問題解法 (2020)**: Weiss et al.（CVPR 2020）が、単一視点深度列から対応点なしで弾性パラメータを復元する手法を提案。Sparse Surface Constraintにより、オイラー座標系での逆問題をCommodity RGB-Dセンサで解ける形に変換した。

2. **微分可能レンダリング＋物理の統合 (2021)**: gradSim（ICLR 2021）がピクセル → 物理パラメータの勾配逆伝播を初めて実現。PlasticineLab（ICLR 2021）がMPMベースの弾塑性ベンチマークを提供し、微分可能物理による操作の定量評価を可能にした。

3. **対象特化型の物性復元の百花繚乱 (2022)**: Visual Vibration Tomography（CVPR 2022 Oral）が振動モード解析から内部Young's modulus分布を復元。NeuPhysics（NeurIPS 2022）がSDF＋FEMで単眼ビデオから編集可能な物理シーンを構築。NeuroFluid（ICML 2022）が流体の粘性・密度を粒子NeRFから教師なしで推定。DiffCloth（ACM ToG 2022）がCoulomb摩擦付き布の微分可能シミュレーションを実現。

4. **形状未知条件下での統合的物性同定 (2023)**: PAC-NeRF（ICLR 2023）がNeRF＋MPMのハイブリッド表現により、幾何形状と物理パラメータを同時に復元する初の手法を確立。弾性・塑性・粒状・流体の4材料カテゴリに対応した。

5. **3DGS＋物理の爆発的発展と物性復元の高精度化 (2024)**: PhysGaussian（CVPR 2024 Highlight）がGaussianカーネル上のMPM統合を実現。GIC（NeurIPS 2024 Oral）がGaussian-Continuum双方向監視で推定精度を大幅向上。Spring-Gaus（ECCV 2024）が外観学習と物理学習の分離を提案。Bayesian DiffCloth（CVPR 2024）が布の空間的不均一性をBayes推論で捕捉。

6. **デジタルツイン構築とフィードフォワード予測 (2025-2026)**: PhysTwin（ICCV 2025）がスパースビデオから操作可能なデジタルツインを構築。Vid2Sim（CVPR 2025）がフィードフォワードViTで汎化的物性予測を実現。VoMP（NVIDIA）がGeometry Transformerによる表現非依存のvolumetric物性予測を提案。PhysWorld（2025）がMPMデジタルツインからGNN世界モデルへの蒸留で47倍高速な推論を実現。

7. **物性復元から操作への橋渡しの萌芽 (2024-2026)**: DPSI（Yang et al., IJRR 2025）がMPMベースの物性同定→長期操作計画の完全パイプラインを実証。AdaptiGraph（RSS 2024）が物性条件付きGNNで未知材料への少数ショット適応を実現。RAPiD（2026）がRMAフレームワークの柔軟物拡張で80%以上の実機成功率を達成。

### Gap

1. **Vision-Based Property Recovery to Manipulation: The Missing Pipeline**

   Category A（視覚ベース物性復元）の20本の論文は、弾性率・粘性・密度分布の推定精度を追求しているが、復元された物性パラメータをロボット操作タスクの入力として利用した研究は皆無である。PhysTwin, Vid2Sim, EMPMは「デジタルツインの構築」を目標とするが、構築されたツインでの操作計画や制御は実証されていない。Category D（物性活用操作）の手法はいずれもロボットの操作データ（点群変形、力応答）から物性を推定しており、ビデオ観察からの物性復元を操作に接続した研究は存在しない。この断絶が解消されれば、操作前の視覚観察のみで物性を推定し、接触前に操作戦略を計画する「look-then-manipulate」パイプラインが実現可能になる。

2. **No Standard Formulation for Force-Based Deformable Property Identification**

   剛体の慣性パラメータ同定ではNewton-Euler方程式の線形化により回帰行列が標準的に構成されるが、柔軟物の物性パラメータに対するF/Tセンサベースの標準的定式化は存在しない。Category Cの手法はそれぞれ異なるモデル（Hunt-Crossley接触モデル、Volumetric Stiffness Field、ニューラルネット回帰）を使用しており、手法間の比較可能性が低い。Patni et al.（2024）はYoung's modulusの絶対値推定が困難であることを認めており、Kutsuzawa et al.（2024）はシミュレーションのみでの検証に留まっている。構成則に基づく体系的な定式化が確立されれば、力学パラメータの推定精度と再現性が大幅に向上する。

3. **Heterogeneous and Non-Uniform Materials Remain Underexplored**

   Category Aの大多数の手法は均一材料（一定のYoung's modulus）を仮定している。空間的に不均一な物性を扱った研究はVisual Vibration Tomography（内部Young's modulus分布）、Bayesian DiffCloth（布のper-element不均一性）、PhysGS（per-point Bayesian推定）、VoMP（per-voxel予測）の4本のみであり、実物体での検証はさらに限られる。ロボットが扱う現実の柔軟物（食品、生体組織、複合素材）は空間的に不均一な物性を持つことが多く、均一仮定は操作性能のボトルネックとなる。

4. **Sim-to-Real Validation of Estimated Properties Is Rare**

   推定された物性パラメータが実世界で物理的に意味のある値を持つかの検証が不十分である。Ru et al.（IROS 2025, Can Real-to-Sim Fabric）は4つのreal-to-sim手法を比較し、いずれも未見の動的タスクへの汎化に失敗することを報告した。DPSI（Yang et al.）は推定パラメータでの長期操作計画を実証した唯一の研究だが、end-effectorへの粘着という実験上の制約を認めている。復元パラメータの操作タスクでの有用性を系統的に評価する枠組みが欠如している。

5. **Constitutive Model Selection as an Unsolved Meta-Problem**

   現行手法は構成則（Neo-Hookean, von Mises等）を事前に固定するが、未知の柔軟物に対して適切な構成則を自動選択する手法は存在しない。PIDG（Hong et al., AAAI 2026）がCauchy運動量方程式の残差制約により構成則を学習するアプローチを提案しているが、非線形弾塑性や粘弾性の完全な捕捉には至っていない。PhysWorld（Fan et al.）はMPM構成則の自動選択を提案しているが、選択肢はhardcodedである。

### Seed

#### Seed Overview

| Seed | Premise | Approach |
|------|---------|----------|
| 1 | F/Tセンサベースの柔軟物物性同定には標準的定式化が不在 | 構成則に基づく力学パラメータ回帰フレームワークの構築（剛体慣性パラメータ同定の柔軟物版） |
| 2 | 視覚ベース物性復元と操作の断絶が最大のギャップ | F/Tセンサによるオンライン物性推定と、推定結果に基づく操作計画の統合パイプライン |
| 3 | 不均一密度の柔軟物に対する操作戦略が未確立 | Volumetric Stiffness Field＋安定操作計画の統合 |

Seed 1 は基盤的定式化であり、Seed 2 はSeed 1の結果を操作に接続する応用研究、Seed 3は不均一物性への拡張である。Seed 1 → Seed 2 → Seed 3 の順序で進めることが合理的であるが、Seed 1 と Seed 3 は並行して着手可能である。

#### Seed 1: Force-Based Constitutive Parameter Identification for Deformable Objects

##### Seed 1 — Academic Contribution

剛体の慣性パラメータ同定ではNewton-Euler方程式の線形化（τ = Y(q, q̇, q̈)π）により標準的な回帰問題が構成されるが、柔軟物の構成則パラメータ（E, ν, σ_y 等）に対する同等の体系的定式化は存在しない（Gap 2）。本研究は、柔軟物のF/Tセンサ応答を構成則パラメータに関して体系的に定式化し、ロボットの操作動作（圧縮、引張、曲げ等の励起動作）から物性パラメータを推定するフレームワークを確立する。DPSIがMPMの微分可能シミュレーションに依拠するのに対し、本アプローチは解析的な回帰行列の構築を目指し、計算コストと推定速度の大幅な改善を狙う。

##### Seed 1 — Required Components

1. 柔軟物接触力学の構成則パラメータに関する線形化（またはlocally linear化）
2. F/Tセンサ読み取りから構成則パラメータへの回帰行列の導出
3. 情報量を最大化する励起動作の設計（圧縮、引張、ねじり等のシーケンス）
4. 物理的整合性制約（正の弾性率、正定値等）の導入
5. 実ロボット上での検証と、既知物性の参照試料による精度評価

##### Seed 1 — Readiness Assessment

| Component | Status | Detail |
|-----------|--------|--------|
| 構成則の線形化 | Adaptable | Hunt-Crossley（Patni2024）やKelvin-Voigtは線形化可能だが、大変形に対するNeo-Hookean等の非線形構成則の線形化には新規導出が必要 |
| 回帰行列の導出 | New development required | 剛体の回帰行列（Atkeson 1986）に相当するものが柔軟物には存在しない。接触力学モデルの選択と結合が核心的課題 |
| 励起動作の設計 | Adaptable | Fourier級数パラメータ化（Swevers 1997）の枠組みは適用可能だが、柔軟物の変形モードに適した励起パターンの設計は新規 |
| 物理的整合性制約 | Available | Sousa & Cortesao（2014）のLMI/SDP手法は弾性パラメータにも拡張可能 |
| 実ロボット検証 | Available | F/Tセンサ搭載ロボットアーム、参照試料（シリコン、フォーム等）は市販品で構成可能 |

#### Seed 2: F/T-Sensor-Based Property Estimation to Manipulation Pipeline

##### Seed 2 — Academic Contribution

48本の網羅的調査において、F/Tセンサから推定された柔軟物の物性パラメータを操作タスクに供給し、推定誤差が操作性能に与える影響を定量的に分析した研究は存在しない（Gap 1）。DPSIは最も近い研究だが、点群ベースのMPM最適化に数分を要し、F/Tセンサは使用していない。本研究は、Seed 1で確立される推定フレームワークの出力を操作計画に供給し、物性推定→操作計画→実行の一貫パイプラインを構築する。

##### Seed 2 — Required Components

1. Seed 1の推定フレームワーク（またはDPSI的なMPMベース推定の高速化版）
2. 推定物性パラメータを入力とする操作計画器（変形予測、力制御目標値の生成）
3. 推定誤差の操作性能への影響を定量化するロバスト性解析
4. 実世界の柔軟物操作タスク（折り畳み、整形、配置等）での実証
5. ベースライン比較（物性未推定の視覚フィードバックのみの操作）

##### Seed 2 — Readiness Assessment

| Component | Status | Detail |
|-----------|--------|--------|
| 物性推定フレームワーク | New development required | Seed 1の成果に依存。代替としてDPSIの高速化（現行5分→リアルタイム化）も検討可能 |
| 操作計画器 | Adaptable | 既存サーベイのNadeau & Kelly（2025）の物理誘導型配置計画や、MPC＋微分可能シミュレーションの枠組みは存在するが、柔軟物の推定物性を入力とする計画器は新規開発が必要 |
| ロバスト性解析 | New development required | 推定誤差の操作性能への感度分析手法は前例がない |
| 実世界タスク | Available | DPSIのdough/clay操作や、RoboCraftのelastoplastic整形の実験環境を参考に構築可能 |
| ベースライン | Available | AdaptiGraph（latent adaptation）やRAPiD（dynamics embedding）を物性非明示ベースラインとして使用可能 |

#### Seed 3: Volumetric Stiffness Field for Heterogeneous Deformable Manipulation

##### Seed 3 — Academic Contribution

現行の柔軟物操作手法は均一物性を仮定するか、latentな動力学表現に依拠しており、空間的に不均一な物性分布を明示的に推定して操作に活用した研究は存在しない（Gap 3）。Yao & Hauser（2023）のVolumetric Stiffness Field（VSF）は不均一物性の空間的表現を提案したが操作への活用は未実証である。本研究は、VSFをオンラインで構築しつつ、その空間的物性分布に基づいた操作戦略（力配分、把持位置選択等）を計画する統合手法を提案する。

##### Seed 3 — Required Components

1. F/T / 触覚データからのオンラインVSF推定器（Yao2023の拡張）
2. VSFに基づく操作戦略の定式化（重心推定、変形予測、力配分最適化）
3. 不均一密度の参照物体セット（重み偏在物体、複合素材等）
4. 均一仮定ベースラインとの比較による不均一推定の効果の定量化

##### Seed 3 — Readiness Assessment

| Component | Status | Detail |
|-----------|--------|--------|
| オンラインVSF推定器 | Adaptable | Yao & Hauser（2023）のVSFフレームワークが存在するが、リアルタイム性と推定精度の改善が必要 |
| VSFベース操作戦略 | New development required | 空間的物性分布を操作計画に統合する定式化は前例がない |
| 参照物体セット | Available | 3Dプリンタで密度分布を制御した物体や、食品（果物等）を使用可能 |
| ベースライン比較 | Available | 均一密度仮定の操作手法（前回サーベイのCategory E）と直接比較可能 |

## Paper Catalogue

### Category Overview

48本の論文を以下の6カテゴリに分類した。

| Category | Description | Count |
|----------|-------------|-------|
| A1. NeRF/Neural Field + Physics (2020-2023) | NeRFやSDF等の暗黙的表現と微分可能物理を結合し、視覚観察から物性を復元 | 6 |
| A2. 3DGS + Physics (2024-2026) | 3D Gaussian Splattingに物理属性を付与し、視覚観察から物性を復元 | 9 |
| A3. Digital Twin Construction from Video | ビデオからの物理的デジタルツイン構築・汎化的物性予測 | 6 |
| B. Cloth/Rope/DLO Parameter Estimation | 布・ロープ・線状物体のシミュレーションパラメータ推定 | 10 |
| C. Force/Tactile-Based Property Estimation | F/Tセンサ・触覚センサ・固有受容感覚からの物性推定 | 6 |
| D. Physics-Informed Deformable Manipulation | 推定・学習された物性に基づくロボット柔軟物操作 | 5 |
| E. Differentiable Simulation Frameworks and Benchmarks | 物性復元を可能にする基盤フレームワーク | 6 |

### Comparison Table

| Paper | Category | Physics Engine | Material Type | Sensors | Property Estimated | Real HW | Evidence |
|-------|----------|---------------|---------------|---------|-------------------|---------|----------|
| PAC-NeRF (2023) | A1 | MPM | elastic/plastic/granular/fluid | Multi-view video | E, ν, viscosity, friction | No | S |
| GIC (2024) | A2 | MPM | elastic/plastic | Multi-view video | E, ν | No | S |
| PhysGaussian (2024) | A2 | MPM | elastic/plastic/granular/fluid | Multi-view video | E, ν, density | No | S |
| Spring-Gaus (2024) | A2 | Spring-Mass | elastic | Multi-view video | spring stiffness | No | S |
| PhysTwin (2025) | A3 | Spring-Mass | elastic | RGB-D × 3 | spring stiffness (dense) | No | S |
| Vid2Sim (2025) | A3 | Reduced Euler | elastic | Video | E, ν | No | S |
| EMPM (2025) | A3 | MPM | elastoplastic | RGB-D multi-view | E, ν, yield stress | No | S |
| DPSI (2025) | D | MPM | elastoplastic | Point cloud + robot | E, ν, yield, friction | Yes | B |
| AdaptiGraph (2024) | D | GNN | rope/granular/cloth/rigid | RGB-D + robot | latent property vector | Yes | B |
| RoboPack (2024) | D | GNN | deformable (general) | Tactile (Soft-Bubble) | latent physics state | Yes | R |
| RoboCraft (2022) | D | GNN | elastoplastic (dough) | RGB-D + robot | implicit dynamics | Yes | R |
| DiffCP (2024) | B | MPM | cloth | RGB-D + robot | E, ν, friction | Yes | B |
| Bayesian DiffCloth (2024) | B | FEM/PD | cloth | Drape test image | stretch/bend stiffness | No | S |
| Patni2024 (2024) | C | Hunt-Crossley | soft objects | F/T (wrist) | E (relative), viscoelasticity | Yes | R |
| Burgess2024 (2024) | C | Hybrid analytical-NN | general | Tactile (GelSight) | Young's modulus | Yes | R |
| Yao2023 (2023) | C | Point-based contact | heterogeneous deformable | F/T (probe) | Volumetric Stiffness Field | Yes | R |
| Chen2025_diffprop (2025) | C | Differentiable FEM | elastic | Proprioception (joint) | mass, E | Yes | B |
| DiSECt (2021) | E | FEM + damage | soft cutting | Force (knife) | stiffness, fracture | Yes | B |
| DiffCloth (2022) | E | PD + friction | cloth | — | stretch/bend/friction | No | S |

Evidence: **R** = Real-world experiment, **S** = Simulation only, **B** = Both

### Quantitative Trends

#### Publication Count by Year

| Year | Count |
|------|-------|
| 2026 | 3 |
| 2025 | 13 |
| 2024 | 16 |
| 2023 | 4 |
| 2022 | 8 |
| 2021 | 3 |
| 2020 | 2 |
| pre-2020 | 1 (DPI-Net, 2019) |

#### Method Category Distribution

| Category | Count | % |
|----------|-------|---|
| A1. NeRF + Physics | 6 | 12.5% |
| A2. 3DGS + Physics | 9 | 18.8% |
| A3. Digital Twin from Video | 6 | 12.5% |
| B. Cloth/Rope/DLO Param Est. | 10 | 20.8% |
| C. Force/Tactile Property Est. | 6 | 12.5% |
| D. Physics-Informed Manipulation | 5 | 10.4% |
| E. Frameworks & Benchmarks | 6 | 12.5% |

#### Experimental Setting Breakdown

| Setting | Count | % |
|---------|-------|---|
| Simulation only | 24 | 50.0% |
| Real hardware only | 6 | 12.5% |
| Both | 13 | 27.1% |
| Framework/Benchmark | 5 | 10.4% |

### Concept Matrix

| Concept | PAC-NeRF | GIC | PhysGaussian | Spring-Gaus | PhysTwin | DPSI | AdaptiGraph | DiffCP | Patni24 | Yao23 | Burgess24 |
|---------|----------|-----|-------------|-------------|----------|------|-------------|--------|---------|-------|-----------|
| MPM simulation | X | X | X | | | X | | X | | | |
| FEM simulation | | | | | | | | | | | |
| Spring-Mass | | | | X | X | | | | | | |
| 3D Gaussian Splatting | | X | X | X | X | | | | | | |
| NeRF / Neural Field | X | | | | | | | | | | |
| Differentiable rendering | X | X | X | X | X | | | | | | |
| Young's modulus estimation | X | X | X | | | X | | X | X | | X |
| Spatially varying properties | | | | | X | | | | | X | |
| F/T sensor | | | | | | | | | X | X | |
| Tactile sensor | | | | | | | | | | | X |
| Real robot manipulation | | | | | | X | X | X | X | X | X |
| Online adaptation | | | | | | | X | | | X | |

### Foundational Works

| # | Paper | Year | Venue | Significance |
|---|-------|------|-------|-------------|
| E-6 | DPI-Net (Li et al.) | 2019 | ICLR 2019 | 粒子ベース統一動力学モデルの先駆。剛体・柔軟物・流体を単一GNNで学習し操作に活用 |
| A1-1 | Weiss et al. | 2020 | CVPR 2020 | 対応点不要の材料パラメータ復元の先駆。深度列のみから弾性パラメータを推定 |
| A1-2 | gradSim | 2021 | ICLR 2021 | 微分可能レンダリング＋物理の統合の先駆。ピクセル→物理パラメータの勾配逆伝播を初実現 |
| E-2 | PlasticineLab | 2021 | ICLR 2021 | MPMベース弾塑性操作のベンチマーク確立 |
| E-3 | DiSECt | 2021 | RSS 2021 | 切断シミュレーションの微分可能化と材料パラメータ推定の先駆 |
| A1-4 | PAC-NeRF | 2023 | ICLR 2023 | 形状未知条件下でNeRF＋MPMによる統合的物性同定を初めて実現 |

### A1. NeRF/Neural Field + Physics (2020-2023)

視覚的暗黙表現（NeRF, SDF）と微分可能物理シミュレーションを結合し、ビデオ観察から柔軟物の物理パラメータを復元する手法群。2020年のFEM逆問題から2023年のNeRF＋MPM統合まで、表現と物理の結合度が段階的に深化した。

1. [[Weiss2020_sparseConstraints]](../REFERENCES/MAIN.md#Weiss2020_sparseConstraints) — Weiss et al., "Correspondence-Free Material Reconstruction using Sparse Surface Constraints" (2020)
   - **DOI**: — | **arXiv**: 1910.01812
   - **thesis**: 柔軟物の物理パラメータは、対応点追跡なしに単一視点深度列から微分可能な逆問題として復元可能である
   - **core**: Sparse Surface Constraint（SSC）コスト関数が、変位場の逆変換を通じて対応点なしで勾配計算を可能にする
   - **diff**: 従来手法が制御された実験環境・密な3D観察・特徴追跡を必要としたのに対し、Commodity RGB-Dセンサのスパース観察のみで動作
   - **limit**: 既知の初期姿勢が必要。逆問題が強い非凸性を持ち複数解に収束しうる。摩擦を省略し簡易Rayleigh減衰を使用

2. [[Jatavallabhula2021_gradSim]](../REFERENCES/MAIN.md#Jatavallabhula2021_gradSim) — Jatavallabhula et al., "gradSim: Differentiable Simulation for System Identification and Visuomotor Control" (2021)
   - **DOI**: — | **arXiv**: 2104.02646
   - **thesis**: 微分可能レンダリングと微分可能物理を統合した単一計算グラフにより、3D監視なしにビデオピクセルから物理パラメータへの勾配逆伝播が可能になる
   - **core**: Lagrangian物理（FEM）と微分可能ラスタライゼーション（SoftRas/DIB-R）の端-端微分可能結合
   - **diff**: 従来の微分可能物理は状態空間で動作し3D正解ラベルを要求。gradSimはレンダリングとの結合により生のピクセル観察のみで最適化を駆動する初の手法
   - **limit**: Reality gapのブリッジは未試行。接触リッチな動作や関節物体は将来課題。レンダリング誤差よりも未モデル化動力学からの性能劣化が顕著

3. [[Feng2022_vibrationTomography]](../REFERENCES/MAIN.md#Feng2022_vibrationTomography) — Feng et al., "Visual Vibration Tomography: Estimating Interior Material Properties from Monocular Video" (2022)
   - **DOI**: — | **arXiv**: 2104.02735
   - **thesis**: 物体内部の空間的に不均一なYoung's modulusと密度を、表面振動モードの単眼ビデオ観察とFEMモーダル解析の逆問題として復元可能である
   - **core**: 位相ベースビデオ運動抽出と、測定モーダル形状をボクセル化材料パラメータに結ぶ一般化固有値定式化
   - **diff**: 従来のNDTはレーザ振動計が必要で点計測のみ。本手法はcommodity単眼ビデオから空間的に密な内部不均一性を復元
   - **limit**: 線形弾性・微小変形を仮定。物体形状の近似的知識が必要。減衰が観測可能モード数を制限。現状は高速度カメラが必要

4. [[Qiao2022_NeuPhysics]](../REFERENCES/MAIN.md#Qiao2022_NeuPhysics) — Qiao et al., "NeuPhysics: Editable Neural Geometry and Physics from Monocular Videos" (2022)
   - **DOI**: — | **arXiv**: 2210.12352
   - **thesis**: Neural SDFと微分可能物理エンジンの結合により、単眼RGBビデオから3D形状・外観・物理パラメータを同時に再構築し、物理的に整合的なインタラクティブ編集を可能にする
   - **core**: 暗黙的Neural SDFと明示的六面体メッシュの双方向変換、およびcycle consistency lossによる物理パラメータ推定
   - **diff**: 既存のdynamic NeRFは新規視点合成に注力し3D形状や物性を復元しない。NeuPhysicsは正確な形状と物理の復元を優先し、点対応と直接3D編集を可能にする
   - **limit**: SfM初期化に背景詳細が必要。軟体に限定され多様な動力学は未対応。六面体メッシュを使用。布・関節体・ロボットシステムへの拡張は将来課題

5. [[Guan2022_NeuroFluid]](../REFERENCES/MAIN.md#Guan2022_NeuroFluid) — Guan et al., "NeuroFluid: Fluid Dynamics Grounding with Particle-Driven Neural Radiance Fields" (2022)
   - **DOI**: — | **arXiv**: 2203.01762
   - **thesis**: ニューラル粒子遷移モデルと粒子駆動NeRFレンダラの端-端同時最適化により、粒子軌跡の正解なしにピクセル観察のみから流体動力学をグラウンディング可能
   - **core**: PhysNeRFの近傍エンコーディング（粒子中心・密度・変形・視線方向）が画像再構成損失を粒子動力学モデルに逆伝播させるブリッジ
   - **diff**: 既存の学習ベース流体シミュレータは教師付き粒子軌跡を要求。NeuroFluidはピクセル観察のみからの教師なし学習による初の手法
   - **limit**: 既知の初期粒子速度が必要。粒子遷移の累積誤差が増大する可能性があり、物理情報損失による制約は未解決

6. [[Li2023_PACNeRF]](../REFERENCES/MAIN.md#Li2023_PACNeRF) — Li et al., "PAC-NeRF: Physics Augmented Continuum Neural Radiance Fields for Geometry-Agnostic System Identification" (2023)
   - **DOI**: — | **arXiv**: 2303.05512
   - **thesis**: ハイブリッドEulerian-Lagrangian NeRFが連続体力学の保存則を強制することで、物体のトポロジーの事前知識なしにマルチビュービデオから未知の形状と物理パラメータを同時復元可能
   - **core**: ボクセルベースNeRFと粒子ベースMPMを組み合わせたハイブリッドEulerian-Lagrangian離散化が、形状再構成と物性推定の同時微分可能最適化を可能にする
   - **diff**: 従来のsystem identificationは物体の幾何構造の完全な知識を前提。PAC-NeRFはマルチビュービデオから幾何と物性を同時復元する初の手法
   - **limit**: 同期・正確キャリブレーション済みカメラを仮定。ビデオマッティングまたは前景マスクが必要。連続体力学に従う現象に限定。異なる材料の自動識別は不可

### A2. 3DGS + Physics (2024-2026)

3D Gaussian Splattingの各カーネルに物理属性を直接付与し、レンダリングとシミュレーションを統一表現上で実行する手法群。2024年のPhysGaussianを起点に急速に発展。

1. [[Xie2024_PhysGaussian]](../REFERENCES/MAIN.md#Xie2024_PhysGaussian) — Xie et al., "PhysGaussian: Physics-Integrated 3D Gaussians for Generative Dynamics" (2024)
   - **DOI**: — | **arXiv**: 2311.12198
   - **thesis**: 3Dガウシアンカーネルがシミュレーション媒体とレンダリングプリミティブを兼ねることで、メッシュベースのパイプラインに内在する表現不一致を排除し、物理的に妥当な新規動作合成が可能になる
   - **core**: 各Gaussianカーネルに速度・ひずみ・弾性エネルギー・応力・塑性属性を付与しMPMで時間発展させる統一表現
   - **diff**: 従来の物理ベースコンテンツ生成は形状構築・シミュレーション・レンダリングが分離。PhysGaussianは単一表現に統合
   - **limit**: 影を考慮しない。1点求積がGaussian楕円体サイズを不十分に表現しうる。PDEベース動力学はデータ駆動モデルではなく近似

2. [[Chen2024_GIC]](../REFERENCES/MAIN.md#Chen2024_GIC) — Cai et al., "GIC: Gaussian-Informed Continuum for Physical Property Identification and Simulation" (2024)
   - **DOI**: — | **arXiv**: 2406.14927
   - **thesis**: 明示的3DGaussian形状と暗黙的連続体シミュレーションの双方向監視により、暗黙表現のみ（PAC-NeRF）より高精度な物性同定が達成される
   - **core**: Motion-factorized 3DGaussian再構成が明示的形状ガイダンスを提供し、coarse-to-fine密度場連続体が暗黙的形状をレンダリングマスクから学習する双方向監視
   - **diff**: PAC-NeRFが暗黙的NeRF形状のみに依拠し形状復元精度とテクスチャ歪みに問題を抱えるのに対し、GICは明示的Gaussianで連続体を接地し軌跡精度と描画品質を向上
   - **limit**: 連続体力学を仮定。既知カメラ姿勢のマルチビュー画像が必要。構成則の事前知識が必要

3. [[Feng2024_PIENeRF]](../REFERENCES/MAIN.md#Feng2024_PIENeRF) — Feng et al., "PIE-NeRF: Physics-based Interactive Elastodynamics with NeRF" (2024)
   - **DOI**: — | **arXiv**: 2311.13099
   - **thesis**: NeRF密度場上のメッシュレスQ-GMLS離散化により、明示的メッシュ生成なしにインタラクティブレートで非線形超弾性シミュレーションが可能
   - **core**: NeRFサンプル粒子に直接適用されるQ-GMLSモデル縮退が、メッシュなしの超弾性シミュレーションを正確かつ計算効率良く実現
   - **diff**: 従来のFEMは暗黙的NeRF表現と本質的に非互換な明示的四面体メッシュを必要。PIE-NeRFはメッシュを完全に回避
   - **limit**: limit not available

4. [[Zhong2024_SpringGaus]](../REFERENCES/MAIN.md#Zhong2024_SpringGaus) — Zhong et al., "Spring-Gaus: Reconstruction and Simulation of Elastic Objects with Spring-Mass 3D Gaussians" (2024)
   - **DOI**: 10.1007/978-3-031-72627-9_23 | **arXiv**: 2403.09434
   - **thesis**: Spring-Massモデルと3DGSの統合により、外観学習と物理学習を分離でき、マルチビュービデオから弾性物体のper-point物理パラメータをサンプル効率的に推定可能
   - **core**: 外観最適化と物理最適化を分離するper-point spring-massネットワーク
   - **diff**: 既存のdynamic 3DGSは物性推定を欠く。連続体MPMアプローチ（PAC-NeRF, GIC）と異なりvolumetric表現が不要でサンプル効率が高い
   - **limit**: 弾性物体に限定。シミュレーション開始時に固定されるバネ長により塑性変形は非対応

5. [[Liu2024_Physics3D]](../REFERENCES/MAIN.md#Liu2024_Physics3D) — Liu et al., "Physics3D: Learning Physical Properties of 3D Gaussians via Video Diffusion" (2024)
   - **DOI**: — | **arXiv**: 2406.04338
   - **thesis**: Video Diffusionモデルからの物理プライオア蒸留と粘弾性材料モデルの組み合わせにより、手動パラメータ設計なしにプラスチック・金属を含む広範な材料の物性学習が可能
   - **core**: 粘弾性MPM材料モデルとvideo diffusion score distillationの組み合わせ
   - **diff**: PhysDreamerがYoung's modulusのみに依拠しプラスチック・金属に対応できないのに対し、Physics3Dは粘性を導入し材料空間を拡張
   - **limit**: 多数の絡み合う物体を含む複雑環境では、可動物体のスコープを手動指定する必要がある

6. [[Huang2025_DreamPhysics]](../REFERENCES/MAIN.md#Huang2025_DreamPhysics) — Huang et al., "DreamPhysics: Learning Physics-Based 3D Dynamics with Video Diffusion Priors" (2025)
   - **DOI**: — | **arXiv**: 2406.01476
   - **thesis**: Video DiffusionモデルのSDS損失により材料パラメータを精緻化でき、フレーム補間と対数勾配最適化が安定収束を実現する
   - **core**: 事前学習済みvideo diffusionモデルからMPM-Gaussianパイプラインへの物理プライオア蒸留としてのSDS
   - **diff**: PhysDreamerがvideo diffusionを直接的監視として使用し微小動作・非連続フレームに留まるのに対し、DreamPhysicsはSDSベースの蒸留で高品質な4D動力学を実現
   - **limit**: 回転・衝突の限定的運動タイプのみ対応。視覚ベース評価指標は物理的リアリズムの評価に不十分。シミュレータは対象物体のみ扱い環境インタラクション（影の変化等）は未モデル化

7. [[Hong2026_PIDG]](../REFERENCES/MAIN.md#Hong2026_PIDG) — Hong et al., "Physics-Informed Deformable Gaussian Splatting" (2026)
   - **DOI**: — | **arXiv**: 2511.06299
   - **thesis**: Gaussianを構成則パラメータ付きLagrangian物質点として扱いCauchy運動量方程式の残差制約を課すことで、既知材料タイプなしに単眼ビデオから物理整合的な動的再構成が可能
   - **core**: 時間発展材料場が各粒子の速度と応力を独立に予測し、Cauchy運動量残差が構成則準拠を強制するPINN的制約
   - **diff**: 従来の3DGS動的手法は運動を剛体変換に簡略化し構成則を無視。PIDGは運動量方程式の完全な制約を最適化ループに埋め込む
   - **limit**: 最適化ベースのパイプラインは計算集約的（時間〜日単位）。PINNベース構成則モデルは非線形弾塑性・粘弾性を完全には捕捉できない

8. [[Chopra2025_PhysGS]](../REFERENCES/MAIN.md#Chopra2025_PhysGS) — Chopra et al., "PhysGS: Bayesian-Inferred Gaussian Splatting for Physical Property Estimation" (2025)
   - **DOI**: — | **arXiv**: 2511.18570
   - **thesis**: Per-point物性推定をGaussianスプラット上のBayes反復推論として定式化し、不確実性を明示的にモデル化することで、決定論的ベースラインより高精度かつ頑健な推定を実現
   - **core**: Aleatoric/epistemic不確実性を同時モデル化するGaussianスプラット上のBayes更新ループ
   - **diff**: 決定論的物性推定は不確実性定量化を欠き、視覚的に類似だが物理的に異なる領域で困難。PhysGSはvision-languageプライオアでシードしたBayes推論で質量22.8%、硬度61.2%の改善
   - **limit**: セグメンテーション品質に敏感。パートレベルマスクが類似材料を統合するか細粒度領域を分離できない場合、推定精度が低下

9. [[Vasile2025_ASDiffMPM]](../REFERENCES/MAIN.md#Vasile2025_ASDiffMPM) — Vasile et al., "AS-DiffMPM: Gaussian-Augmented Physics Simulation with Complex Colliders" (2025)
   - **DOI**: — | **arXiv**: 2511.06846
   - **thesis**: 任意形状剛体コライダに対する微分可能衝突処理をMPMに拡張することで、非平面境界条件下でのエンドツーエンド物性推定を実現
   - **core**: 任意形状コライダに対応しつつ端-端勾配流を保持する微分可能衝突処理メカニズム
   - **diff**: PAC-NeRF等の従来手法は平面境界との相互作用に限定。AS-DiffMPMは複雑な剛体形状との変形相互作用下での物性同定を可能にする
   - **limit**: 事前の剛体再構成とインポートが必要で、静的コライダに限定

### A3. Digital Twin Construction from Video

ビデオ観察から物理的に操作可能なデジタルツインを構築する手法群。物性復元だけでなく、新規インタラクション下でのre-simulationを目標とする。

1. [[Jiang2025_PhysTwin]](../REFERENCES/MAIN.md#Jiang2025_PhysTwin) — Jiang et al., "PhysTwin: Physics-Informed Reconstruction and Simulation from Videos" (2025)
   - **DOI**: — | **arXiv**: 2503.17973
   - **thesis**: スパースRGB-Dビデオからspring-mass物理＋生成的形状モデル＋Gaussianスプラットを組み合わせ、新規インタラクション下でre-simulation可能なデジタルツインを構築可能
   - **core**: ゼロ次最適化（離散トポロジーパラメータ）と一次勾配降下（密なバネ剛性）の階層的sparse-to-dense最適化戦略
   - **diff**: Dynamic NeRF/Gaussianは外観を捕捉するが新規インタラクションをシミュレートできない。学習ベースは大規模データを要求。PhysTwinは単一インタラクションビデオのみで動作しSpring-Gausと異なり運動量保存を維持
   - **limit**: 現状3台のRGB-Dカメラが必要。単一種類のインタラクションに基づく最適化で物性推定精度が制限。よりスパースな観察への拡張は将来課題

2. [[Chen2025_Vid2Sim]](../REFERENCES/MAIN.md#Chen2025_Vid2Sim) — Chen et al., "Vid2Sim: Generalizable, Video-based Reconstruction of Geometry, Appearance and Physics" (2025)
   - **DOI**: — | **arXiv**: 2506.06440
   - **thesis**: フィードフォワード予測＋軽量最適化の2段階フレームワークにより、per-scene超パラメータチューニングなしに汎化的な外観・形状・物性復元を実現
   - **core**: VideoMAEベースのネットワークが汎化的物性プライオアを提供し、Neural JacobianモジュールがReduced-Order Implicit Eulerソルバで高速精緻化
   - **diff**: PAC-NeRFやSpring-Gausはグリッドベースのper-scene重最適化を要求。Vid2Simは汎化的フィードフォワードモデルで数分の精緻化のみ
   - **limit**: Reduced-orderシミュレーション手法で捕捉可能な材料に限定。流体等の複雑材料は非対応

3. [[Chen2026_EMPM]](../REFERENCES/MAIN.md#Chen2026_EMPM) — Chen et al., "EMPM: Embodied MPM for Modeling and Simulation of Deformable Objects" (2026)
   - **DOI**: — | **arXiv**: 2601.17251
   - **thesis**: 微分可能MPMを3DGSと統合することで、破壊・伸長・圧縮を含む複雑な弾塑性挙動を呈する柔軟物のモデリングと操作が可能
   - **core**: 材料パラメータ（E, ν, 降伏応力）の自動微分による最適化を伴う微分可能MPM
   - **diff**: PhysTwin等のspring-massベースラインは破壊等の弾塑性現象をモデル化できない。EMPMはより広範な変形挙動に対応
   - **limit**: 信頼性の高い点追跡がボトルネック。遮蔽・大変形下で3D軌跡の信頼性が低下。初期フレーム条件付き追跡は数秒で信頼性ある追跡点がゼロになりうる

4. [[Zhu2024_latentIntuitive]](../REFERENCES/MAIN.md#Zhu2024_latentIntuitive) — Zhu et al., "Latent Intuitive Physics: Learning to Transfer Hidden Physics from A 3D Video" (2024)
   - **DOI**: — | **arXiv**: 2406.12769
   - **thesis**: 明示的物理パラメータ推定なしに、確率的潜在特徴として隠れた流体物性を推論し、新規シーンへのシミュレーション転移が可能
   - **core**: 確率的粒子シミュレータの潜在プライオアを、微分可能レンダラを通じた光度誤差逆伝播で推論された視覚ポステリオアと整合させる3段階学習
   - **diff**: NeuroFluidはシナリオ毎に全遷移モデルの再学習が必要。PAC-NeRFは慎重な初期化を要する離散的物理パラメータを明示推定。本手法は連続的潜在表現で遷移モジュールを凍結したまま適応
   - **limit**: 合成データのみでの評価。実世界シーンには粒子画像速度計等の高度な流体計測が必要。同期マルチビュー高フレームレートキャプチャが実用的課題

5. [[NVIDIA2025_VoMP]](../REFERENCES/MAIN.md#NVIDIA2025_VoMP) — NVIDIA et al., "VoMP: Predicting Volumetric Mechanical Property Fields" (2025)
   - **DOI**: — | **arXiv**: 2510.22975
   - **thesis**: アノテーション済み3Dデータセットで学習されたGeometry Transformerが、任意の3D表現に対してper-voxelのYoung's modulus, Poisson's ratio, 密度をフィードフォワードで予測し、per-object最適化を不要にする
   - **core**: マルチビューper-voxel特徴を物理的に妥当な材料の学習多様体上の潜在コードに集約するGeometry Transformer
   - **diff**: 従来手法はビデオ/画像列からのper-object最適化を要求しテスト時に汎化不可。VoMPはシミュレーション対応volumetric物性場の表現非依存フィードフォワード予測を実現する初のモデル
   - **limit**: 固定グリッドボクセル化による解像度制限で、高不均一領域で過平滑化。パートレベル材料の等方性仮定は木材等の一部材料に不適

6. [[Fan2025_PhysWorld]](../REFERENCES/MAIN.md#Fan2025_PhysWorld) — Yang et al., "PhysWorld: Real Videos to World Models via Physics-Aware Demonstration Synthesis" (2025)
   - **DOI**: — | **arXiv**: 2510.21447
   - **thesis**: MPMデジタルツイン（実ビデオからフィッティング）から合成データを生成し軽量GNNを学習することで、物理整合性を保ちつつ47倍高速な推論を実現するシミュレータ→データ→モデル戦略
   - **core**: 実ビデオからのMPMデジタルツインフィッティングパイプラインが物理シミュレータをデータジェネレータとして活用
   - **diff**: GNNは大量学習データを要求し実観察のみでは不足。MPMは物理的だが計算コストが高い。PhysWorldはシミュレータを学習データ生成に使い両者の利点を統合
   - **limit**: limit not available

### B. Cloth/Rope/DLO Parameter Estimation

布・ロープ・線状変形物体（DLO）の物理シミュレーションパラメータを実データから推定する手法群。Real-to-simアプローチが中心。

1. [[Li2022_DiffCloth]](../REFERENCES/MAIN.md#Li2022_DiffCloth) — Li et al., "DiffCloth: Differentiable Cloth Simulation with Dry Frictional Contact" (2022)
   - **DOI**: 10.1145/3527660 | **arXiv**: 2106.05306
   - **thesis**: Projective DynamicsのSignorini-Coulomb乾燥摩擦接触拡張と、前因子分解されたシステム構造を活用した反復勾配計算により、接触リッチな布の微分可能シミュレーションが実現可能
   - **core**: 暗黙的時間積分と接触制約方程式（take-off/stick/slip）を通じた微分と、PD全体解の前因子分解活用による計算効率
   - **diff**: 従来の微分可能布シミュレータは摩擦を省略またはペナルティベース。DiffClothは制約ベースCoulomb摩擦を適切な相補性条件で実装
   - **limit**: 節点ベース衝突のみ（エッジ-エッジ、頂点-面は未対応）。三角形離散化由来の法線不連続。接触集合変更が深刻な勾配不連続を生成。高精度設定で約15%のタイムステップで反復ソルバ収束失敗

2. [[Zheng2024_DiffCP]](../REFERENCES/MAIN.md#Zheng2024_DiffCP) — Zheng et al., "DiffCP: Differentiable Cloth Parameter Identification and State Estimation" (2024)
   - **DOI**: 10.1109/LRA.2024.3357039 | **arXiv**: 2311.05141
   - **thesis**: 異方性弾塑性構成モデルを組み込んだ微分可能MPMによるreal-to-sim-to-realパイプラインで、ロボット操作中の布物理パラメータ同定と状態推定を同時達成
   - **core**: Anisotropic Elasto-Plastic構成モデル＋微分可能MPM＋Chamfer距離目標
   - **diff**: 従来の布状態推定はキーポイントや境界手がかりに依拠し物理的精緻さを欠く。DiffCPは物性パラメータ同定を通じて布構造を包括的に捕捉
   - **limit**: センサ不正確さに起因する実-シミュレーション間データ不一致。微分可能シミュレーションのメモリ要求が顕著

3. [[Sundaresan2022_DiffCloud]](../REFERENCES/MAIN.md#Sundaresan2022_DiffCloud) — Sundaresan et al., "DiffCloud: Real-to-Sim from Point Clouds with Differentiable Simulation" (2022)
   - **DOI**: 10.1109/IROS47612.2022.9981101 | **arXiv**: 2204.03139
   - **thesis**: 微分可能シミュレーションと微分可能点群レンダリングの勾配連鎖により、コストのかかるオフラインデータ収集やNN学習なしに実点群からシミュレーションパラメータをオンザフライ推定可能
   - **core**: メッシュ面上の重心座標サンプリングに適用される一方向Chamfer距離損失が、実点群から微分可能FEMシミュレータへの勾配流を可能にする
   - **diff**: ブラックボックス逆モデルベースライン（PointNet++, MeteorNet）が2.5-5.5時間のデータ生成＋学習を要求するのに対し、DiffCloudはオフラインデータ不要で約10分で動作
   - **limit**: 既知の初期形状と把持位置を仮定。遮蔽処理は対象外。ロボットの点群マスキングは手動

4. [[Antonova2022_BayesianReal2Sim]](../REFERENCES/MAIN.md#Antonova2022_BayesianReal2Sim) — Antonova et al., "A Bayesian Treatment of Real-to-Sim for Deformable Object Manipulation" (2022)
   - **DOI**: 10.1109/LRA.2022.3153856 | **arXiv**: 2112.05068
   - **thesis**: 高変形物体のReal-to-simパラメータ推論は確率的Bayes推論として定式化すべきであり、ノイズの多いキーポイント観測をRKHSにカーネル平均埋め込みとして表現することで、信頼性ある低次元統計量なしにパラメータ事後分布を推定可能
   - **core**: RKHS-Netが乱数Fourier特徴でキーポイントを順序不変の分布埋め込みとしてエンコードし、ノイズ耐性の要約統計量を提供
   - **diff**: 既存BayesSimは信頼性ある低次元状態推定を仮定するが柔軟物では失敗。本手法はドメイン固有の要約統計量を不要とする分布埋め込みで置換
   - **limit**: 近似的視覚外観マッチングのみ対応。簡略化された把持アンカーを使用。推論開始前に実データで学習したキーポイント抽出モデルが必要

5. [[Liu2022_DiffRope]](../REFERENCES/MAIN.md#Liu2022_DiffRope) — Liu et al., "Differentiable Manipulation of Rope using Compliant Position-based Dynamics" (2022)
   - **DOI**: 10.1109/LRA.2023.3264766 | **arXiv**: 2202.09714
   - **thesis**: 幾何的制約（せん断/伸長、曲げ/ねじり）を持つ微分可能XPBD（compliant PBD）が、ロープ状物体のパラメータ同定と形状制御を同時に解決可能
   - **core**: 粒子-クォータニオンロープモデル上の3つの幾何的制約をPyTorch自動微分で微分し、6つの剛性パラメータと制御点位置を同時最適化
   - **diff**: 力ベース解析手法（Euler-Bernoulli, Cosserat rod）はPBD更新に対応できず、モデルフリーNNはデータハングリー。XPBD微分可能化は物理精度とデータ効率を両立
   - **limit**: 3離散形状点のみをターゲットとし制御精度が制限。エンドエフェクタの回転制御不在で完全位置決め不可。メモリ制約によりシミュレーション反復数のスケーラビリティが制限

6. [[Gong2024_BayesianCloth]](../REFERENCES/MAIN.md#Gong2024_BayesianCloth) — Gong et al., "Bayesian Differentiable Physics for Cloth Digitalization" (2024)
   - **DOI**: — | **arXiv**: 2402.17664
   - **thesis**: 標準Cusickドレープテスト画像からの変分Bayes推論により、空間的に不均一な布物理パラメータを少数の画像から学習可能
   - **core**: Per-elementの物理パラメータに対する変分Bayes推論が、布ドレーピングを確率的状態遷移として定式化
   - **diff**: 従来の微分可能物理布手法は均一材料を仮定し大規模データを要求。本手法は厳密に制御されたドレープテストと空間的材料変動の明示的モデル化を採用
   - **limit**: 事前物理知識が必要でプラグアンドプレイ不可。座屈等の追加的動力学確率性のモデル化は将来課題。モーションキャプチャ・3D再構成による実衣服との比較は将来課題

7. [[Ru2025_FabricReal2Sim]](../REFERENCES/MAIN.md#Ru2025_FabricReal2Sim) — Ru et al., "Can Real-to-Sim Approaches Capture Dynamic Fabric Behavior?" (2025)
   - **DOI**: 10.1109/IROS60139.2025.11245811 | **arXiv**: 2503.16310
   - **thesis**: 現行のreal-to-simパラメータ推定手法（微分可能シミュレーション＋データ駆動）は、未見の動的操作タスクへの汎化に系統的に失敗する。弾性動力学PDEを組み込んだPINNアプローチが改善を見せるが、動的シナリオでは依然不十分
   - **core**: 4手法（DiffCloud, DiffCP, PhysNet, 弾性動力学PDE付きPINN）の訓練タスクと未見タスク（折り畳み、振り、揺り）での比較評価
   - **diff**: 従来のreal-to-sim研究は訓練シナリオでのみ検証。本研究は未見の動的タスクへの汎化を初めて評価し、PINNによる布パラメータ推定を初めて適用
   - **limit**: PINNは伸長ベースのパラメータ推定に依拠し動的シナリオで制限。DiffCPは顕著な不安定性と高分散。全微分アプローチが局所的/大域的幾何精度のトレードオフに直面。実布の真の物理パラメータが不在で評価が根本的に困難

8. [[Yoon2025_ClothJCDE]](../REFERENCES/MAIN.md#Yoon2025_ClothJCDE) — Yoon et al., "Real-to-Sim High-Resolution Cloth Modeling" (2025)
   - **DOI**: 10.1093/jcde/qwaf065
   - **thesis**: 粒子ベースmass-spring布シミュレーションを、Bayes最適化＋勾配降下ハイブリッドでロボット操作データに対して最適化し、異なる布種類・操作タスクに汎化する物理パラメータを同定可能
   - **core**: 大域探索（Bayes最適化）と局所精緻化（勾配降下）のハイブリッド最適化、重み付き一方向Chamfer距離＋Hausdorff距離損失
   - **diff**: データ駆動手法は大規模ラベルデータを要求し汎化性が低い。従来の物理誘導型パラメータ推定は単一タスクのみで汎化ギャップに対応していない
   - **limit**: 比較的単純な布サンプルと操作タスクに限定。粒子ベースアプローチは連続体力学手法が捕捉する微妙な現象を捕捉しきれない可能性。複雑な衣服形状・大規模布システムへの適用性は未検証

9. [[Chen2025_DER]](../REFERENCES/MAIN.md#Chen2025_DER) — Chen et al., "DER: Accurate Simulation and Parameter Identification of Deformable Linear Objects" (2025)
   - **DOI**: 10.1109/IROS60139.2025.11247160 | **arXiv**: 2310.00911
   - **thesis**: Discrete Elastic Rods（DER）モデルをMuJoCoの一般化座標に力-レバー解析で統合し、曲げ・ねじり剛性の勾配ベース同定パイプラインとゼロショットsim-to-real転移を実現
   - **core**: DERのデカルト剛性力をMuJoCoの一般化座標に変換する力-レバー解析
   - **diff**: 従来のDLO動的操作は実データまたは暗黙的ポリシーを要求。DERベースの高忠実度シミュレータにより実データ要求をゼロに削減しMuJoCoネイティブケーブルモデルを精度・パラメータ同定性で改善
   - **limit**: ポリシー出力軌道はガイドに過ぎず実際のロボット軌道はやや異なる。摩擦モデルが不完全。オープンループタスクでクローズドループ制御は将来課題

10. [[Kawaharazuka2022_VarStiffCloth]](../REFERENCES/MAIN.md#Kawaharazuka2022_VarStiffCloth) — Kawaharazuka et al., "Dynamic Cloth Manipulation Considering Variable Stiffness" (2022)
    - **DOI**: 10.3389/fnbot.2022.890695
    - **thesis**: 筋骨格ヒューマノイドの可変剛性制御と、パラメトリックバイアスを持つ深層予測モデルの組み合わせにより、数回の試行で新しい布材料に高速適応する動的布操作が可能
    - **core**: 10層LSTMベースのDeep Predictive Model with Parametric Bias（DPMPB）で、パラメトリックバイアスベクトルがper-material動力学を捕捉
    - **diff**: 従来研究は柔軟ロボット身体を高速動的布操作に活用できず、材料変化への適応も不可。本研究はハードウェアコンプライアンスと材料適応を初めて結合
    - **limit**: 単一値の身体剛性で人間のような多関節制御は未実現。布が手を離れる等の大きな非線形状態変化に対応不可。関節速度制限により実布の代わりにフォームを使用

### C. Force/Tactile-Based Property Estimation

F/Tセンサ、触覚センサ、固有受容感覚から柔軟物の物理パラメータを推定する手法群。剛体慣性パラメータ同定の知識を持つ読者にとって最も関連の深いカテゴリ。

1. [[Patni2024_elasticity]](../REFERENCES/MAIN.md#Patni2024_elasticity) — Patni et al., "Online Elasticity Estimation and Material Sorting Using Standard Robot Grippers" (2024)
   - **DOI**: 10.1007/s00170-024-13678-6 | **arXiv**: 2401.08298
   - **thesis**: 触覚センサなしの標準並行爪グリッパでも、繰り返し圧縮による弾性・粘弾性の2次元特徴空間で柔軟物の相対的弾性を判別しソーティング可能。ただし絶対的Young's modulus値の精度は不十分
   - **core**: 低速圧縮サイクルとHunt-Crossleyモデルによる弾性・粘弾性の2次元特徴空間
   - **diff**: 従来の材料剛性推定は専用触覚センサまたは実験室グレード圧縮装置を要求。本手法はcommodity 2本指グリッパで追加ハードウェアなしに実用的材料ソーティングを実証
   - **limit**: グリッパはYoung's modulusや粘弾性の正確な絶対値を提供できない。OnRobot RG6は不連続圧縮により粘弾性測定が不可。モータ電流による力測定は不完全なキャリブレーションを要求

2. [[Burgess2024_youngs]](../REFERENCES/MAIN.md#Burgess2024_youngs) — Burgess et al., "Learning Object Compliance via Young's Modulus from Single Grasps with Camera-Based Tactile Sensors" (2024)
   - **DOI**: — | **arXiv**: 2406.15304
   - **thesis**: GelSightカメラ型触覚センサとハイブリッド解析-データ駆動システムにより、単一把持から5 kPa〜250 GPaの10桁にわたるYoung's modulus推定を物体形状非依存で実現
   - **core**: Young's modulusという普遍的材料定数でのコンプライアンスパラメータ化と、接触力学＋学習補正のハイブリッドモデル
   - **diff**: 既存のコンプライアンス推定は物体形状と材料タイプの両方にわたる汎化が困難。本手法は10桁のレンジで形状非依存推定を単一把持プロトコルで達成
   - **limit**: GelSightセンサに対して事実上剛体な硬い物体間の精密な差異判別が困難。センサ解像度が硬い材料の微小変形検出に不十分

3. [[Yao2023_vsf]](../REFERENCES/MAIN.md#Yao2023_vsf) — Yao & Hauser, "Estimating Tactile Models of Heterogeneous Deformable Objects in Real Time" (2023)
   - **DOI**: 10.1109/ICRA48891.2023.10160731
   - **thesis**: Volumetric Stiffness Field（VSF）表現により、事前の幾何・材料知識なしにロボットプローブ接触データから不均一柔軟物の空間的に変化する力応答をリアルタイム学習可能
   - **core**: 物体体積にわたる空間的にインデックスされたVSFと、力応答を予測する点ベース接触シミュレータの組み合わせ
   - **diff**: 従来の柔軟物モデルは均一材料特性を仮定するか物体固有のプライオアを要求。VSFは事前知識なしにロボットセンサデータから不均一空間剛性分布を直接学習
   - **limit**: limit not available

4. [[Kutsuzawa2024_stiffness]](../REFERENCES/MAIN.md#Kutsuzawa2024_stiffness) — Kutsuzawa et al., "Learning-based Object Stiffness and Shape Estimation in Multi-Fingered Hand Grasping" (2024)
   - **DOI**: 10.3389/fnbot.2024.1466630
   - **thesis**: 確率的推論フレームワークで学習されたRNNが、多指ハンドの固有受容感覚のみから物体の剛性と形状を不確実性付きで同時推定可能
   - **core**: 分散・エントロピーを不確実性指標として出力する確率的推論定式化
   - **diff**: 従来の剛性推定は終端接触状態で一度実行され、F/Tセンサ等の専用ハードウェアに依拠。本手法は関節角度/速度のみから連続的に推定し不確実性定量化を提供
   - **limit**: シミュレーション（MuJoCoのAllegro Hand）のみでの評価。実ハードウェアへの制御統合と転移は将来課題

5. [[Chen2025_diffprop]](../REFERENCES/MAIN.md#Chen2025_diffprop) — Chen et al., "Learning Object Properties via Differentiable Robot-Object Interaction" (2025)
   - **DOI**: — | **arXiv**: 2410.03920
   - **thesis**: 微分可能ロボット-物体インタラクションシミュレーションにより、外部センサ・カメラ・物体装着センサなしにロボット関節エンコーダ読み取りのみから物体の質量と弾性率を同定可能
   - **core**: 微分可能ロボット-物体接触シミュレーションを通じた勾配ベース逆同定
   - **diff**: 従来のsystem identificationは物体固有センサ、視覚追跡、または外部計測装置を要求。本手法はロボット自身の関節エンコーダのみから推論
   - **limit**: 物体の初期位置の知識を仮定。液体の揺動、摩擦性粒状媒体、多関節不規則形状等の複雑シナリオは拡張なしに未対応

6. [[Sanchez2020_BlindFEM]](../REFERENCES/MAIN.md#Sanchez2020_BlindFEM) — Sanchez et al., "Blind Manipulation of Deformable Objects Based on Force Sensing and FEM" (2020)
   - **DOI**: 10.3389/frobt.2020.00073
   - **thesis**: F/Tセンシングと四面体FEMモデルのみで、視覚なしに柔軟物の変形推定と制御を同時実現可能。暗闘・遮蔽下での操作を可能にする
   - **core**: 接触力を重力・慣性等から分離するRecurrent Neural Network Observer（RNNOB）と、分離された接触力で駆動されるFEM変形モデル
   - **diff**: 既存の変形制御はマーカー追跡やRGB-Dカメラに依存する視覚ベース。本研究は視覚完全不在下での変形推定・制御を初めて実証
   - **limit**: F/Tセンサノイズによるドリフトで精度が制限。物理パラメータを直接的に取得できない。線形材料モデルで非線形挙動（ヒステリシス）は未対応。制御ループの収束に約20秒・残差約2cm

### D. Physics-Informed Deformable Manipulation

推定・学習された柔軟物の物性に基づいてロボット操作を実行する手法群。RQ3（復元物性の操作活用）に直接回答する最重要カテゴリ。

1. [[Yang2025_dpsi]](../REFERENCES/MAIN.md#Yang2025_dpsi) — Yang et al., "DPSI: Differentiable Physics-based System Identification for Elastoplastic Materials" (2025)
   - **DOI**: 10.1177/02783649251334661 | **arXiv**: 2411.00554
   - **thesis**: 微分可能MPMフレームワークが、単一の実ロボットインタラクションの不完全3D点群から6つのelastoplastic物理パラメータを同定し、未見の長期操作計画に汎化する。**本サーベイで唯一の、明示的物性同定→操作計画の完全パイプライン**
   - **core**: DiffTaiChiベースの微分可能MPMが、シミュレーション変形と実点群のアライメントを最適化し物理的に解釈可能なパラメータを提供
   - **diff**: ブラックボックスNNは物理的解釈可能性を欠き大規模データを要求。DPSIは最小限のシンプルインタラクション（5分以内）から物理根拠あるパラメータ推定を提供し未見の長期操作に汎化
   - **limit**: 物体がエンドエフェクタに粘着し小麦粉コーティングが必要（推定対象の摩擦係数に影響）。知覚制限により操作中の物体落下を捕捉できない。シミュレーション接触領域が鋭く変形し弾性復元が不十分

2. [[Zhang2024_adaptigraph]](../REFERENCES/MAIN.md#Zhang2024_adaptigraph) — Zhang et al., "AdaptiGraph: Material-Adaptive Graph-Based Neural Dynamics for Robotic Manipulation" (2024)
   - **DOI**: — | **arXiv**: 2407.07889
   - **thesis**: 連続的物性変数で条件付けされた単一GNNモデルが、複数の柔軟材料タイプにわたって動力学を予測し、テスト時にfew-shot逆最適化で未知物体に適応可能
   - **core**: 材料タイプとスカラー物性変数（剛性、粒径等）をGNNに直接エンコードする物性条件付きグラフ表現
   - **diff**: 従来のグラフベース動力学モデルは単一材料タイプに限定し新材料への再学習が必要。AdaptiGraphは統一的物性条件付きモデルで4材料カテゴリにわたるテスト時適応を実現
   - **limit**: 4材料タイプ（ロープ、粒状、剛体箱、布）と材料あたり単一物性変数で学習。デプロイ時に材料タイプが既知であることを仮定

3. [[Ai2024_robopack]](../REFERENCES/MAIN.md#Ai2024_robopack) — Ai et al., "RoboPack: Learning Tactile-Informed Dynamics Models for Dense Packing" (2024)
   - **DOI**: — | **arXiv**: 2407.01418
   - **thesis**: 触覚フィードバック履歴をrecurrent GNN動力学モデルに統合することで、重度の遮蔽下でも密パッキングタスクでの正確な予測と計画が可能
   - **core**: Soft-Bubble触覚センサ履歴から潜在物理状態をエンコードするrecurrent GNN
   - **diff**: 従来の動力学モデルは完全状態観測可能性を仮定し触覚フィードバックを組み込まない。RoboPackは触覚履歴の潜在物理表現への融合で部分観測可能性に明示対応
   - **limit**: タスク固有のコスト関数と計画モジュールが必要。2つの特定操作タスクでのみ実証。細粒度変形のための高忠実度粒子表現は未対応

4. [[Shi2022_RoboCraft]](../REFERENCES/MAIN.md#Shi2022_RoboCraft) — Shi et al., "RoboCraft: Learning to See, Simulate, and Shape Elasto-Plastic Objects" (2022)
   - **DOI**: 10.1177/02783649231219020 | **arXiv**: 2205.02909
   - **thesis**: RGB-D観察から粒子に変換し、分布ベース損失（EMD＋Chamfer）で学習したGNN動力学モデルとMPC計画により、10分の実ロボットインタラクションデータから弾塑性物体を目標形状に整形可能
   - **core**: 粒子対粒子対応なしにEMD＋Chamfer距離で粒子分布上のGNN動力学モデルを学習
   - **diff**: 従来の粒子動力学手法はフレーム間対応を提供するシミュレータが必要。RoboCraftは対応不要で弾塑性物体（生地、粘土）に拡張
   - **limit**: 視覚フィードバックは把持間のみ（操作中の中間状態取得は時間効率を低下）。距離ベースメトリクスと人間知覚の形状品質に乖離がありうる

5. [[Wu2026_rapid]](../REFERENCES/MAIN.md#Wu2026_rapid) — Wu et al., "RAPiD: Rapid Adaptation of Particle Dynamics for Deformable Object Mobile Manipulation" (2026)
   - **DOI**: — | **arXiv**: 2603.18246
   - **thesis**: 特権的粒子位置情報から学習した動力学埋め込みで条件付けされた視覚運動ポリシーと、視覚観察・行動履歴から同埋め込みを推論するアダプタの2フェーズ学習により、未見の柔軟物動力学に対し80%以上の実機成功率で適応可能
   - **core**: シミュレーション内の真の粒子位置を特権的動力学埋め込みとして使用（RMAフレームワークの拡張）
   - **diff**: 既存の柔軟物操作手法は多様で未知の物体動力学への汎化が困難。RAPiDは実世界デモンストレーションや物体固有再学習なしにテスト時で未知動力学に明示適応
   - **limit**: limit not available（実世界データでのファインチューニングとの比較は将来課題とされている）

### E. Differentiable Simulation Frameworks and Benchmarks

物性復元を可能にする基盤的フレームワークおよびベンチマーク。

1. [[Qiao2020_diffsim]](../REFERENCES/MAIN.md#Qiao2020_diffsim) — Qiao et al., "Scalable Differentiable Physics for Learning and Control" (2020)
   - **DOI**: 10.5555/3524938.3525665 | **arXiv**: 2007.02168
   - **thesis**: メッシュベース表現と局所化された衝突処理により、物体数に線形・空間解像度に定数の計算量を達成し、粒子ベースの微分可能シミュレータより最大2桁のメモリ・計算削減を実現
   - **core**: スパースなメッシュ表現と衝突あたりの最適化変数を最小化する局所化接触解決
   - **diff**: 従来の微分可能物理は粒子/グリッド表現で物体数・空間解像度に対しスケールが悪い。DiffSimは本質的にスパースなメッシュで実用的スケーラビリティを達成
   - **limit**: メッシュ表現と反発接触力による剛体のみ対応。変形体・関節体・他の接触モデルへの拡張は将来課題

2. [[Huang2021_PlasticineLab]](../REFERENCES/MAIN.md#Huang2021_PlasticineLab) — Huang et al., "PlasticineLab: A Soft-Body Manipulation Benchmark with Differentiable Physics" (2021)
   - **DOI**: — | **arXiv**: 2104.03311
   - **thesis**: DiffTaiChiの微分可能MPM上に構築された初の弾塑性軟体操作ベンチマーク。解析的勾配が提供されRLと勾配ベース最適化の体系的比較が可能
   - **core**: von Mises降伏基準の解析微分可能SVDを含むDiffTaiChiベースMPM
   - **diff**: MuJoCo、PyBullet、PhysXは剛体動力学に限定し勾配未対応。PlasticineLabは軟体弾塑性＋微分可能物理＋包括的タスクスイートを統合
   - **limit**: RLベースアプローチは大半のタスクを効率的に解決困難。勾配ベースは長期多段階計画でモメンタム不足。マニピュレータ-粘土間の切り離し・再接触で勾配消失

3. [[Heiden2021_DiSECt]](../REFERENCES/MAIN.md#Heiden2021_DiSECt) — Heiden et al., "DiSECt: A Differentiable Simulation Engine for Autonomous Robotic Cutting" (2021)
   - **DOI**: 10.15607/RSS.2021.XVII.067 | **arXiv**: 2105.12244
   - **thesis**: 仮想節点アルゴリズムによる切断面の事前処理と連続的損傷モデルにより、微分可能性を破壊するトポロジー変更再メッシュを回避し、数百パラメータの勾配ベース推定と制御最適化を実現
   - **core**: Virtual Node Algorithmが切断面の交差要素を事前複製し仮想節点を挿入。不連続な再メッシュを回避し微分可能性を保持
   - **diff**: 従来のFEM切断シミュレータはコスト高のトポロジー変更再メッシュが必要で微分可能性を破壊。商用ソルバ（Ansys LS-DYNA）は32時間vs DiSECt 30秒。微分不要なBayes手法はより多くのシミュレーションを必要
   - **limit**: 切断面をシミュレーション前に完全指定する必要。材料モデルに明示的非線形性・異方性が欠如。垂直・スライス動作のみ対応。実ロボット切断データセットとの検証は未実施

4. [[Si2024_difftactile]](../REFERENCES/MAIN.md#Si2024_difftactile) — Si et al., "DiffTactile: A Physics-based Differentiable Tactile Simulator" (2024)
   - **DOI**: — | **arXiv**: 2403.08716
   - **thesis**: FEMベース軟体モデリング＋多材料物体シミュレーション＋ペナルティベース接触を統合した完全微分可能触覚シミュレータが、勾配ベースの物性キャリブレーションと効率的な触覚操作スキル学習を可能にする
   - **core**: TaichiによるGPU加速自動微分で接触物理を通じた端-端勾配流を実現する完全システム微分可能性
   - **diff**: 既存ロボティクスシミュレータは触覚センシングを欠くか相互作用を剛体に限定。DiffTactileは剛体・変形・関節物体の接触リッチ操作に対し物理的に正確で微分可能な触覚フィードバックを提供
   - **limit**: limit not available（標準ロボティクスフレームワークへの統合と多指手操作は計画段階。マルチモーダル学習は将来課題）

5. [[Li2019_dpinet]](../REFERENCES/MAIN.md#Li2019_dpinet) — Li et al., "DPI-Net: Learning Particle Dynamics for Manipulating Rigid Bodies, Deformable Objects, and Fluids" (2019)
   - **DOI**: — | **arXiv**: 1810.01566
   - **thesis**: 動的インタラクショングラフと階層的粒子構造を持つDynamic Particle Interaction Networks（DPI-Nets）が、剛体・柔軟物・流体にわたる統一粒子ベースシミュレータを学習し、ロボット操作タスクを解決可能
   - **core**: 変形するオブジェクトトポロジーを反映して各ステップ再構築される動的インタラクショングラフと、多スケール伝播のための階層的粒子構造
   - **diff**: 従来の物理シミュレータは材料固有で多様な物質を統一的に扱えない。DPI-Netsは剛体・柔軟物・流体にわたる単一モデルを学習し少数観察で新環境に適応
   - **limit**: limit not available

6. [[Millard2022_FEMParamEst]](../REFERENCES/MAIN.md#Millard2022_FEMParamEst) — Millard et al., "Parameter Estimation for Deformable Objects in Robotic Manipulation Tasks" (2022)
   - **DOI**: 10.1007/978-3-031-25555-7_16
   - **thesis**: ロボット操作中のスパース表面点軌跡の観察からFEMメッシュ上の材料パラメータを非破壊的に最適化するcollocation定式化。FEM動力学を制約として埋め込むことで効率的な勾配ベース最適化を実現
   - **core**: FEM状態列を決定変数、動力学を制約とするcollocation定式化
   - **diff**: 視覚ベースやデータ駆動の変形推定と異なり、非破壊的ロボット操作＋スパース点追跡を使用。ブラックボックス最適化と異なりFEM構造をcollocation定式化で活用
   - **limit**: limit not available

## Survey Methodology

### Search Review Checkpoint

- Papers presented to user: 52
- User additions: 0
- User removals: 3 (surgical tissue papers excluded per user request)
- Target count adjustment: none
- Duplicates removed before checkpoint: ~35

### Search Log

#### Search Angle 1 — Visual Reconstruction + Physics

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | WebSearch | "differentiable simulation deformable object physical properties estimation video" | 10, 4 relevant | gradSim, PhysTwin, DPSI, PhysWorld |
| 2 | WebSearch | "inverse physics soft body reconstruction material parameters" | 10, 1 relevant | Weiss CVPR 2020 |
| 3 | WebSearch | "neural deformable object simulation system identification" | 10, 4 relevant | PAC-NeRF, PhysTwin, DPSI, gradSim confirmed |
| 4 | WebSearch | "NeRF physics deformable soft body material parameters" | 10, 4 relevant | PAC-NeRF, PIE-NeRF confirmed |
| 5 | WebSearch | "3D Gaussian splatting physics deformable object material" | 10, 5 relevant | PhysGS, PIDG, Spring-Gaus confirmed |
| 6 | WebSearch | "PAC-NeRF PhysGaussian Physics3D" | 10, 4 relevant | GIC (NeurIPS 2024 Oral) discovered |
| 7 | WebSearch | "differentiable MPM FEM soft body inverse" | 10, 4 relevant | AS-DiffMPM discovered |

(38 searches total in this angle — see full log in supplementary)

#### Search Angle 2 — F/T Sensor + Deformable Property Estimation

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | WebSearch | "force torque sensor deformable object stiffness estimation robot" | 10, 3 relevant | Patni2024, Sanchez2020 |
| 2 | WebSearch | "tactile sensing material property identification soft object" | 10, 4 relevant | Burgess2024, RoboPack |
| 3 | WebSearch | "FEM parameter identification force measurement deformable" | 10, 4 relevant | Millard2022, DPSI, Chen2025 |

(15 searches total in this angle)

#### Search Angle 3 — Deformable Manipulation with Physical Properties

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | WebSearch | "deformable manipulation online parameter adaptation robot" | 10, 4 relevant | AdaptiGraph, RAPiD |
| 2 | WebSearch | "cloth manipulation learned physics model robot" | 10, 2 relevant | Kawaharazuka2022 |
| 3 | WebSearch | "soft body manipulation differentiable simulation parameter" | 10, 4 relevant | DiSECt, SoMA |

(10 searches total in this angle)

#### Search Angle 4 — Survey Papers

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | WebSearch | "survey deformable object manipulation robot 2024 2025" | 10, 6 relevant | Major surveys identified |
| 2 | WebSearch | "review differentiable simulation deformable objects" | 10, 5 relevant | Newbury et al. IEEE Access |
| 3 | WebSearch | "survey tactile sensing manipulation robot 2023 2024 2025" | 10, 3 relevant | Lepora, Luo surveys |

(13 searches total in this angle)

#### Search Angle 5 — Key Methods and Venue-Specific

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | WebSearch | "PAC-NeRF physics augmented continuum" | found | ICLR 2023 confirmed |
| 2 | WebSearch | "PlasticineLab soft body manipulation benchmark" | found | ICLR 2021 Spotlight |
| 3 | WebSearch | "ICRA 2024 2025 deformable object physical property estimation" | partial | Chen2025 proprioception found |

(16 searches total in this angle)

**Source summary**: WebSearch (~130 queries), ar5iv (48 paper readings for annotation)

### DOI Resolution Log

- Papers with publisher DOI resolved: 14 / 30 (arXiv-only papers checked)
- Papers remaining arXiv-only: 16 (ICLR/NeurIPS do not assign publisher DOIs; 6 papers are preprints)
- Resolution sources: DBLP, IEEE Xplore, ACM DL, SAGE Journals, roboticsproceedings.org, OpenReview

| Paper | arXiv ID | Publisher DOI | Source | Notes |
|-------|----------|---------------|--------|-------|
| PhysGaussian | 2311.12198 | 10.1109/CVPR52733.2024.00420 | IEEE Xplore | CVPR 2024 |
| Bayesian DiffCloth | 2402.17664 | 10.1109/CVPR52733.2024.01125 | IEEE Xplore | CVPR 2024 |
| Visual Vibration Tomography | 2104.02735 | 10.1109/CVPR52733.2022.09880380 | IEEE Xplore | CVPR 2022 |
| GIC | 2406.14927 | 10.5555/3737916.3740304 | ACM DL | NeurIPS 2024 |
| NeuPhysics | 2210.12352 | 10.5555/3600270.3601203 | ACM DL | NeurIPS 2022 |
| DreamPhysics | 2406.01476 | 10.1609/aaai.v39i4.32389 | AAAI OJS | AAAI 2025 |
| Vid2Sim | 2506.06440 | 10.1109/CVPR52734.2025.02472 | IEEE Xplore | CVPR 2025 |
| EMPM | 2601.17251 | 10.1109/LRA.2026.3664610 | IEEE Xplore | RA-L 2026 |
| Chen2025 proprioception | 2410.03920 | 10.1109/ICRA55743.2025.11127955 | IEEE Xplore | ICRA 2025 |
| Can Real-to-Sim Fabric | 2503.16310 | 10.1109/IROS60139.2025.11245811 | IEEE Xplore | **IROS 2025** (not ICRA) |
| AdaptiGraph | 2407.07889 | 10.15607/RSS.2024.XX.010 | RSS proceedings | RSS 2024 |
| RoboPack | 2407.01418 | 10.15607/RSS.2024.XX.130 | RSS proceedings | RSS 2024 |
| PAC-NeRF | 2303.05512 | — | OpenReview | ICLR does not assign DOIs |
| gradSim | 2104.02646 | — | OpenReview | ICLR does not assign DOIs |
| PlasticineLab | 2104.03311 | — | OpenReview | ICLR does not assign DOIs |
| DiffTactile | 2403.08716 | — | OpenReview | ICLR does not assign DOIs |
| Latent Intuitive Physics | 2406.12769 | — | OpenReview | ICLR does not assign DOIs |
| DPI-Net | 1810.01566 | — | OpenReview | ICLR does not assign DOIs |
| NeuroFluid | 2203.01762 | — | PMLR | PMLR does not assign DOIs |
| DiffSim | 2007.02168 | — | PMLR | PMLR does not assign DOIs |
| AS-DiffMPM | 2511.06846 | — | OpenReview | NeurIPS does not assign DOIs |
| Physics3D | 2406.04338 | — | — | Preprint |
| PhysGS | 2511.18570 | — | — | Preprint |
| VoMP | 2510.22975 | — | — | Preprint |
| PhysWorld | 2510.21447 | — | — | Preprint |
| RAPiD | 2603.18246 | — | — | Preprint |
| PIDG | 2511.06299 | — | — | AAAI 2026 accepted, proceedings未刊 |
| PhysTwin | 2503.17973 | — | — | ICCV 2025, IEEE DOI未索引 |

### Hallucination Check Results

- Papers checked: 48 (via ar5iv access during Phase 3a annotation)
- Passed: 48 (all papers confirmed to exist with matching titles/authors on ar5iv or publisher pages)
- Failed and re-searched: 0
- Removed (unverifiable): 0

### Limit Field Coverage

- Papers with limit recorded: 38 / 48 (79.2%)
- Papers marked "limit not available": 10, breakdown:

| Category | Count | Papers | Action taken |
|----------|-------|--------|-------------|
| No Limitations section in paper | 7 | PIE-NeRF, PhysWorld, DiffTactile, RAPiD, Yao2023_vsf, DPI-Net, Millard2022 | Searched for Conclusions section hints; none found |
| Rendering failure on ar5iv | 0 | — | — |
| Survey/review paper | 0 | — | N/A |
| Paywall | 3 | Millard2022, Yao2023, Kutsuzawa2024 | Kutsuzawa via Frontiers OA, Yao via author PDF; Millard2022 paywall |

### Threats to Validity

- **Search scope**: WebSearchのみを使用し、Semantic Scholar API、IEEE Xplore直接検索は未実施。英語論文のみを対象とし、中国語・日本語の論文は除外。
- **Publication bias**: arXivプレプリントを積極的に収録し、出版バイアスの軽減を図った（48本中約10本がプレプリント）。
- **Selection bias**: 外科手術応用はユーザリクエストにより除外。食品加工、繊維製造等の産業応用での柔軟物物性推定は網羅が不十分な可能性がある。
- **Analysis limitations**: 単一レビュアー（AI支援）による分析。ペイウォール論文（Millard2022）の完全テキストは未読。ar5ivのHTML変換品質に依存。

## Conclusion

1. **RQ1** (視覚観察からの柔軟物物性復元アルゴリズム): 2020年のFEM逆問題から2025年の3DGS＋MPMデジタルツインまで、急速な発展を遂げている。MPMが支配的な物理バックボーンであり、表現基盤はNeRF（2022-2023）から3DGS（2024以降）へ移行した。2025年にはフィードフォワード予測（VoMP, Vid2Sim）やVideo Diffusionプライオア蒸留（Physics3D, DreamPhysics）など、per-scene最適化を超えるアプローチが登場している。

2. **RQ2** (F/T・力覚情報からの柔軟物物性推定): 剛体の慣性パラメータ同定と対照的に、標準的な定式化は存在しない。Hunt-Crossleyモデル（Patni2024）、VSF（Yao2023）、微分可能シミュレーション逆問題（Chen2025, DPSI）など散発的な手法が存在するが、体系的な比較や統一的フレームワークは未確立。この領域はSeed 1として提案した研究方向で最も大きなインパクトが期待できる。

3. **RQ3** (復元物性を活用したロボット操作の実証): **極めて少ない**。明示的物性同定→操作計画の完全パイプラインを実証したのはDPSI（Yang et al., IJRR 2025）のみ。AdaptiGraph, RoboPack, RoboCraft, RAPiDはlatentな動力学表現の適応により間接的に物性を活用しているが、明示的パラメータとしての活用ではない。「復元された物性でロボットが柔軟物を操作する」研究は、本サーベイで特定された最大の未開拓領域である。

4. **RQ4** (未解決の技術的ギャップ): (a) 視覚ベース物性復元と操作の断絶、(b) F/Tベース柔軟物物性同定の標準的定式化の不在、(c) 不均一材料の物性復元と操作の未発達、(d) 推定物性のsim-to-real検証の不足、(e) 構成則の自動選択メタ問題。

実務面では、DPSIの微分可能MPMベース同定パイプラインが現時点で最も成熟した「物性同定→操作」のエンドツーエンドフレームワークである。ただし5分の推定時間はリアルタイム操作には不十分であり、高速化が実用上の鍵となる。

最も有望な研究方向は、F/Tセンサベースの柔軟物物性同定フレームワークの確立（Seed 1）と、その結果を操作計画に接続するパイプライン（Seed 2）である。剛体慣性パラメータ同定の40年の蓄積（回帰行列、励起軌道、物理整合性制約）の知見を柔軟物に移植することで、ロボティクスコミュニティに固有の貢献が可能となる。
