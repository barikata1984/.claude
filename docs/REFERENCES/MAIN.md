# References

## A. Explicit Physical Parameter Conditioning

### Yu2017_uposi

**Preparing for the Unknown: Learning a Universal Policy with Online System Identification**
Yu, Tan, Liu, Turk — RSS, 2017
arXiv: `1702.02453` | [URL](https://arxiv.org/abs/1702.02453)

> First policy explicitly conditioned on online-estimated physical parameters (mass, inertia, friction). Established the UP+OSI paradigm for parameter-aware policy learning.

### Pinto2018_asymmetric_ac

**Asymmetric Actor Critic for Image-Based Robot Learning**
Pinto, Andrychowicz, Welinder, Zaremba, Abbeel — RSS, 2018
arXiv: `1710.06542` | [URL](https://www.roboticsproceedings.org/rss14/p08.html)

> Critic receives full simulator state (including physical parameters) while actor sees only images. Demonstrates privileged physical information accelerates policy learning.

### Kumar2021_rma

**RMA: Rapid Motor Adaptation for Legged Robots**
Kumar, Fu, Pathak, Malik — RSS, 2021
arXiv: `2107.04034` | [URL](https://arxiv.org/abs/2107.04034)

> Canonical two-phase paradigm: base policy conditioned on privileged environment factors, then adaptation module estimates latent from proprioceptive history. Template for manipulation adaptation.

### Liang2024_rma2

**Rapid Motor Adaptation for Robotic Manipulator Arms**
Liang, Ellis, Henriques — CVPR, 2024
DOI: `10.1109/CVPR52733.2024.01552` | arXiv: `2312.04670`

> Extends RMA to manipulation with depth-based adapter for pre-contact reasoning about object physical properties.

### Memmel2024_asid

**ASID: Active Exploration for System Identification in Robotic Manipulation**
Memmel, Wagenmaker, Zhu, Yin, Fox, Gupta — ICLR (Oral), 2024
arXiv: `2404.12308` | [URL](https://openreview.net/forum?id=jNR6s6OSBT)

> Fisher-information-maximizing exploration for active physical parameter identification. Zero-shot sim-to-real via targeted system identification.

## B. Implicit Physical Adaptation

### Peng2018_dynamics_rand

**Sim-to-Real Transfer of Robotic Control with Dynamics Randomization**
Peng, Andrychowicz, Zaremba, Abbeel — ICRA, 2018
arXiv: `1710.06537` | [URL](https://arxiv.org/abs/1710.06537)

> Established dynamics randomization + LSTM for zero-shot sim-to-real manipulation without explicit parameter identification.

### Li2018_pushnet

**Push-Net: Deep Planar Pushing for Objects with Unknown Physical Properties**
Li, Lee, Hsu — RSS, 2018
[URL](https://www.roboticsproceedings.org/rss14/p24.html)

> LSTM-based pushing with implicit physical reasoning from interaction history. 97%+ success on novel objects, sim-to-real zero-shot.

### Andrychowicz2020_dexterous

**Learning Dexterous In-Hand Manipulation**
Andrychowicz, Baker, Chociej et al. (OpenAI) — IJRR, 2020
DOI: `10.1177/0278364919887447` | arXiv: `1808.00177`

> Comprehensive physical parameter randomization for dexterous manipulation. Landmark demonstration of sim-only training for 24-DOF hand.

### Xue2024_ima

**Robust Contact-rich Manipulation through Implicit Motor Adaptation**
Xue, Razmjoo, Shetty, Calinon — IJRR, 2025
DOI: `10.1177/02783649251344638` | arXiv: `2412.11829`

> Implicit policy representation via advantage-function maximization over parameter distributions. Robust to estimation error without retraining.

### Kawaharazuka2022_cloth_pb

**Dynamic Cloth Manipulation Considering Variable Stiffness and Material Change Using Deep Predictive Model with Parametric Bias**
Kawaharazuka, Miki, Bando, Okada, Inaba — Frontiers in Neurorobotics, 2022
DOI: `10.3389/fnbot.2022.890695` | arXiv: `2409.15635`

> Parametric bias as explicit material-specific context code for online adaptation to physical property changes without retraining.

## C. Physical Parameter Estimation

### Jatavallabhula2021_gradsim

**gradSim: Differentiable Simulation for System Identification and Visuomotor Control**
Jatavallabhula, Macklin, Golemo et al. — ICLR, 2021
arXiv: `2104.02646` | [URL](https://openreview.net/forum?id=c_E8kFWfhp0)

> First differentiable physics+rendering pipeline for physical parameter identification from raw video.

### Xu2019_densephysnet

**DensePhysNet: Learning Dense Physical Object Representations via Multi-step Dynamic Interactions**
Xu, Wu, Zeng, Tenenbaum, Song — RSS, 2019
arXiv: `1906.03853` | [URL](https://arxiv.org/abs/1906.03853)

> Pixel-level physical property representations (mass, friction) learned from active multi-step interactions. First dense physical representation.

### Lou2024_dream

**DREAM: Differentiable Real-to-Sim-to-Real Engine for Learning Robotic Manipulation**
Lou, Zhang, Geng et al. — OpenReview, 2024
[URL](https://openreview.net/forum?id=S0FmCZ6by5)

> Unified Gaussian Splatting + differentiable physics for simultaneous visual and physical digital twin construction. Mass-conditioned grasping policy.

### Li2025_pinwm

**PIN-WM: Learning Physics-INformed World Models for Non-Prehensile Manipulation**
Li, Zhao, Yu et al. — RSS, 2025
arXiv: `2504.16693` | [URL](https://arxiv.org/abs/2504.16693)

> End-to-end visual-to-physics parameter identification (mass, friction, restitution) for non-prehensile manipulation via differentiable physics-rendering.

### Wang2025_phys2real

**Phys2Real: Fusing VLM Priors with Interactive Online Adaptation for Uncertainty-Aware Sim-to-Real Manipulation**
Wang, Tian, Swann, Shorinwa, Wu, Schwager — ICRA, 2026
arXiv: `2510.11689` | [URL](https://arxiv.org/abs/2510.11689)

> Fuses VLM-inferred physical parameter priors with online interaction-based estimation for pushing manipulation.

### Chen2025_proprioception

**Learning Object Properties Using Robot Proprioception via Differentiable Robot-Object Interaction**
Chen, Liu, Ma et al. — ICRA, 2025
arXiv: `2410.03920` | [URL](https://arxiv.org/abs/2410.03920)

> Physical property identification (mass, elastic modulus) from joint encoders alone via differentiable contact simulation.

## D. Object-Centric / Pose-Based Policy Representations

### Hsu2024_spot

**SPOT: SE(3) Pose Trajectory Diffusion for Object-Centric Manipulation**
Hsu, Wen, Xu, Narang, Wang et al. — arXiv preprint, 2024
arXiv: `2411.00965` | [URL](https://arxiv.org/abs/2411.00965)

> Eliminates RGB entirely, conditioning diffusion policy on SE(3) pose trajectories. Cross-embodiment transfer from 8 demonstrations.

### Sun2025_prism_dp

**PRISM-DP: Pose-based Observations for Diffusion-Policies via Segmentation, Mesh Generation, and Pose Tracking**
Sun, Chen, Rakita — arXiv preprint, 2025
arXiv: `2504.20359` | [URL](https://arxiv.org/abs/2504.20359)

> Automated mesh generation removes manual mesh requirement for pose-based diffusion policies. Approaches ground-truth state performance.

### Pan2025_omnimanip

**OmniManip: Towards General Robotic Manipulation via Object-Centric Interaction Primitives as Spatial Constraints**
Pan, Zhang, Wu, Zhao, Gao et al. — CVPR (Highlight), 2025
arXiv: `2501.03841` | [URL](https://arxiv.org/abs/2501.03841)

> Object-centric interaction primitives in canonical space bridge VLM reasoning with 6-DoF manipulation constraints.

### Haldar2025_point_policy

**Point Policy: Unifying Observations and Actions with Key Points for Robot Manipulation**
Haldar, Pinto — CoRL, 2025
arXiv: `2502.20391` | [URL](https://proceedings.mlr.press/v305/haldar25a.html)

> Unified keypoint representation for observation and action, enabling policy learning from human video without teleoperation.

### Wang2025_skil

**SKIL: Semantic Keypoint Imitation Learning for Generalizable Data-Efficient Manipulation**
Wang, You, Hu, Li, Gao et al. — RSS, 2025
arXiv: `2501.14400` | [URL](https://arxiv.org/abs/2501.14400)

> Semantic keypoints from vision foundation models with feature descriptors for cross-instance and cross-embodiment generalization.

### Simeonov2022_ndf

**Neural Descriptor Fields: SE(3)-Equivariant Object Representations for Manipulation**
Simeonov, Du, Tagliasacchi, Tenenbaum, Rodriguez, Agrawal, Sitzmann — ICRA, 2022
DOI: `10.1109/ICRA46639.2022.9812146` | arXiv: `2112.05124`

> SE(3)-equivariant implicit neural fields for few-shot manipulation generalization across instances and orientations.

### Zhu2023_groot

**GROOT: Learning Generalizable Manipulation Policies with Object-Centric 3D Representations**
Zhu, Jiang, Stone, Zhu — CoRL, 2023
arXiv: `2310.14386` | [URL](https://proceedings.mlr.press/v229/zhu23b.html)

> Object-centric 3D representations via segmentation correspondence model. Generalizes across backgrounds, viewpoints, and instances.

### Ze2024_dp3

**3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations**
Ze, Zhang, Zhang, Hu, Wang, Xu — RSS, 2024
arXiv: `2403.03954` | [URL](https://arxiv.org/abs/2403.03954)

> Compact point-cloud representations for diffusion policy. 55.3% improvement over image-based baselines on 72 tasks.

### Wang2024_gendp

**GenDP: 3D Semantic Fields for Category-Level Generalizable Diffusion Policy**
Wang, Yin, Huang, Kelestemur, Wang et al. — CoRL, 2024
arXiv: `2410.17488` | [URL](https://proceedings.mlr.press/v270/wang25m.html)

> 3D semantic fields from foundation model descriptors for category-level generalization. 20%→93% success on unseen instances.

## E. Base Architectures

### Zhao2023_act

**Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware**
Zhao, Kumar, Levine, Finn — RSS, 2023
arXiv: `2304.13705` | [URL](https://arxiv.org/abs/2304.13705)

> Action Chunking with Transformers (ACT). Overcomes compounding error via sequence prediction + temporal ensemble.

### Chi2023_diffusion_policy

**Diffusion Policy: Visuomotor Policy Learning via Action Diffusion**
Chi, Xu, Feng, Cousineau, Du, Burchfiel, Tedrake, Song — RSS 2023 / IJRR 2024
DOI: `10.1177/02783649241273668` | arXiv: `2303.04137`

> Conditional denoising diffusion for visuomotor policy. Handles multimodal action distributions inherently. 46.9% average improvement over SoTA.

### Shridhar2023_peract

**PerAct: A Multi-Task Transformer for Robotic Manipulation**
Shridhar, Manuelli, Fox — CoRL, 2022
arXiv: `2209.05451` | [URL](https://proceedings.mlr.press/v205/shridhar23a.html)

> Next-best-voxel-action formulation with Perceiver Transformer. Single model learns 18 diverse 6-DoF tasks.

### Goyal2023_rvt

**RVT: Robotic View Transformer for 3D Object Manipulation**
Goyal, Xu, Guo, Blukis, Chao, Fox — CoRL, 2023
arXiv: `2306.14896` | [URL](https://proceedings.mlr.press/v229/goyal23a.html)

> Virtual viewpoint re-rendering + cross-view attention. 36× faster than PerAct with superior performance.

## F. Surveys

### Mavrakis2020_inertia_survey

**Estimation and Exploitation of Objects' Inertial Parameters in Robotic Grasping and Manipulation: A Survey**
Mavrakis, Stolkin — Robotics and Autonomous Systems (Elsevier), 2020
arXiv: `1911.04397` | [URL](https://arxiv.org/abs/1911.04397)

> Comprehensive survey of inertial parameter estimation methods and their exploitation in manipulation planning and control.

### Ai2025_dynamics_review

**A Review of Learning-Based Dynamics Models for Robotic Manipulation**
Ai, Tian, Shi, Wang, Pfaff, Tan, Christensen, Su, Wu, Li — Science Robotics, 2025
DOI: `10.1126/scirobotics.adt1497`

> First systematic review of learning-based dynamics models spanning architecture, state representations, and control integration for manipulation.
