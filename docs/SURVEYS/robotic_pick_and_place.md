# Literature Survey: Robotic Pick-and-Place — Grasping and Stable Object Placement

| | |
|---|---|
| **Date** | 2026-04-06 |
| **Scope** | 物体の把持と安定配置（pick-and-place）を直接研究した論文、およびpick-and-placeをデモタスクとして使用したロボット工学・ロボット学習の文献。2020年以降のトップ会議・ジャーナル対象。 |
| **Papers found** | 48 |

## Research Landscape Overview

ロボットによる物体の把持と安定配置（pick-and-place）は、ロボット操作研究における最も基本的かつ重要なタスクの一つである。2020年以降、この分野は3つの大きな潮流によって急速に発展してきた。第一に、Transporter Networks (Zeng et al., 2020) に端を発する空間変位ベースの操作表現が、言語条件付き操作（CLIPort）やSE(3)等変表現（R-NDF, TAX-Pose）へと発展し、少数のデモンストレーションから新規物体への汎化を可能にした。第二に、拡散モデルの操作分野への導入（Diffusion Policy, 2023）により、多峰性のある行動分布の表現が可能となり、RPDiffやStructDiffusionに代表される関係的再配置手法が花開いた。第三に、大規模Vision-Language-Action (VLA) モデル（RT-1/RT-2, OpenVLA, pi0）が登場し、Webスケールの知識をロボット制御に転移する基盤モデルパラダイムが確立された。

安定配置そのものを直接研究する論文群は、これらの主流と比較して規模は小さいが着実に進展している。Paxton et al. (2021) による意味的配置予測から始まり、6-DoFusion (2023) による拡散モデルベースの安定ポーズ生成、Nadeau & Kelly (2025) による接触点ロバスト性に基づく配置計画、そしてNadeau et al. (2025) の物理誘導拡散モデルへと至る系譜は、「配置安定性」を明示的に扱う研究の重要性を示している。主要な研究拠点として、MIT (SimPLE, R-NDF, RPDiff)、Washington大学/NVIDIA (Transporter, CLIPort, StructFormer, CabiNet)、Google DeepMind (RT-1/RT-2, SayCan, Beyond Pick-and-Place)、Toronto大学 (Nadeau, AnyPlace)、Physical Intelligence (pi0) が挙げられる。対象ベニューはCoRL、RSS、ICRA、IROS、NeurIPS、ICLR、T-RO、RA-L、Science Roboticsと広範にわたる。

## Survey Findings

### Thesis

本サーベイが明らかにする分野の根本的未解決問題は、**汎化性・配置精度・物理的安定性の三要素を同時に満たすpick-and-placeシステムの実現**である。VLA系の汎化的アプローチ（RT-2, OpenVLA, pi0）はWebスケールの意味的知識を活用して多様なタスクに対応するが、配置精度はサブミリメートルに到達せず、物理的安定性の明示的保証を欠く。精密配置系（SimPLE, Pick2Place）はミリメートル以下の精度を達成するが、物体CADモデルやタスク固有のデータを必要とし、汎化が困難である。安定配置予測系（Paxton et al., 6-DoFusion, Nadeau et al.）は物理的根拠に基づく安定性推論を試みるが、センサノイズ、未知の慣性パラメータ、閉ループ制御との統合が課題として残る。

この三者間の緊張は、根本的にはロボット操作の表現学習問題に帰着する。意味的理解（「何をどこに置くか」）と物理的推論（「どう置けば安定するか」）、そして行動の精緻さ（「どの精度で置くか」）を統一的に表現・学習する枠組みの不在が、分野全体の進展を律速している。

### Foundation

本サーベイで調査した論文群が依拠する共通技術基盤は以下の5つに集約される。

1. **点群ベースの物体・環境表現**: Category A〜Cの論文のほぼ全てが、RGB-D画像から得られる点群を基本入力として採用している。Transporter Networksの俯瞰画像ベース表現を除き、R-NDF, RPDiff, AnyPlace, UOP-Net, TAX-Pose, NeRPなど、3D点群上の幾何推論が配置・再配置手法の共通基盤を形成している。例外はRT-1/RT-2やpi0のようなVLA系であり、これらはRGB画像のみで動作する。

2. **拡散モデルによるSE(3)ポーズ生成**: 2023年以降、拡散モデルがpick-and-place分野の支配的な生成手法となった。Diffusion Policy (行動系列の生成)、RPDiff (関係的配置ポーズ)、StructDiffusion (構造生成)、6-DoFusion (安定配置ポーズ)、SE(3)-DiffusionFields (把持ポーズ+軌道)、Nadeau et al. 2025 (物理誘導配置) と、把持から配置、行動計画まで拡散モデルが浸透している。

3. **SE(3)等変アーキテクチャ**: R-NDF, TAX-Pose, Eisner et al. (2024) が示すように、SE(3)等変性を持つニューラルネットワークは、少数のデモンストレーションからの配置タスクの汎化に不可欠な帰納的バイアスを提供する。この系譜は理論的保証と実用的精度の両立を目指す。

4. **シミュレーションベースの訓練とsim-to-real転移**: SimPLE (Science Robotics), CabiNet, UOP-Net, Paxton et al., NeRPなど、多くの配置系論文がシミュレーションで訓練しゼロショットで実世界に転移する戦略を採用している。VLA系もOpen X-Embodimentのような大規模実ロボットデータに加え、SIMPLERのようなシミュレーション評価環境を活用している。

5. **Transporterスタイルの空間変位表現**: Transporter Networks (2020) が導入した「深層特徴の空間変位による行動表現」は、CLIPort, StructFormerへと受け継がれ、pick-and-placeタスクにおける空間的帰納バイアスの有効性を実証した。ただし、この表現は本質的にSE(2)に制限されるため、6-DoF操作への拡張にはRPDiffやTAX-Poseのような異なるアプローチが必要となった。

### Progress

pick-and-placeおよび安定配置の研究は、2020年以降に以下の主要な能力遷移を経てきた。

1. **空間変位ベースのpick-and-placeの確立 (2020)**: Transporter Networksが、深層特徴の空間変位（クロス相関）によるpick-and-place行動表現を確立した。1-10回のデモンストレーションで10種類のタスクに汎化し、従来のend-to-end強化学習が必要とした100-1000倍のデータ効率を達成した。

2. **言語条件付き操作と意味的配置の実現 (2021)**: CLIPortがCLIPの意味的特徴とTransporterの空間的精度を統合し、言語指示による多タスクpick-and-placeを可能にした。同時期にPaxton et al.が物理的妥当性と意味的関係を結合した安定配置予測を提案し、Contact-GraspNetがポイントクラウドベースの効率的6-DoFグラスプ検出を確立した。

3. **SE(3)等変表現による少数ショット関係的再配置 (2022)**: R-NDFとTAX-Poseが、5-10回のデモンストレーションで新規物体間の関係的再配置（棚への配置、フックへの吊り下げ等）を実現した。ReorientBotは配置のための物体再方向づけ問題を定式化し、学習ベースのウェイポイント選択と古典的動作計画の組み合わせで解決した。

4. **拡散モデルの操作分野への浸透 (2023)**: Diffusion Policyが行動拡散による汎用的visuomotorポリシー学習を確立し、先行手法に対し平均46.9%の改善を達成した。RPDiffが反復的ポーズデノイジングにより多峰性のある関係的再配置を実現し、StructDiffusionが言語指示からの物理的に妥当な構造生成を可能にした。SE(3)-DiffusionFieldsが把持と軌道の同時最適化を拡散モデルで統合した。

5. **基盤モデルパラダイムの確立とpick-and-placeの精密化 (2024)**: OpenVLA, pi0, Octoなどの汎化的VLAが登場し、数百万のロボットエピソードから事前学習された基盤モデルがpick-and-placeを含む多様なタスクで高い汎化性を示した。同時に、SimPLEが視触覚フィードバックにより1mm以下の精度を達成し（Science Robotics）、Eisner et al.がSE(3)等変幾何推論による精密配置を少数ショットで実現した。

6. **物理誘導型配置生成の登場 (2025)**: Nadeau et al.が拡散モデルに微分可能な静的ロバスト性損失を合成し、物理シミュレーションなしで安定配置を生成する手法を提案した。AnyPlaceがVLMとローカルポーズ予測の2段階手法で、挿入・スタッキング・吊り下げなど多様な配置モードへの汎化を実現した。

### Gap

1. **Grasp-Placement Coupling**

多くの手法が把持選択と配置計画を独立に扱うが、Category Bが示すように、把持の選択は実現可能な配置ポーズを根本的に制約する。SimPLEは把持からの全パイプラインを統合するがCADモデルを必要とし、Pick2Placeは配置アフォーダンスから把持への微分可能なマッピングを提案するがNeRFの再構成時間が律速となる。Shanthi et al. (2024) は「joint pick-and-place planning」がsequentialアプローチに対し厳密に優位であることを実証したが、この知見はVLA系やrearrangement系の手法に統合されていない。把持-配置の結合を任意の物体・環境で効率的に実現できれば、実世界のcluttered環境におけるpick-and-place成功率が大幅に向上する。

2. **Physical Grounding of Placement Stability**

Category Dの基盤モデル（RT-2, OpenVLA, pi0）は意味的汎化に優れるが、配置安定性の物理的保証を一切持たない。一方、Category Aの物理ベース手法（Nadeau & Kelly, Li et al.）は安定性を明示的に推論するが、既知の物体形状・慣性パラメータを前提とする。6-DoFusionとNadeau et al. (2025) の物理誘導拡散モデルはこのギャップを埋め始めているが、6-DoFusionはground-truth SDFをシミュレーションから取得しておりノイズを含む推定SDFでの動作は未検証、Nadeau & KellyはCAD形状と一律密度仮定に依存しておりノイズを含む推定慣性パラメータでの感度分析は未実施である。物理的安定性の推論を、センサデータからの形状推定を含む汎化的な知覚パイプラインと統合できれば、VLAベースのシステムでも安定した配置が保証可能になる。

3. **Closed-Loop Placement with Tactile Feedback**

Category Aの触覚ベース論文（Ota et al., Takahashi et al.）は配置時の触覚フィードバックの有効性を実証したが、いずれも限定的な実験設定（既知物体、単一スタッキング）にとどまる。SimPLEは触覚ポーズ推定を統合するが配置自体はオープンループである。RPDiff, StructDiffusion, AnyPlaceを含むrearrangement系の手法は全てオープンループ実行であり、配置時の接触フィードバックを活用しない。閉ループ配置制御を汎化的な配置計画と統合できれば、接触不確実性下での配置ロバスト性が大幅に改善される。

4. **Generalization to Novel Objects with Unknown Physical Properties**

Category Aの多くの手法が既知の物体モデルを前提とするが、要求される事前知識の種類と、それを推定するために必要な技術領域・センサモダリティが異なる。6-DoFusionはground-truth SDFを前提とし、その推定には視覚センサに基づく光学・コンピュータビジョン・ニューラル暗黙表現（VolSDF, NeuS等）の技術が必要となるが、ノイズを含む推定SDFでの動作ロバスト性は未検証である。Nadeau & KellyはCAD形状に加え慣性パラメータ（質量分布・摩擦係数）を必要とし、実験では一律の密度仮定（415 kg/m³）で代用している。慣性パラメータの推定には力覚センサに基づく動力学モデリング・パラメータ回帰等の技術が必要となるが、ノイズを含む推定慣性パラメータでの感度分析は未実施である。SPOTSはreal-to-simシーン再構成にCADモデルを要する。いずれの手法もアーキテクチャ上は推定値への置換が原理的に可能だが、推定誤差に対するロバスト性の検証が欠如している点で共通する。学習ベース手法（UOP-Net, AnyPlace）は慣性パラメータを明示的に入力せず安定配置を予測するが、訓練データの生成において物理特性（密度・摩擦・重心位置）のランダマイズは報告されておらず、均一密度のシミュレーションで安定性ラベルを生成している可能性が高い。すなわち、これらの手法が暗黙に汎化を期待できるのは多様な幾何重心に対してであり、幾何重心と質量重心が乖離する物体（内部に偏った重りを持つ箱、液体が片側に溜まった容器、素材が不均一な複合物体等）への対応は根拠がない。物理ベース手法（Nadeau & Kelly, 6-DoFusion）はこれらのパラメータを明示的に利用するが、推定値での検証は未実施である。幾何重心と質量重心の乖離を含む未知の物理特性を持つ物体に対する安定配置の予測は、いずれのアプローチにおいても未達成であり、物流・家庭環境での実用化における共通の課題である。

5. **Long-Horizon Multi-Step Rearrangement with Stable Intermediate Placements**

Category Cのrearrangement手法は配置精度よりもタスク完遂率に焦点を当て、中間配置の安定性を明示的に検証しない。Category Fの計画手法（LLM-TAMP, LGMCTS）はhigh-levelな配置計画を提供するがlow-levelの安定性を保証しない。ManiSkill-HABが指摘するように、長期的なスキル連鎖における安定した中間配置の確保は、現在のロボット学習手法の主要な課題であり続けている。安定配置の検証をrearrangement計画ループに統合できれば、より信頼性の高い長期操作が可能になる。

## Paper Catalogue

### Category Overview

本サーベイでは48本の論文を6つのカテゴリに分類した。Category A（安定配置予測）は配置の物理的安定性を直接扱う論文群であり、本サーベイの中核を成す。Category B（統合Pick-and-Place）は把持と配置を密結合したシステムを扱い、Transporter NetworksからSimPLEに至る系譜を含む。Category C（関係的物体再配置）はpick-and-placeを基本操作として学習ベースの再配置を行う論文群であり、SE(3)等変手法と拡散モデルが主要なアプローチである。Category D（汎化的ロボットポリシー）はpick-and-placeをデモタスクとして使用した基盤モデル・VLAを収録する。Category E（把持計画・知覚）は配置を間接的に支える把持検出と統合的把持-動作計画を扱う。Category F（タスク計画）は言語誘導型の配置計画およびベンチマークを扱う。

| Category | Description | Count |
|----------|-------------|-------|
| A — Stable Placement Prediction | 安定配置の予測・計画を直接研究 | 11 |
| B — Integrated Pick-and-Place | 把持と配置の統合システム・ポリシー | 9 |
| C — Relational Object Rearrangement | pick-and-placeを基本操作とする再配置 | 10 |
| D — Generalist Robot Policies | pick-and-placeをデモタスクとして使用した基盤モデル | 8 |
| E — SE(3) Grasp & Motion Optimization | 把持検出・把持-動作統合計画 | 5 |
| F — Task Planning & Benchmarks | 言語誘導型配置計画・ベンチマーク | 5 |

### Foundational Works

| # | Paper | Year | Venue | Significance |
|---|-------|------|-------|-------------|
| B1 | Transporter Networks | 2020 | CoRL | 空間変位ベースのpick-and-place表現を確立。1-shotデモンストレーションでの汎化を実現し、後続のCLIPort, StructFormerの基盤となった |
| B2 | CLIPort | 2021 | CoRL | CLIP意味特徴とTransporter空間精度を統合し、言語条件付きpick-and-placeを確立 |
| E1 | Contact-GraspNet | 2021 | ICRA | ポイントクラウドベースの効率的6-DoFグラスプ生成を確立。後続の把持-配置統合手法の基盤 |
| D2 | Diffusion Policy | 2023 | RSS | 行動拡散による汎用visuomotorポリシー学習を確立。操作分野への拡散モデル導入の画期的論文 |
| D4 | RT-1 | 2022 | RSS | 大規模実ロボットデータによるTransformerポリシーの汎化を実証。VLAパラダイムの先駆 |

### A — Stable Placement Prediction

安定配置を直接研究する論文群。物理的安定性の予測（Paxton, 6-DoFusion, Nadeau）、触覚フィードバックによる配置制御（Ota, Takahashi）、微分可能接触力学（Li）、汎化的配置学習（AnyPlace, UOP-Net, Eisner）という4つのアプローチが存在する。

1. [[Paxton2021_stable_placement]](../REFERENCES/MAIN.md#Paxton2021_stable_placement) — Chris Paxton, Christopher Xie, Tucker Hermans, Dieter Fox, "Predicting Stable Configurations for Semantic Placement of Novel Objects" (2021)
   - **DOI**: arXiv:2108.12062 (CoRL 2021)
   - **thesis**: 新規物体の信頼性ある意味的配置には、物理的妥当性と学習された意味的関係の同時推論が必要であり、関係分類器のみでは不十分
   - **core**: シーン弁別器（物理的リアリズム判定）と関係述語分類器（意味的適切性判定）の2つの学習済みコンポーネントをサンプリングベース計画に統合。シミュレーションのみで訓練しゼロショットで実世界に転移
   - **diff**: 先行する関係予測研究はロボット計画・制御との統合なし。先行配置予測手法は完全な物体知識を前提とするか、安定性最大化のみを目的としており汎化に乏しい。学習弁別器とサンプリングベース計画の結合により、RGB-Dのみから未知物体の意味的配置を実現
   - **limit**: (1) 不完全な物体形状知覚による交差型配置エラー。(2) 遮蔽ベースの意味的述語の分類精度が低い。(3) 実世界での最大の失敗要因は配置計画ではなく把持

2. [[Eisner2024_se3_equivariant_placement]](../REFERENCES/MAIN.md#Eisner2024_se3_equivariant_placement) — Ben Eisner, Yi Yang, Todor Davchev, Mel Vecerik, Jonathan Scholz, David Held, "Deep SE(3)-Equivariant Geometric Reasoning for Precise Placement Tasks" (2024)
   - **DOI**: arXiv:2404.13478 (ICLR 2024)
   - **thesis**: 精密な相対配置は、SE(3)不変なタスク表現とSE(3)等変な幾何推論層への分解により、少数デモンストレーションから理論的保証と高精度の両方を達成できる
   - **core**: SE(3)不変表現の学習（クロスオブジェクト点対応）と、証明可能なSE(3)等変性を持つ微分可能マルチラテレーション層による距離からポーズへの変換の2段階アーキテクチャ
   - **diff**: NDF (Vector Neurons) は等変性は証明可能だが実用性能が劣る。TAX-Poseは高い実用性能を達成するが等変性はデータ拡張による近似。本手法は両方を同時に達成
   - **limit**: (1) 対称物体や多峰性配置タスクに対応不可（単一ポーズのみ予測）。(2) タスクに関連する2物体のセグメンテーションが前提

3. [[Ota2024_tactile_contact_patch]](../REFERENCES/MAIN.md#Ota2024_tactile_contact_patch) — Keita Ota, Devesh K. Jha, Krishna Murthy Jatavallabhula, Asako Kanezaki, Joshua B. Tenenbaum, "Tactile Estimation of Extrinsic Contact Patch for Stable Placement" (2024)
   - **DOI**: 10.1109/ICRA57147.2024.10611504
   - **thesis**: 配置安定性は触覚読み取りのみから外因性接触パッチを推定することで推論可能であり、既知形状なしで複雑形状物体のスタッキングに閉ループフィードバックを提供できる
   - **core**: 複合触覚信号（グリッパー-物体間の内因性接触と物体-環境間の外因性接触）を分離して外因性接触パッチを推定し、確率的フィルタリングによるフィードバックベースのスタッキング
   - **diff**: 先行スタッキング研究はオープンループ制御と既知形状を前提。Neural Contact Fields (NCF) はシミュレーション限定。本手法は形状仮定なしで実世界の複雑形状物体に対応
   - **limit**: (1) 剛体・平面を持つ物体に限定。(2) 複数物体上へのスタッキング時に性能低下（約60%成功率）

4. [[Zhao2025_anyplace]](../REFERENCES/MAIN.md#Zhao2025_anyplace) — Yuchi Zhao, Miroslav Bogdanovic, Chen Luo, Steven Tohme, Kourosh Darvish, Alan Aspuru-Guzik, Florian Shkurti, Animesh Garg, "AnyPlace: Learning Generalized Object Placement for Robot Manipulation" (2025)
   - **DOI**: arXiv:2502.04531
   - **thesis**: 多様な配置モード（挿入、スタッキング、吊り下げ）への汎化的物体配置は、VLMによる高レベル位置提案と合成データで訓練されたローカルポーズ予測の2段階分離により達成可能
   - **core**: (1) VLM (Molmo) による配置位置と配置モードの特定、(2) ランダム生成物体で訓練されたローカル配置ポーズ予測モデルによる精密SE(3)ポーズ予測
   - **diff**: 少数ショット等変手法（NDF, TAX-Pose, Eisner）はタスク間汎化に乏しく単一モード予測。RPDiffはシナリオごとに別モデルを訓練。AnyPlaceはVLM誘導分解により単一モデルで多モード対応を実現
   - **limit**: (1) 全ての安定把持が目標配置ポーズを実現できるわけではなく、実機でのリジェクションサンプリングが困難。(2) 不完全な点群データにより高精度配置が困難。(3) ローカルポーズ予測モデルに言語条件付けがなく、同一位置での異なる配置タイプを区別不可。(4) 訓練データ生成時の物理特性（密度・摩擦・重心位置）のランダマイズは報告されておらず、幾何形状のランダマイズのみ実施。均一密度を暗黙に仮定している可能性が高く、幾何重心と質量重心が乖離する物体への汎化は根拠がない

5. [[Noh2024_unseen_placement]](../REFERENCES/MAIN.md#Noh2024_unseen_placement) — Sangjun Noh, Raeyoung Kang, Taewon Kim, Seunghyeok Back, Seungbum Bak, Kyoobin Lee, "Learning to Place Unseen Objects Stably using Large-Scale Simulation" (2024)
   - **DOI**: 10.1109/LRA.2024.3360810
   - **thesis**: 未知物体の安定配置は、形状補完を介さず部分点群から最安定面を直接検出するセグメンテーションベースネットワークにより達成可能
   - **core**: UOP-Sim（多様な形状に対応する大規模合成データセット）とUOP-Net（単一視点部分点群から最安定面を直接検出する点群セグメンテーションネットワーク）
   - **diff**: 解析的手法は完全3Dモデルと重心計算が必要。形状補完アプローチは不正確な復元による誤差が生じる。UOP-Netは中間的な形状補完なしで部分観測から安定面を直接予測
   - **limit**: (1) 球形物体、極小物体、深度値が小さい物体を除外。(2) 完全観測シナリオでは効果が低下するが、実環境での完全観測は非現実的。(3) 訓練データ（UOP-Sim）生成時の物理特性（密度・摩擦・重心位置）のランダマイズは報告されておらず、幾何形状のランダマイズのみ実施。均一密度を暗黙に仮定している可能性が高く、幾何重心と質量重心が乖離する物体への汎化は根拠がない

6. [[Nadeau2025_contact_robustness]](../REFERENCES/MAIN.md#Nadeau2025_contact_robustness) — Philippe Nadeau, Jonathan Kelly, "Stable Object Placement Planning From Contact Point Robustness" (2025)
   - **DOI**: 10.1109/TRO.2025.3577049
   - **thesis**: 安定配置計画は従来の「サンプル→評価」パラダイムを反転し、接触点を先に選択してからその接触点を誘発する配置ポーズを決定すべきであり、これにより物理的に根拠のある計画が高速化・汎化される
   - **core**: 接触点先行計画アルゴリズムと、慣性パラメータ（質量分布、摩擦）を取り入れた第一原理から導出された安定性ヒューリスティック。錐摩擦近似による静的ロバスト性評価
   - **diff**: 従来手法はポーズをサンプリングしてから安定性を評価（計算コスト大）。学習ベース手法（Paxton等）はタスク間汎化が困難。物理シミュレータは計画には遅すぎる。本手法はパイプラインを反転し、アブレーションに対し約20倍の高速化を達成
   - **limit**: (1) 物体形状はCADモデル、慣性パラメータは一律の密度仮定（実験では415 kg/m³）として与えており、推定モジュールは含まない。アーキテクチャ上は推定値への置換が可能だが、ノイズを含む推定慣性パラメータに対する感度分析・ロバスト性検証は未実施。(2) ピラミッド型摩擦錐近似を使用し、多物体アセンブリでは不正確な場合がある。(3) 複数の特徴ペアマッチング時にランダム選択を行い、最適構成を見逃す可能性

7. [[Lee2024_spots]](../REFERENCES/MAIN.md#Lee2024_spots) — Joonhyung Lee, Sangbeom Park, Jeongeun Park, Kyungjae Lee, Sungjoon Choi, "SPOTS: Stable Placement of Objects with Reasoning in Semi-Autonomous Teleoperation Systems" (2024)
   - **DOI**: 10.1109/ICRA57147.2024.10611613
   - **thesis**: テレオペレーションにおける効果的な物体配置には、real-to-sim物理シミュレーションによる安定性検証とLLMによる意味的推論の両方が必要
   - **core**: (1) real-to-sim物理シミュレーションによる安定性検証モジュール、(2) LLMによるユーザー嗜好・シーン文脈を考慮した受容器推論モジュール。両者の結合確率分布を配置候補に対して計算
   - **diff**: 先行テレオペレーション研究は運動学的デモンストレーションが必要（Losey等）。既存のLLMベースロボティクスはLLMをタスク計画やポリシー生成に使用するが空間的配置推論には使用していない。SPOTSは物理検証と意味的推論を分離
   - **limit**: (1) 正確なopen-vocabulary物体検出モデルとシーン内物体の上位集合の事前知識が必要。(2) real-to-simシーン再構築にCADモデルが必要。(3) リアルタイム柔軟性と多様な状況での有効性に改善の余地

8. [[Yoneda2024_6dofusion]](../REFERENCES/MAIN.md#Yoneda2024_6dofusion) — Takuma Yoneda, Tianchong Jiang, Gregory Shakhnarovich, Matthew R. Walter, "6-DoFusion: 6-DoF Stability Field via Diffusion Models" (2024)
   - **DOI**: arXiv:2310.17649
   - **thesis**: 拡散モデルは文脈依存の安定6-DoFポーズ分布を学習可能であり、リジェクションサンプリング、安定性分類器、手動ヒューリスティックなしで安定配置を直接生成できる
   - **core**: SE(3)ポーズ上で動作する拡散モデルが、シーン物体のSDF条件付きで安定構成の学習分布から反復的にリファインメント。正例のみで訓練（不安定ラベル不要）
   - **diff**: 手動ヒューリスティックは汎化性に制限。リジェクションサンプリングは安定領域が小さい場合に非効率。StructDiffusionは局所的な妥当性に焦点を当てシーン全体の安定性や物体間相互作用を考慮しない。Paxton et al.は平面回転のみ。本手法は正例データのみから完全6-DoFの安定配置を生成
   - **limit**: (1) シーン内全物体のポーズとground-truth SDFを前提としており、実験はシミュレーション（MuJoCo）内のみ。アーキテクチャ上はSDFを条件入力として受け取るモジュラー設計のため、推定SDFへの置換は原理的に可能だが、ノイズを含む推定SDFや点群での動作ロバスト性は未検証。著者はRGBDからの推定への拡張を将来課題として挙げている

9. [[Takahashi2024_tactile_curl_diff]](../REFERENCES/MAIN.md#Takahashi2024_tactile_curl_diff) — Kuniyuki Takahashi, Shimpei Masuda, Tadahiro Taniguchi, "Stable Object Placing using Curl and Diff Features of Vision-based Tactile Sensors" (2024)
   - **DOI**: 10.1109/IROS58592.2024.10801674
   - **thesis**: GelSightのドット変位パターンから解析的に導出されるCurlとDiff特徴は、F/Tセンサの代替として訓練不要・キャリブレーション不要で配置時の補正回転方向を推定可能
   - **core**: GelSightドット変位からベクトル解析で計算される2つの特徴：Curl（回転場の大きさと方向→トルク方向推定）とDiff（左右指先の変位差）。学習なしで直接使用
   - **diff**: F/Tセンサはケーブル張力効果とセンサノイズに悩まされる。学習ベースの触覚アプローチは大量の訓練データが必要で分布外問題に脆弱。本手法は訓練不要・キャリブレーション不要で、特に小さな支持多角形を持つ物体でF/Tセンサを上回る
   - **limit**: (1) Joint物体（小支持多角形）で約2度の残留誤差。(2) センサ表面のクラックや製造差異に対するロバスト性は確認済みだが、センサ品質依存性は認識

10. [[Li2025_differentiable_contact]](../REFERENCES/MAIN.md#Li2025_differentiable_contact) — Linfeng Li, Gang Yang, Lin Shao, David Hsu, "Differentiable Contact Dynamics for Stable Object Placement Under Geometric Uncertainties" (2025)
    - **DOI**: 10.1109/LRA.2025.3641124
    - **thesis**: 微分可能な接触力学はF/Tセンサ読み取りと幾何パラメータの勾配関係を導出可能であり、勾配降下によるオンライン不確実性推定がパーティクルフィルタリングを上回る
    - **core**: 微分可能シミュレータ(Jade)内でF/Tセンサ読み取りの幾何パラメータに対する勾配を導出し、センサデータとモデル予測の不一致を勾配ベースで最小化。複数推定値の信念維持により初期化感度を緩和
    - **diff**: 先行微分可能剛体シミュレータは接触力の幾何パラメータに対する勾配を提供しなかった。学習ベース配置は制限的条件（平面・平行面）を前提。パーティクルフィルタリングは粒子枯渇で発散。本手法は統一的な勾配ベースアプローチ
    - **limit**: (1) 幾何的不確実性のみを考慮、センサ不正確性や制御不精度は未対応。(2) リアルタイム速度未達成（平均3.36秒/アクション）。(3) 接触特徴の幾何パラメータに対する導関数を手動で指定する必要

11. [[Nadeau2025_physics_diffusion]](../REFERENCES/MAIN.md#Nadeau2025_physics_diffusion) — Philippe Nadeau, Miguel Rogel, Ivan Bilic, Ivan Petrovic, Jonathan Kelly, "Generating Stable Placements via Physics-guided Diffusion Models" (2025)
    - **DOI**: arXiv:2509.21664
    - **thesis**: 学習された幾何aware事前分布と微分可能な物理ベースロバスト性損失をスコア合成することで、再訓練やファインチューニングなしにオフザシェルフ拡散モデルに安定性を統合可能
    - **core**: (1) オフライン計画器からの多峰性配置ラベルで訓練された拡散モデル（シーン・物体点群条件付き）と、(2) デノイジングステップごとに適用される微分可能な安定性aware損失関数のスコア合成
    - **diff**: 既存手法は安定性評価に動力学シミュレータ（計算コスト大）やヒューリスティックな外観ベース評価（物理的根拠なし）を使用。6-DoFusionやRPDiffは安定性や力平衡を明示的に考慮しない。Nadeau & Kelly (T-RO) はサンプル-評価型で低速。本手法は物理的事前知識を生成モデルに初めて統合し、56%頑健な配置を達成しつつ実行時間を47%短縮
    - **limit**: (1) 滑り・転がり効果や変動する質量分布を調査していない。(2) 点群はボリュームを記述不可で物体の実体性の学習を阻害。(3) ロバスト性ガイダンスの適用により一部シーンで貫通配置が増加。(4) 物体モデルの事前知識を前提。(5) メッシュや幾何プリミティブの使用で貫通ペナルティを改善可能

### B — Integrated Pick-and-Place

把持と配置を統合的に扱うシステム。Transporter NetworksとCLIPortが空間変位ベースの表現を確立し、SimPLEが精密pick-and-placeの新基準を打ち立てた。Pick2PlaceとShanthi et al.は把持-配置の結合計画の重要性を実証し、ReorientBotとCheng et al.は再把持・再方向づけによる配置実現を研究した。

1. [[Zeng2020_transporter]](../REFERENCES/MAIN.md#Zeng2020_transporter) — Andy Zeng, Pete Florence, Jonathan Tompson, Stefan Welker, Jonathan Chien, Maria Attarian, Travis Armstrong, Ivan Krasin, Dan Duong, Vikas Sindhwani, Johnny Lee, "Transporter Networks: Rearranging the Visual World for Robotic Manipulation" (2020)
   - **DOI**: arXiv:2010.14406 (CoRL 2020)
   - **thesis**: ロボット操作は端-端のモノリシックポリシーや物体中心のポーズ表現ではなく、深層特徴の空間変位推論により最も効果的に学習可能であり、桁違いのサンプル効率を達成する
   - **core**: 「transport」操作 — クエリ（pick）特徴マップとキー（place）特徴マップのクロス相関により深層特徴を明示的に再配置し、SE(2)空間変位を推論。行動空間上の回帰・分類を空間構造化密予測で置換
   - **diff**: 先行end-to-end visuomotor政策（form2fit, deep RL）はデータ効率が悪く、空間構造を活用しない。Transporter Networksは先行手法が100-1000倍のデモンストレーションを要するタスクで1-shot汎化を達成
   - **limit**: (1) カメラ-ロボットキャリブレーションに敏感。(2) トルク/力行動と空間行動空間の統合不可。(3) ステートレス（メモリなし）で非マルコフタスクに対応不可。(4) 変形物体に対する剛体変換バイアスの限界。(5) SE(3)拡張はSE(2)版に比べ1-shot汎化が低下

2. [[Shridhar2021_cliport]](../REFERENCES/MAIN.md#Shridhar2021_cliport) — Mohit Shridhar, Lucas Manuelli, Dieter Fox, "CLIPort: What and Where Pathways for Robotic Manipulation" (2021)
   - **DOI**: arXiv:2109.12098 (CoRL 2021)
   - **thesis**: 大規模視覚-言語モデル（CLIP）の意味的理解（"what"）とTransporter Networksの空間精度（"where"）の結合により、未知の意味概念に汎化しつつ精細な空間推論を維持する言語条件付き操作エージェントが実現可能
   - **core**: 意味的パスウェイ（CLIP特徴：言語根拠付き"what"情報）と空間パスウェイ（Transporterスタイルの密特徴transport："where"情報）の2ストリームアーキテクチャ
   - **diff**: Transporter Networksは空間精度を達成するが意味的に汎化不可。CLIPは意味的に汎化するが操作に必要な空間的根拠を欠く。CLIPortは両パスウェイを統合した初の手法で、10以上の多様なテーブルトップタスクに対応
   - **limit**: (1) 2ステップpick-and-placeプリミティブを超える器用な6-DoF操作に対応不可。(2) 部分観測シーン、多指ハンドの連続制御、タスク完了予測に対応不可。(3) 頑健な実世界性能に50-100のデモンストレーションが必要。(4) 長期タスクでは入力-行動ペアの不十分なカバレッジにより性能低下。(5) 訓練データのバイアスを利用する場合がある

3. [[Lee2021_beyond_pick_place]](../REFERENCES/MAIN.md#Lee2021_beyond_pick_place) — Alex X. Lee, Coline Devin, Yuxiang Zhou, Thomas Lampe, et al., "Beyond Pick-and-Place: Tackling Robotic Stacking of Diverse Shapes" (2021)
   - **DOI**: arXiv:2110.06192 (CoRL 2021)
   - **thesis**: 多様で複雑な形状の物体のスタッキングは標準的pick-and-placeを超える戦略（道具使用、バランス維持、精密位置合わせ）を要求し、RLによるビジョンベース政策蒸留とsim-to-real転移でこれらの創発的スキルを獲得可能
   - **core**: (1) 非自明なスタッキング戦略を要求する幾何的に多様な「RGB物体」ベンチマーク。(2) 特権状態RLポリシーからRGBポリシーへのインタラクティブ政策蒸留とsim-to-real転移。(3) デプロイ済みポリシーが収集したデータでのオフラインRL改善
   - **diff**: 先行スタッキング研究（Deisenroth, Lee 2019等）は単純な幾何プリミティブ（立方体、円筒）に限定。本研究は道具使用、バランス維持、精密位置合わせを明示的に要求する物体を導入
   - **limit**: (1) 訓練三つ組での82%成功率が新規三つ組では54%に低下する顕著な汎化ギャップ。(2) 手動スクリプトベースラインでも51%で本質的なタスク困難性を確認。(3) 5つの物体カテゴリに限定、任意の新規物体への汎化は未対応

4. [[Bauza2024_simple]](../REFERENCES/MAIN.md#Bauza2024_simple) — Maria Bauza, Antonia Bronars, Yifan Hou, Ian Taylor, Nikhil Chavan-Dafle, Alberto Rodriguez, "SimPLE: a visuotactile method learned in simulation to precisely pick, localize, regrasp, and place objects" (2024)
   - **DOI**: 10.1126/scirobotics.adi8808
   - **thesis**: 精密汎化 — 多様なpick-and-placeタスクをミリメートル精度で解決すること — は、タスクaware把持、視触覚ポーズ推定、グラフベース再把持計画を統合するシミュレーション学習パイプラインにより、実世界経験なしで達成可能
   - **core**: (1) 安定性・観測可能性・配置好適性を同時最適化するタスクaware把持選択。(2) 実触覚/視覚観測とシミュレーション観測のマッチングによる教師あり視触覚ポーズ推定。(3) 手-手間再把持のグラフ上最短経路としての多段再把持計画（デュアルアーム）
   - **diff**: 先行精密配置システム（form2fit, Transporter Networks）は1mm以下の精度に到達しないか実世界訓練データを必要。SimPLEはCADモデルとシミュレーションのみで1mm以下の配置精度を達成（6/15物体で>90%成功率）
   - **limit**: (1) 初回把持・触覚観測後はオープンループ実行、搬送・配置中のポーズ更新なし。(2) ±0.5mmの許容誤差内でのニアサクセス失敗が閉ループ力覚フィードバックで解決可能だが未対応。(3) 観測可能性メトリクスが触覚のみを考慮し視覚の曖昧性解消能力を無視。(4) 再把持がポーズ推定誤差を蓄積させる傾向

5. [[He2023_pick2place]](../REFERENCES/MAIN.md#He2023_pick2place) — Zhanpeng He, Nikhil Chavan-Dafle, Jinwook Huh, Shuran Song, Volkan Isler, "Pick2Place: Task-aware 6DoF Grasp Estimation via Object-Centric Perspective Affordance" (2023)
   - **DOI**: 10.1109/ICRA48891.2023.10160736
   - **thesis**: pick-and-placeにおける把持選択は配置aware（配置の幾何的関係をオブジェクト中心のパースペクティブアフォーダンスマップにエンコードすること）であるべきであり、これにより配置と把持の1対1マッピングが可能になる
   - **core**: 配置シーンのパースペクティブビューから配置アフォーダンスマップをレンダリングし、各配置ポーズ候補と必要な把持ポーズの間に微分可能な1対1対応を確立するオブジェクト中心行動空間
   - **diff**: 先行タスクaware把持手法は把持を配置実現可能性と独立に評価するか、pickとplaceの逐次計画が必要。Pick2Placeは配置アフォーダンスから把持選択への直接的な微分可能マッピングを6-DoFで初めて実現
   - **limit**: (1) 手首カメラによるNeRFベースシーン表現の構築に時間を要する。(2) 1デモンストレーションのみでは多様性不足により性能低下。(3) 微分可能パイプラインのアクション計画への統合は将来課題

6. [[Wada2022_reorientbot]](../REFERENCES/MAIN.md#Wada2022_reorientbot) — Kentaro Wada, Stephen James, Andrew J. Davison, "ReorientBot: Learning Object Reorientation for Specific-Posed Placement" (2022)
   - **DOI**: 10.1109/icra46639.2022.9811881
   - **thesis**: 任意の目標ポーズでの配置実現には中間ステップとしての再方向づけが必要であり、学習ベースのウェイポイント選択と古典的動作計画のハイブリッドが高成功率で解決可能
   - **core**: (1) 視覚入力（RGB-Dポーズ推定+体積再構築）から好適な中間再方向づけポーズを予測する学習ウェイポイントセレクタ。(2) ウェイポイント間の衝突回避軌道を生成する古典的動作計画。学習は「何をするか」のみ選択し、「どうするか」は計画が担当
   - **diff**: ヒューリスティックな再方向づけアプローチは多様な物体形状に適応不可で低成功率。ReorientBotはYCB物体でヒューリスティックベースラインに対し成功率81%改善、実行時間22%短縮
   - **limit**: (1) 2ウェイポイント（開始、終了）のみ評価、より長期のタスク最適化には細粒度の学習-計画相互作用が必要。(2) ナビゲーションやマルチロボットは未対応。(3) ポーズ推定に既知物体モデルが前提

7. [[Cheng2021_regrasp_place]](../REFERENCES/MAIN.md#Cheng2021_regrasp_place) — Shuo Cheng, Kaichun Mo, Lin Shao, "Learning to Regrasp by Learning to Place" (2021)
   - **DOI**: arXiv:2109.08817 (CoRL 2021)
   - **thesis**: 再把持は安定した中間配置を予測することで最も効果的に解決され、支持環境を活用する（壁や端に置く等）ことで再把持空間を平面配置を超えて拡張可能
   - **core**: (1) 部分点群から未知物体の安定配置を予測するニューラル配置予測器。(2) 予測された配置からpick-and-place遷移のエッジを持つ再把持グラフを構築し、グラフ探索で多段再把持計画
   - **diff**: 先行再把持手法（Tournassoud 1987, Wan & Harada 2020）は既知物体モデル、事前定義配置集合、解析的安定性基準に依存。本研究は未知物体の点群から配置を学習し、環境（壁、端）を再方向づけのツールとして活用
   - **limit**: (1) 力覚・触覚信号の未使用。(2) 安定ポーズ予測が小摂動に敏感な場合がある。(3) 配置後の物体姿勢が予測と異なる場合がある。(4) センサノイズにより衝突回避アプローチ経路の発見に失敗する場合がある。(5) 最頻失敗モードは偽安定物体ポーズ予測。(6) 物体セグメンテーションの事前提供と全物体が把持可能であることを前提

8. [[Shanthi2024_joint_pick_place]](../REFERENCES/MAIN.md#Shanthi2024_joint_pick_place) — Manoj Shanthi, Tucker Hermans, "Pick and Place Planning is Better Than Pick Planning Then Place Planning" (2024)
   - **DOI**: 10.1109/LRA.2024.3360892
   - **thesis**: 把持と配置の同時推論は、従来の逐次アプローチ（まず把持を選択、次に配置を計画）に対し厳密に優位であり、特にクラッター環境で把持実現可能性が配置要件と密結合する
   - **core**: 学習ベースの多指把持分類器と配置コスト関数を統一最適化フレームワークで結合するモジュラー同時pick-and-place計画アルゴリズム
   - **diff**: 先行タスクaware把持研究は把持と配置を逐次的に処理するか、最新の学習ベース多指把持計画器を活用しない。本研究は逐次「pick then place」が同時推論に対し厳密に劣ることを実ハードウェアで初めて実証
   - **limit**: (1) 物体が初期計画時の剛体オフセットを維持する前提（把持・搬送中の物体移動に未対応）。(2) 配置時の視覚・触覚フィードバックなし。(3) 傾斜面・非平面への配置は未対応

9. [[Xu2024_grasp_see_place]](../REFERENCES/MAIN.md#Xu2024_grasp_see_place) — Kechun Xu, Zhongxiang Zhou, Jun Wu, Haojian Lu, Rong Xiong, Yue Wang, "Grasp, See, and Place: Efficient Unknown Object Rearrangement with Policy Structure Prior" (2024)
   - **DOI**: 10.1109/TRO.2024.3502520
   - **thesis**: 知覚ノイズは把持と配置に数学的に分離可能な影響を与え、この分離構造を政策事前知識として活用するデュアルループアーキテクチャが、モノリシックなアプローチよりも効率的で頑健な未知物体再配置を実現する
   - **core**: (1) 把持と配置における知覚ノイズの分離影響を示す理論的解析。(2) CLIPベースの把持後物体マッチングによるインナーループ「see」政策。(3) 物体マッチング信頼度と把持能力を考慮したアウターループ「grasp」政策。(4) CLIP基づく再配置完了の自己終了検出
   - **diff**: 先行未知物体再配置システム（Goyal 2022, Huang 2022）は知覚と行動を密結合し、知覚エラーに敏感で不要な余分ステップを生じる。GSPは知覚ノイズの分離影響を初めて形式的に分析し、これを活用した政策構造事前知識を設計
   - **limit**: (1) ゴールシーンに遮蔽やスタッキングがないことを前提。(2) 6-DoF設定でクラッター中の未知物体に対する知覚ノイズが深刻。(3) ゴール指定に単一RGB-D画像のみ使用し遮蔽下のゴール表現が限定的

### C — Relational Object Rearrangement

pick-and-placeを基本操作とする学習ベースの物体再配置。SE(3)等変表現（R-NDF, TAX-Pose）、拡散モデル（RPDiff, StructDiffusion）、ニューラル計画（NeRP）、VLM統合（Dream2Real）の4つの主要アプローチが存在する。

1. [[Liu2022_structformer]](../REFERENCES/MAIN.md#Liu2022_structformer) — Weiyu Liu, Chris Paxton, Tucker Hermans, Dieter Fox, "StructFormer: Learning Spatial Structure for Language-Guided Semantic Rearrangement of Novel Objects" (2022)
   - **DOI**: 10.1109/ICRA46639.2022.9811931
   - **thesis**: 言語指示からの多物体意味的再配置には、ペアワイズ空間プリミティブの連鎖ではなく、全物体間の関係構造の同時推論が必要
   - **core**: 物体選択エンコーダと自己回帰ポーズ生成デコーダの2段階Transformerアーキテクチャ。学習された仮想構造フレームに固定された目標位置を部分観測点群と言語埋め込みから予測
   - **diff**: ペアワイズ空間関係手法は多物体関係制約の捕捉に失敗。StructFormerはTransformerにより全先行配置物体を条件として各配置を生成し、多物体間の依存関係を明示的に推論
   - **limit**: クラッター中の配置や最適再配置順序の決定は未対応。構造化言語入力を使用（自然言語未対応）。テーブルトップ以外の多様な環境への拡張が将来課題

2. [[Pan2022_tax_pose]](../REFERENCES/MAIN.md#Pan2022_tax_pose) — Chuer Pan, Brian Okorn, Harry Zhang, Ben Eisner, David Held, "TAX-Pose: Task-Specific Cross-Pose Estimation for Robot Manipulation" (2022)
   - **DOI**: pmlr-v205-pan23a (CoRL 2022)
   - **thesis**: 新規物体のタスク固有操作は、各物体のポーズを独立推定するのではなく、2つの相互作用物体間の「cross-pose」（SE(3)関係変換）を密なクロスオブジェクト対応から学習することで達成可能
   - **core**: DGCNN + クロスオブジェクト注意Transformerによるソフト対応予測、学習残差変位、微分可能重み付きSVD (Procrustes) による相対変換抽出。10デモンストレーションから学習
   - **diff**: NDF、Dense Object Netsはアンカー物体が既知の正準構成にあることを前提。TAX-Poseは両物体の幾何を同時推論しこの制約を除去。DCP（同一形状登録）とは異なりタスク固有の異なるカテゴリ間の関係を推定
   - **limit**: (1) 正確な2物体セグメンテーションが必要。(2) 遮蔽下で性能低下。(3) 単一グローバルポーズ推定のみで多峰性関係に不適。(4) 完全未知マグでの実機マグ吊りは54%成功率

3. [[Simeonov2022_rndf]](../REFERENCES/MAIN.md#Simeonov2022_rndf) — Anthony Simeonov, Yilun Du, Lin Yen-Chen, Alberto Rodriguez, Leslie Pack Kaelbling, Tomas Lozano-Perez, Pulkit Agrawal, "SE(3)-Equivariant Relational Rearrangement with Neural Descriptor Fields" (2022)
   - **DOI**: pmlr-v205-simeonov23a (CoRL 2022)
   - **thesis**: 2つの新規物体を含む関係的再配置タスクは、NDFによるタスク関連座標フレームの特定とエネルギーベースモデルによる結合構成のリファインメントにより、5-10デモンストレーションで解決可能
   - **core**: 各物体のNDFによる記述子分散最小化でタスク関連座標フレームを特定（単一3Dキーポイント注釈のみ必要）し、エネルギーベースリファインメントモデルで結合構成を補正する2段階最適化
   - **diff**: 先行NDF研究は一方の物体（Object A）が既知であることを前提。R-NDFは「両方の物体の幾何と状態が未知」のケースで汎化可能。密な手動キーポイントラベリングの代わりに「単一3Dキーポイント」のみ必要
   - **limit**: 各カテゴリの事前学習NDFと3Dモデルデータセットが必要。タスク関連部位の特定に注釈キーポイントが必要。深度カメラはノイズや薄い/透明物体で困難。セグメント済み物体点群が必要

4. [[Liu2023_structdiffusion]](../REFERENCES/MAIN.md#Liu2023_structdiffusion) — Weiyu Liu, Yilun Du, Tucker Hermans, Sonia Chernova, Chris Paxton, "StructDiffusion: Language-Guided Creation of Physically-Valid Structures using Unseen Objects" (2023)
   - **DOI**: 10.15607/RSS.2023.XIX.031
   - **thesis**: 拡散モデルとオブジェクト中心Transformerの結合は、自己回帰的・直接回帰的アプローチに固有のモード崩壊と矛盾制約問題を克服し、言語指示から物理的に妥当な多物体構造を生成可能
   - **core**: オブジェクト中心Transformerを通じて物体ポーズを反復的にデノイズする拡散モデルと、物理的に無効なサンプル（貫通等）を棄却する学習弁別器。生成器-弁別器設計で多様かつ制約充足的な構成を生成
   - **diff**: StructFormerの自己回帰予測はモード崩壊と「複数の潜在的に矛盾する制約」への対処困難。StructDiffusionは拡散ベース生成で複数解モードを捕捉し、未知物体でStructFormerに対し16%改善
   - **limit**: 剛体物体とpick-and-placeプリミティブのみ前提。実世界の失敗は把持計画と動作計画に起因。サンプリングベースTAMPとの統合が将来課題

5. [[Qureshi2021_nerp]](../REFERENCES/MAIN.md#Qureshi2021_nerp) — Ahmed H. Qureshi, Arsalan Mousavian, Chris Paxton, Michael C. Yip, Dieter Fox, "NeRP: Neural Rearrangement Planning for Unknown Objects" (2021)
   - **DOI**: 10.15607/RSS.2021.XVII.072
   - **thesis**: エンドツーエンドのニューラル計画は、モデルベースアプローチより少ないステップと短い計画時間で未知物体の再配置を実現可能
   - **core**: 高次GNNが現在シーンとターゲットシーンをエンコードし、物体選択、デルタ提案（確率的ドロップアウトによる多様性）、ゴール充足スコアリング、衝突検出の4つの専門ネットワークに入力。サンプリングベースロールアウト計画
   - **diff**: 「未知物体のエンドツーエンド再配置計画の初のシステム」。物体モデルや既知IDなしで動作。合成データのみで訓練し、モデルベースエキスパートの90.67%に対し94.56%の成功率を達成
   - **limit**: 「既存のシーンセグメンテーションと特徴ベース物体対応技術が実環境で失敗しがち」であり、sim-to-real性能が低下。将来はロバストなセグメンテーションと完全SE(3)計画（現在は並進のみ）への拡張

6. [[Simeonov2023_rpdiff]](../REFERENCES/MAIN.md#Simeonov2023_rpdiff) — Anthony Simeonov, Ankit Goyal, Lucas Manuelli, Lin Yen-Chen, Alina Sarmiento, Alberto Rodriguez, Pulkit Agrawal, Dieter Fox, "Shelving, Stacking, Hanging: Relational Pose Diffusion for Multi-modal Rearrangement" (2023)
   - **DOI**: pmlr-v229-simeonov23a (CoRL 2023)
   - **thesis**: ローカル幾何特徴条件付きの反復的ポーズデノイジングは、関係的再配置タスク（棚、スタッキング、吊り下げ）の多峰性を自然に捕捉しつつ、多様な新規形状・シーンレイアウトで高い配置精度を維持する
   - **core**: ポイントクラウドポーズデノイジング用Transformerネットワーク：摂動された物体ポーズを反復的に有効配置に向けてリファインメント。デノイジング反復間で条件付け領域サイズを動的に調整するローカルシーンクロッピング（粗→細）
   - **diff**: NSMは単一出力で多峰性を捕捉不可。NSM+CVAEはモード間の「over-smoothing」。R-NDF（グローバルエンコーディング）はシーン汎化に限界。RPDiffはローカルかつ反復依存のクロッピングと拡散ベース多様性で全てに対応
   - **limit**: デモンストレーションデータにスクリプト化されたシミュレーション政策が必要。シミュレーション点群で訓練のためsim-to-realギャップが存在。オープンループ実行で閉ループフィードバックや外乱回復なし

7. [[Kapelyukh2024_dream2real]](../REFERENCES/MAIN.md#Kapelyukh2024_dream2real) — Ivan Kapelyukh, Yifei Ren, Ignacio Alzugaray, Edward Johns, "Dream2Real: Zero-Shot 3D Object Rearrangement with Vision-Language Models" (2024)
   - **DOI**: 10.1109/ICRA57147.2024.10611220
   - **thesis**: NeRFによる3Dシーン表現を構築し、仮想的に物体を再配置し、レンダリング画像をVLM（CLIP）で評価する「評価的アプローチ」により、タスク固有の訓練データなしでゼロショット言語条件付き再配置が達成可能
   - **core**: (1) 前景/背景別NeRFによる自律シーン再構築。(2) SE(3)候補ポーズのサンプリングと2D画像レンダリング。(3) 正規化言語キャプションに対するCLIPベーススコアリング
   - **diff**: DALL-E-Bot（生成的アプローチ）は拡散モデルでゴール画像を合成し「物体マッチング問題」が生じ2Dに限定。Dream2Realは評価的アプローチで実物体配置をスコアリングし完全6-DoFを実現
   - **limit**: 低許容誤差タスク（挿入等）は密なポーズサンプリングが必要で計算コスト大。シーンスキャン3-5分、ポーズ評価約6分。CLIPの「bag-of-words」挙動により空間関係の語順を誤解する場合がある

8. [[Murali2023_cabinet]](../REFERENCES/MAIN.md#Murali2023_cabinet) — Adithyavairavan Murali, Arsalan Mousavian, Clemens Eppner, Adam Fishman, Dieter Fox, "CabiNet: Scaling Neural Collision Detection for Object Rearrangement with Procedural Scene Generation" (2023)
   - **DOI**: 10.1109/ICRA48891.2023.10161528
   - **thesis**: 手続き的シーン生成による大規模訓練（650K以上のシーン、約600億衝突クエリ）でニューラル衝突検出をスケールすることで、シミュレーションから実世界にゼロショット転移可能な衝突回避再配置が実現可能
   - **core**: 3D畳み込みシーンエンコーダ（ボクセル化、7マイクロ秒推論）とIMLE訓練ウェイポイントサンプラー、MPPI軌道生成の統合
   - **diff**: SceneCollisionNet（先行研究）はテーブルトップシーンに限定。CabiNetは訓練を30倍スケールし複数環境タイプ（キャビネット、棚）に対応。学習ウェイポイントサンプラーにより狭空間での遷移成功率を約35%改善
   - **limit**: 3Dボクセル化がモデルワークスペース内にクエリを制限し操作中に範囲外になる場合がある。将来はより複雑なシーン、合成シーン生成手順の学習、ハイブリッドアーキテクチャ

9. [[Wu2022_targf]](../REFERENCES/MAIN.md#Wu2022_targf) — Mingdong Wu, Fangwei Zhong, Yulong Xia, Hao Dong, "TarGF: Learning Target Gradient Field for Object Rearrangement" (2022)
   - **DOI**: arXiv:2209.00853 (NeurIPS 2022)
   - **thesis**: 規範的ターゲット分布への再配置は、明示的ゴール指定やエキスパートデモンストレーションなしに、ターゲット分布の尤度を増加させる方向を示すスコアマッチングで学習した勾配場により達成可能
   - **core**: デノイジングスコアマッチングでターゲット分布の対数密度勾配を推定するニューラルネットワーク。勾配場が衝突回避プランナー(ORCA)の参照速度と、残差政策学習によるRLの報酬・探索ガイダンスの二重役割を果たす
   - **diff**: 模倣学習はエキスパート軌道が必要。分類器ベース手法は高次元疎性と無効ゴール状態生成に悩む。TarGFはスコアベース生成モデリングで連続的方向ガイダンスを提供
   - **limit**: 平面・速度制御環境に制限。視覚観測なし（状態ベース入力）。ORCA適用に円形物体を前提。将来はワールドモデル経由の視覚観測、力制御の階層的政策

10. [[Tang2022_selective_rearrangement]](../REFERENCES/MAIN.md#Tang2022_selective_rearrangement) — Bingjie Tang, Gaurav S. Sukhatme, "Selective Object Rearrangement in Clutter" (2022)
    - **DOI**: pmlr-v205-tang23a (CoRL 2022)
    - **thesis**: クラッター中の選択的再配置（一部の物体のみ移動、他は破棄）は、グラフベースシーケンシング、プッシュ/グラスプ行動選択、視覚対応ベース配置の組み合わせにより、純粋画像ベースで解決可能
    - **core**: (1) グラフベース物体シーケンシング、(2) 特徴ベース行動選択（プッシュ or グラスプ + ポーズ）、(3) 視覚対応ベース配置政策の3段階分解。選択的再配置、クラッター、占有ゴールの3課題を純粋画像ベースで初めて同時対応
    - **diff**: 先行再配置手法（NeRP等）は全物体の再配置を前提とし、クラッター中の選択的再配置に未対応。本研究は先行手法に対し約8%改善し、ゼロショットsim-to-real転移を達成
    - **limit**: limit not available（arXiv版なし、フルテキスト未アクセス）。引用論文（Guo 2024）によると、2-DoFポーズ変更（平面並進のみ）に限定され、クラッターシーンでの知覚エラーに敏感

### D — Generalist Robot Policies

pick-and-placeを主要なデモタスクとして使用した基盤モデル・VLA。RT-1がスケールの効果を実証し、RT-2がVLMの知識転移を確立、Diffusion Policyが行動拡散パラダイムを創出した。OpenVLA, pi0, Octoがオープンソース基盤を提供し、SIMPLERがシミュレーション評価手法を確立した。

1. [[Ahn2022_saycan]](../REFERENCES/MAIN.md#Ahn2022_saycan) — Michael Ahn, Anthony Brohan, Noah Brown, et al., "SayCan: Do As I Can, Not As I Say — Grounding Language in Robotic Affordances" (2022)
   - **DOI**: arXiv:2204.01691 (CoRL 2022)
   - **thesis**: LLMはアフォーダンス関数（事前学習スキルの価値関数）による提案の根拠付けにより効果的なロボットタスクプランナーとなり、各ステップで物理的に実現可能な行動のみが選択される
   - **core**: pi = argmax p(completion|state) × p(language_step|instruction) — LLMのタスク知識スコアと学習アフォーダンス（価値関数）スコアの積によるスキル選択
   - **diff**: LLM直接プロンプティング（根拠付けなしで67-74%計画成功）に対し、SayCan's根拠付けで84%に向上。行動クローニング（0%成功）やハンドクラフト記号タスク仕様（先行階層的計画）と異なり、LLM意味論で分解
   - **limit**: LLMのバイアスと制約を継承。スキルレパートリーの範囲と能力が主要ボトルネック。スキル失敗時の反応が困難。否定や曖昧な参照に脆弱（LLM固有の問題）

2. [[Chi2023_diffusion_policy]](../REFERENCES/MAIN.md#Chi2023_diffusion_policy) — Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, Shuran Song, "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion" (2023)
   - **DOI**: 10.1177/02783649241273668 (RSS 2023 / IJRR)
   - **thesis**: visuomotorポリシーを条件付きデノイジング拡散過程として表現することは、多峰性行動分布と高次元行動空間を自然に処理し、先行最先端手法に対し平均46.9%の改善をもたらす優れたパラダイム
   - **core**: 行動系列上の条件付きDDPM。リセディングホライズン制御（行動チャンク予測・部分実行）、FiLM変調による視覚条件付け、時系列拡散Transformerアーキテクチャ
   - **diff**: 明示的政策（直接回帰, MDN）は多峰性を表現不可。暗黙的政策（IBC/エネルギーベース）は負例サンプリングの不安定性。Diffusion Policyは反復デノイジングで多峰分布を自然にモデル化。先行拡散計画（Janner等）との違いは状態-行動結合分布ではなく観測条件付き行動分布のみを学習
   - **limit**: 不十分なデモンストレーションデータでの行動クローニングの限界を継承。より単純な手法に比べ計算コストと推論遅延が大きい。加速技術（ノイズスケジュール改善、高速推論ソルバー、一貫性モデル）が将来の方向

3. [[Brohan2023_rt2]](../REFERENCES/MAIN.md#Brohan2023_rt2) — Anthony Brohan, Noah Brown, Justice Carbajal, et al., "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control" (2023)
   - **DOI**: arXiv:2307.15818 (CoRL 2023)
   - **thesis**: VLMは行動をテキストトークンとして表現しロボット軌道データとWebスケール視覚-言語タスクで共同ファインチューニングすることで、アーキテクチャ変更なしにVLAに直接変換可能であり、Webスケールの意味知識がロボット制御に転移される
   - **core**: 行動のテキストトークン化：7-DoF連続行動を次元あたり256ビンに離散化しテキスト文字列としてエンコード。VLM（PaLI-X 55B, PaLM-E 12B）をロボット+Webデータで標準次トークン予測で共同ファインチューニング
   - **diff**: CLIPort, MOOは2Dに制限。SayCan はVLMを高レベル計画にのみ使用。RT-1はカスタムアーキテクチャ。RT-2はVLM重みを直接再利用し行動固有層なしでエンドツーエンド統合
   - **limit**: ロボット訓練データ分布を超える新しい物理動作の獲得不可。推論速度制限（最大モデルで1-3 Hz）。必要なファインチューニングをサポートするVLMが少数

4. [[Brohan2022_rt1]](../REFERENCES/MAIN.md#Brohan2022_rt1) — Anthony Brohan, Noah Brown, Justice Carbajal, et al., "RT-1: Robotics Transformer for Real-World Control at Scale" (2022)
   - **DOI**: arXiv:2212.06817 (RSS 2023)
   - **thesis**: 大規模で多様な実ロボットデータセット（130kエピソード、700+タスク）で訓練された高容量Transformerは、データサイズ・多様性・モデルサイズとともにスケーラブルな汎化特性を示し、「基盤モデル」パラダイムが実世界ロボティクスに転移可能
   - **core**: FiLM条件付きEfficientNet-B3、TokenLearner圧縮（81トークン→8、3Hzリアルタイム推論）、デコーダのみTransformer（8注意層）、次元あたり256ビン離散化行動（7アーム+3ベース+1モード）
   - **diff**: 既知タスク97%（BC-Z 72%, Gato 65%）、未知タスク76%（Gato 52%, BC-Z 19%）。Gatoと異なりTokenLearner圧縮でリアルタイム推論。BC-Z（ResNetベース）よりTransformerが多様データを吸収
   - **limit**: 模倣学習としてデモンストレータ性能を超過不可。既知概念の新規組み合わせへの汎化に限定。操作タスクセットは大規模だが高い器用性は未達成

5. [[Kim2024_openvla]](../REFERENCES/MAIN.md#Kim2024_openvla) — Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, et al., "OpenVLA: An Open-Source Vision-Language-Action Model" (2024)
   - **DOI**: arXiv:2406.09246 (CoRL 2024)
   - **thesis**: DINOv2+SigLIP融合視覚エンコーダとLlama 2上に構築されたオープンソース7BパラメータVLAは、クローズドソース55Bモデル（RT-2-X）を16.5%上回りつつ消費者GPUで効率的にファインチューニング可能であり、VLAベースロボティクスを広範な研究コミュニティに開放する
   - **core**: デュアル視覚エンコーダ（DINOv2：空間特徴 + SigLIP：意味特徴）のMLP射影によるLlama 2言語モデル空間への統合。分位点ベースビニング（256ビン/次元）による行動離散化。Open X-Embodimentの970k実世界デモンストレーションで事前訓練
   - **diff**: RT-2-X（55B、クローズドソース）に対し7倍少ないパラメータで+16.5%成功率、完全オープンソース。Octo（93M、拡散ベース）より強い言語根拠付け。Diffusion Policy（スクラッチ学習）に対し多様なマルチタスク設定で+20.4%
   - **limit**: 単一画像観測のみサポート、複数カメラ・固有受容覚・観測履歴への拡張が必要。高頻度制御に不十分な推論スループット。典型的成功率は90%未満。VLMベースサイズ、共同訓練戦略、ロボティクス向け最適視覚特徴が未探索

6. [[Black2024_pi0]](../REFERENCES/MAIN.md#Black2024_pi0) — Kevin Black, Noah Brown, Danny Driess, et al., "pi0: A Vision-Language-Action Flow Model for General Robot Control" (2024)
   - **DOI**: arXiv:2410.24164
   - **thesis**: 事前学習VLM上に構築されたフローマッチングアーキテクチャを、約10,000時間の多様な器用ロボットデータで訓練することで、ゼロショット汎化、言語指示追従、複雑な長期操作タスクへの効率的ファインチューニングが可能なロボット基盤モデルとなる
   - **core**: PaliGemma（3B VLM）バックボーンに専用300Mパラメータ「アクションエキスパート」モジュールを追加。自己回帰トークン予測ではなく条件付きフローマッチングで50Hz連続行動生成。50タイムステップの行動チャンク
   - **diff**: 自己回帰VLA（RT-2, OpenVLA）は行動離散化と低頻度制御に制限。タスク固有手法（ACT, Diffusion Policy）は汎化に乏しい。Octo（93M）より大規模なVLM初期化で大幅に強い性能。訓練データセット（約10,000時間）は「これまでで最大のロボット学習実験」
   - **limit**: 事前学習データセットの構成と重み付けが十分に理解されていない。全評価タスクが確実に動作するわけではない。高度に異なるドメイン（自動運転、ナビゲーション、脚式移動）への正の転移は未確認

7. [[Ghosh2024_octo]](../REFERENCES/MAIN.md#Ghosh2024_octo) — Dibya Ghosh, Homer Walke, Karl Pertsch, et al., "Octo: An Open-Source Generalist Robot Policy" (2024)
   - **DOI**: arXiv:2405.12213 (RSS 2024)
   - **thesis**: 最大の操作データセット（800k軌道、Open X-Embodiment）で訓練されたモジュラー・オープンソース汎用ロボット政策は、消費者GPUで数時間以内に新しい観測モダリティ、行動空間、ロボットプラットフォームに効率的にファインチューニング可能な汎用的初期化として機能する
   - **core**: ブロックワイズマスク注意と学習可能リードアウトトークンを持つTransformerバックボーン。T5（111M）による言語、浅いCNN+パッチトークン化による画像。拡散ベース行動デコーディングヘッド。モジュラー設計で新センサ/行動空間はアダプタ追加のみ
   - **diff**: RT-1-Xに対しゼロショット多ロボット評価で29%改善。RT-1-X, RoboCat（クローズドソース、言語のみ）と異なり言語・ゴール画像両条件付けをサポートし完全オープンソース。モジュラーアーキテクチャでファインチューニング時のセンサ/行動空間適応が可能
   - **limit**: 手首カメラ処理が困難（訓練データの27%のみ手首カメラ含む）。言語条件付けとゴール条件付け間の大きな性能差（訓練データの56%のみ言語注釈）。最適デモンストレーションのみの訓練、サブ最適やオンラインインタラクションデータは未利用

8. [[Li2024_simpler]](../REFERENCES/MAIN.md#Li2024_simpler) — Xuanlin Li, Kyle Hsu, Jiayuan Gu, et al., "SIMPLER: Simulated Manipulation Policy Evaluation for Real Robot" (2024)
   - **DOI**: arXiv:2405.05941 (CoRL 2024)
   - **thesis**: シミュレーション評価は、制御ギャップ（システム同定）と視覚ギャップ（グリーンスクリーン+テクスチャマッチング）を体系的に緩和すれば、完全忠実デジタルツインなしでも実世界ポリシー評価のスケーラブルで再現性のある信頼性高い代理となり得る
   - **core**: シミュレーテッドアニーリングによるPDコントローラパラメータのシステム同定。「グリーンスクリーン」（実世界背景のシミュレーションシーンへのオーバーレイ）とテクスチャ射影による視覚ギャップ緩和。Mean Maximum Rank Violation (MMRV) メトリクス
   - **diff**: 標準sim-to-real方向の反転：シミュレーションで訓練して実機デプロイではなく、実訓練ポリシーをシミュレーションで評価。ナビゲーションベンチマーク（Habitat, RoboTHOR）のような3Dスキャンデジタルツインが不要
   - **limit**: 剛体操作のみに焦点。グリーンスクリーンは固定カメラに限定、影や細かい視覚ディテールを捕捉不可。シミュレーション評価環境の作成に手動アセットキュレーションが必要

### E — SE(3) Grasp & Motion Optimization

配置を間接的に支える把持検出と統合的把持-動作計画。Contact-GraspNetが効率的6-DoF把持検出の基盤を確立し、SE(3)-DiffusionFieldsとNGDFが把持と軌道の同時最適化を拡散/距離場で実現した。

1. [[Sundermeyer2021_contact_graspnet]](../REFERENCES/MAIN.md#Sundermeyer2021_contact_graspnet) — Martin Sundermeyer, Arsalan Mousavian, Rudolph Triebel, Dieter Fox, "Contact-GraspNet: Efficient 6-DoF Grasp Generation in Cluttered Scenes" (2021)
   - **DOI**: 10.1109/ICRA48506.2021.9561877
   - **thesis**: 観測3D点群上の点を潜在的把持接触点として扱い、点ごとの把持パラメータを予測することで、6-DoF把持学習を4-DoF問題に還元可能であり、クラッターシーンで失敗率を半減するエンドツーエンドのクラスagnostic把持生成が実現する
   - **core**: PointNet++で全シーン深度点群を処理、点ごとの把持可能性スコア、3-DoFアプローチ/ベースライン回転、把持幅を予測。把持ポーズを観測接触点に根拠付けることで6-DoF→4-DoF次元削減
   - **diff**: 先行6-DoF手法（6-DoF GraspNet等）は物体セグメンテーションを前提とする複雑な逐次パイプライン。Contact-GraspNetはインスタンスセグメンテーションなしで全シーン点群上でエンドツーエンド動作し、成功率90.2%（先行80.39%、失敗率半減）
   - **limit**: 明示的なLimitations/Future Workセクションなし。厚い物体（最大把持幅に近い）と小物体（低信頼度予測）での失敗を報告

2. [[Huang2023_scenediffuser]](../REFERENCES/MAIN.md#Huang2023_scenediffuser) — Siyuan Huang, Zan Wang, Puhao Li, Baoxiong Jia, Tengyu Liu, Yixin Zhu, Wei Liang, Song-Chun Zhu, "SceneDiffuser: Diffusion-based Generation, Optimization, and Planning in 3D Scenes" (2023)
   - **DOI**: 10.1109/CVPR52729.2023.01607
   - **thesis**: 単一の条件付き拡散モデルがシーン条件付き生成、物理ベース最適化、ゴール指向計画を統一可能であり、各デノイジングステップでの勾配ベースガイダンスの統合により別個モジュール間の不整合と事後崩壊を軽減する
   - **core**: ベイズ分解 p(τ|S,G) = p_θ(τ|S) × p_φ(G|τ,S)。φは物理ベース最適化目的（衝突回避）とゴール到達目的に分解。各デノイジングステップでテイラー展開近似により勾配ベースガイダンスを微分可能に統合
   - **diff**: cVAEベースアプローチは事後崩壊と多様性制限に悩む。物理ベース後処理最適化を生成と分離する手法と異なり、SceneDiffuserは制約を各サンプリングステップで微分可能に統合
   - **limit**: 先行シーン条件付き生成モデルに比べ訓練・テスト速度が遅い（拡散の共通課題）。最適化と計画が目的設計に高度に依存し、ハイパーパラメータ調整に大きな労力が必要

3. [[Ichnowski2021_dex_nerf]](../REFERENCES/MAIN.md#Ichnowski2021_dex_nerf) — Jeffrey Ichnowski, Yahav Avigal, Justin Kerr, Ken Goldberg, "Dex-NeRF: Using a Neural Radiance Field to Grasp Transparent Objects" (2021)
   - **DOI**: arXiv:2110.14217 (CoRL 2021)
   - **thesis**: NeRFの視点非依存学習密度と戦略的照明配置による鏡面反射の誘発、透明性aware深度レンダリングの組み合わせにより、従来の深度センサが完全に失敗する透明物体の信頼性のある把持が可能
   - **core**: (1) 透明性aware深度レンダリング（標準期待深度ではなく各レイ上でσが閾値を超える最初のサンプルを検出）。(2) 鏡面反射を誘発する戦略的照明。(3) Dex-Net把持プランナーとの統合
   - **diff**: CNNベース透明物体検出は大量注釈データセットが必要。標準深度カメラ（RealSense等）は透明物体で失敗。バニラNeRF深度抽出は透明表面形状に対応不可。Dex-NeRFは注釈なしの多視点画像のみで使用可能な深度マップを生成
   - **limit**: NeRFの長い訓練時間が主な欠点。将来はロボット固有機能の活用（深度カメラデータの追加訓練データ利用、関心領域検査用マニピュレータ搭載カメラ、環境変化への適応）による訓練高速化

4. [[Urain2023_se3_diffusion_fields]](../REFERENCES/MAIN.md#Urain2023_se3_diffusion_fields) — Julen Urain, Niklas Funk, Jan Peters, Georgia Chalvatzaki, "SE(3)-DiffusionFields: Learning Smooth Cost Functions for Joint Grasp and Motion Optimization" (2023)
   - **DOI**: 10.1109/ICRA48891.2023.10161569
   - **thesis**: SE(3)上でスコアマッチングで訓練された拡散モデルは、把持選択と軌道生成の同時最適化を単一の微分可能フレームワークで可能にする滑らかで勾配豊富なコスト関数を提供し、従来の逐次パイプラインの分離を除去する
   - **core**: SE(3)多様体上のLogmap/Expmap変換を用いたデノイジングスコアマッチング。固定グリッパー点群と学習物体SDFによる把持ポーズ表現。逆ランジュバン動力学による軌道最適化への学習エネルギーランドスケープの統合
   - **diff**: 分離型grasp-then-planパイプラインと異なり同時最適化。交差エントロピーや対照的ダイバージェンスで学習されたコスト関数（硬い判別領域と大きな無情報プラトーを生成）と異なり、拡散ベーススコアマッチングは「全空間にわたる情報のある勾配」を提供
   - **limit**: 完全な物体状態知識を前提、複雑な知覚システムなし。不完全な知覚と手動コスト項によるsim-to-realギャップの可能性。タスク複雑性増加時の複数コスト項の重み付けが困難

5. [[Weng2023_ngdf]](../REFERENCES/MAIN.md#Weng2023_ngdf) — Thomas Weng, David Held, Franziska Meier, Mustafa Mukadam, "Neural Grasp Distance Fields for Robot Manipulation" (2023)
   - **DOI**: 10.1109/ICRA48891.2023.10160217
   - **thesis**: 有効把持の多様体をニューラル距離場のゼロレベル集合として表現することで、把持学習を勾配ベース軌道最適化にシームレスに統合可能であり、到達-把持計画中に把持ターゲットが滑らかに変化できる
   - **core**: 6Dクエリポーズと形状埋め込みから最近接有効把持までの距離を予測する8層MLP。修正CHOMP軌道オプティマイザでの微分可能コスト項として滑らかさ・衝突回避と同時に最小化
   - **diff**: Contact-GraspNet等の離散把持集合予測は別途選択段階が必要。NGDFの連続表現は明示的把持選択なしで直接勾配ベース最適化を可能にし、Contact-GraspNetベースラインに対し実行成功率63%改善（0.61 vs. 0.37-0.39）
   - **limit**: グリッパー固有のデータセットで訓練、他グリッパー用には別データセットが必要。上流の物体セグメンテーションに依存。到達-把持計画でのコスト重みが固定、反復的重み学習が性能改善の可能性。オープンループ計画のみ

### F — Task Planning & Benchmarks

言語誘導型の配置計画、ベンチマーク。LLMベースのTAMP（Ding et al.）がゼロショット常識配置を実現し、LGMCTSがポーズ生成と行動計画の統合を提案した。SoFarがオリエンテーションの意味的理解を導入し、HomeRobotとManiSkill-HABがpick-and-placeベンチマークを確立した。

1. [[Ding2023_llm_tamp]](../REFERENCES/MAIN.md#Ding2023_llm_tamp) — Yan Ding, Xiaohan Zhang, Chris Paxton, Shiqi Zhang, "Task and Motion Planning with Large Language Models for Object Rearrangement" (2023)
   - **DOI**: 10.1109/IROS55552.2023.10342169
   - **thesis**: LLMは意味的に妥当な物体配置（空間関係と距離）に関する常識知識を提供可能であり、幾何衝突チェック付きTAMPでインスタンス化することで、変動するシーン形状全体でゼロショット汎化が達成可能
   - **core**: (1) LLMがテンプレートプロンプトで記号的空間関係を抽出、ASPロジックで検証。(2) LLMが計量距離を推薦、2Dガウシアンからサンプリングし衝突/境界制約でフィルタ。(3) GROPアルゴリズムで最適ナビゲーションゴールと配置行動を計算
   - **diff**: DALL-E-Bot（視覚のみ、視点依存）と異なり任意視点対応。StructFormer（訓練データ必要）と異なりゼロショット。SayCan（タスクレベルのみ）と異なり細粒度配置決定。純粋GROP（意味なし）と異なり常識配置を実現
   - **limit**: 完全未知物体のピッキング・操作への拡張と、より広いセットの配置問題への適用が将来課題

2. [[Qi2025_sofar]](../REFERENCES/MAIN.md#Qi2025_sofar) — Zekun Qi, Wenyao Zhang, et al., "SoFar: Language-Grounded Orientation Bridges Spatial Reasoning and Object Manipulation" (2025)
   - **DOI**: arXiv:2502.13143
   - **thesis**: 物体の向き（位置だけでなく）が6-DoF操作に不可欠であり、自然言語によるオリエンテーション定義（「semantic orientation」）が参照フレーム不要の表現を提供し、VLM空間推論と精密ロボット操作のギャップを橋渡しする
   - **core**: PointSOモデル：3D点群トークンと言語埋め込みをトークンレベル加算で融合し単位球上の意味的オリエンテーションベクトルを予測するTransformer。OrienText300Kデータセット：GPT-4oによる350K+の3Dモデル意味的オリエンテーション注釈
   - **diff**: 先行VLMシステムは位置理解（「物体はどこか」）に焦点を当て操作に必要なオリエンテーションを無視。エンドツーエンドVLA（Octo, OpenVLA）と異なり、タスク固有訓練なしで多様なエンボディメントにゼロショット汎化
   - **limit**: 分離システムとして、サブモジュールエラーにより実行が失敗する場合がある（不安定な把持や不正確な視覚知覚による予期しないポーズ）。将来はエンドツーエンドと分離手法の組み合わせ探索

3. [[Chang2024_lgmcts]](../REFERENCES/MAIN.md#Chang2024_lgmcts) — Haonan Chang, Kai Gao, et al., "LGMCTS: Language-Guided Monte-Carlo Tree Search for Executable Semantic Object Rearrangement" (2024)
   - **DOI**: 10.1109/IROS58592.2024.10802562
   - **thesis**: 言語誘導ポーズ生成とMCTSベース行動計画の統合（逐次段階への分離ではなく）により、衝突回避、意味的整合性、実行可能性を備えた再配置計画を生成可能であり、2段階アプローチを大幅に上回る
   - **core**: (1) LLMベース言語パースで物体選択とポーズ分布記述を抽出。(2) パラメトリック曲線ベースパターン事前知識と空き空間制約による分布生成。(3) 障害物と実行不可能構成を処理するMCTS計画
   - **diff**: StructFormerとStructDiffusion（ポーズ生成と行動計画を分離）に対し、LGMCTSは両方を統合し線パターンで95.99%成功率（StructDiffusion 61.49%）。純粋LLMベースTAMPと異なり幾何的に複雑なタスクに対応
   - **limit**: 複雑シーンでの実行時間延長がMCTS効率改善の主要課題。テーブルトップpick-place設定に特化、より複雑な再配置文脈への適応が将来方向

4. [[Shukla2025_maniskill_hab]](../REFERENCES/MAIN.md#Shukla2025_maniskill_hab) — Arth Shukla, Stone Tao, Hao Su, "ManiSkill-HAB: A Benchmark for Low-Level Manipulation in Home Rearrangement Tasks" (2025)
   - **DOI**: arXiv:2412.13211 (ICLR 2025)
   - **thesis**: 現実的なlow-level制御（「magical grasp」抽象化ではない）を持つGPU加速ベンチマークと、体系的な軌道ラベリング・フィルタリングの組み合わせにより、先行実装の3倍高速で効率的・制御されたデータ生成を可能にする、より忠実な家庭再配置研究の試験台が提供可能
   - **core**: ManiSkill3上のGPU加速HAB実装（4000+サンプル/秒）。物体ごとのRL政策（Pick/PlaceにSAC、Open/CloseにPPO）。特権シミュレータ情報による自動軌道カテゴリ化（Contact, Grasped, Dropped, Success, Excessive Collisions）
   - **diff**: Habitat 2.0の約3倍高速で現実的low-level制御をサポート。RoboCasaの125倍高速でRGB-Dレンダリングと動的物体処理。実ロボットデータセットと異なり効率的オンラインサンプリングと特権クエリをサポート。150以上の訓練済み政策で既存ベンチマークより広範なベースライン提供
   - **limit**: ベースライン性能に大幅な改善余地。実ロボットへの転移は未主張。制約下のクラッター環境での全身制御、長期スキル連鎖、シーンレベル再配置が現行手法の課題

5. [[Yenamandra2023_homerobot]](../REFERENCES/MAIN.md#Yenamandra2023_homerobot) — Sriram Yenamandra, Arun Ramachandran, et al., "HomeRobot: Open-Vocabulary Mobile Manipulation" (2023)
   - **DOI**: arXiv:2306.11565 (CoRL 2023)
   - **thesis**: Open-Vocabulary Mobile Manipulation (OVMM) — 未知環境で任意物体をpick-and-placeすること — は、シミュレーションと実世界の統合ベンチマークを手頃なハードウェア上で必要とする基盤的課題であり、現行手法は約20%の実世界成功率にとどまり改善の方向性が明確
   - **core**: Hello Robot Stretch（$25k）上のシミュレーション-実世界統合ベンチマーク。60 HSSDシーン、2535物体、129カテゴリ。ヒューリスティック（DETIC検出、セマンティックマッピング、フロンティア探索）とRL（DDPPO）のベースライン
   - **diff**: シミュレーションと実ハードウェアにまたがるマッチングAPIを持つ初の統合sim-to-realプラットフォーム。先行単一部屋/離散行動ベンチマークと異なり多部屋連続環境をサポート。固定物体セットではなくVLMによるopen-vocabulary対応
   - **limit**: 現行ベンチマーク版では把持が物理シミュレーションされていない。完全自然言語クエリは範囲外。再計画を伴うTAMP評価は未実施だが長期タスクには理想的

## Survey Methodology

### Search Review Checkpoint

- Papers presented to user: 48
- User additions: 0
- User removals: 0
- Target count adjustment: none
- Duplicates removed before checkpoint: ~60

### Search Log

#### Search Angle 1: Core Pick-and-Place

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | Semantic Scholar | `"robotic pick and place learning"` (2020+, limit=40) | 40/667 | 高関連性。RL、計画、ビジョンベースアプローチの混合 |
| 2 | Semantic Scholar | `"stable object placement robot"` (2020+, limit=40) | 40/2255 | 配置安定性、接触力学、触覚フィードバックに関する強い結果 |
| 3 | Semantic Scholar | `"robot grasp place manipulation"` (2020+, limit=40) | 40/2821 | 広範。器用ハンド、HRI、把持サーベイを含む |
| 4 | WebSearch | `"robotic pick and place learning 2024 2025 conference paper"` | 10 | ICLR 2025, CoRL 2024論文を発見 |
| 5 | WebSearch | `"stable object placement robot manipulation ICRA CoRL"` | 10 | AnyPlace, Paxton, Pick2Placeを確認 |
| 6 | WebSearch | `"pick and place policy learning robot 2023 2024"` | 10 | SimPLE, Diffusion Policyを確認 |
| 7 | OpenAlex | `"robotic pick and place learning"` (2020+, cited_by_count:desc) | 20/34363 | 過度に広範、一般ML/DLサーベイが上位。低収量 |

#### Search Angle 2: Grasp Planning + Placement

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | Semantic Scholar | `"grasp planning for placement"` (2020+, limit=40) | 40/83 | 高関連性：配置aware把持、joint計画 |
| 2 | Semantic Scholar | `"SE3 grasp pose estimation"` (2020+, limit=40) | 40/411 | 6-DoF把持ポーズ推定 |
| 3 | Semantic Scholar | `"6-DOF grasping neural network"` (2020+, limit=40) | 40/538 | 6-DoF把持検出ネットワーク |
| 4 | WebSearch | `"placement-aware grasping robot learning 2023 2024 2025"` | 10 | RoboCup、サーベイ論文 |
| 5 | WebSearch | `"6-DOF grasp detection deep learning robot 2022 2023 2024"` | 10 | NeuGraspNet、Rethinking 6-DoF |
| 6 | Semantic Scholar | `"Contact-GraspNet efficient 6-DoF"` | 5/19 | Contact-GraspNet (472 cites) 確認 |
| 7 | Semantic Scholar | `"SE3 diffusion fields grasp motion"` | 10/216 | SE(3)-DiffusionFields, SceneDiffuser確認 |

#### Search Angle 3: Sim-to-Real + Manipulation

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | Semantic Scholar | `"sim-to-real transfer robot manipulation"` (2020+, limit=40) | 40 | TRANSIC, DrEureka発見 |
| 2 | Semantic Scholar | `"reinforcement learning pick and place"` (2020+, limit=40) | 40 | RL for P&Pサーベイ、階層的分解 |
| 3 | Semantic Scholar | `"imitation learning robot manipulation grasping"` (2020+, limit=40) | 40 | Diffusion Policy、ACT、言語条件付きIL |
| 4 | WebSearch | `"sim-to-real manipulation policy learning 2023 2024 2025"` | 10 | TRANSIC, SIMPLERを確認 |
| 5 | WebSearch | `"imitation learning pick and place robot 2024 2025"` | 10 | Diffusion Policy拡張群 |

#### Search Angle 4: Foundation Models + Manipulation

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | Semantic Scholar | `"foundation model robot manipulation"` (2020+, limit=40) | 40 | RT-1, RT-2, SayCan中心 |
| 2 | Semantic Scholar | `"language conditioned robot manipulation pick place"` (2020+, limit=40) | 40 | CLIPort, 言語条件付き政策 |
| 3 | Semantic Scholar | `"vision language action model robot"` (2020+, limit=40) | 40 | OpenVLA, pi0, Octo |
| 4 | WebSearch | `"foundation model robotic manipulation survey 2024 2025"` | 10 | VLAサーベイ、IJRR基盤モデルサーベイ |
| 5 | WebSearch | `"VLA vision language action model robot 2024 2025"` | 10 | pi0, OpenVLA確認 |

#### Search Angle 5: Object Rearrangement + Pose

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | Semantic Scholar | `"object rearrangement robot learning"` (2020+, limit=40) | 40/9415 | NeRP, StructFormer, TarGF, Dream2Real |
| 2 | Semantic Scholar | `"stable placement prediction robot"` (2020+, limit=40) | 40/863 | Paxton, 6-DoFusion。足配置等の偽陽性あり |
| 3 | Semantic Scholar | `"tabletop rearrangement planning"` (2020+, limit=40) | 40/1350 | 計画アルゴリズム、デュアルアーム |
| 4 | Semantic Scholar | `"TAX-Pose task-driven cross-pose"` (2022+) | 10/861 | TAX-Pose (74 cites) 確認 |
| 5 | Semantic Scholar | `"StructDiffusion language-guided rearrangement"` (2022+) | 3/3 | StructDiffusion (67 cites) 確認 |
| 6 | WebSearch | `"object rearrangement robot learning 2023 2024 2025 CoRL RSS"` | 10 | CoRL/RSS論文確認 |
| 7 | WebSearch | `"tabletop object rearrangement planning 2022 2023 2024"` | 10 | ORLA*, Dynamic Buffers |

**Source summary**: Google via WebSearch (~20 queries), Semantic Scholar API (~30 queries), OpenAlex API (~2 queries, low yield), ar5iv (~30 accesses for full-text limit extraction), DBLP API (~21 queries for DOI resolution)

### DOI Resolution Log

- Papers with publisher DOI: 21 / 48
- Papers with PMLR/OpenReview identifier (no publisher DOI): 14
- Papers remaining arXiv-only (preprint): 5
- Papers with IEEE/RSS DOI confirmed: 8 (ICRA) + 2 (IROS) + 3 (RA-L) + 2 (T-RO) + 1 (Science Robotics) + 2 (CVPR/CVPR) + 3 (RSS)
- Resolution sources used: DBLP (21 queries)

| Paper | arXiv ID | Publisher DOI | Source | Notes |
|-------|----------|---------------|--------|-------|
| RT-1 | 2212.06817 | 10.15607/RSS.2023.XIX.025 | DBLP | RSS 2023 confirmed |
| Octo | 2405.12213 | 10.15607/RSS.2024.XX.090 | DBLP | RSS 2024 confirmed |
| Paxton et al. | 2108.12062 | — | DBLP | CoRL 2021, PMLR v164/paxton22a |
| Transporter | 2010.14406 | — | DBLP | CoRL 2020, PMLR v155/zeng21a |
| CLIPort | 2109.12098 | — | DBLP | CoRL 2021, PMLR v164/shridhar22a |
| Beyond P&P | 2110.06192 | — | DBLP | CoRL 2021, PMLR v164/lee22b |
| Learning to Regrasp | 2109.08817 | — | DBLP | CoRL 2021, PMLR v164/cheng22a |
| TarGF | 2209.00853 | — | DBLP | NeurIPS 2022 confirmed |
| SayCan | 2204.01691 | — | DBLP | CoRL 2022, PMLR v205/ichter23a |
| RT-2 | 2307.15818 | — | DBLP | CoRL 2023, PMLR v229/zitkovich23a |
| OpenVLA | 2406.09246 | — | DBLP | CoRL 2024, PMLR v270/kim25c |
| Dex-NeRF | 2110.14217 | — | DBLP | CoRL 2021, PMLR v164/ichnowski22a |
| Eisner et al. | 2404.13478 | — | DBLP | ICLR 2024, OpenReview 2inBuwTyL2 |
| HomeRobot | 2306.11565 | — | DBLP | CoRL 2023, PMLR v229/yenamandra23a |
| ManiSkill-HAB | 2412.13211 | — | DBLP | ICLR 2025, OpenReview 6bKEWevgSd |
| SIMPLER | 2405.05941 | — | DBLP | CoRL 2024, PMLR v270/li25c |
| 6-DoFusion | 2310.17649 | — | DBLP | Preprint only |
| AnyPlace | 2502.04531 | — | DBLP | Preprint only |
| Nadeau (phys. diff.) | 2509.21664 | — | DBLP | Preprint only |
| pi0 | 2410.24164 | — | DBLP | Preprint only |
| SoFar | 2502.13143 | — | DBLP | Preprint only |

注: CoRL (PMLR), NeurIPS, ICLRはpublisher DOIを発行しない。PMLR proceedings IDまたはOpenReview IDで一意に識別可能。

### Hallucination Check Results

- Papers checked: 48
- Passed: 48 (全論文がarXiv ID、DOI、またはvenueURL経由で確認済み)
- Failed and re-searched: 0
- Removed (unverifiable): 0

### Limit Field Coverage

- Papers with limit recorded: 47 / 48 (97.9%)
- Papers marked "limit not available": 1, breakdown:

| Category | Count | Papers | Action taken |
|----------|-------|--------|-------------|
| No arXiv / paywall | 1 | Tang2022_selective_rearrangement | CoRL PMLR proceedings確認、引用論文から制約情報を補足 |
