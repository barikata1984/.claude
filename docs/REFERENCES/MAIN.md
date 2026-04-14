# References

プロジェクト全体の文献データベース。

---

## Category A — Stable Placement Prediction

### Paxton2021_stable_placement

**Predicting Stable Configurations for Semantic Placement of Novel Objects**
Chris Paxton, Christopher Xie, Tucker Hermans, Dieter Fox — CoRL, 2021
arXiv: `2108.12062` | [arXiv](https://arxiv.org/abs/2108.12062)

> 物理的妥当性と意味的関係を結合した安定配置予測の先駆的研究。シミュレーション訓練→ゼロショット実世界転移。

### Eisner2024_se3_equivariant_placement

**Deep SE(3)-Equivariant Geometric Reasoning for Precise Placement Tasks**
Ben Eisner, Yi Yang, Todor Davchev, Mel Vecerik, Jonathan Scholz, David Held — ICLR, 2024
arXiv: `2404.13478` | [arXiv](https://arxiv.org/abs/2404.13478)

> SE(3)等変幾何推論により少数デモンストレーションから精密配置を達成。理論的保証と実用精度の両立。

### Ota2024_tactile_contact_patch

**Tactile Estimation of Extrinsic Contact Patch for Stable Placement**
Keita Ota, Devesh K. Jha, Krishna Murthy Jatavallabhula, Asako Kanezaki, Joshua B. Tenenbaum — ICRA, 2024
DOI: `10.1109/ICRA57147.2024.10611504`

> 触覚読み取りから外因性接触パッチを推定し、未知形状物体のフィードバックベース安定スタッキングを実現。

### Zhao2025_anyplace

**AnyPlace: Learning Generalized Object Placement for Robot Manipulation**
Yuchi Zhao, Miroslav Bogdanovic, Chen Luo, Steven Tohme, Kourosh Darvish, Alan Aspuru-Guzik, Florian Shkurti, Animesh Garg — arXiv, 2025
arXiv: `2502.04531` | [arXiv](https://arxiv.org/abs/2502.04531)

> VLM+合成データで挿入・スタッキング・吊り下げなど多様な配置モードへの汎化を実現。

### Noh2024_unseen_placement

**Learning to Place Unseen Objects Stably using Large-Scale Simulation**
Sangjun Noh, Raeyoung Kang, Taewon Kim, Seunghyeok Back, Seungbum Bak, Kyoobin Lee — RA-L, 2024
DOI: `10.1109/LRA.2024.3360810`

> 部分点群から形状補完なしで安定面を直接検出するUOP-Net。大規模合成データで未知物体に汎化。

### Nadeau2025_contact_robustness

**Stable Object Placement Planning From Contact Point Robustness**
Philippe Nadeau, Jonathan Kelly — T-RO, 2025
DOI: `10.1109/TRO.2025.3577049` | arXiv: `2410.12483`

> 接触点先行の配置計画アルゴリズム。慣性パラメータを考慮した物理ベース安定性ヒューリスティックで従来手法の20倍高速。

### Lee2024_spots

**SPOTS: Stable Placement of Objects with Reasoning in Semi-Autonomous Teleoperation Systems**
Joonhyung Lee, Sangbeom Park, Jeongeun Park, Kyungjae Lee, Sungjoon Choi — ICRA, 2024
DOI: `10.1109/ICRA57147.2024.10611613` | arXiv: `2309.13937`

> real-to-sim物理シミュレーションとLLM意味推論の結合によるテレオペレーション配置支援。

### Yoneda2024_6dofusion

**6-DoFusion: 6-DoF Stability Field via Diffusion Models**
Takuma Yoneda, Tianchong Jiang, Gregory Shakhnarovich, Matthew R. Walter — arXiv, 2024
arXiv: `2310.17649` | [arXiv](https://arxiv.org/abs/2310.17649)

> SE(3)上の拡散モデルで安定6-DoF配置ポーズ分布を学習。正例のみで訓練、リジェクションサンプリング不要。

### Takahashi2024_tactile_curl_diff

**Stable Object Placing using Curl and Diff Features of Vision-based Tactile Sensors**
Kuniyuki Takahashi, Shimpei Masuda, Tadahiro Taniguchi — IROS, 2024
DOI: `10.1109/IROS58592.2024.10801674` | arXiv: `2403.19129`

> GelSightドット変位から訓練不要・キャリブレーション不要で配置補正方向を推定。F/Tセンサの代替。

### Li2025_differentiable_contact

**Differentiable Contact Dynamics for Stable Object Placement Under Geometric Uncertainties**
Linfeng Li, Gang Yang, Lin Shao, David Hsu — RA-L, 2025
DOI: `10.1109/LRA.2025.3641124` | arXiv: `2409.17725`

> 微分可能接触力学でF/Tセンサ読み取りから幾何的不確実性を勾配降下で推定。

### Nadeau2025_physics_diffusion

**Generating Stable Placements via Physics-guided Diffusion Models**
Philippe Nadeau, Miguel Rogel, Ivan Bilic, Ivan Petrovic, Jonathan Kelly — arXiv, 2025
arXiv: `2509.21664` | [arXiv](https://arxiv.org/abs/2509.21664)

> 学習幾何事前分布と微分可能物理ロバスト性損失のスコア合成。再訓練なしで拡散モデルに安定性を統合。

---

## Category B — Integrated Pick-and-Place

### Zeng2020_transporter

**Transporter Networks: Rearranging the Visual World for Robotic Manipulation**
Andy Zeng, Pete Florence, Jonathan Tompson, Stefan Welker, Jonathan Chien, Maria Attarian, Travis Armstrong, Ivan Krasin, Dan Duong, Vikas Sindhwani, Johnny Lee — CoRL, 2020
arXiv: `2010.14406` | [arXiv](https://arxiv.org/abs/2010.14406)

> 深層特徴の空間変位によるpick-and-place表現を確立。1-shotデモンストレーション汎化の先駆。

### Shridhar2021_cliport

**CLIPort: What and Where Pathways for Robotic Manipulation**
Mohit Shridhar, Lucas Manuelli, Dieter Fox — CoRL, 2021
arXiv: `2109.12098` | [arXiv](https://arxiv.org/abs/2109.12098)

> CLIP意味特徴とTransporter空間精度を統合し、言語条件付きpick-and-placeを確立。

### Lee2021_beyond_pick_place

**Beyond Pick-and-Place: Tackling Robotic Stacking of Diverse Shapes**
Alex X. Lee, Coline Devin, Yuxiang Zhou, Thomas Lampe, et al. — CoRL, 2021
arXiv: `2110.06192` | [arXiv](https://arxiv.org/abs/2110.06192)

> 多様な形状のスタッキングでpick-and-placeを超える創発的スキル（道具使用、バランス維持）をRL+政策蒸留で獲得。

### Bauza2024_simple

**SimPLE: a visuotactile method learned in simulation to precisely pick, localize, regrasp, and place objects**
Maria Bauza, Antonia Bronars, Yifan Hou, Ian Taylor, Nikhil Chavan-Dafle, Alberto Rodriguez — Science Robotics, 2024
DOI: `10.1126/scirobotics.adi8808` | arXiv: `2307.13133`

> 視触覚フィードバックにより1mm以下の配置精度を達成。シミュレーションのみで訓練、実世界経験不要。

### He2023_pick2place

**Pick2Place: Task-aware 6DoF Grasp Estimation via Object-Centric Perspective Affordance**
Zhanpeng He, Nikhil Chavan-Dafle, Jinwook Huh, Shuran Song, Volkan Isler — ICRA, 2023
DOI: `10.1109/ICRA48891.2023.10160736` | arXiv: `2304.04100`

> 配置アフォーダンスから把持への微分可能マッピングによる配置aware 6-DoF把持推定。

### Wada2022_reorientbot

**ReorientBot: Learning Object Reorientation for Specific-Posed Placement**
Kentaro Wada, Stephen James, Andrew J. Davison — ICRA, 2022
DOI: `10.1109/icra46639.2022.9811881` | arXiv: `2202.11092`

> 目標ポーズ配置のための学習ベースウェイポイント選択と古典動作計画のハイブリッド。

### Cheng2021_regrasp_place

**Learning to Regrasp by Learning to Place**
Shuo Cheng, Kaichun Mo, Lin Shao — CoRL, 2021
arXiv: `2109.08817` | [arXiv](https://arxiv.org/abs/2109.08817)

> 安定中間配置予測による再把持計画。環境（壁、端）を再方向づけツールとして活用。

### Shanthi2024_joint_pick_place

**Pick and Place Planning is Better Than Pick Planning Then Place Planning**
Manoj Shanthi, Tucker Hermans — RA-L, 2024
DOI: `10.1109/LRA.2024.3360892` | arXiv: `2401.16585`

> 把持と配置の同時推論が逐次アプローチに対し厳密に優位であることを実証。

### Xu2024_grasp_see_place

**Grasp, See, and Place: Efficient Unknown Object Rearrangement with Policy Structure Prior**
Kechun Xu, Zhongxiang Zhou, Jun Wu, Haojian Lu, Rong Xiong, Yue Wang — T-RO, 2024
DOI: `10.1109/TRO.2024.3502520` | arXiv: `2402.15402`

> 知覚ノイズの分離影響を理論解析し、デュアルループ政策構造事前知識で未知物体再配置を効率化。

---

## Category C — Relational Object Rearrangement

### Liu2022_structformer

**StructFormer: Learning Spatial Structure for Language-Guided Semantic Rearrangement of Novel Objects**
Weiyu Liu, Chris Paxton, Tucker Hermans, Dieter Fox — ICRA, 2022
DOI: `10.1109/ICRA46639.2022.9811931` | arXiv: `2110.10189`

> 多物体間関係構造を同時推論するTransformerで言語指示からの意味的再配置を実現。

### Pan2022_tax_pose

**TAX-Pose: Task-Specific Cross-Pose Estimation for Robot Manipulation**
Chuer Pan, Brian Okorn, Harry Zhang, Ben Eisner, David Held — CoRL, 2022
arXiv: `2211.09325` | [PMLR](https://proceedings.mlr.press/v205/pan23a.html)

> 2物体間のSE(3)関係変換（cross-pose）を密対応から学習。10デモンストレーションで新規物体に汎化。

### Simeonov2022_rndf

**SE(3)-Equivariant Relational Rearrangement with Neural Descriptor Fields**
Anthony Simeonov, Yilun Du, Lin Yen-Chen, Alberto Rodriguez, Leslie Pack Kaelbling, Tomas Lozano-Perez, Pulkit Agrawal — CoRL, 2022
arXiv: `2211.09786` | [PMLR](https://proceedings.mlr.press/v205/simeonov23a.html)

> NDFによるタスク関連座標フレーム特定とエネルギーベースリファインメントで5-10デモから関係的再配置。

### Liu2023_structdiffusion

**StructDiffusion: Language-Guided Creation of Physically-Valid Structures using Unseen Objects**
Weiyu Liu, Yilun Du, Tucker Hermans, Sonia Chernova, Chris Paxton — RSS, 2023
DOI: `10.15607/RSS.2023.XIX.031` | arXiv: `2211.04604`

> 拡散モデル+オブジェクト中心Transformerで言語指示から物理的に妥当な構造を生成。

### Qureshi2021_nerp

**NeRP: Neural Rearrangement Planning for Unknown Objects**
Ahmed H. Qureshi, Arsalan Mousavian, Chris Paxton, Michael C. Yip, Dieter Fox — RSS, 2021
DOI: `10.15607/RSS.2021.XVII.072` | arXiv: `2106.01352`

> 未知物体のエンドツーエンド再配置計画の初のシステム。GNNベース。

### Simeonov2023_rpdiff

**Shelving, Stacking, Hanging: Relational Pose Diffusion for Multi-modal Rearrangement**
Anthony Simeonov, Ankit Goyal, Lucas Manuelli, Lin Yen-Chen, Alina Sarmiento, Alberto Rodriguez, Pulkit Agrawal, Dieter Fox — CoRL, 2023
arXiv: `2307.04751` | [PMLR](https://proceedings.mlr.press/v229/simeonov23a.html)

> 反復ポーズデノイジングとローカルシーンクロッピングで多峰性関係的再配置を実現。

### Kapelyukh2024_dream2real

**Dream2Real: Zero-Shot 3D Object Rearrangement with Vision-Language Models**
Ivan Kapelyukh, Yifei Ren, Ignacio Alzugaray, Edward Johns — ICRA, 2024
DOI: `10.1109/ICRA57147.2024.10611220` | arXiv: `2312.04533`

> NeRF+CLIP評価によるゼロショット言語条件付き6-DoF再配置。訓練データ不要。

### Murali2023_cabinet

**CabiNet: Scaling Neural Collision Detection for Object Rearrangement with Procedural Scene Generation**
Adithyavairavan Murali, Arsalan Mousavian, Clemens Eppner, Adam Fishman, Dieter Fox — ICRA, 2023
DOI: `10.1109/ICRA48891.2023.10161528` | arXiv: `2304.09302`

> 大規模手続き的シーン生成でニューラル衝突検出をスケール。狭空間再配置に対応。

### Wu2022_targf

**TarGF: Learning Target Gradient Field for Object Rearrangement**
Mingdong Wu, Fangwei Zhong, Yulong Xia, Hao Dong — NeurIPS, 2022
arXiv: `2209.00853` | [arXiv](https://arxiv.org/abs/2209.00853)

> スコアマッチングでターゲット分布の勾配場を学習。明示的ゴールやデモなしで再配置を誘導。

### Tang2022_selective_rearrangement

**Selective Object Rearrangement in Clutter**
Bingjie Tang, Gaurav S. Sukhatme — CoRL, 2022
[PMLR](https://proceedings.mlr.press/v205/tang23a.html)

> クラッター中の選択的再配置を画像ベースで解決。プッシュ/グラスプ行動選択と視覚対応配置の統合。

---

## Category D — Generalist Robot Policies

### Ahn2022_saycan

**Do As I Can, Not As I Say: Grounding Language in Robotic Affordances**
Michael Ahn, Anthony Brohan, Noah Brown, et al. — CoRL, 2022
arXiv: `2204.01691` | [arXiv](https://arxiv.org/abs/2204.01691)

> LLMをアフォーダンス関数で根拠付けし、物理的に実現可能なタスク計画を生成。

### Chi2023_diffusion_policy

**Diffusion Policy: Visuomotor Policy Learning via Action Diffusion**
Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, Shuran Song — RSS 2023 / IJRR
DOI: `10.1177/02783649241273668` | arXiv: `2303.04137`

> 行動拡散による汎用visuomotorポリシー学習。先行手法に対し平均46.9%改善。

### Brohan2023_rt2

**RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control**
Anthony Brohan, Noah Brown, et al. — CoRL, 2023
arXiv: `2307.15818` | [arXiv](https://arxiv.org/abs/2307.15818)

> VLMを行動テキストトークン化で直接VLAに変換。Webスケール知識のロボット制御への転移。

### Brohan2022_rt1

**RT-1: Robotics Transformer for Real-World Control at Scale**
Anthony Brohan, Noah Brown, et al. — RSS, 2023
arXiv: `2212.06817` | [arXiv](https://arxiv.org/abs/2212.06817)

> 130kエピソード、700+タスクで訓練されたTransformer。基盤モデルパラダイムの実世界ロボティクスへの転移を実証。

### Kim2024_openvla

**OpenVLA: An Open-Source Vision-Language-Action Model**
Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, et al. — CoRL, 2024
arXiv: `2406.09246` | [arXiv](https://arxiv.org/abs/2406.09246)

> オープンソース7B VLA。RT-2-X (55B) を16.5%上回り消費者GPUでファインチューニング可能。

### Black2024_pi0

**pi0: A Vision-Language-Action Flow Model for General Robot Control**
Kevin Black, Noah Brown, Danny Driess, et al. — arXiv, 2024
arXiv: `2410.24164` | [arXiv](https://arxiv.org/abs/2410.24164)

> フローマッチングVLA。約10,000時間のロボットデータで訓練、50Hz連続行動生成。

### Ghosh2024_octo

**Octo: An Open-Source Generalist Robot Policy**
Dibya Ghosh, Homer Walke, Karl Pertsch, et al. — RSS, 2024
arXiv: `2405.12213` | [arXiv](https://arxiv.org/abs/2405.12213)

> 800k軌道で訓練されたモジュラー汎用ロボット政策。消費者GPUで効率的ファインチューニング可能。

### Li2024_simpler

**SIMPLER: Simulated Manipulation Policy Evaluation for Real Robot**
Xuanlin Li, Kyle Hsu, Jiayuan Gu, et al. — CoRL, 2024
arXiv: `2405.05941` | [arXiv](https://arxiv.org/abs/2405.05941)

> シミュレーション評価で実世界ポリシー性能を予測。制御・視覚ギャップの体系的緩和。

---

## Category E — SE(3) Grasp & Motion Optimization

### Sundermeyer2021_contact_graspnet

**Contact-GraspNet: Efficient 6-DoF Grasp Generation in Cluttered Scenes**
Martin Sundermeyer, Arsalan Mousavian, Rudolph Triebel, Dieter Fox — ICRA, 2021
DOI: `10.1109/ICRA48506.2021.9561877` | arXiv: `2103.14127`

> 観測点群の点を把持接触点として6-DoF→4-DoF還元。クラッターで90.2%成功率。

### Huang2023_scenediffuser

**SceneDiffuser: Diffusion-based Generation, Optimization, and Planning in 3D Scenes**
Siyuan Huang, Zan Wang, Puhao Li, et al. — CVPR, 2023
DOI: `10.1109/CVPR52729.2023.01607` | arXiv: `2301.06015`

> 単一拡散モデルでシーン条件付き生成・物理最適化・計画を統一。

### Ichnowski2021_dex_nerf

**Dex-NeRF: Using a Neural Radiance Field to Grasp Transparent Objects**
Jeffrey Ichnowski, Yahav Avigal, Justin Kerr, Ken Goldberg — CoRL, 2021
arXiv: `2110.14217` | [arXiv](https://arxiv.org/abs/2110.14217)

> NeRFの透明性aware深度レンダリングで透明物体の信頼性ある把持を実現。

### Urain2023_se3_diffusion_fields

**SE(3)-DiffusionFields: Learning Smooth Cost Functions for Joint Grasp and Motion Optimization**
Julen Urain, Niklas Funk, Jan Peters, Georgia Chalvatzaki — ICRA, 2023
DOI: `10.1109/ICRA48891.2023.10161569` | arXiv: `2209.03855`

> SE(3)上のスコアマッチングで把持と軌道の同時最適化を単一微分可能フレームワークで実現。

### Weng2023_ngdf

**Neural Grasp Distance Fields for Robot Manipulation**
Thomas Weng, David Held, Franziska Meier, Mustafa Mukadam — ICRA, 2023
DOI: `10.1109/ICRA48891.2023.10160217` | arXiv: `2211.02647`

> 有効把持多様体のニューラル距離場表現。勾配ベース軌道最適化にシームレスに統合。

---

## Category F — Task Planning & Benchmarks

### Ding2023_llm_tamp

**Task and Motion Planning with Large Language Models for Object Rearrangement**
Yan Ding, Xiaohan Zhang, Chris Paxton, Shiqi Zhang — IROS, 2023
DOI: `10.1109/IROS55552.2023.10342169` | arXiv: `2303.06247`

> LLMの常識知識をTAMPで幾何的にインスタンス化し、ゼロショット意味的配置を実現。

### Qi2025_sofar

**SoFar: Language-Grounded Orientation Bridges Spatial Reasoning and Object Manipulation**
Zekun Qi, Wenyao Zhang, et al. — arXiv, 2025
arXiv: `2502.13143` | [arXiv](https://arxiv.org/abs/2502.13143)

> 「semantic orientation」概念で物体の向きを自然言語で定義。OrienText300Kデータセット。

### Chang2024_lgmcts

**LGMCTS: Language-Guided Monte-Carlo Tree Search for Executable Semantic Object Rearrangement**
Haonan Chang, Kai Gao, et al. — IROS, 2024
DOI: `10.1109/IROS58592.2024.10802562` | arXiv: `2309.15821`

> 言語誘導ポーズ生成とMCTS計画の統合。StructDiffusionに対し線パターンで95.99% vs 61.49%。

### Shukla2025_maniskill_hab

**ManiSkill-HAB: A Benchmark for Low-Level Manipulation in Home Rearrangement Tasks**
Arth Shukla, Stone Tao, Hao Su — ICLR, 2025
arXiv: `2412.13211` | [arXiv](https://arxiv.org/abs/2412.13211)

> GPU加速家庭再配置ベンチマーク。現実的low-level制御でHabitat 2.0の3倍高速。

### Yenamandra2023_homerobot

**HomeRobot: Open-Vocabulary Mobile Manipulation**
Sriram Yenamandra, Arun Ramachandran, et al. — CoRL, 2023
arXiv: `2306.11565` | [arXiv](https://arxiv.org/abs/2306.11565)

> Open-Vocabulary Mobile Manipulation統合ベンチマーク。実世界成功率~20%で改善の方向性を明示。

---

## F/T Sensor-Based Inertial Parameter Estimation

### Atkeson1986_foundational

**Estimation of Inertial Parameters of Manipulator Loads and Links**
C. Atkeson, C. An, J. Hollerbach — IJRR, 1986
DOI: `10.1177/027836498600500306`

> F/Tセンサによる操作対象の慣性パラメータ同定の先駆的定式化。線形回帰モデルによる10パラメータ推定の基礎を確立。

### Gautier1992_excitation

**Exciting Trajectories for the Identification of Base Inertial Parameters of Robots**
Maxime Gautier, W. Khalil — IJRR, 1992
DOI: `10.1177/027836499201100408`

> ロボット基底慣性パラメータ同定のための励起軌道設計理論を体系化。観測行列の条件数最小化による最適励起の枠組みを提供。

### Swevers1997_optimal

**Optimal Robot Excitation and Identification**
J. Swevers, C. Ganseman, D. Tükel, J. De Schutter, H. Van Brussel — IEEE TRA, 1997
DOI: `10.1109/70.631234`

> 有限フーリエ級数軌道によるロボット最適励起と慣性パラメータ同定の実験的検証。産業ロボット同定の標準的方法論を確立。

### Swevers2002_experimental

**An Experimental Robot Load Identification Method for Industrial Application**
J. Swevers, W. Verdonck, B. Naumer, S. Pieters, E. Biber — IJRR, 2002
DOI: `10.1177/027836402761412449`

> 産業応用に向けたロボットペイロード同定の実験的手法。リアルタイム計測と最小二乗同定を組み合わせた実用的プロトコルを提案。

### Duan2022_ft_payload

**Payload Identification and Gravity/Inertial Compensation for Six-Dimensional Force/Torque Sensor**
Jinjun Duan, Zhouchi Liu, Yiming Bin, Kunkun Cui, Zhendong Dai — Sensors (MDPI), 2022
DOI: `10.3390/s22020439`

> 6軸F/Tセンサのペイロード同定と重力・慣性補償を統合した手法。ロバスト軌道設計でF/Tセンサ読み取りから10慣性パラメータを高精度に推定。

### Lambert2023_real2sim

**Identifying Objects' Inertial Parameters for Real2Sim Assets**
Nathan Lambert, Franziska Meier, Paloma Sodhi, Michael Kaess — MIT CSAIL, 2023
URL: [PDF](https://groups.csail.mit.edu/robotics-center/public_papers/Lambert23.pdf)

> シミュレーション資産の実世界転移に向けた物体慣性パラメータの同定手法。Real2Simギャップ解消に対するデータ駆動アプローチ。

### Robert2026_spectral

**Spectral Identification of Inertial Parameters in Forced Sinusoidal Regimes**
Robert, C., Krut, S., Company, O., Vissiere, A., Noire, P., Pierrot, F. — ASME JDSMC, 2026
DOI: `10.1115/1.4070775`

> ヘキサポッド並列ロボットによる強制正弦波励起と周波数領域Newton-Euler解法により、再位置決めなしで全慣性パラメータをスペクトル同定。

### Tian2024_excitation

**Excitation Trajectory Optimization for Dynamic Parameter Identification Using Virtual Constraints**
Tian et al. — ICRA, 2024
DOI: `10.1109/ICRA57147.2024.10610950` | [arXiv](https://arxiv.org/abs/2401.16566)

> 仮想制約を用いた動力学パラメータ同定のための励起軌道最適化。ハンズオンロボットシステムへの適用でリアルタイム同定精度を向上。

### Lee2021_geometric_excitation

**Optimal Excitation Trajectories for Mechanical Systems Identification**
Lee, Lee, Park — Automatica, 2021
DOI: `10.1016/j.automatica.2021.109773`

> 幾何学的アプローチによる機械系同定最適励起軌道の理論的枠組み。条件数最小化と物理的制約の両立を実現。

### Hartwig2025_human_demo

**Estimation of Payload Inertial Parameters from Human Demonstrations by Hand Guiding**
Hartwig, Lienhardt, Henrich — arXiv, 2025
[arXiv](https://arxiv.org/abs/2507.15604)

> ハンドガイディングによる人間デモンストレーションからペイロード慣性パラメータを推定。専用キャリブレーション軌道不要でコボット現場導入を容易化。

### Kubus2008_rtls

**On-line Estimation of Inertial Parameters Using a Recursive Total Least-Squares Approach**
D. Kubus, T. Kröger, F. Wahl — IROS, 2008
DOI: `10.1109/IROS.2008.4650672`

> 再帰的全最小二乗法によるリアルタイム慣性パラメータ推定。データ行列のノイズを明示的に扱い、約1.5秒で10パラメータを同定。

### Farsoni2018_realtime_kf

**Real-Time Identification of Robot Payload Using a Multirate Quaternion-Based Kalman Filter and Recursive Total Least-Squares**
Farsoni, Landi, Ferraguti, Secchi, Bonfe — ICRA, 2018
DOI: `10.1109/ICRA.2018.8461167`

> マルチレートクォータニオンKFとRTLSを組み合わせたリアルタイムペイロード同定。異なるサンプリング周波数の慣性・運動学センサデータを融合。

### Gaz2017_coefficients

**Payload Estimation Based on Identified Coefficients of Robot Dynamics**
C. Gaz, A. De Luca — IROS, 2017
DOI: `10.1109/IROS.2017.8206142`

> 同定済みロボット動力学係数からのペイロード推定手法。標準動力学モデルとの係数差分を利用した実用的アプローチ。

### Chu2017_space

**Inertial Parameter Identification Using Contact Force for Space Manipulator**
Z. Chu, J. Ma, Y. Hou, F. Wang — Acta Astronautica, 2017
DOI: `10.1016/j.actaastro.2016.11.019`

> 宇宙マニピュレータの接触力情報を用いた未知物体慣性パラメータ同定。軌道上サービシング向けにノイズ下でのロバスト同定を実現。

### Uchida2025_space_rls

**Online Inertia Parameter Estimation for Unknown Objects Grasped by a Manipulator Towards Space Applications**
Uchida, Richard, Uno, Olivares-Mendez, Yoshida — arXiv, 2025
[arXiv](https://arxiv.org/abs/2512.21886)

> 宇宙ロボット応用に向けたグラスプ中の未知物体オンライン慣性パラメータ推定。再帰的最小二乗法を用いた軌道上リアルタイム同定。

### Foster2024_humanoid_adaptation

**Physically Consistent Online Inertial Adaptation for Humanoid Loco-manipulation**
Foster, McCrory et al. — IROS, 2024
[arXiv](https://arxiv.org/abs/2405.07901)

> 拡張カルマンフィルタによる慣性パラメータ推定と全身コントローラを組み合わせ、重量ペイロードを持つヒューマノイドのロコマニピュレーションを実現。

### Bai2025_sensorless_hri

**Sensorless Human–Robot Interaction: Real-Time Estimation of Co-Grasped Object Mass and Human Wrench for Compliant Interaction**
Bai et al. — Advanced Intelligent Systems, 2025
DOI: `10.1002/aisy.202400616`

> 外乱オブザーバとEKFを統合し、専用センサなしで共把持物体の質量と人間の力レンチをリアルタイム推定するHRIフレームワーク。

### Nadeau2024_bias

**Automated Continuous Force-Torque Sensor Bias Estimation**
Philippe Nadeau, Miguel Rogel Garcia, Emmett Wise, Jonathan Kelly — arXiv, 2024
[arXiv](https://arxiv.org/abs/2403.01068)

> ロボット操作中の6軸F/Tセンサバイアスドリフトを継続的に自動推定。慣性パラメータ同定の前処理として精度向上に直接貢献。

### Sousa2014_lmi

**Physical Feasibility of Robot Base Inertial Parameter Identification: A Linear Matrix Inequality Approach**
Cristóvão D. Sousa, Rui Cortesão — IJRR, 2014
DOI: `10.1177/0278364913514870`

> 慣性パラメータの物理的整合性条件をLMI（線形行列不等式）として定式化。SDP技術で実行不可能な推定値の最近傍整合解を算出。

### Traversaro2016_manifold

**Identification of Fully Physical Consistent Inertial Parameters Using Optimization on Manifolds**
S. Traversaro, S. Brossette, A. Escande, F. Nori — IROS, 2016
DOI: `10.1109/IROS.2016.7759801` | [arXiv](https://arxiv.org/abs/1610.08703)

> 多様体上の最適化により完全に物理整合性のある慣性パラメータを同定。iCubヒューマノイドでの検証で非整合推定の問題を解消。

### Janot2021_sdp

**Sequential Semidefinite Programming for Physically and Statistically Consistent Robot Identification**
A. Janot, P. Wensing — Control Engineering Practice, 2021
DOI: `10.1016/j.conengprac.2020.104699`

> 逐次半正定値計画法により物理整合性と統計的一致性を同時に満たすロボット慣性パラメータ同定を実現。

### Khorshidi2024_contact_id

**Physically-Consistent Parameter Identification of Robots in Contact**
Khorshidi et al. — arXiv, 2024
[arXiv](https://arxiv.org/abs/2409.09850)

> 接触中のロボットに対する物理整合性保証付きパラメータ同定手法。Spot四脚ロボットでのジョイントトルク計測を用いた検証を実施。

### Zhang2025_safe_id

**Provably-Safe, Online System Identification**
Bohao Zhang, Zichang Zhou, Ram Vasudevan — RSS, 2025
[arXiv](https://arxiv.org/abs/2504.21486)

> ロボットマニピュレータがペイロードパラメータを同定しながら安全性保証を維持する証明可能安全なオンライン同定フレームワーク。

### Nadeau2022_fast_cobot

**Fast Object Inertial Parameter Identification for Collaborative Robots**
Philippe Nadeau, Matthew Giamou, Jonathan Kelly — ICRA, 2022
DOI: `10.1109/ICRA46639.2022.9916213` | [arXiv](https://arxiv.org/abs/2203.00830)

> 協調ロボット向け高速物体慣性パラメータ同定。F/Tセンサと最小二乗推定を組み合わせ、短時間の探索動作で10パラメータを同定。

### Nadeau2023_visual_parts

**The Sum of Its Parts: Visual Part Segmentation for Inertial Parameter Identification of Manipulated Objects**
Philippe Nadeau, Matthew Giamou, Jonathan Kelly — ICRA, 2023
DOI: `10.1109/ICRA48891.2023.10160394` | [arXiv](https://arxiv.org/abs/2302.06685)

> 視覚的部品分割で物体形状事前知識を同定に統合。F/T計測と幾何情報の融合により同定精度とサンプル効率を向上。

### Baek2024_humanoid_learning

**Online Learning-Based Inertial Parameter Identification of Unknown Object for Model-Based Control of Wheeled Humanoids**
Donghoon Baek, Bo Peng, Saurabh Gupta, Joao Ramos — arXiv, 2024
[arXiv](https://arxiv.org/abs/2309.09810)

> 車輪付きヒューマノイドのモデルベース制御向けオンライン学習による慣性パラメータ同定。操作中リアルタイムで物体パラメータを更新しコントローラを適応。

### Chen2025_differentiable

**Learning Object Properties Using Robot Proprioception via Differentiable Robot-Object Interaction**
Peter Yichen Chen, Liu, Ma et al. — ICRA, 2025
[arXiv](https://arxiv.org/abs/2410.03920)

> 微分可能ロボット-物体インタラクションにより、外部センサなしでジョイントエンコーダのみから物体質量・弾性率等の物性を学習。

### Shan2024_fast_calibration

**Fast Payload Calibration for Sensorless Contact Estimation Using Model Pre-training**
Shilin Shan, Quang-Cuong Pham — IEEE RA-L, 2024
[arXiv](https://arxiv.org/abs/2409.03369)

> モデル事前学習を活用したセンサレス接触推定向け高速ペイロードキャリブレーション。新規ペイロードへの迅速な適応を実現。

### Jin2025_ugraph

**Learning to Double Guess: An Active Perception Approach for Estimating the Center of Mass of Arbitrary Objects (U-GRAPH)**
Shengmiao Jin, Yuchen Mo, Wenzhen Yuan — ICRA, 2025
[arXiv](https://arxiv.org/abs/2502.02663)

> ベイズニューラルネットワークで不確実性を定量化しCoM推定の情報豊富な探索を誘導するアクティブ知覚フレームワーク。

### RobotScale2023

**RobotScale: A Framework for Adaptable Estimation of Static and Dynamic Object Properties with Object-dependent Sensitivity Tuning**
various — IEEE RO-MAN, 2023
DOI: `10.1109/RO-MAN57019.2023.10309315`

> 物体依存感度チューニングを用いた静的・動的物体特性の適応的推定フレームワーク。多様な物体に対する慣性パラメータ推定の汎用化に取り組む。

### Wang2021_fingertip

**Parameter Estimation and Object Gripping Based on Fingertip Force/Torque Sensors**
Wang, Zang, Zhang et al. — Measurement, 2021
DOI: `10.1016/j.measurement.2021.109479`

> 指先F/Tセンサを用いた物体パラメータ推定と把持制御の統合。把持中のリアルタイム慣性パラメータ同定により安定把持を実現。

### Yu2022_bias_gravity

**Bias Estimation and Gravity Compensation for Wrist-Mounted Force/Torque Sensor**
Yongqiang Yu, Ran Shi, Yunjiang Lou — IEEE Sensors Journal, 2022
DOI: `10.1109/JSEN.2021.3056943`

> 手首搭載F/Tセンサのバイアス推定と重力補償のための統合手法。センサ-ロボット間変換未知の状態での回転キャリブレーションを実現。

### Farsoni2019_safety

**Safety-Oriented Robot Payload Identification Using Collision-Free Path Planning and Decoupling Motions**
Farsoni, Ferraguti et al. — Robotics and Computer-Integrated Manufacturing, 2019
DOI: `10.1016/j.rcim.2019.04.011`

> 衝突回避経路計画と分離動作を用いた安全指向ペイロード同定。人間-ロボット共存環境での安全な同定軌道設計手法を提案。

### Farsoni2022_hrc

**Complete and Consistent Payload Identification During Human-Robot Collaboration: A Safety-Oriented Procedure**
S. Farsoni, M. Bonfè — Springer (Human-Friendly Robotics 2021), 2022
DOI: `10.1007/978-3-030-96359-0_2`

> HRC中の完全かつ一致したペイロード同定のための安全指向手順。同定精度と人間安全性の両立を実証。

### Liu2025_twostage

**A Two-Stage Payload Dynamic Parameter Identification Method for Interactive Industrial Robots With Large Components**
Mingxuan Liu et al. — IEEE TASE, 2025
DOI: `10.1109/TASE.2025.3557064`

> 大型コンポーネントを持つ産業ロボット向け2段階ペイロード動力学パラメータ同定。制限付き全最小二乗法（RRTLS）による低消費電力オンライン同定を実現。

---

## Stable Placement Planning (Additional)

### Lerner2024_ft_placement

**Precise Object Placement Using Force-Torque Feedback**
Osher Lerner, Zachary Tam, Michael Equi — arXiv, 2024
[arXiv](https://arxiv.org/abs/2404.17668)

> F/Tフィードバックを用いた高精度物体配置。計画誤差とセンサノイズに対してロバストな配置制御を実証し、F/T情報の配置精度向上への直接的寄与を示す。

### Ferrad2025_placeit

**Placeit! A Framework for Learning Robot Object Placement Skills**
Ferrad, Huber et al. — arXiv, 2025
[arXiv](https://arxiv.org/abs/2510.09267)

> 進化計算ベースの配置スキル学習フレームワーク。120回の実世界デプロイで90%成功率を達成し、SOTA手法を大幅に上回る汎化性能を示す。

### Haustein2019_placement

**Object Placement Planning and Optimization for Robot Manipulators**
Joshua A. Haustein, Kaiyu Hang, Johannes Stork, Danica Kragic — arXiv, 2019
[arXiv](https://arxiv.org/abs/1907.02555)

> 把持状態での物体配置の動作計画と最適化手法。クラッター環境での配置目標最適化と衝突回避を統合した計画フレームワーク。

---

## Adjacent — CoM-Informed Manipulation

### Kubus2007_recognition

**On-line Rigid Object Recognition and Pose Estimation Based on Inertial Parameters**
D. Kubus, T. Kröger, F. Wahl — IROS, 2007
DOI: `10.1109/IROS.2007.4399184`

> F/T・加速度・角速度センサ融合による把持物体のオンライン剛体認識とポーズ推定。慣性パラメータを物体識別に活用する先駆的手法。

### Kanoulas2018_com_grasp

**Center-of-Mass-Based Grasp Pose Adaptation Using 3D Range and Force/Torque Sensing**
Dimitrios Kanoulas, Jinoh Lee, Darwin G. Caldwell, Nikos G. Tsagarakis — IJHR, 2018
DOI: `10.1142/S0219843618500135` | [arXiv](https://arxiv.org/abs/1802.06392)

> 3DレンジセンサとF/Tセンシングを組み合わせたCoMベース把持ポーズ適応。外受容・固有受容センサ融合による動的把持調整手法。

### Feng2020_com_grasp

**Center-of-Mass-Based Robust Grasp Planning Using Tactile-Visual Sensors**
Feng et al. — ICRA, 2020
DOI: `10.1109/ICRA40945.2020.9196815` | [arXiv](https://arxiv.org/abs/2006.00906)

> 触覚-視覚センサ融合によるCoMベースロバスト把持計画。スリップ検出76.88%精度と把持成功率31%向上を達成し、CoM情報の把持安定化への有効性を実証。

### Feng2024_com_regrasp

**Center-of-Mass-Based Object Regrasping: A Reinforcement Learning Approach and the Effects of Perception Modality**
Feng et al. — IEEE RA-L, 2024
DOI: `10.1109/LRA.2024.3439540`

> RLとCoMベース再把持の統合。視覚・指先触覚・手首F/Tセンサの知覚モダリティが再把持効率に与える影響を体系的に比較検証。

### Kang2025_cog_grasping

**Foundation Model-Driven Grasping of Unknown Objects via Center of Gravity Estimation**
Kang, He, Gong, Liu, Bai — arXiv, 2025
[arXiv](https://arxiv.org/abs/2507.19242)

> 拡散モデルによる重心推定を活用した未知物体把持。従来のキーポイントベース手法に対し49%高い成功率を達成。

### Dutta2025_visuotactile

**Predictive Visuo-Tactile Interactive Perception Framework for Object Properties Inference**
Anirvan Dutta, Etienne Burdet, Mohsen Kaboli — IEEE T-RO, 2025
DOI: `10.1109/TRO.2025.3531816` | [arXiv](https://arxiv.org/abs/2411.09020)

> 視触覚インタラクティブ知覚フレームワークで質量・CoM・剛性・摩擦係数・形状を推定。能動形状知覚メカニズムにより探索行動を自律的に制御。

### Watanabe2025_ftact

**FTACT: Force Torque Aware Action Chunking Transformer for Pick-and-Reorient**
Watanabe, Alvarez, Ferreiro, Savkin, Sano — arXiv, 2025
[arXiv](https://arxiv.org/abs/2509.23112)

> F/T感知をAction Chunking Transformerに統合したマルチモーダル模倣学習。F/T情報がボトル再方向づけタスクの成功率を顕著に向上することを実証。

### Ye2026_flyaware

**FlyAware: Inertia-Aware Aerial Manipulation via Vision-Based Estimation and Post-Grasp Adaptation**
Ye et al. — IEEE RA-L, 2026
[arXiv](https://arxiv.org/abs/2601.22686)

> 視覚ベース慣性特性推定とグラスプ後適応制御を組み合わせた慣性aware空中操作。ペイロード変動と構成変化への適応メカニズムを提案。

### Kruzliak2024_interactive

**Interactive Learning of Physical Object Properties Through Robot Manipulation and Database of Object Measurements**
Kruzliak, Hartvich, Patni et al. — IROS, 2024
DOI: `10.1109/IROS58592.2024.10802249` | [arXiv](https://arxiv.org/abs/2404.07344)

> ロボット操作を通じた物理的物体特性（材質・質量・体積・剛性）のインタラクティブ学習フレームワーク。計測データベースの自動構築と物体モデリングを統合。

---

## Surveys — Inertial Parameter Identification

### Mavrakis2020_survey

**Estimation and Exploitation of Objects' Inertial Parameters in Robotic Grasping and Manipulation: A Survey**
N. Mavrakis, R. Stolkin — Robotics and Autonomous Systems, 2020
DOI: `10.1016/j.robot.2019.103374` | [arXiv](https://arxiv.org/abs/1911.04397)

> ロボット把持・操作における物体慣性パラメータ推定と活用に関する包括的サーベイ。F/Tセンサベース手法から学習ベース手法まで体系的にレビュー。

### Leboutet2021_birdy

**Inertial Parameter Identification in Robotics: A Survey (BIRDy)**
Leboutet, Roux, Janot et al. — Applied Sciences (MDPI), 2021
DOI: `10.3390/app11094303`

> ロボティクスにおける慣性パラメータ同定の包括的サーベイ（BIRDyツールボックス）。古典的同定手法から最新の学習・物理整合性手法まで網羅。

### Swevers2007_tutorial

**Dynamic Model Identification for Industrial Robots**
J. Swevers, W. Verdonck, J. De Schutter — IEEE Control Systems Magazine, 2007
DOI: `10.1109/MCS.2007.904659`

> 産業ロボット動力学モデル同定の実践チュートリアル。励起軌道設計・パラメータ推定・検証の全工程を体系的に解説。

---

## Category G — Deformable Object Physical Property Recovery

### Weiss2020_sparseConstraints

**Correspondence-Free Material Reconstruction using Sparse Surface Constraints**
Martin Weiss et al. — CVPR, 2020
arXiv: `1910.01812` | [arXiv](https://arxiv.org/abs/1910.01812)

> 対応点追跡なしに単一視点深度列から弾性パラメータを復元。Sparse Surface Constraintによる微分可能逆問題定式化。

### Jatavallabhula2021_gradSim

**gradSim: Differentiable Simulation for System Identification and Visuomotor Control**
Krishna Murthy Jatavallabhula et al. — ICLR, 2021
arXiv: `2104.02646` | [arXiv](https://arxiv.org/abs/2104.02646)

> 微分可能レンダリング＋物理の統合により、ビデオピクセルから物理パラメータへの勾配逆伝播を初実現。

### Feng2022_vibrationTomography

**Visual Vibration Tomography: Estimating Interior Material Properties from Monocular Video**
Berthy Feng et al. — CVPR, 2022 (Oral)
arXiv: `2104.02735` | [arXiv](https://arxiv.org/abs/2104.02735)

> 表面振動モードの単眼ビデオ観察とFEMモーダル解析の逆問題として、物体内部のYoung's modulus・密度分布を復元。

### Qiao2022_NeuPhysics

**NeuPhysics: Editable Neural Geometry and Physics from Monocular Videos**
Yi-Ling Qiao et al. — NeurIPS, 2022
arXiv: `2210.12352` | [arXiv](https://arxiv.org/abs/2210.12352)

> Neural SDF＋微分可能FEMにより単眼ビデオから3D形状・物理パラメータを同時再構築し、インタラクティブ編集を実現。

### Guan2022_NeuroFluid

**NeuroFluid: Fluid Dynamics Grounding with Particle-Driven Neural Radiance Fields**
Shanyan Guan et al. — ICML, 2022 (Spotlight)
arXiv: `2203.01762` | [arXiv](https://arxiv.org/abs/2203.01762)

> 粒子駆動NeRFレンダラとの端-端最適化により、粒子軌跡正解なしにピクセル観察から流体の粘性・密度を推定。

### Li2023_PACNeRF

**PAC-NeRF: Physics Augmented Continuum Neural Radiance Fields for Geometry-Agnostic System Identification**
Xuan Li et al. — ICLR, 2023
arXiv: `2303.05512` | [arXiv](https://arxiv.org/abs/2303.05512)

> NeRF＋MPMハイブリッド表現で形状未知条件下のマルチビュービデオから弾性率・粘性等を同時復元する初の手法。

### Xie2024_PhysGaussian

**PhysGaussian: Physics-Integrated 3D Gaussians for Generative Dynamics**
Tianyi Xie et al. — CVPR, 2024 (Highlight)
arXiv: `2311.12198` | [arXiv](https://arxiv.org/abs/2311.12198)

> 3DGaussianカーネルにMPM物理属性を直接付与し「what you see is what you simulate」パラダイムを確立。

### Chen2024_GIC

**GIC: Gaussian-Informed Continuum for Physical Property Identification and Simulation**
Junhao Cai et al. — NeurIPS, 2024 (Oral)
arXiv: `2406.14927` | [arXiv](https://arxiv.org/abs/2406.14927)

> 明示的3DGaussianと暗黙的連続体の双方向監視でPAC-NeRFを大幅に超える物性同定精度を達成。

### Feng2024_PIENeRF

**PIE-NeRF: Physics-based Interactive Elastodynamics with NeRF**
Tianhao Feng et al. — CVPR, 2024
arXiv: `2311.13099` | [arXiv](https://arxiv.org/abs/2311.13099)

> NeRF密度場上のメッシュレスQ-GMLS離散化で、メッシュなしの超弾性インタラクティブシミュレーションを実現。

### Zhong2024_SpringGaus

**Reconstruction and Simulation of Elastic Objects with Spring-Mass 3D Gaussians**
Licheng Zhong et al. — ECCV, 2024
DOI: `10.1007/978-3-031-72627-9_23` | arXiv: `2403.09434`

> Spring-Massと3DGSの統合。外観学習と物理学習の分離によるサンプル効率的なper-point物性推定。

### Liu2024_Physics3D

**Physics3D: Learning Physical Properties of 3D Gaussians via Video Diffusion**
Fangfu Liu et al. — arXiv, 2024
arXiv: `2406.04338` | [arXiv](https://arxiv.org/abs/2406.04338)

> Video Diffusion SDSによる粘弾性パラメータ蒸留。弾性のみのPhysDreamerを材料空間で拡張。

### Huang2025_DreamPhysics

**DreamPhysics: Learning Physics-Based 3D Dynamics with Video Diffusion Priors**
Tianyu Huang et al. — AAAI, 2025
arXiv: `2406.01476` | [arXiv](https://arxiv.org/abs/2406.01476)

> SDS損失＋フレーム補間＋対数勾配最適化により、Video DiffusionからMPM-Gaussianへの安定的物理プライオア蒸留。

### Hong2026_PIDG

**Physics-Informed Deformable Gaussian Splatting: Towards Unified Constitutive Laws for Time-Evolving Material Field**
Haoqin Hong et al. — AAAI, 2026
arXiv: `2511.06299` | [arXiv](https://arxiv.org/abs/2511.06299)

> Cauchy運動量方程式残差制約をGaussian粒子に課し、既知構成則なしで単眼ビデオから物理整合的動的再構成。

### Chopra2025_PhysGS

**PhysGS: Bayesian-Inferred Gaussian Splatting for Physical Property Estimation**
Abhinav Chopra et al. — arXiv, 2025
arXiv: `2511.18570` | [arXiv](https://arxiv.org/abs/2511.18570)

> Per-point物性のBayes反復推論。Vision-languageプライオアでシードし不確実性を明示モデル化。

### Vasile2025_ASDiffMPM

**Gaussian-Augmented Physics Simulation and System Identification with Complex Colliders**
Federico Vasile et al. — NeurIPS, 2025
arXiv: `2511.06846` | [arXiv](https://arxiv.org/abs/2511.06846)

> 任意形状剛体コライダとの微分可能衝突処理でMPMを拡張。非平面境界条件下での物性推定を実現。

### Jiang2025_PhysTwin

**PhysTwin: Physics-Informed Reconstruction and Simulation of Deformable Objects from Videos**
Hanxiao Jiang et al. — ICCV, 2025
arXiv: `2503.17973` | [arXiv](https://arxiv.org/abs/2503.17973)

> スパースRGB-Dビデオからspring-mass＋Gaussianスプラットでre-simulation可能なデジタルツインを構築。

### Chen2025_Vid2Sim

**Vid2Sim: Generalizable, Video-based Reconstruction of Appearance, Geometry and Physics for Mesh-free Simulation**
Chuhao Chen et al. — CVPR, 2025
arXiv: `2506.06440` | [arXiv](https://arxiv.org/abs/2506.06440)

> VideoMAEベースのフィードフォワード物性予測＋Neural JacobianによるReduced-Order精緻化で汎化的復元。

### Chen2026_EMPM

**EMPM: Embodied MPM for Modeling and Simulation of Deformable Objects**
Yunuo Chen et al. — RA-L, 2025
arXiv: `2601.17251` | [arXiv](https://arxiv.org/abs/2601.17251)

> 微分可能MPM＋3DGS統合で破壊・伸長・圧縮を含むelastoplastic挙動のモデリングと操作。

### Zhu2024_latentIntuitive

**Latent Intuitive Physics: Learning to Transfer Hidden Physics from A 3D Video**
Xiangming Zhu et al. — ICLR, 2024
arXiv: `2406.12769` | [arXiv](https://arxiv.org/abs/2406.12769)

> 確率的潜在特徴として流体物性を推論し新規シーンに転移。明示的パラメータ推定なしの適応。

### NVIDIA2025_VoMP

**VoMP: Predicting Volumetric Mechanical Property Fields for Any 3D Asset**
NVIDIA et al. — arXiv, 2025
arXiv: `2510.22975` | [arXiv](https://arxiv.org/abs/2510.22975)

> Geometry Transformerでper-voxelのE, ν, 密度をフィードフォワード予測。表現非依存の初のvolumetric物性予測。

### Fan2025_PhysWorld

**PhysWorld: From Real Videos to World Models of Deformable Objects via Physics-Aware Demonstration Synthesis**
Yu Yang et al. — arXiv, 2025
arXiv: `2510.21447` | [arXiv](https://arxiv.org/abs/2510.21447)

> MPMデジタルツインから合成データ生成→GNN世界モデル学習で47倍高速推論。シミュレータ→データ→モデル戦略。

### Li2022_DiffCloth

**DiffCloth: Differentiable Cloth Simulation with Dry Frictional Contact**
Yifei Li et al. — ACM ToG, 2022
DOI: `10.1145/3527660` | arXiv: `2106.05306`

> Projective DynamicsのSignorini-Coulomb摩擦拡張で接触リッチな布の微分可能シミュレーション。

### Zheng2024_DiffCP

**Differentiable Cloth Parameter Identification and State Estimation in Manipulation**
Dongzhe Zheng et al. — RA-L, 2024
DOI: `10.1109/LRA.2024.3357039` | arXiv: `2311.05141`

> 異方性弾塑性MPMによるreal-to-sim-to-real布パラメータ同定と状態推定。

### Sundaresan2022_DiffCloud

**DiffCloud: Real-to-Sim from Point Clouds with Differentiable Simulation and Rendering of Deformable Objects**
Priya Sundaresan et al. — IROS, 2022
DOI: `10.1109/IROS47612.2022.9981101` | arXiv: `2204.03139`

> 微分可能FEM＋微分可能点群レンダリングで実点群からオンザフライのシミュレーションパラメータ推定（約10分）。

### Antonova2022_BayesianReal2Sim

**A Bayesian Treatment of Real-to-Sim for Deformable Object Manipulation**
Rika Antonova et al. — RA-L, 2022
DOI: `10.1109/LRA.2022.3153856` | arXiv: `2112.05068`

> RKHS-Netでキーポイントを分布埋め込みとしてエンコードし、柔軟物の弾性・摩擦のBayes事後推定。

### Liu2022_DiffRope

**Differentiable Robotic Manipulation of Deformable Rope-like Objects Using Compliant Position-based Dynamics**
Fei Liu et al. — RA-L, 2022
DOI: `10.1109/LRA.2023.3264766` | arXiv: `2202.09714`

> 微分可能XPBDによるロープ剛性パラメータ同定と形状制御。Baxter/da Vinciロボットで検証。

### Gong2024_BayesianCloth

**Bayesian Differentiable Physics for Cloth Digitalization**
Deshan Gong et al. — CVPR, 2024
arXiv: `2402.17664` | [arXiv](https://arxiv.org/abs/2402.17664)

> 変分Bayes推論で布のper-element不均一物性を少数ドレープテスト画像から学習。

### Ru2025_FabricReal2Sim

**Can Real-to-Sim Approaches Capture Dynamic Fabric Behavior for Robotic Fabric Manipulation?**
Yingdong Ru et al. — IROS, 2025
DOI: `10.1109/IROS60139.2025.11245811`
arXiv: `2503.16310` | [arXiv](https://arxiv.org/abs/2503.16310)

> 4つのreal-to-sim手法を比較し、未見動的タスクへの汎化失敗を系統的に実証。PINNベース手法を新規提案。

### Yoon2025_ClothJCDE

**Real-to-Sim High-Resolution Cloth Modeling: Physical Parameter Optimization Using Particle-Based Simulation with Robot Manipulation Data**
Kang-il Yoon, Soo-Chul Lim — JCDE, 2025
DOI: `10.1093/jcde/qwaf065` | [DOI](https://doi.org/10.1093/jcde/qwaf065)

> Bayes最適化＋勾配降下ハイブリッドで布パラメータを最適化。複数布種類・タスクに汎化。

### Chen2025_DER

**Accurate Simulation and Parameter Identification of Deformable Linear Objects using Discrete Elastic Rods in Generalized Coordinates**
Qi Jing Chen et al. — IROS, 2025
DOI: `10.1109/IROS60139.2025.11247160` | arXiv: `2310.00911`

> DERモデルのMuJoCo統合と曲げ・ねじり剛性の勾配ベース同定。ゼロショットsim-to-realワイヤフリング。

### Kawaharazuka2022_VarStiffCloth

**Dynamic Cloth Manipulation Considering Variable Stiffness and Material Change Using Deep Predictive Model With Parametric Bias**
Kento Kawaharazuka et al. — Frontiers in Neurorobotics, 2022
DOI: `10.3389/fnbot.2022.890695` | [DOI](https://doi.org/10.3389/fnbot.2022.890695)

> パラメトリックバイアスLSTMで布材料特性をオンライン同定し、可変剛性筋骨格ロボットの動的布操作に適応。

### Patni2024_elasticity

**Online Elasticity Estimation and Material Sorting Using Standard Robot Grippers**
Shubhan P. Patni et al. — IJAMT, 2024
DOI: `10.1007/s00170-024-13678-6` | arXiv: `2401.08298`

> 標準並行爪グリッパによる繰り返し圧縮＋Hunt-Crossleyモデルで相対的弾性判別とソーティング。

### Burgess2024_youngs

**Learning Object Compliance via Young's Modulus from Single Grasps with Camera-Based Tactile Sensors**
Michael Burgess et al. — arXiv, 2024
arXiv: `2406.15304` | [arXiv](https://arxiv.org/abs/2406.15304)

> GelSight触覚＋ハイブリッドモデルで単一把持から10桁レンジのYoung's modulus推定。

### Yao2023_vsf

**Estimating Tactile Models of Heterogeneous Deformable Objects in Real Time**
Shaoxiong Yao, Kris Hauser — ICRA, 2023
DOI: `10.1109/ICRA48891.2023.10160731` | [PDF](https://motion.cs.illinois.edu/papers/ICRA2023_Yao_VolumeStiffnessField.pdf)

> Volumetric Stiffness Fieldによる不均一柔軟物の空間的力応答のリアルタイム学習。

### Kutsuzawa2024_stiffness

**Learning-based Object Stiffness and Shape Estimation with Confidence Level in Multi-Fingered Hand Grasping**
Gaku Kutsuzawa et al. — Frontiers in Neurorobotics, 2024
DOI: `10.3389/fnbot.2024.1466630` | [DOI](https://doi.org/10.3389/fnbot.2024.1466630)

> 多指ハンド固有受容感覚のみから剛性・形状を不確実性付き同時推定。確率的推論フレームワーク。

### Chen2025_diffprop

**Learning Object Properties Using Robot Proprioception via Differentiable Robot-Object Interaction**
Peter Yichen Chen et al. — ICRA, 2025
arXiv: `2410.03920` | [arXiv](https://arxiv.org/abs/2410.03920)

> 微分可能ロボット-物体シミュレーションで関節エンコーダのみから質量・弾性率を逆同定。

### Sanchez2020_BlindFEM

**Blind Manipulation of Deformable Objects Based on Force Sensing and Finite Element Modeling**
Jesus Sanchez et al. — Frontiers in Robotics and AI, 2020
DOI: `10.3389/frobt.2020.00073` | [DOI](https://doi.org/10.3389/frobt.2020.00073)

> F/Tセンサ＋四面体FEMのみで視覚なしに柔軟物の変形推定と制御を実証。

### Yang2025_dpsi

**Differentiable Physics-based System Identification for Robotic Manipulation of Elastoplastic Materials**
Xintong Yang et al. — IJRR, 2025
DOI: `10.1177/02783649251334661` | arXiv: `2411.00554`

> 微分可能MPMで単一ロボットインタラクションからelastoplastic物性6パラメータを同定→長期操作計画。唯一の完全パイプライン。

### Zhang2024_adaptigraph

**AdaptiGraph: Material-Adaptive Graph-Based Neural Dynamics for Robotic Manipulation**
Kaifeng Zhang et al. — RSS, 2024
arXiv: `2407.07889` | [arXiv](https://arxiv.org/abs/2407.07889)

> 物性条件付きGNNで4材料カテゴリにわたる動力学予測。テスト時few-shot逆最適化で未知物体に適応。

### Ai2024_robopack

**RoboPack: Learning Tactile-Informed Dynamics Models for Dense Packing**
Bo Ai et al. — RSS, 2024
arXiv: `2407.01418` | [arXiv](https://arxiv.org/abs/2407.01418)

> Soft-Bubble触覚履歴からのlatent物理推定＋recurrent GNNで遮蔽下の密パッキング。

### Shi2022_RoboCraft

**RoboCraft: Learning to See, Simulate, and Shape Elasto-Plastic Objects with Graph Networks**
Haochen Shi et al. — RSS 2022 / IJRR, 2024
DOI: `10.1177/02783649231219020` | arXiv: `2205.02909`

> RGB-Dから粒子分布ベースGNN動力学学習。10分の実データでdough整形操作。

### Wu2026_rapid

**Rapid Adaptation of Particle Dynamics for Generalized Deformable Object Mobile Manipulation**
Bohan Wu et al. — arXiv, 2026
arXiv: `2603.18246` | [arXiv](https://arxiv.org/abs/2603.18246)

> RMAフレームワークの柔軟物拡張。特権的粒子埋め込みを視覚アダプタに蒸留し80%超の実機成功率。

### Qiao2020_diffsim

**Scalable Differentiable Physics for Learning and Control**
Yi-Ling Qiao et al. — ICML, 2020
DOI: `10.5555/3524938.3525665` | arXiv: `2007.02168`

> メッシュベース微分可能物理。局所化衝突処理で粒子ベースの2桁のメモリ・計算削減。

### Huang2021_PlasticineLab

**PlasticineLab: A Soft-Body Manipulation Benchmark with Differentiable Physics**
Zhiao Huang et al. — ICLR, 2021 (Spotlight)
arXiv: `2104.03311` | [arXiv](https://arxiv.org/abs/2104.03311)

> DiffTaiChiベースMPM上の弾塑性操作ベンチマーク。RLと勾配ベース最適化の体系的比較を提供。

### Heiden2021_DiSECt

**DiSECt: A Differentiable Simulation Engine for Autonomous Robotic Cutting**
Eric Heiden et al. — RSS, 2021 (Best Student Paper)
DOI: `10.15607/RSS.2021.XVII.067` | arXiv: `2105.12244`

> 仮想節点アルゴリズムで再メッシュ不要の微分可能切断シミュレーション。数百パラメータの勾配ベース推定。

### Si2024_difftactile

**DiffTactile: A Physics-based Differentiable Tactile Simulator for Contact-rich Robotic Manipulation**
Zilin Si et al. — ICLR, 2024
arXiv: `2403.08716` | [arXiv](https://arxiv.org/abs/2403.08716)

> FEM＋多材料＋ペナルティ接触の完全微分可能触覚シミュレータ。物性キャリブレーションとスキル学習を統合。

### Li2019_dpinet

**Learning Particle Dynamics for Manipulating Rigid Bodies, Deformable Objects, and Fluids**
Yunzhu Li et al. — ICLR, 2019
arXiv: `1810.01566` | [arXiv](https://arxiv.org/abs/1810.01566)

> 動的インタラクショングラフ＋階層的粒子構造のDPI-Nets。剛体・柔軟物・流体の統一粒子動力学学習。

### Millard2022_FEMParamEst

**Parameter Estimation for Deformable Objects in Robotic Manipulation Tasks**
David Millard et al. — ISRR 2022 / Springer SPAR vol. 27
DOI: `10.1007/978-3-031-25555-7_16`

> Collocation定式化によるFEMメッシュ上の材料パラメータ最適化。ロボット操作中のスパース点追跡から非破壊推定。
