# Paper Catalogue — F/T Sensor-Based Inertial Parameter Estimation and Placement Planning

---

## A — Classical & Batch Estimation

古典的バッチ識別法の系譜は，Newton-Euler方程式を観測行列に線形化し，最小二乗法で慣性パラメータを一括推定するという枠組みを確立した。励起軌道の最適設計（観測行列の条件数最小化）は1990年代に理論的に整備され，以降の研究の標準的ベースラインとなっている。2020年代に入ってもFourier級数軌道の改良や周波数領域同定など，この枠組みの精緻化が続いている。

1. [[Atkeson1986_foundational]](../REFERENCES/MAIN.md#Atkeson1986_foundational) — Atkeson, An, Hollerbach, "Estimation of Inertial Parameters of Manipulator Loads and Links" (1986)
   - **DOI**: `10.1177/027836498600500306`
   - **thesis**: ロボットリンクおよびペイロードの慣性パラメータは，Newton-Euler方程式を観測行列に線形化してトルク・加速度データに最小二乗フィットすることで体系的に推定できる。
   - **core**: 各関節トルクを慣性パラメータに関して線形な観測行列で表現し，最小二乗法で全パラメータを一括推定するバッチ識別の基本枠組みを確立。
   - **diff**: 当時の手法が個別リンクを物理的直感で校正していたのに対し，本研究は系全体を統一的な線形回帰問題として定式化した最初の系統的アプローチである。
   - **limit**: 測定ノイズに対する感度分析や物理的整合性の保証がなく，観測行列の条件数を考慮した励起軌道設計は後続研究に委ねられた。

2. [[Gautier1992_excitation]](../REFERENCES/MAIN.md#Gautier1992_excitation) — Gautier, Khalil, "Exciting Trajectories for Identification of Base Inertial Parameters of Robots" (1992)
   - **DOI**: `10.1177/027836499201100408`
   - **thesis**: ロボットの基底慣性パラメータを高精度に同定するには，観測行列の条件数を最小化するよう設計された励起軌道が必要である。
   - **core**: Fourier級数で軌道を表現し，観測行列の条件数を最小化する係数をオフラインで最適化することで励起軌道を設計。
   - **diff**: Atkeson et al. (1986) が任意軌道を用いていたのに対し，本研究は同定精度に直結する指標（条件数）を明示的に最適化する設計手法を初めて提案した。
   - **limit**: 関節の速度・加速度制限や自己衝突回避などのロボット運動制約が最適化に組み込まれておらず，実機適用には追加の制約処理が必要。

3. [[Swevers1997_optimal]](../REFERENCES/MAIN.md#Swevers1997_optimal) — Swevers et al., "Optimal Robot Excitation and Identification" (1997)
   - **DOI**: `10.1109/70.631234`
   - **thesis**: 産業用ロボットの動力学モデル同定において，摩擦モデルを陽に含めた励起軌道の最適化と最小二乗推定を組み合わせることで，高精度な同定が実現できる。
   - **core**: Fourier級数軌道の係数を，観測行列の条件数と摩擦パラメータを含む拡張パラメータベクトルに対して同時最適化する枠組みを提案。
   - **diff**: 従来の軌道最適化が慣性パラメータのみを対象としていたのに対し，本研究は摩擦モデルを一体化した同定を実現した。
   - **limit**: 最適化が局所解に陥るリスクがあり，収束はFourier級数の次数と初期値に依存する。実時間推定への拡張は対象外。

4. [[Swevers2002_experimental]](../REFERENCES/MAIN.md#Swevers2002_experimental) — Swevers et al., "An Experimental Robot Load Identification Method for Industrial Application" (2002)
   - **DOI**: `10.1177/027836402761412449`
   - **thesis**: 産業現場での実用に耐えるロボットペイロード同定には，専用励起軌道と外部測定機器なしで動作可能な実験的手法が不可欠である。
   - **core**: 関節トルクセンサデータと最小二乗推定を組み合わせ，産業環境で実施可能な実験プロトコルを構築。摩擦補償を組み込んだ回帰モデルを使用。
   - **diff**: 学術的な最適励起軌道研究を産業適用レベルに落とし込み，実機での再現性と実用性を実証した点で先行研究と異なる。
   - **limit**: 専用の関節トルクセンサを必要とし，センサ非搭載の低コストロボットへの直接適用は困難。高速動作時の測定誤差の影響が残る。

5. [[Duan2022_ft_payload]](../REFERENCES/MAIN.md#Duan2022_ft_payload) — Duan, Liu, Bin, Cui, Dai, "Payload Identification and Gravity/Inertial Compensation for 6D F/T Sensor" (2022)
   - **DOI**: `10.3390/s22020439`
   - **thesis**: 手首搭載6軸F/Tセンサのペイロード慣性パラメータと重力・慣性力は，Fourier級数励起軌道の条件数最適化と最小二乗推定により，約10秒の短時間で高精度に同定できる。
   - **core**: 観測行列の条件数を最小化するFourier級数軌道を設計し，加速度計を内蔵したF/Tセンサから慣性加速度項も含めた12パラメータを最小二乗で一括推定。
   - **diff**: 従来の重力補償手法が静的ポーズのみで精度が低かったのに対し，本研究は動的慣性補償まで含めた同定を実現し，識別時間を60秒以上から約10秒に短縮。
   - **limit**: 加速度計内蔵型F/Tセンサという特殊なハードウェアが必要であり，正確なロボット運動学モデルへの依存度が高い。

6. [[Lambert2023_real2sim]](../REFERENCES/MAIN.md#Lambert2023_real2sim) — Lambert, Meier, Sodhi, Kaess, "Identifying Objects' Inertial Parameters for Real2Sim Assets" (2023)
   - **arXiv**: `Lambert23.pdf (MIT CSAIL)`
   - **thesis**: 標準的なロボットペイロード同定手法を，適切な励起軌道設計と摩擦モデリングを組み合わせることで，Real2Simパイプライン向けの精度の高い3Dアセット生成に実用的に適用できる。
   - **core**: Newton-Euler方程式から観測行列を構築し，Fourier級数励起軌道による最小二乗推定で質量・重心・慣性テンソルを同定。粘性・Coulomb・オフセット摩擦を陽に模型化。
   - **diff**: 既存のReal2Simパイプラインが物体の動力学を無視するか単純な質量分布仮定を置くのに対し，本研究はペイロード同定手法を系統的に適用した初期の取り組みの一つである。
   - **limit**: 著者による制約の明示的記載は利用不可。励起軌道の設計や摩擦モデルの選択が同定精度に与える影響の定量的分析は限定的。

7. [[Robert2026_spectral]](../REFERENCES/MAIN.md#Robert2026_spectral) — Robert, Krut, Company et al., "Spectral Identification of Inertial Parameters in Forced Sinusoidal Regimes" (2026)
   - **DOI**: `ASME JDSMC 148(4):041009`
   - **thesis**: 強制正弦波励起下での周波数領域識別（スペクトル解析）は，時間領域の最小二乗法よりも測定ノイズの影響を受けにくく，慣性パラメータの高精度推定を実現できる。
   - **core**: 正弦波励起軌道下でF/Tセンサ出力のDFTを取り，周波数ビンごとにNewton-Euler回帰を解くことで，時間領域ノイズの影響を抑制したスペクトル識別法を提案。
   - **diff**: Swevers et al. (1997, 2002) ら従来手法が時間領域最小二乗に基づくのに対し，本研究は周波数領域解析による雑音耐性の向上という新しいアプローチを取る。
   - **limit**: 強制正弦波という特定の励起形式に限定されており，汎用的な軌道への拡張や実時間適用については検討されていない。

8. [[Tian2024_excitation]](../REFERENCES/MAIN.md#Tian2024_excitation) — Tian et al., "Excitation Trajectory Optimization for Dynamic Parameter Identification Using Virtual Constraints" (2024)
   - **DOI**: `10.1109/ICRA57147.2024.10610950`
   - **thesis**: 動力学パラメータ同定用励起軌道の最適化を，自己衝突回避制約を考慮したまま計算効率よく解くには，条件数の代わりにFrobeniusノルムに基づくサロゲート目的関数を用いることが有効である。
   - **core**: グラム行列とその逆行列のFrobeniusノルム和が条件数の上界となることを定理として示し，このサロゲートをO(n)シンボリック勾配でIPOPTオプティマイザに埋め込んで衝突回避制約と同時最適化。
   - **diff**: Stürz et al. (2017) は衝突回避なしの単体識別に留まり，Tika et al. (2020) の条件数57,890に対して本手法では51を達成。
   - **limit**: IPOPT二段階最適化はグローバル最適を保証しない。関節A1のトルク誤差が運動範囲の制限により最大1.5 Nmに達する。

9. [[Lee2021_geometric_excitation]](../REFERENCES/MAIN.md#Lee2021_geometric_excitation) — Lee, Lee, Park, "Optimal Excitation Trajectories for Mechanical Systems Identification" (2021)
   - **DOI**: `10.1016/j.automatica.2021.109773`
   - **thesis**: 機械系の慣性パラメータ同定において，観測行列の幾何学的性質（特異値分布）を直接操作する励起軌道設計が，従来の条件数最小化よりも系統的な最適化を可能にする。
   - **core**: 観測行列の特異値に基づく幾何学的指標を目的関数とし，制約付き最適化で励起軌道を設計する枠組みを提案。
   - **diff**: Gautier & Khalil (1992) 以来の条件数最小化という目的関数に対し，より直接的な幾何学的指標を用いることで最適化の見通しを改善。
   - **limit**: 複雑な多関節ロボットへのスケーラビリティや，関節制約・自己衝突回避との統合については言及が限定的。

10. [[Hartwig2025_human_demo]](../REFERENCES/MAIN.md#Hartwig2025_human_demo) — Hartwig, Lienhardt, Henrich, "Estimation of Payload Inertial Parameters from Human Demonstrations by Hand Guiding" (2025)
    - **arXiv**: `2507.15604`
    - **thesis**: ペイロード慣性パラメータは，専用の励起軌道なしに手動誘導デモンストレーションの非接触フェーズから抽出できるが，十分な角度励起がなければ慣性テンソル推定は信頼性を欠く。
    - **core**: 手動誘導デモの自由運動区間からF/Tセンサと運動学データを抽出し，Newton-Euler方程式に非線形最小二乗（TLS, Ceres/Levenberg-Marquardt）をフィットして全パラメータを推定。
    - **diff**: Kubus et al. らは設計された正弦波軌道を必要とするのに対し，本手法は任意のヒューマンデモを受け入れ，非専門家にも利用可能な低障壁なアプローチを提供する。
    - **limit**: すべての手動誘導動作が十分な角度励起を提供するわけではない。慣性テンソル誤差は実験で200〜1200%に達し，意図的に設計された軌道の精度には及ばない。

---

## B — Online & Real-Time Estimation

オンライン推定法は，ロボット動作中にリアルタイムで慣性パラメータを更新し続けることで，ペイロード交換や環境変化に適応する能力を持つ。KFやRLSを中心としたオンライン推定は1990年代から研究されてきたが，物理整合性の保証や宇宙・ヒューマノイドなど特殊環境への拡張が近年の課題となっている。バイアスドリフトの逐次補正も，長時間稼働するロボットシステムにおける精度維持の重要な要素として注目されている。

1. [[Kubus2008_rtls]](../REFERENCES/MAIN.md#Kubus2008_rtls) — Kubus, Kroger, Wahl, "On-Line Estimation of Inertial Parameters Using Recursive Total Least-Squares" (2008)
   - **DOI**: `10.1109/IROS.2008.4650789`
   - **thesis**: ロボットがペイロードを把持した直後からリアルタイムに慣性パラメータを推定するには，測定誤差をモデル行列と観測ベクトルの両方に考慮する逐次全最小二乗法（RTLS）が適している。
   - **core**: 通常のRLSが観測ベクトルのみの誤差を仮定するのに対し，RTLSはモデル行列と観測ベクトル双方のノイズを考慮し，より統計的に整合した逐次推定を実現。
   - **diff**: 最小二乗法に基づく従来のバッチ手法と比較して，RTLSは動作中に逐次更新することでリアルタイム適応を可能にし，EIV（errors-in-variables）モデルを明示的に取り扱う。
   - **limit**: 低速運動（重力支配域）ではSNRが低下し，慣性力項の同定精度が著しく劣化する。物理的整合性の保証機構を持たず，非物理的な推定値が出力されうる。

2. [[Farsoni2018_realtime_kf]](../REFERENCES/MAIN.md#Farsoni2018_realtime_kf) — Farsoni, Landi et al., "Real-Time Payload Identification via Multirate Quaternion KF + RTLS" (2018)
   - **DOI**: not available (ICRA 2018)
   - **thesis**: マルチレートカルマンフィルタによるクォータニオンベースの姿勢推定とRTLSを組み合わせることで，F/Tセンサの微分ノイズを抑制しながらリアルタイムペイロード同定を実現できる。
   - **core**: 高レートの姿勢更新にクォータニオンKFを用い，その出力をRTLS識別器の入力として供給するマルチレートアーキテクチャにより，速度・加速度の数値微分に起因するノイズを低減。
   - **diff**: 単一レートのF/T生データを直接RTLSに入力する従来手法と異なり，姿勢フィルタリングを前段に置くことで同定精度を改善。
   - **limit**: カルマンフィルタのプロセスノイズ・観測ノイズの調整が精度に大きく影響し，適切なチューニングが実用上の障壁となる。

3. [[Gaz2017_coefficients]](../REFERENCES/MAIN.md#Gaz2017_coefficients) — Gaz, De Luca, "Payload Estimation Based on Identified Coefficients of Robot Dynamics" (2017)
   - **DOI**: `10.1109/IROS.2017.8206142`
   - **thesis**: ロボット自体の動力学係数をあらかじめ識別しておくことで，ペイロードによる動力学変化分からペイロード慣性パラメータを分離・推定できる。
   - **core**: ロボット空荷時の識別済み動力学係数を基準として，ペイロード装着後のトルク残差から慣性パラメータを推定する差分アプローチ。
   - **diff**: 従来のペイロード同定がロボットとペイロードを同時推定するのに対し，本手法はロボット動力学を先に識別して固定し，ペイロード推定問題を簡略化する。
   - **limit**: ロボット自体の動力学モデルの精度に強く依存し，モデル誤差がペイロード推定に直接波及する。動的に変化するロボット特性（摩耗等）への追従が困難。

4. [[Chu2017_space]](../REFERENCES/MAIN.md#Chu2017_space) — Chu, Ma, Hou, Wang, "Inertial Parameter Identification Using Contact Force for Space Manipulator" (2017)
   - **DOI**: `10.1016/j.actaastro.2016.11.019`
   - **thesis**: 宇宙マニピュレータが捕捉した物体の慣性パラメータは，接触力センサ情報を用いたモメンタムベース推定法により，微小重力環境下でも同定できる。
   - **core**: 微小重力下での浮遊物体の運動量変化と接触力の関係を利用し，関節トルクと接触力の測定から慣性パラメータを推定するモメンタムベース回帰法。
   - **diff**: 地上ロボットの慣性同定手法をそのまま適用することが困難な微小重力環境に対し，モメンタム保存則を基礎にした宇宙特有の識別アプローチを提案。
   - **limit**: 剛体構造を仮定しており，可撓性ある宇宙構造物への適用は困難。実際の宇宙環境でのセンサノイズや外乱の影響評価が限定的。

5. [[Uchida2025_space_rls]](../REFERENCES/MAIN.md#Uchida2025_space_rls) — Uchida, Richard, Uno, Olivares-Mendez, Yoshida, "Online Inertia Parameter Estimation for Unknown Objects Grasped by a Manipulator" (2025)
   - **arXiv**: `2512.21886`
   - **thesis**: 自由浮遊宇宙ロボットの慣性パラメータ推定を信頼性高く行うには，モメンタム保存ベース回帰と対数行列式ダイバージェンス正則化を組み合わせて擬慣性行列の物理整合性を担保する必要がある。
   - **core**: モメンタムベース回帰器で加速度依存性を排除しつつ，擬慣性行列への幾何学的（対数行列式ダイバージェンス）正則化で正定値性を強制し，従来の宇宙ロボットRLS定式化にない物理整合性を実現。
   - **diff**: Abiko et al.，Xu et al. らの先行宇宙ロボット推定器はモメンタム保存を用いたが物理整合性を保証しなかった。本研究は地上ロボット用の幾何学的正則化を自由浮遊軌道ケースに初めて適用した。
   - **limit**: 剛体構造を仮定（柔軟性は無視），識別可能性は軌道の豊富さに依存，実ハードウェアでの検証は今後の課題。

6. [[Foster2024_humanoid_adaptation]](../REFERENCES/MAIN.md#Foster2024_humanoid_adaptation) — Foster, McCrory et al., "Physically Consistent Online Inertial Adaptation for Humanoid Loco-manipulation" (2024)
   - **arXiv**: `2405.07901`
   - **thesis**: 未知ペイロードを持つヒューマノイドのロコマニピュレーションタスクを確実に実行するには，log-Cholesky再パラメータ化によって物理整合性を構造的に保証するEKFによるオンライン慣性推定が有効である。
   - **core**: log-Cholesky再パラメータ化で慣性パラメータを非制約空間にマッピングし，任意の推定値が物理的に実現可能な剛体に対応することを保証。オフライン識別の公称モデルに対する差分をEKFで逐次更新。
   - **diff**: 大半の先行慣性識別はオフラインで物理整合性を保証しない。従来の適応制御はコントローラへの密な結合を要するが，本手法は独立した推定モジュールとして機能する。
   - **limit**: オフライン公称パラメータの不完全さが状態依存バイアスを引き起こす。歩行中の接触過渡が推定スパイクを発生させ，手動チューニングのイノベーションゲーティングが必要。

7. [[Bai2025_sensorless_hri]](../REFERENCES/MAIN.md#Bai2025_sensorless_hri) — Bai et al., "Sensorless HRI: Real-Time Estimation of Co-Grasped Object Mass and Human Wrench" (2025)
   - **DOI**: `10.1002/aisy.202400616`
   - **thesis**: センサレスHRI（ヒューマン・ロボット・インタラクション）環境下で共把持された物体の質量と人間が加えるレンチを同時にリアルタイム推定できる。
   - **core**: ロボット関節トルク情報のみを用い，人間の入力レンチとペイロード慣性パラメータを同時に推定する逐次推定アルゴリズムを構築。外部F/Tセンサを排除。
   - **diff**: 外部センサに依存する従来のHRI質量推定と異なり，ロボット固有の関節センサのみで共把持物体と人間入力の分離推定を実現。
   - **limit**: 人間の入力レンチが未知であるため分離推定の収束条件が複雑。高ダイナミクス動作や突発的な人間動作への追従性が課題。

8. [[Nadeau2024_bias]](../REFERENCES/MAIN.md#Nadeau2024_bias) — Nadeau, Rogel Garcia, Wise, Kelly, "Automated Continuous Force-Torque Sensor Bias Estimation" (2024)
   - **arXiv**: `2403.01068`
   - **thesis**: F/Tセンサのバイアスドリフトを継続的にオンライン推定するには，ジャーク入力を仮定したカルマンパイプラインで運動学推定とバイアス追跡を統合する三段階構造が有効である。
   - **core**: ジャークノイズモデルを用いた関節状態カルマンフィルタが運動学推定を提供し，その出力を受けたバイアス推定カルマンフィルタがバイアスとそのドリフトレートを継続追跡。
   - **diff**: 先行のオンラインバイアス推定法は原理的なジャークノイズ運動学モデルを統合していなかった。本手法は周期的な再校正ではなく，常時稼働するパイプラインを提供する。
   - **limit**: F/Tセンサより遠位に装着されたグリッパの慣性パラメータが既知であることを前提とする。グリッパ特性の不確かさはバイアス推定を汚染する。

---

## C — Physical Consistency & Identifiability

慣性パラメータの物理整合性（正の質量，正半定値慣性テンソル，三角不等式等）を識別の段階で保証することは，モデルの現実妥当性と下流制御の安定性に直結する。LMI/SDP定式化は2010年代に確立され，SO(3)多様体上の直接最適化や浮動ベースロボットへの拡張が近年の発展として注目される。安全な識別軌道の生成を物理整合性保証と統合する試みも新たな研究フロンティアを形成している。

1. [[Sousa2014_lmi]](../REFERENCES/MAIN.md#Sousa2014_lmi) — Sousa, Cortesao, "Physical Feasibility of Robot Base Inertial Parameter Identification: LMI Approach" (2014)
   - **DOI**: `10.1177/0278364913514870`
   - **thesis**: ロボット基底慣性パラメータの同定において物理的実現可能性（正の質量・正半定値慣性行列）を保証するには，線形行列不等式（LMI）制約を持つ凸最適化として問題を定式化すべきである。
   - **core**: 慣性パラメータの物理整合性条件をLMI制約として定式化し，最小二乗コストを持つ凸半正定値計画（SDP）として解くことで，物理的に実現可能なパラメータ推定を保証。
   - **diff**: 無制約最小二乗法が非物理的な推定値（負の質量など）を出力しうるのに対し，本研究は凸最適化により物理整合性を構造的に保証した最初期の主要研究の一つ。
   - **limit**: 正半定値慣性行列と正の質量のみを要求し，主軸慣性モーメントの三角不等式（より厳しい必要十分条件）は考慮されていない。

2. [[Traversaro2016_manifold]](../REFERENCES/MAIN.md#Traversaro2016_manifold) — Traversaro, Brossette, Escande, Nori, "Identification of Fully Physical Consistent Inertial Parameters Using Optimization on Manifolds" (2016)
   - **DOI**: `10.1109/IROS.2016.7759801`
   - **thesis**: 標準的な物理整合性条件（正の質量・正半定値慣性）は必要条件に過ぎず，慣性テンソルの三角不等式を追加で満たす完全物理整合再パラメータ化が必要十分条件であり，多様体最適化で実現できる。
   - **core**: 慣性パラメータを主軸姿勢（SO(3)），主慣性モーメント，重心，質量で再パラメータ化し，この空間上で多様体最適化を直接実行することで構造的に完全物理整合を保証。
   - **diff**: 先行のSDP手法は正半定値条件を満たすが三角不等式を無視し非物理的解を許容していた。本研究が初めて必要十分条件を満たすパラメータ化を提供した。
   - **limit**: 単一剛体の同定のみを実証。多体構造への拡張は将来課題として明示されている。

3. [[Janot2021_sdp]](../REFERENCES/MAIN.md#Janot2021_sdp) — Janot, Wensing, "Sequential SDP for Physically and Statistically Consistent Robot Identification" (2021)
   - **DOI**: `10.1016/j.conengprac.2020.104699`
   - **thesis**: ロボット慣性パラメータの同定において，物理整合性と統計的整合性（最良線形不偏推定）を同時に達成するには，逐次半正定値計画（SDP）による段階的最適化が有効である。
   - **core**: 第一段階で無制約最小二乗推定を行い，第二段階でLMI/SDP制約を課して物理整合性を修正することで，物理整合性と統計効率の両立を実現。
   - **diff**: Sousa & Cortesao (2014) が制約付きSDPを直接解くのに対し，本手法は二段階化により統計的最適性を保ちつつ計算効率を改善。
   - **limit**: 逐次アプローチは真のグローバル最適（同時最適化）を保証しない。三角不等式を含む完全物理整合性については Traversaro et al. (2016) の枠組みに比べて劣る。

4. [[Khorshidi2024_contact_id]](../REFERENCES/MAIN.md#Khorshidi2024_contact_id) — Khorshidi et al., "Physically-Consistent Parameter Identification of Robots in Contact" (2024)
   - **arXiv**: `2409.09850`
   - **thesis**: 接触状態にある浮動ベースロボットの全身慣性パラメータ同定は，接触制約のヤコビアンのヌル空間への動力学射影と凸LMI最適化を組み合わせることで，F/Tセンサなしに関節トルク測定だけから解くことができる。
   - **core**: 浮動ベース全身動力学回帰器を接触ヤコビアンのヌル空間に射影して未測定の接触力への依存を除去し，物理整合性制約を持つ凸LMI問題として帰着。
   - **diff**: 先行手法はエンドエフェクタや力プレートでのF/T計測を必要とした。本研究はWensing et al. のLMI枠組みを固定ベースから接触あり浮動ベースロボットへと初めて拡張。
   - **limit**: 接触パラメータ自体は同定問題に含まれていない。適応MPC制御器との統合は将来課題として残る。

5. [[RSS2025_safe_id]](../REFERENCES/MAIN.md#RSS2025_safe_id) — (Univ. Michigan), "Provably-Safe, Online System Identification" (2025)
   - **arXiv**: `2504.21486`
   - **thesis**: ロボット動作中に衝突回避を保証しながらエンドエフェクタ慣性パラメータの厳密な過大近似境界をオンラインで計算することは，安全軌道プランナとモメンタムベース区間演算識別法の組み合わせにより実現可能である。
   - **core**: モメンタムベース回帰器と摂動論的区間演算を組み合わせて厳密な保守的パラメータ境界を計算。5次ベジエ曲線プランナが衝突安全性を証明可能に保証しながら励起軌道を生成。
   - **diff**: 先行の励起軌道最適化手法は回帰行列の条件数を最適化したが識別中の安全性を無視。唯一の先行安全識別研究はサンプリングベースプランナでサンプル間の安全性を保証できなかった。
   - **limit**: 5次ベジエ曲線はFourierベース軌道より条件数が大きい。log-Cholesky再パラメータ化が厳密な区間境界計算を複雑にする。識別はタスク実行前に行うため総完了時間が増加する。

---

## D — Cobot-Adapted & Sensor-Fusion Estimation

協働ロボット（コボット）の低速・安全優先動作環境では，従来の動的識別が重力支配のSNR問題に直面する。視覚・触覚・関節センサの融合，学習ベースのアプローチ，そしてコボット速度域に特化した物理整合推定法が近年活発に研究されている。外部センサ非依存の「センサレス」識別とオンラインキャリブレーションの高速化も重要な研究トレンドを形成している。

1. [[Nadeau2022_fast_cobot]](../REFERENCES/MAIN.md#Nadeau2022_fast_cobot) — Nadeau, Giamou, Kelly, "Fast Object Inertial Parameter Identification for Collaborative Robots" (2022)
   - **DOI**: `10.1109/ICRA46639.2022.9916213`
   - **thesis**: コボットの安全速度制限下では重力支配のSNR問題で標準最小二乗識別が失敗する。Point Mass Discretization法が重力専用モデルと完全動力学モデルを適応的に混合することで，わずか1.5秒のコボット速度動作から正確な質量と重心を回復できる。
   - **core**: PMDはオブジェクトを離散点質量（形状既知の位置）で表現し凸プログラムを解く。動態信号のtanhベース重み関数で重力専用縮約モデルと完全動力学モデルを混合し物理整合性を保証。
   - **diff**: Atkeson et al. (1986) やKubus et al. (2008, RTLS) はノイズに敏感で低速時に非物理的結果を出す。PMDは完全なコボット速度域を保証付き物理整合性で初めて扱う。
   - **limit**: 点質量配置に物体形状の事前知識が必要。完全慣性テンソルは重力支配動作のみからは識別不可（質量と重心のみ観測可能）。

2. [[Nadeau2023_visual_parts]](../REFERENCES/MAIN.md#Nadeau2023_visual_parts) — Nadeau, Giamou, Kelly, "The Sum of Its Parts: Visual Part Segmentation for Inertial Parameter Identification" (2023)
   - **DOI**: `10.1109/ICRA48891.2023.10160394`
   - **thesis**: 協働ロボットでの慣性パラメータ識別は，視覚的部品セグメンテーションによって未知数を10から部品ごとの質量に削減することで，停止後の静的F/T読み取りだけでも高精度に実施できる。
   - **core**: Homogeneous Part Segmentationが表面ベース点群クラスタリングと体積的階層四面体クラスタリングで均一密度部品に分割。部品形状が判明すれば，静的ポーズのF/Tから各部品質量のみを推定。
   - **diff**: 従来手法（OLS，GEO）は10パラメータ同時推定に動的励起が必要で低励起動作時に非物理的推定を出す。本手法は視覚構造を活用して未知数を削減し静的ポーズで十分にする。
   - **limit**: 均一密度部品仮定が必要で，異なる密度の部品が誤マージされると失敗。静的ポーズは質量と重心のみを識別可能で完全慣性テンソルは推定不可。

3. [[Baek2024_humanoid_learning]](../REFERENCES/MAIN.md#Baek2024_humanoid_learning) — Baek, Peng, Gupta, Ramos, "Online Learning-Based Inertial Parameter Identification for Wheeled Humanoids" (2024)
   - **arXiv**: `2309.09810`
   - **thesis**: ヒューマノイドロボットは，シミュレーションで学習したLSTMネットワークと三段階シムトゥリアルパイプラインを用いることで，把持物体の全慣性パラメータを固有感覚関節データのみから0.5秒以内に識別できる。
   - **core**: PSO（粒子群最適化）によるロボット系識別でシミュレーションを実機に合わせ，残差誤差をGPでモデル化。5,000軌道で学習した物理整合正則化損失付きLSTMが0.5秒の振り動作から全慣性パラメータを推定。
   - **diff**: 先行の学習ベース手法は質量と重心のみ識別。F/Tセンサ手法は35秒の励起が必要でドリフトしやすい。本研究がF/Tセンサなしで1秒以内に全慣性パラメータを推定した最初の事例。
   - **limit**: 慣性行列を対角近似。推定は軌道依存でリアルタイム適応性を欠く。大きな物体に対して性能が劣化する。

4. [[Chen2025_differentiable]](../REFERENCES/MAIN.md#Chen2025_differentiable) — Chen, Liu, Ma et al., "Learning Object Properties Using Robot Proprioception via Differentiable Robot-Object Interaction" (2025)
   - **arXiv**: `2410.03920`
   - **thesis**: 物体の物理特性（質量・弾性率）は，外部センサや視覚なしにロボット関節エンコーダデータだけから，微分可能シミュレーションによる逆問題として識別できる。
   - **core**: 物体操作中の関節エンコーダでのロボット力学反応を観測として，微分可能物理シミュレータを通じて逆方向にバックプロパゲーションし物体パラメータを回復。
   - **diff**: 先行研究はロボット固有データからロボット特性を，物体固有センサから物体特性を識別していた。本手法はロボット側固有感覚測定のみから物体特性を抽出する点で新規。
   - **limit**: 管理上の問題によりarXivから削除された論文（ライセンス問題）。著者が明示した制限の記述は利用不可。

5. [[Shan2024_fast_calibration]](../REFERENCES/MAIN.md#Shan2024_fast_calibration) — Shan, Pham, "Fast Payload Calibration for Sensorless Contact Estimation Using Model Pre-training" (2024)
   - **arXiv**: `2409.03369`
   - **thesis**: 多様なペイロード設定での事前学習により，ペイロード適応型ニューラルネットワークが4秒以内のオンラインキャリブレーションを実現できる。これはペイロード残差の予測を学習することで達成される。
   - **core**: Payload-adaptive Model（PaPM）が短いキャリブレーション軌道をコンパクトなPayload Indicatorベクトルにエンコードし，ロード時と空荷時の動力学残差を予測する統一MLPを条件付け。
   - **diff**: 先行の事前学習研究（Selingue et al. 2023）はペイロード質量の事前知識を要求したが，PaPMはキャリブレーション軌道からペイロード特徴を自律的に抽出する。
   - **limit**: 大規模訓練データへの依存がポータビリティを制限。ペイロードパラメータ化は質量と重心のみ調整し慣性変化を除外。低速協調動作に制限。

6. [[Jin2025_ugraph]](../REFERENCES/MAIN.md#Jin2025_ugraph) — Jin, Mo, Yuan, "Learning to Double Guess: Active Perception for Estimating CoM (U-GRAPH)" (2025)
   - **arXiv**: `2502.02663`
   - **thesis**: 任意の実世界物体に対して正確な3D重心推定を行うには，センサ不精度と物体多様性により単一F/T読み取りが不十分なため，不確実性に基づいて2回目の計測姿勢を能動的に選択する必要がある。
   - **core**: ベイズニューラルネットワークが6D F/T読み取りとグリッパ姿勢から不確実性付き3D重心推定を生成し，補完的ActiveNetが不確実性を最大削減する次姿勢をスコアリング。両推定をベイズ事後更新で融合。
   - **diff**: 先行手法（Hyland et al. のプッシング，McGovern et al. のシミュレーション専用）は高々2D重心または制限物体クラスに対応。U-GRAPHは連続姿勢能動知覚による任意未見実物体の3D重心推定を初めて実現。
   - **limit**: 訓練重量範囲外（43.4〜613.2 g）の物体で性能劣化。重大なスリップが重い/偏心重心物体で課題。収束保証のための最適計測回数は将来課題。

7. [[RobotScale2023]](../REFERENCES/MAIN.md#RobotScale2023) — various, "RobotScale: Framework for Adaptable Estimation of Static and Dynamic Object Properties" (2023)
   - **DOI**: `10.1109/RO-MAN57019.2023.10309315`
   - **thesis**: ロボットが把持した物体の静的・動的特性を適応的に推定するための汎用フレームワークは，異なる推定モードと物体種別にスケーラブルに対応できる。
   - **core**: 静的（重力方向の力から質量推定）と動的（励起動作からの完全パラメータ推定）の複数推定モードを統一フレームワークで管理し，物体種別や利用可能センサに応じてモードを選択。
   - **diff**: 既存の慣性識別手法が特定の推定モードに特化するのに対し，本フレームワークは状況適応的なモード選択と複数物体カテゴリへの対応を統一的に提供する。
   - **limit**: 公開論文情報が限定的であり，アルゴリズム詳細と包括的な実験評価の全容は把握が困難。

8. [[Wang2021_fingertip]](../REFERENCES/MAIN.md#Wang2021_fingertip) — Wang, Zang, Zhang et al., "Parameter Estimation and Object Gripping Based on Fingertip F/T Sensors" (2021)
   - **DOI**: `10.1016/j.measurement.2021.109479`
   - **thesis**: 指先搭載F/Tセンサを用いることで，把持時の接触力情報から物体慣性パラメータを推定し，より安定した把持制御に活用できる。
   - **core**: 指先F/Tセンサの測定値から接触力分布と物体への作用力を推定し，静力学・動力学方程式から物体の質量・重心・慣性テンソルを識別するアルゴリズムを構築。
   - **diff**: 手首搭載センサを用いた従来手法と異なり，指先近傍での接触力直接測定により接触点詳細情報を活用した推定が可能。
   - **limit**: 指先センサの設置位置と数に依存した精度制約があり，把持状態での相対運動の計測誤差がパラメータ推定に波及する。

9. [[Yu2022_bias_gravity]](../REFERENCES/MAIN.md#Yu2022_bias_gravity) — Yu, Shi, Lou, "Bias Estimation and Gravity Compensation for Wrist-Mounted F/T Sensor" (2022)
   - **DOI**: `10.1109/JSEN.2022.3170969`
   - **thesis**: 手首搭載F/Tセンサのバイアスと重力補償パラメータを同時推定することで，正確な外力測定に必要なセンサ校正を効率的に実施できる。
   - **core**: 複数の静的姿勢でのF/T測定から，センサバイアスとペイロード重力パラメータ（質量・重心）を同時推定する線形最小二乗アプローチ。重力方向を既知として利用。
   - **diff**: バイアス推定と重力補償を別々に行う従来の二段階手法に対し，統一的な同時推定で工程を簡略化し相互依存誤差を低減。
   - **limit**: 静的ポーズのみを用いるため動的慣性補償項は考慮されない。センサの温度ドリフトなど時変バイアスへの対応は言及されていない。

10. [[Farsoni2019_safety]](../REFERENCES/MAIN.md#Farsoni2019_safety) — Farsoni, Ferraguti et al., "Safety-Oriented Robot Payload Identification Using Collision-Free Path Planning" (2019)
    - **DOI**: `10.1016/j.rcim.2019.04.011`
    - **thesis**: ロボットペイロード識別専用の励起軌道は，衝突回避経路計画と統合することで産業環境でも安全に実施可能であり，識別精度と安全性の両立ができる。
    - **core**: 安全制約（自己衝突・環境衝突回避）を考慮した経路計画と識別励起最適化を統合し，実産業環境での安全なペイロード同定プロトコルを構築。
    - **diff**: 従来の励起軌道最適化は識別精度のみを追求し安全制約を後処理で付加していたのに対し，本研究は安全性を設計段階から組み込む。
    - **limit**: 事前の環境モデル（衝突回避用）が必要。安全制約の強さによっては励起品質が大幅に低下し識別精度とのトレードオフが生じる。

11. [[Farsoni2022_hrc]](../REFERENCES/MAIN.md#Farsoni2022_hrc) — Farsoni, Bonfe, "Complete and Consistent Payload Identification During HRC" (2022)
    - **DOI**: `10.1007/978-3-030-96359-0_2`
    - **thesis**: ヒューマン・ロボット協調（HRC）作業中に，人間の動きを阻害することなく完全で整合したペイロード慣性パラメータを識別できる。
    - **core**: HRC文脈での安全制約（人間との干渉回避）を維持しながら，適切な動的励起を確保するペイロード識別プロトコルを設計。物理整合性制約を識別最適化に組み込む。
    - **diff**: 従来のペイロード識別は人間不在の孤立環境を前提としていた。本研究はHRC文脈での識別という実用上重要だが研究が少ない問題に取り組む。
    - **limit**: HRCシナリオ下では利用可能な励起軌道が制限され，特に高ダイナミクスな動作が制約される。人間の予測不能な動きへのロバスト性が課題。

12. [[Liu2025_twostage]](../REFERENCES/MAIN.md#Liu2025_twostage) — Liu, Li, Duan et al., "Two-Stage Payload Dynamic Parameter Identification for Interactive Industrial Robots" (2025)
    - **DOI**: `10.1109/TASE.2025`
    - **thesis**: インタラクティブ産業ロボットのペイロード動力学パラメータ識別において，二段階アプローチ（初期粗推定から精密識別への段階的精緻化）が実用的な精度と効率のバランスを実現する。
    - **core**: 第一段階で低コストの初期推定（静的または低動的）を行い，第二段階で最適励起軌道を用いた精密識別を実施する二段階識別プロトコル。前段の推定を後段の初期値として活用。
    - **diff**: 単一段階での識別に比べ，二段階化により各段階の最適化問題を簡略化し，収束速度と最終精度を改善する。インタラクティブ動作環境への適応性も向上。
    - **limit**: 二段階構造により総識別時間が増加する可能性。第一段階の推定精度が第二段階の収束に影響するため，初期推定が極端に悪い場合は精密識別が失敗しうる。

---

## E — Stable Placement Planning

安定配置計画は，接触幾何・物理安定性・意味的文脈の三要素を統合する挑戦的な問題領域である。F/Tフィードバックによる実接触ベースのループ閉結から，微分可能シミュレーション，拡散モデル，品質多様性最適化まで，近年多様なアプローチが提案されている。物理ベースと学習ベースの融合が現在の研究主流を形成しており，特に未知物体への汎化と計画効率の改善が重要課題として残っている。

1. [[Nadeau2025_contact_robustness]](../REFERENCES/MAIN.md#Nadeau2025_contact_robustness) — Nadeau, Kelly, "Stable Object Placement Planning From Contact Point Robustness" (2025)
   - **DOI**: `10.1109/TRO.2025.3577049`
   - **thesis**: 物理ベース静的ロバスト性指標でランク付けされた接触点を優先的にサンプリングすることで，従来のポーズ優先サンプリングより高速かつ安定した配置計画が実現できる。
   - **core**: 摩擦コーン滑り解析と凸包転倒解析を組み合わせた静的ロバスト性ヒューリスティックで接触点をウェイト付けし，適合する物体点と有効なポーズを導出するパイプライン。
   - **diff**: 先行プランナがポーズをサンプリングして事後にシミュレーションで安定性を評価し8〜20倍遅くなるのに対し，本研究は探索空間を事前に刈り込むパイプラインを反転させる。
   - **limit**: 摩擦コーンの角錐近似を使用。配置が線形・単調・逐次であることを仮定し，一度配置した物体を再配置できない。

2. [[Nadeau2025_diffusion_placement]](../REFERENCES/MAIN.md#Nadeau2025_diffusion_placement) — Nadeau, Rogel, Bilic, Petrovic, Kelly, "Generating Stable Placements via Physics-guided Diffusion Models" (2025)
   - **arXiv**: `2509.21664`
   - **thesis**: 物理ベースのロバスト性ガイダンス信号を推論時に拡散生成に注入することで，シミュレーションや再学習なしに安定配置生成が実現できる。
   - **core**: 接触品質・表面法線整合・シーンロバスト性をエンコードした微分可能安定性損失を，点群条件付き配置ポーズの拡散サンプリング中のガイダンスとして使用し追加学習不要。
   - **diff**: 先行の幾何手法は候補ごとに高コストのシミュレーションが必要。本研究はシミュレーションを勾配ベースガイダンスで置換し，47%の高速化と56%のよりロバストな配置を達成。
   - **limit**: 滑り・転がり効果が安定性を損なう表面では未評価。点群表現が浸透誤差を増加させる場合がある。物体モデルが必要。

3. [[Lerner2024_ft_placement]](../REFERENCES/MAIN.md#Lerner2024_ft_placement) — Lerner, Tam, Equi, "Precise Object Placement Using Force-Torque Feedback" (2024)
   - **arXiv**: `2404.17668`
   - **thesis**: 物体スタッキングの最終接触フェーズでは，F/Tフィードバックがトルク不均衡を検出して安定平衡に向けて反復的に再配置することで，視覚の代替となりうる。
   - **core**: 準静的着地時にレンチ平衡方程式から接触位置と表面法線を推定。ロボットが物体重心を接触点上に移動するまでトルクがゼロに近づくよう反復的にシフト。
   - **diff**: 視覚のみまたは学習ベースの配置手法と異なり，物理平衡ループを直接センサ測定でクローズする。
   - **limit**: 反復調整ステップが必要な場合のアルゴリズム発散により成功率が17%に留まる。主に平坦な物体と垂直アプローチ方向に制限。

4. [[Li2024_diff_contact]](../REFERENCES/MAIN.md#Li2024_diff_contact) — Li, Yang, Shao, Hsu, "Differentiable Contact Dynamics for Stable Object Placement Under Geometric Uncertainties" (2024)
   - **arXiv**: `2409.17725`
   - **thesis**: 接触力を幾何学パラメータに関して微分化することで，F/T測定から物体と環境の幾何不確実性をオンライン推定できる統一フレームワークが構築できる。
   - **core**: 微分可能シミュレータが予測接触レンチの幾何パラメータに対する勾配を伝播。粒子ベース勾配降下が予測F/T測定値と実測値の不一致を最小化。
   - **diff**: 先行の微分可能シミュレータは幾何パラメータに関する微分をサポートしない。既存の接触ベース推定手法は特定の不確実性タイプのみを処理する。
   - **limit**: 1アクションあたり3.36秒の計算時間により準静的タスクのみ実行可能。幾何不確実性に限定。各URDFの微分関数を手動で指定する必要がある。

5. [[Lee2023_spots]](../REFERENCES/MAIN.md#Lee2023_spots) — Lee et al., "SPOTS: Stable Placement of Objects with Reasoning in Semi-Autonomous Teleoperation" (2023)
   - **DOI**: `10.1109/ICRA57147.2024.10611613`
   - **thesis**: 物理ベースの安定性シミュレーションとLLM意味推論を組み合わせることで，半自律テレオペレーションに適した文脈的かつ物理的に安定した配置候補が生成できる。
   - **core**: MuJoCoでのリアルツーシムシーン再構成が摂動前向き動力学で安定性候補を評価。VLM/GPTが意味的適切性を割り当て。カーネル密度推定が両スコアを統合。
   - **diff**: 先行のLLMベース配置手法が意味推論のみに依存し物理安定性検証を欠くのに対し，SPOTSは大幅に少ないトークンで物理シミュレーションステージを追加。
   - **limit**: 精度の高いオープン語彙物体検出，既知の物体スーパーセット，リアルツーシム再構成用のCADモデルが必要。

6. [[Ferrad2025_placeit]](../REFERENCES/MAIN.md#Ferrad2025_placeit) — Ferrad, Huber et al., "Placeit! A Framework for Learning Robot Object Placement Skills" (2025)
   - **arXiv**: `2510.09267`
   - **thesis**: 品質多様性最適化によりシミュレーション内で多様な安定配置ポーズの大規模アーカイブを自動生成することで，手動データ収集なしにデータ駆動型配置ポリシーが構築できる。
   - **core**: CMA-MAE品質多様性アルゴリズムがシミュレーション内のSE(3)配置パラメータ空間を探索。摂動を伴うドメインランダム化が不安定な平衡をフィルタリング。
   - **diff**: 先行の配置データ生成が幾何ヒューリスティックやランダムサンプリングに依存するのに対し，QD最適化が解空間を系統的にカバーし全ベースラインを上回る。
   - **limit**: シミュレーション品質（メッシュ精度・慣性特性・接触モデリング）への強い依存。剛体非変形物体に限定。

7. [[Zhao2025_anyplace]](../REFERENCES/MAIN.md#Zhao2025_anyplace) — Zhao et al., "AnyPlace: Learning Generalized Object Placement for Robot Manipulation" (2025)
   - **arXiv**: `2502.04531`
   - **thesis**: 物体配置をVLMによる高レベル位置提案と合成データで学習した拡散ベースSE(3)姿勢予測に分解することで，多様な実世界物体への汎化可能な配置が実現できる。
   - **core**: MolmoのVLMとSAM-2セグメンテーションが2D配置キーポイントを特定。拡散トランスフォーマーが切り取り点群からSE(3)変換を予測し，完全に合成データで学習。
   - **diff**: 先行手法（RPDiff）はタスク固有の実世界データセットを必要とする。AnyPlaceは合成データのみの学習で多モード挿入において92.74%対16.51%の成功率を達成。
   - **limit**: 全ての安定配置に対して把持ポーズの互換性が保証されない。低レベルモジュールに言語条件付けがない。

8. [[Haustein2019_placement]](../REFERENCES/MAIN.md#Haustein2019_placement) — Haustein, Hang, Stork, Kragic, "Object Placement Planning and Optimization for Robot Manipulators" (2019)
   - **arXiv**: `1907.02555`
   - **thesis**: アーム・面・領域の階層構造（AFR）とMCTSによる目的最適化を統合した配置・動作計画が，乱雑な環境でのナイーブな棄却サンプリングを上回る性能を示す。
   - **core**: 三レベルAFR階層が配置探索空間を整理。UCB1を用いたMCTSが空間実現可能性の相関を活用してユーザ定義目的と衝突回避の自由な構成をサンプリング。
   - **diff**: 先行の配置研究は実行可能な表面を特定することに注力し，障害物間のリーチャビリティとユーザ定義目的を同時最適化しなかった。
   - **limit**: 衝突回避退避制約を除外。把持は既知と仮定。水平面配置のみに限定。

---

## F — CoM-Informed Downstream Manipulation

重心（CoM）情報は把持計画，把持後の再把持，テレオペレーション，空中マニピュレーションまで幅広い下流タスクで活用されている。視覚・触覚・F/Tセンサの融合によるCoM推定と，その推定結果を把持戦略やコントローラに直接フィードバックするループが研究の主軸を形成している。学習ベースのCoG推定と能動知覚による効率的な情報収集が近年のトレンドとして際立っている。

1. [[Kubus2007_recognition]](../REFERENCES/MAIN.md#Kubus2007_recognition) — Kubus, Kroger, Wahl, "On-Line Rigid Object Recognition and Pose Estimation Based on Inertial Parameters" (2007)
   - **DOI**: `10.1109/IROS.2007.4399382`
   - **thesis**: ロボットが把持した物体を，オンライン推定した慣性パラメータのフィンガープリント照合によりリアルタイムに認識・ポーズ推定できる。
   - **core**: 動作中にオンライン推定した慣性パラメータ（質量・重心・慣性テンソル）を，既知物体の慣性パラメータデータベースと照合する識別ベース認識パイプライン。
   - **diff**: 画像ベースの視覚認識が把持中の遮蔽に弱いのに対し，本手法は接触力・トルクから直接物体を認識し遮蔽に影響されない。
   - **limit**: 認識精度はデータベースの網羅性と慣性パラメータ推定精度に強く依存。形状が異なっても慣性特性が類似した物体の弁別が困難。

2. [[Kanoulas2018_com_grasp]](../REFERENCES/MAIN.md#Kanoulas2018_com_grasp) — Kanoulas et al., "CoM-Based Grasp Pose Adaptation Using 3D Range and F/T Sensing" (2018)
   - **DOI**: `10.1142/S0219843618500135`
   - **thesis**: 3D点群からの幾何学的重心推定と手首F/T測定からの真の重心推定を反復的に組み合わせることで，重い非均一密度物体に対して手首トルクを低減し信頼性の高い把持を実現できる。
   - **core**: 外感覚段階で点群をボクセル化して幾何学的重心を推定し最近傍ハンドル把持を選択。固有感覚段階で持ち上げ時のレンチから真の重心線を算出しトルク最小化ハンドルを選択。安定化まで反復。
   - **diff**: 先行手法が幾何のみ（質量分布を無視）または単一モーダル感覚を用いるのに対し，本研究は外感覚と固有感覚知覚を反復統合したCoMガイド把持適応を初めて実現。
   - **limit**: 物体が平坦な表面上にあることが必要。ボクセル化時に均一密度を仮定。ハンドル状の把持に限定，片腕のみ。

3. [[Feng2020_com_grasp]](../REFERENCES/MAIN.md#Feng2020_com_grasp) — Feng et al., "CoM-Based Robust Grasp Planning Using Tactile-Visual Sensors" (2020)
   - **DOI**: `10.1109/ICRA40945.2020.9196815`
   - **thesis**: 触覚・トルクデータからのスリップ検出と重心推定に駆動されたクローズドループ把持再計画は，未知物体での安定把持回復を実現し，視覚のみの計画より大幅に高い成功率を達成できる。
   - **core**: 三段階パイプライン：深度画像からの対蹠把持サンプリング，触覚シーケンスのSVMによるスリップ検出，触覚・トルクデータから重心位置を予測する再把持プランナのニューラルネットワーク。
   - **diff**: 先行の再把持手法が静的接触仮定下での把持力調整や形状のみの調整を行うのに対し，本研究はマルチセンサのスリップ予測を用いて動的持ち上げ中の新把持ポーズ計画を初めて実現。
   - **limit**: 把持ポーズを一つの回転方向のみに修正可能。データセットが小規模（訓練14，テスト5物体）。

4. [[Feng2024_com_regrasp]](../REFERENCES/MAIN.md#Feng2024_com_regrasp) — Feng et al., "CoM-Based Object Regrasping via RL and Effects of Perception Modality" (2024)
   - **DOI**: `10.1109/LRA.2024.3439540`
   - **thesis**: 強化学習ベースの重心誘導再把持は，知覚モダリティ（視覚・触覚・力覚）の組み合わせが成功率に有意な影響を与えるため，モダリティ選択が実用設計の重要な変数である。
   - **core**: 重心推定を報酬信号に組み込んだRLエージェントが再把持戦略を学習。視覚（RGB-D）・触覚・F/T各モダリティの組み合わせの影響をアブレーション実験で定量評価。
   - **diff**: Feng et al. (2020) の再把持がヒューリスティックベースであるのに対し，本研究はRL枠組みへと拡張し知覚モダリティの体系的評価を実施する。
   - **limit**: シミュレーション中心の評価で実環境への転移性が課題。特定の物体カテゴリに限定されたモダリティ評価の汎化性が不明確。

5. [[Kang2025_cog_grasping]](../REFERENCES/MAIN.md#Kang2025_cog_grasping) — Kang, He, Gong, Liu, Bai, "Foundation Model-Driven Grasping via Center of Gravity Estimation" (2025)
   - **arXiv**: `2507.19242`
   - **thesis**: 少数の注釈付きデータベースから拡散ベースの意味的対応によって物体の重心を推定することで，非均一質量分布のツールに対して安定把持が可能になる。
   - **core**: CLIPが視覚的に類似した注釈付き物体を検索。DIFTが意味的対応を行って重心注釈を転移。GraspNetのポーズを推定重心に最も近いものを優先してフィルタリング。
   - **diff**: 従来のアフォーダンスベース把持が質量分布を無視して成功率27%に留まるのに対し，重心ガイドフィルタリングにより物理センサなしで76%に向上。
   - **limit**: データセットが10ツールカテゴリのみをカバー。汎化は視覚的に類似した物体に限定。

6. [[Dutta2025_visuotactile]](../REFERENCES/MAIN.md#Dutta2025_visuotactile) — Dutta, Burdet, Kaboli, "Predictive Visuo-Tactile Interactive Perception Framework for Object Properties Inference" (2025)
   - **DOI**: `10.1109/TRO.2025.3531816`
   - **thesis**: 視触覚インタラクティブ知覚フレームワークは，能動的探索動作と予測モデルを組み合わせることで，物体の物理特性（質量・剛性等）を効率的に推定できる。
   - **core**: 視覚と触覚のマルチモーダル観測を統合した予測モデルが，次の探索動作を選択して物体特性推定の不確実性を低減する能動知覚フレームワーク。
   - **diff**: 受動的観測に基づく従来の物体特性推定と異なり，能動的インタラクションと予測モデルを組み合わせて効率的な探索戦略を実現。
   - **limit**: 評価は特定の物体カテゴリと探索動作セットに限定されており，多様な形状・素材への汎化性が課題。

7. [[Watanabe2025_ftact]](../REFERENCES/MAIN.md#Watanabe2025_ftact) — Watanabe, Alvarez, Ferreiro, Savkin, Sano, "FTACT: Force Torque aware Action Chunking Transformer for Pick-and-Reorient" (2025)
   - **arXiv**: `2509.23112`
   - **thesis**: 6自由度手首F/T信号でAction Chunking Transformerを拡張することで，視覚的観察では接触状態遷移の検出が不十分な接触豊富なマニピュレーションタスクの性能が向上する。
   - **core**: 6DOF F/T読み取りをジョイント状態と連結したものをカメラ画像と並んでACTトランスフォーマーの追加エンコーダ入力として統合。
   - **diff**: 先行のACTベース模倣学習が視覚と固有感覚のみを使用するのに対し，F/Tを一腕グリッパーベースの小売マニピュレーションに統合。
   - **limit**: 評価が一タスクファミリー（ボトルのピックアンドリオリエント）に限定。より広いタスク多様性への汎化は未実証。

8. [[Ye2026_flyaware]](../REFERENCES/MAIN.md#Ye2026_flyaware) — Ye et al., "FlyAware: Inertia-Aware Aerial Manipulation via Vision-Based Estimation and Post-Grasp Adaptation" (2026)
   - **arXiv**: `2601.22686`
   - **thesis**: 把持前ビジョンベース慣性推定と把持後外乱オブザーバ適応の組み合わせにより，空中マニピュレータが未知ペイロードを桁違いに速く収束する推定のみのアプローチより処理できる。
   - **core**: RGB-D + IST-Net + GPT-4密度推論による事前感知で質量と慣性モーメントを予測。外乱オブザーバが把持後に精緻化し，慣性認識ゲインスケジュールコントローラにフィード。
   - **diff**: 先行の空中マニピュレーションが把持後推定のみに依存して20秒以上の収束時間を要するのに対し，FlyAwareの二段階パイプラインは約2秒に短縮し28.2%のRMSE改善。
   - **limit**: 物体重心が幾何フレーム原点と一致しマニピュレータの質量・慣性が無視できると仮定。GPT APIへのインターネットアクセスが必要。

9. [[Kruzliak2024_interactive]](../REFERENCES/MAIN.md#Kruzliak2024_interactive) — Kruzliak et al., "Interactive Learning of Physical Object Properties Through Robot Manipulation" (2024)
   - **DOI**: `10.1109/IROS58592.2024.10802249`
   - **thesis**: 物理特性に関するベイズネットワークと情報利得駆動の探索動作選択を組み合わせることで，ロボットが操作を通じて物体特性を効率的に抽出でき，ランダム動作選択を上回る性能を示す。
   - **core**: 離散材質・カテゴリノードと連続物理特性ノードを連結するベイズネットワーク。動作選択が5つのロボット動作にわたる期待エントロピー削減を最大化。
   - **diff**: 先行手法が固定動作シーケンスや受動視覚に依存するのに対し，能動的情報理論的動作選択を導入して適応的な動作決定といつ停止するかを実現。
   - **limit**: グリッパ力解像度閾値が硬い物体に対して二値的弾性出力を生成。連続分布から離散カテゴリ重みを推論する際に数値不安定性が生じる。

---

## G — Surveys & Benchmarks

慣性パラメータ識別分野の体系的レビューは，その方法論的多様性と応用範囲の広さを明確にしてきた。特にBIRDyツールボックスによる17手法の比較ベンチマークは再現可能な評価基盤を提供し，Mavrakis & Stolkinのサーベイは推定と活用の双方を網羅した最初の統合的概観として位置づけられる。Sweversらのチュートリアルは産業識別の標準プロトコルとして広く参照されている。

1. [[Mavrakis2020_survey]](../REFERENCES/MAIN.md#Mavrakis2020_survey) — Mavrakis, Stolkin, "Estimation and Exploitation of Objects' Inertial Parameters in Robotic Grasping and Manipulation: A Survey" (2020)
   - **DOI**: `10.1016/j.robot.2019.103374`
   - **thesis**: 未知物体の慣性パラメータは三つのインタラクションレベル（視覚的・探索的・固定物体）を通じて推定可能であり，この知識はロボット把持・マニピュレーション計画と制御を定量的に改善する。
   - **core**: 推定を視覚的/探索的/固定物体の分類法に整理し，活用を把持計画・インハンドマニピュレーション・プッシング・投擲の分類法に整理して，どの推定モダリティがどのマニピュレーション能力を実現するかをマッピング。
   - **diff**: 既存のレビューがロボット自己識別または特定マニピュレーションサブタスクをカバーするのに対し，本研究は外部物体の慣性パラメータの推定と活用の両方を初めて共同でカバーした。
   - **limit**: ロボット自己パラメータ識別を除外。平面プッシング解析がxz平面のみをカバーし複数の慣性パラメータが識別不可。

2. [[Leboutet2021_birdy]](../REFERENCES/MAIN.md#Leboutet2021_birdy) — Leboutet, Roux, Janot et al., "Inertial Parameter Identification in Robotics: A Survey (BIRDy)" (2021)
   - **DOI**: `10.3390/app11094303`
   - **thesis**: 単一の慣性パラメータ識別アルゴリズムがすべての動作条件で優位というわけではなく，17の確立された手法にわたるトレードオフを特徴付けるためにオープンソースツールボックス（BIRDy）による系統的ベンチマークが必要である。
   - **core**: BIRDyはロボット非依存のオープンソースMATLABツールボックスで，17の識別アルゴリズムをモンテカルロシミュレーションで評価し，産業用マニピュレータで実プラットフォーム検証を実施。
   - **diff**: 先行の比較研究が範囲が狭かったのに対し，BIRDyは古典的・統計的・ニューラル・物理制約アプローチを網羅した最初の包括的・再現可能なベンチマークを提供。
   - **limit**: 並列ロボットと浮動ベースロボットは未実装。評価が直列マニピュレータのみに限定。

3. [[Swevers2007_tutorial]](../REFERENCES/MAIN.md#Swevers2007_tutorial) — Swevers, Verdonck, De Schutter, "Dynamic Model Identification for Industrial Robots" (2007)
   - **DOI**: `10.1109/MCS.2007.904659`
   - **thesis**: 産業用ロボットの動力学モデル識別は，励起軌道設計・データ収集・パラメータ推定・モデル検証の標準的手順に従うことで，制御性能向上や力制御への活用が可能な精度に到達できる。
   - **core**: Fourier級数励起軌道の設計，最小二乗識別，摩擦モデリング，検証手順を体系的に解説した産業識別のチュートリアルペーパー。多数の産業実装例を含む。
   - **diff**: 研究論文では個別の技術的貢献が提示されるが，本チュートリアルは実務者向けに全工程を統合した唯一の包括的実装ガイドとして機能。
   - **limit**: 産業用固定ベースロボットに特化しており，浮動ベース・移動ロボット・協働ロボットの特殊要件は対象外。2007年以降の物理整合性保証手法は含まれない。
