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
