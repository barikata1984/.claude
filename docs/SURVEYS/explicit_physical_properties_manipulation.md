# Literature Survey: Conditioning Manipulation Policies on Explicit Physical Properties for Object Generalization

| | |
|---|---|
| **Date** | 2026-03-27 |
| **Scope** | Explicit/interpretable physical property conditioning (inertia, friction, shape, 6D pose) for object generalization in imitation learning for rigid-body manipulation |
| **Papers found** | 31 |

## Research Landscape Overview

Robot manipulation policy learning has seen rapid progress since 2017, driven by two parallel research streams. The first stream — physical parameter conditioning — originated with UP-OSI (Yu et al., RSS 2017) and was consolidated by RMA (Kumar et al., RSS 2021), establishing the paradigm of training policies conditioned on privileged physical parameters in simulation and then distilling that conditioning into online estimators. The second stream — structured geometric representations — has replaced raw RGB inputs with point clouds (DP3), SE(3) pose trajectories (SPOT), or semantic keypoints (SKIL), dramatically improving spatial generalization.

These two streams have developed largely in isolation. Physical parameter conditioning research has focused on locomotion (RMA) and dexterous manipulation (Andrychowicz et al., IJRR 2020), predominantly using domain randomization over parameters rather than explicit numerical conditioning of the policy. Meanwhile, geometric/pose-based approaches have targeted visual robustness (viewpoint, appearance, background) but have not incorporated physical dynamics properties. The intersection — conditioning a manipulation policy on both interpretable physical quantities and structured geometric state — remains unexplored.

Key venues include RSS (where the foundational UP-OSI and RMA appeared), CoRL (dominant for object-centric representation work), ICRA/IROS (for sim-to-real and system identification), and ICLR/NeurIPS (for differentiable simulation). Active research groups include CMU/Berkeley (RMA, Asymmetric AC), Stanford (Phys2Real, ACT), Columbia (Diffusion Policy, GenDP), UT Austin (SPOT, GROOT), MIT (DensePhysNet, NDF), and NVIDIA (PerAct, RVT, SPOT).

## Survey Findings

### Thesis

The central tension in the field is between **data-scaling approaches** and **structure-injection approaches** to object generalization. Data-scaling approaches (OpenAI dexterous manipulation, broad domain randomization) achieve generalization by covering the space of possible dynamics through sheer volume of randomized experience, producing LSTM-mediated implicit adaptation. Structure-injection approaches (UP-OSI, RMA, NDF, SPOT) achieve generalization by providing the policy with structured priors — physical parameters, SE(3) equivariance, or object-centric representations — that compress the space the policy must generalize over. Neither paradigm has resolved the problem alone: data-scaling approaches are sample-inefficient and produce opaque policies, while structure-injection approaches have been fragmented — injecting either physical structure or geometric structure, but not both simultaneously.

### Foundation

1. **Simulation as training substrate**: Every surveyed learning-based approach trains in simulation (MuJoCo, Isaac Gym, RoboCasa). Real-world data, when used, serves only for adaptation or fine-tuning. This universal dependence on simulation is what makes physical parameter randomization and privileged information feasible.

2. **Privileged information paradigm**: The teacher-student framework — training a teacher policy with access to ground-truth physical parameters, then distilling to a student that infers from observation history — is the shared substrate of UP-OSI, RMA, RMA2, ASID, and Asymmetric AC. Without simulator access to privileged state, these methods cannot be trained.

3. **Transformer/diffusion as policy backbone**: Since ACT (2023) and Diffusion Policy (2023), the dominant policy architectures are Transformer-based (ACT, PerAct, RVT, Point Policy, SKIL) or diffusion-based (Diffusion Policy, DP3, GenDP, SPOT, PRISM-DP). These architectures provide the expressiveness needed for multimodal action distributions and long-horizon action chunking.

4. **Domain randomization over physical parameters**: Randomizing mass, friction, inertia, and damping during training is the standard technique for producing dynamics-robust policies (Peng et al. 2018, Andrychowicz et al. 2020). This technique is applied by nearly all sim-to-real papers in the survey, even those that also perform online adaptation.

### Progress

1. **2017 — Online physical parameter conditioning**: UP-OSI (Yu et al.) first demonstrated that a policy explicitly conditioned on estimated physical parameters (mass, inertia, friction) outperforms domain-randomization-only policies, by coupling a Universal Policy with Online System Identification. However, this was validated only in simulation-to-simulation transfer.

2. **2018 — Zero-shot sim-to-real via dynamics randomization**: Peng et al. (ICRA 2018) showed that LSTM policies trained under broad dynamics randomization can transfer to real robots for pushing without any real-world data, eliminating the need for explicit system identification — at the cost of implicit, uninterpretable adaptation.

3. **2018–2019 — Physical reasoning for pushing**: Push-Net (Li et al., RSS 2018) and DensePhysNet (Xu et al., RSS 2019) addressed the specific problem of pushing objects with unknown physical properties, using recurrent interaction histories and dense physical representations respectively. These established pushing as a key benchmark for physical property-aware manipulation.

4. **2021 — Rapid online adaptation**: RMA (Kumar et al., RSS 2021) introduced the two-phase paradigm (privileged training → proprioceptive adaptation) that enables sub-second adaptation to novel dynamics. While demonstrated on locomotion, this paradigm became the template for manipulation adaptation (RMA2, 2024).

5. **2022–2023 — Structured 3D policy representations**: NDF (Simeonov et al., ICRA 2022), GROOT (Zhu et al., CoRL 2023), and DP3 (Ze et al., RSS 2024) progressively demonstrated that replacing RGB with structured 3D representations (neural fields, point clouds) dramatically improves spatial and instance-level generalization, overcoming the viewpoint and appearance fragility of image-based policies.

6. **2024–2025 — Pose-only policies**: SPOT (Hsu et al., 2024) and PRISM-DP (Sun et al., 2025) eliminated image inputs entirely, conditioning diffusion policies on SE(3) pose trajectories. This represents the geometric stream's logical endpoint — but these methods have no mechanism for adapting to physical property variation.

7. **2024–2025 — Differentiable physics for parameter identification**: PIN-WM (RSS 2025), DREAM (2024), and gradSim (ICLR 2021) advanced the identification of physical parameters from visual/proprioceptive observations via differentiable simulation. PIN-WM specifically addresses non-prehensile manipulation, identifying inertia, friction, and restitution end-to-end from video.

### Gap

1. **No integration of explicit physical quantities with structured geometric representations**

   The physical parameter conditioning line (Category A: UP-OSI, RMA, RMA2, ASID) and the geometric/pose-based representation line (Category D: SPOT, PRISM-DP, DP3, NDF) have developed independently. Physical parameter methods use proprioception or latent embeddings as the adaptation signal but condition the policy on low-dimensional state, not structured object representations. Conversely, pose-based methods capture geometric structure but have no mechanism for incorporating physical dynamics (mass, friction, inertia). No existing work conditions a manipulation policy simultaneously on interpretable physical quantities and structured 6D pose — the specific combination that would enable a policy to understand both *where* an object is and *how* it will respond to contact. Closing this gap would enable object generalization that is both geometrically and dynamically grounded, without requiring demonstration scaling.

2. **Pushing and non-prehensile manipulation under-explored with modern policy architectures**

   As Categories A and D show, push-specific work with physical reasoning dates to 2018–2019 (Push-Net, DensePhysNet), using pre-Transformer architectures. PIN-WM (2025) addresses pushing with physics world models but does not condition the policy on explicit physical parameters. Meanwhile, modern architectures (ACT, Diffusion Policy) have been evaluated primarily on prehensile tasks (grasping, insertion, bimanual assembly). The combination of explicit physical parameter conditioning with a Transformer-based policy for pushing remains untested, despite pushing being the canonical task where physical properties (friction, mass distribution, inertia) most directly determine success.

3. **Interpretability of physical parameter contributions is unexplored**

   While Transformer-based manipulation policies are now standard (Categories D and E), no surveyed work has analyzed which input modalities (among pose, inertia, friction, shape) contribute to task performance via attention mechanisms. The opacity of multi-modal conditioning is noted implicitly by several papers (RMA2, IMA) but never addressed directly. Attention-based interpretability would provide empirical evidence for which physical quantities are decision-relevant, informing both policy design and the minimum-necessary sensing requirements for real-world deployment.

## Paper Catalogue

### Category Overview

The 31 papers are organized into six categories reflecting the field's structural divisions.

| Category | Description | Count |
|----------|-------------|-------|
| A. Explicit Physical Parameter Conditioning | Policies directly conditioned on physical quantities (mass, friction, inertia) or latent encodings thereof | 5 |
| B. Implicit Physical Adaptation | Policies that adapt to physical variation via domain randomization + recurrence, without explicit parameter identification | 5 |
| C. Physical Parameter Estimation | Methods for identifying physical parameters from observation, potentially feeding downstream policies | 6 |
| D. Object-Centric / Pose-Based Policy Representations | Policies using structured geometric inputs (6D pose, point clouds, keypoints, neural fields) instead of RGB | 9 |
| E. Base Architectures | Foundational policy architectures that serve as backbones for Categories A–D | 4 |
| F. Surveys | Review papers providing field-level context | 2 |

### Foundational Works

| # | Paper | Year | Venue | Significance |
|---|-------|------|-------|-------------|
| A1 | UP-OSI (Yu et al.) | 2017 | RSS | First policy conditioned on online-estimated explicit physical parameters |
| B1 | Dynamics Randomization (Peng et al.) | 2018 | ICRA | Established dynamics randomization + LSTM for zero-shot sim-to-real |
| A4 | RMA (Kumar et al.) | 2021 | RSS | Defined the privileged-training → online-adaptation paradigm |
| D6 | NDF (Simeonov et al.) | 2022 | ICRA | First SE(3)-equivariant neural field for manipulation |
| E1 | ACT (Zhao et al.) | 2023 | RSS | Introduced action chunking with Transformers for fine manipulation |
| E2 | Diffusion Policy (Chi et al.) | 2023 | RSS/IJRR | Established diffusion as the dominant policy representation |

### A. Explicit Physical Parameter Conditioning

Policies in this category are directly conditioned on physical quantities — either ground-truth parameters during training, or online estimates at deployment. The defining characteristic is that the physical parameter vector is an explicit, identifiable input to the policy network, not a latent embedding learned end-to-end.

1. [[Yu2017_uposi]](../REFERENCES/MAIN.md#Yu2017_uposi) — Yu, Tan, Liu, Turk, "Preparing for the Unknown: Learning a Universal Policy with Online System Identification" (2017)
   - **arXiv**: 1702.02453
   - **thesis**: A universal policy conditioned on dynamics parameters, coupled with online system identification from state-action history, produces control that is robust to unknown and time-varying dynamics — without real-world training.
   - **core**: The coupling of the Universal Policy (conditioned on dynamics parameters) with the OSI module that infers those parameters from recent history. Neither alone suffices.
   - **diff**: Prior universal policies used domain randomization but ignored parameter identity at runtime. UP-OSI is the first to close the loop: online parameter estimation directly feeds a parameter-conditioned policy.
   - **limit**: Real-world transfer was not demonstrated (simulation-to-simulation only). Cannot handle dynamics outside the training distribution. The parametric model may not represent real-world dynamics accurately.

2. [[Pinto2018_asymmetric_ac]](../REFERENCES/MAIN.md#Pinto2018_asymmetric_ac) — Pinto, Andrychowicz, Welinder, Zaremba, Abbeel, "Asymmetric Actor Critic for Image-Based Robot Learning" (2018)
   - **arXiv**: 1710.06542
   - **thesis**: Training a critic on full simulator state (including physical parameters) while the actor observes only images dramatically accelerates learning and enables sim-to-real transfer without real-world data.
   - **core**: The asymmetry between critic (full state) and actor (images only) during training. The critic provides low-variance value estimates that guide the actor.
   - **diff**: Standard actor-critic trains both on images, causing high-variance value estimates. Prior privileged-information methods require an expert policy. Asymmetric AC needs no expert — only simulator state.
   - **limit**: limit not available (no formal limitations section).

3. [[Kumar2021_rma]](../REFERENCES/MAIN.md#Kumar2021_rma) — Kumar, Fu, Pathak, Malik, "RMA: Rapid Motor Adaptation for Legged Robots" (2021)
   - **arXiv**: 2107.04034
   - **thesis**: A quadruped trained in simulation can adapt to novel terrains and payloads within fractions of a second by learning to infer a compact latent encoding of environmental factors from proprioceptive history.
   - **core**: Two-phase training: (1) base policy conditioned on ground-truth environment factor vector, (2) adaptation module regresses that vector from proprioceptive history.
   - **diff**: Prior sim-to-real used domain randomization alone (producing conservative behaviors) or required real-world fine-tuning. RMA enables instant adaptation without gradient updates at test time.
   - **limit**: Blind locomotion fails on larger perturbations (stairs, multiple leg obstructions). Authors state that exteroception (vision) is needed for truly reliable locomotion.

4. [[Liang2024_rma2]](../REFERENCES/MAIN.md#Liang2024_rma2) — Liang, Ellis, Henriques, "Rapid Motor Adaptation for Robotic Manipulator Arms" (2024)
   - **arXiv**: 2312.04670
   - **thesis**: A manipulation policy can adapt to unseen object physical properties at deployment by inferring a compact environment embedding from action history and depth observations — without real-world fine-tuning.
   - **core**: Two-stage training (RMA paradigm) extended to manipulation with depth perception in the adapter for pre-contact reasoning about object identity.
   - **diff**: RMA applied to locomotion with proprioception only. RMA2 extends to manipulation, where visual reasoning before contact is necessary. Depth is incorporated into the adapter.
   - **limit**: Performance gap between Oracle and RMA2 on faucet tasks. Separate per-task policies rather than unified multi-task. Variable object counts not handled.

5. [[Memmel2024_asid]](../REFERENCES/MAIN.md#Memmel2024_asid) — Memmel, Wagenmaker, Zhu, Yin, Fox, Gupta, "ASID: Active Exploration for System Identification in Robotic Manipulation" (2024)
   - **arXiv**: 2404.12308
   - **thesis**: A small number of actively collected real-world interactions — guided by Fisher-information-maximizing exploration — is sufficient to identify physical parameters for zero-shot sim-to-real transfer.
   - **core**: The exploration policy trained to maximize Fisher information over unknown physical parameters. This ensures maximally diagnostic data collection.
   - **diff**: Prior methods use domain randomization (no simulator refinement) or passive data collection. ASID is the first to couple active exploration with information gain over dynamics parameters.
   - **limit**: Center-of-mass near rod middle creates parameter ambiguity. Fisher information uses domain randomization as approximation. Requires differentiable simulator. Modest real-world success rates (6/9 rod, 7/10 shuffleboard).

### B. Implicit Physical Adaptation

Policies in this category adapt to physical variation without explicit parameter identification — typically through domain randomization during training and recurrent architectures that implicitly infer dynamics from interaction history.

1. [[Peng2018_dynamics_rand]](../REFERENCES/MAIN.md#Peng2018_dynamics_rand) — Peng, Andrychowicz, Zaremba, Abbeel, "Sim-to-Real Transfer of Robotic Control with Dynamics Randomization" (2018)
   - **arXiv**: 1710.06537
   - **thesis**: Training recurrent policies over randomized simulator dynamics is sufficient to produce policies that adapt at runtime to unknown real dynamics, bridging the reality gap through diversity rather than accuracy.
   - **core**: LSTM policy + randomized dynamics. The recurrence enables implicit online system identification from action-observation history.
   - **diff**: Prior sim-to-real either tuned the simulator or required real-world data. Dynamics randomization requires neither — it covers real dynamics within the training distribution.
   - **limit**: limit not available (validated on planar pushing only; no formal limitations section).

2. [[Li2018_pushnet]](../REFERENCES/MAIN.md#Li2018_pushnet) — Li, Lee, Hsu, "Push-Net: Deep Planar Pushing for Objects with Unknown Physical Properties" (2018)
   - **DOI**: roboticsproceedings.org/rss14/p24.html
   - **thesis**: A deep recurrent model trained in simulation can push unknown objects to arbitrary goal poses using only visual observations, by implicitly tracking interaction history to infer effective dynamics online.
   - **core**: LSTM-based interaction history tracker with auxiliary center-of-mass estimation. The recurrent encoding builds up an implicit physical model from sequential pushes.
   - **diff**: Prior pushing methods require known or pre-identified physical parameters. Push-Net sidesteps explicit system identification entirely, transferring zero-shot from sim to real.
   - **limit**: limit not available (validated on planar pushing only; no formal limitations section).

3. [[Andrychowicz2020_dexterous]](../REFERENCES/MAIN.md#Andrychowicz2020_dexterous) — Andrychowicz, Baker, Chociej et al. (OpenAI), "Learning Dexterous In-Hand Manipulation" (2020)
   - **DOI**: 10.1177/0278364919887447
   - **thesis**: Sufficiently aggressive randomization of all physical parameters in simulation — combined with large-scale distributed RL and LSTM policies — is enough to transfer dexterous in-hand manipulation to a physical Shadow Hand without real-world training data.
   - **core**: Comprehensive randomization suite covering physical (friction, mass, surface), visual, and unmodeled effects. Breadth of randomization rather than any single modeling choice closes the reality gap.
   - **diff**: Prior dexterous manipulation required real-world training or simple domains. First demonstration that RL in simulation alone achieves fingertip-level cube reorientation on a 24-DOF hand.
   - **limit**: Hardware breakage changed system properties across experiments. Only simulated sensing modalities used — tactile sensors excluded.

4. [[Xue2024_ima]](../REFERENCES/MAIN.md#Xue2024_ima) — Xue, Razmjoo, Shetty, Calinon, "Robust Contact-rich Manipulation through Implicit Motor Adaptation" (2024)
   - **DOI**: 10.1177/02783649251344638
   - **thesis**: Representing a policy implicitly as the argmax of an advantage function — rather than as an explicit network conditioned on estimated parameters — produces policies naturally robust to parameter uncertainty in contact-rich tasks.
   - **core**: Tensor Train decomposition of state-value and advantage functions, enabling tractable retrieval of the implicitly defined optimal policy across a continuous distribution of physical parameters.
   - **diff**: Explicit motor adaptation (RMA) is sensitive to estimation error. IMA retrieves policies via advantage-function maximization over the estimated parameter distribution, robust to rough estimates without retraining.
   - **limit**: Probabilistic system adaptation uses a straightforward MLP. Demonstrated on contact-rich manipulation primitives only. High-dimensional parameter spaces may strain TT computation. Uniform parameter distribution assumption.

5. [[Kawaharazuka2022_cloth_pb]](../REFERENCES/MAIN.md#Kawaharazuka2022_cloth_pb) — Kawaharazuka, Miki, Bando, Okada, Inaba, "Dynamic Cloth Manipulation Considering Variable Stiffness and Material Change Using Deep Predictive Model with Parametric Bias" (2022)
   - **DOI**: 10.3389/fnbot.2022.890695
   - **thesis**: A musculoskeletal robot can adapt to cloths of different stiffness by encoding material-specific information in a low-dimensional parametric bias vector that modulates a deep predictive model — enabling online adaptation without retraining.
   - **core**: The parametric bias — a small trainable vector that serves as a material-specific context code. Without it, a single network cannot disambiguate different materials.
   - **diff**: Prior cloth manipulation assumed fixed properties or required retraining. Parametric bias is applied to physical property change for the first time, enabling online adaptation by optimizing only the bias vector.
   - **limit**: Stiffness modeled as a single scalar rather than spatially variable. Cannot handle large nonlinear changes (cloth leaving hand). "Still far from reaching human-like adaptive dynamic cloth manipulation."

### C. Physical Parameter Estimation

Methods for identifying physical parameters from observations — visual, proprioceptive, or interaction-based. These may or may not be coupled with downstream policy conditioning.

1. [[Jatavallabhula2021_gradsim]](../REFERENCES/MAIN.md#Jatavallabhula2021_gradsim) — Jatavallabhula, Macklin, Golemo et al., "gradSim: Differentiable Simulation for System Identification and Visuomotor Control" (2021)
   - **arXiv**: 2104.02646
   - **thesis**: Physical parameters (mass, friction, elasticity) can be recovered from video by backpropagating through a unified differentiable physics-plus-rendering pipeline — eliminating the need for 3D annotations.
   - **core**: End-to-end differentiability connecting pixel-level rendering loss through the physics simulator to physical parameters.
   - **diff**: Prior differentiable simulators required 3D state annotations. gradSim is the first to compose differentiable physics with differentiable rendering for parameter identification from raw video.
   - **limit**: Cannot handle tiny masses (≤100g). No articulated bodies. Only simple contact geometries. Unmodeled real-world phenomena.

2. [[Xu2019_densephysnet]](../REFERENCES/MAIN.md#Xu2019_densephysnet) — Xu, Wu, Zeng, Tenenbaum, Song, "DensePhysNet: Learning Dense Physical Object Representations via Multi-step Dynamic Interactions" (2019)
   - **arXiv**: 1906.03853
   - **thesis**: A robot can learn pixel-level physical property representations (encoding mass, friction) by actively executing multi-step dynamic interactions and training a deep predictive model that grounds visual motion in physics.
   - **core**: Multi-step dynamic interaction protocol paired with a predictive model that associates visual motion with physical attributes at the pixel level.
   - **diff**: Prior visual representations captured appearance or geometry but not physical properties. DensePhysNet is the first dense physical representation learned from interaction dynamics.
   - **limit**: Uses depth only, not RGB. Interaction set (sliding, collision) is limited.

3. [[Lou2024_dream]](../REFERENCES/MAIN.md#Lou2024_dream) — Lou, Zhang, Geng et al., "DREAM: Differentiable Real-to-Sim-to-Real Engine for Learning Robotic Manipulation" (2024)
   - **URL**: https://openreview.net/forum?id=S0FmCZ6by5
   - **thesis**: Differentiably combining 3D Gaussian Splatting with physics simulation enables identifying object mass from real interactions and constructing physically plausible digital twins for force-aware policy transfer.
   - **core**: The differentiable rendering-physics loop jointly optimizing visual appearance (Gaussian Splat) and physical parameters (mass) from real observations.
   - **diff**: Prior real-to-sim identifies geometry and physics independently. DREAM unifies Gaussian Splatting with differentiable physics for simultaneous visual and physical digital twin construction.
   - **limit**: limit not available.

4. [[Li2025_pinwm]](../REFERENCES/MAIN.md#Li2025_pinwm) — Li, Zhao, Yu et al., "PIN-WM: Learning Physics-INformed World Models for Non-Prehensile Manipulation" (2025)
   - **arXiv**: 2504.16693
   - **thesis**: Physical dynamics parameters (mass, friction, restitution) can be identified end-to-end from visual interaction sequences via differentiable physics-rendering, and these parameters seed "physics-aware digital cousins" for reliable sim-to-real pushing transfer.
   - **core**: Differentiable coupling of rigid-body physics with rendering, allowing gradients from pixel loss to flow into physical parameter estimates.
   - **diff**: Prior non-prehensile work assumes known parameters or uses blind randomization. PIN-WM performs end-to-end visual-to-physics parameter identification and introduces physics-aware digital cousins as a principled alternative to blind DR.
   - **limit**: Rendering sensitive to shadows from robot movement. Restricted to rigid-body dynamics. Differentiable relighting proposed as remedy.

5. [[Wang2025_phys2real]](../REFERENCES/MAIN.md#Wang2025_phys2real) — Wang, Tian, Swann, Shorinwa, Wu, Schwager, "Phys2Real: Fusing VLM Priors with Interactive Online Adaptation for Uncertainty-Aware Sim-to-Real Manipulation" (2025)
   - **arXiv**: 2510.11689
   - **thesis**: Combining VLM-inferred prior distributions over physical parameters with online interaction-based estimation via inverse-variance weighting achieves more reliable sim-to-real than either source alone.
   - **core**: Inverse-variance weighting fusion that combines epistemic uncertainty from ensemble-based online adaptation with aleatoric uncertainty from VLM priors.
   - **diff**: RMA learns latent embeddings without physical interpretability. DR ignores object-specific information. Phys2Real is the first to fuse interpretable online parameter estimation with VLM priors in closed-loop control.
   - **limit**: Focuses on center-of-mass along a single axis. Needs evaluation on wider geometries. Ensemble uncertainty calibration may be suboptimal.

6. [[Chen2025_proprioception]](../REFERENCES/MAIN.md#Chen2025_proprioception) — Chen, Liu, Ma et al., "Learning Object Properties Using Robot Proprioception via Differentiable Robot-Object Interaction" (2025)
   - **arXiv**: 2410.03920
   - **thesis**: Physical object properties (mass, elastic modulus) can be identified purely from robot proprioception (joint encoders) by differentiating through simulated robot-object interaction — without vision or force-torque sensors.
   - **core**: Differentiable simulation of robot-object contact mapping proprioceptive observations to physical parameters via gradient-based inverse optimization.
   - **diff**: Prior methods rely on vision or force-torque sensors. This demonstrates that proprioception alone is sufficient when paired with differentiable contact simulation.
   - **limit**: limit not available.

### D. Object-Centric / Pose-Based Policy Representations

Policies using structured geometric inputs — 6D pose trajectories, point clouds, keypoints, or neural fields — instead of raw RGB. These methods eliminate visual fragility but currently have no mechanism for physical property conditioning.

1. [[Hsu2024_spot]](../REFERENCES/MAIN.md#Hsu2024_spot) — Hsu, Wen, Xu, Narang, Wang et al., "SPOT: SE(3) Pose Trajectory Diffusion for Object-Centric Manipulation" (2024)
   - **arXiv**: 2411.00965
   - **thesis**: SE(3) object pose trajectories relative to the target — rather than raw sensory observations — are sufficient for learning constraint-respecting, cross-embodiment policies from as few as eight demonstrations.
   - **core**: SE(3) pose trajectory as intermediate representation decoupling embodiment from task, combined with diffusion policy conditioning.
   - **diff**: Prior work does not encode planning constraints and requires action-labeled robot demonstrations. SPOT uses action-free demonstrations (iPhone video, human hand) with constraint compliance emerging from the pose-trajectory representation.
   - **limit**: Cannot handle non-prehensile tasks. Relies on 6D pose tracking assuming rigid objects. Requires reconstructed object mesh.

2. [[Sun2025_prism_dp]](../REFERENCES/MAIN.md#Sun2025_prism_dp) — Sun, Chen, Rakita, "PRISM-DP: Pose-based Observations for Diffusion-Policies via Segmentation, Mesh Generation, and Pose Tracking" (2025)
   - **arXiv**: 2504.20359
   - **thesis**: Replacing images with structured pose observations of task-relevant objects enables compact, data-efficient diffusion policies that approach ground-truth-state performance — and mesh generation eliminates the barrier to open-set deployment.
   - **core**: Automatic mesh generation (removing manual mesh requirement) integrated with 6D pose estimation and tracking for structured observation streams.
   - **diff**: Prior pose-based policies (SPOT) required pre-scanned meshes. PRISM-DP replaces manual preparation with learned mesh generation for arbitrary objects.
   - **limit**: Mesh generation too slow (~1 min) or insufficient topology quality. Unit quaternion representation causes learning instability; 6D parameterization preferred.

3. [[Pan2025_omnimanip]](../REFERENCES/MAIN.md#Pan2025_omnimanip) — Pan, Zhang, Wu, Zhao, Gao et al., "OmniManip: Towards General Robotic Manipulation via Object-Centric Interaction Primitives as Spatial Constraints" (2025)
   - **arXiv**: 2501.03841
   - **thesis**: Object-centric interaction primitives (functional keypoints and direction vectors in canonical space) bridge VLM reasoning with precise 6-DoF constraints, enabling zero-shot cross-category generalization.
   - **core**: Canonical-space affordance representation combined with dual closed-loop system (VLM resampling + 6D pose tracking).
   - **diff**: Prior primitive methods generate task-agnostic proposals and rely on manual post-processing. OmniManip replaces both with VLM-grounded canonical-space primitives.
   - **limit**: Cannot model deformable objects. Depends on mesh quality from 3D AI-generated content. Multiple VLM calls introduce computational overhead.

4. [[Haldar2025_point_policy]](../REFERENCES/MAIN.md#Haldar2025_point_policy) — Haldar, Pinto, "Point Policy: Unifying Observations and Actions with Key Points for Robot Manipulation" (2025)
   - **arXiv**: 2502.20391
   - **thesis**: Semantically meaningful keypoints from vision models are sufficient as a unified observation-action representation for learning manipulation from human video without robot teleoperation data.
   - **core**: Unified keypoint representation for both observations and actions, enabling morphology-agnostic transfer from human video.
   - **diff**: Prior human-video methods require teleoperation as a bridge. Point Policy eliminates teleoperation entirely via shared keypoint space.
   - **limit**: Depends on vision model reliability. Point-only abstraction sacrifices scene context. Fixed third-person camera only.

5. [[Wang2025_skil]](../REFERENCES/MAIN.md#Wang2025_skil) — Wang, You, Hu, Li, Gao et al., "SKIL: Semantic Keypoint Imitation Learning for Generalizable Data-Efficient Manipulation" (2025)
   - **arXiv**: 2501.14400
   - **thesis**: Semantic keypoints from vision foundation models, augmented with feature descriptors, reduce sample complexity while generalizing to unseen objects, variations, and cross-embodiment settings.
   - **core**: Semantic keypoint descriptor pairing foundation-model-extracted keypoints with deep features for instance-level correspondence.
   - **diff**: Prior methods use raw images (overfitting) or handcrafted keypoints (requiring annotation). SKIL automatically extracts semantic keypoints via DiFT.
   - **limit**: Performance upper-bounded by vision foundation model (DiFT). Lacks environment-level perception for multi-obstacle safety.

6. [[Simeonov2022_ndf]](../REFERENCES/MAIN.md#Simeonov2022_ndf) — Simeonov, Du, Tagliasacchi, Tenenbaum, Rodriguez, Agrawal, Sitzmann, "Neural Descriptor Fields: SE(3)-Equivariant Object Representations for Manipulation" (2022)
   - **DOI**: 10.1109/ICRA46639.2022.9812146
   - **thesis**: Continuous implicit neural fields that are SE(3)-equivariant, trained self-supervisedly, enable few-shot manipulation generalization across novel instances and arbitrary 3D orientations without keypoint annotation.
   - **core**: SE(3)-equivariant neural field architecture mapping 3D query points to dense descriptors consistent across instances and orientations.
   - **diff**: Prior dense-descriptor methods are not SE(3)-equivariant, require surface-only keypoints, and need human annotation. NDF overcomes all three.
   - **limit**: Non-rigid objects untested. Transfers poses but not trajectories. Static placement targets only.

7. [[Zhu2023_groot]](../REFERENCES/MAIN.md#Zhu2023_groot) — Zhu, Jiang, Stone, Zhu, "GROOT: Learning Generalizable Manipulation Policies with Object-Centric 3D Representations" (2023)
   - **arXiv**: 2310.14386
   - **thesis**: Object-centric 3D representations from segmented point clouds, processed by a transformer, confer visual-invariance sufficient for generalization across backgrounds, viewpoints, and new instances.
   - **core**: Segmentation correspondence model mapping task-relevant objects to consistent 3D representations at test time.
   - **diff**: Prior 3D methods use fixed encoders or cannot segment novel instances. GROOT introduces open-vocabulary segmentation correspondence.
   - **limit**: Assumes one instance per category. Fixed robot morphology only.

8. [[Ze2024_dp3]](../REFERENCES/MAIN.md#Ze2024_dp3) — Ze, Zhang, Zhang, Hu, Wang, Xu, "3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations" (2024)
   - **arXiv**: 2403.03954
   - **thesis**: Compact 3D representations from sparse point clouds via a lightweight encoder are sufficient for diffusion-policy learning that generalizes in space, viewpoint, appearance, and instance.
   - **core**: Compact 3D visual representation from efficient point encoder — low-dimensional yet informative.
   - **diff**: Prior diffusion policies rely on 2D RGB images (high-dimensional, view-dependent). DP3 replaces with point encoder output for stronger generalization.
   - **limit**: Optimal 3D representation for control not identified. Long-horizon tasks not addressed.

9. [[Wang2024_gendp]](../REFERENCES/MAIN.md#Wang2024_gendp) — Wang, Yin, Huang, Kelestemur, Wang et al., "GenDP: 3D Semantic Fields for Category-Level Generalizable Diffusion Policy" (2024)
   - **arXiv**: 2410.17488
   - **thesis**: Grounding diffusion policies in 3D semantic fields — per-point semantic relevance scores from foundation model descriptors — provides the consistency needed for category-level generalization.
   - **core**: 3D semantic field encoding geometric structure and category-level semantic consistency simultaneously.
   - **diff**: Diffusion Policy on RGB fails on unseen instances (20% success). DP3 uses geometry but lacks semantics. GenDP adds the semantic channel, raising success to 93%.
   - **limit**: Fixed reference features per task. Adaptive semantic field construction needed for long-horizon/fine-grained tasks.

### E. Base Architectures

Foundational policy architectures that serve as backbones for work in Categories A–D.

1. [[Zhao2023_act]](../REFERENCES/MAIN.md#Zhao2023_act) — Zhao, Kumar, Levine, Finn, "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware" (2023)
   - **arXiv**: 2304.13705
   - **thesis**: Action chunking with a transformer-based CVAE overcomes compounding error and non-stationarity in imitation learning for high-precision fine manipulation, even on low-cost hardware.
   - **core**: Action chunking (predicting fixed-length action sequences) + temporal ensemble (averaging overlapping predictions). Without chunking, error compounds.
   - **diff**: Prior behavior cloning on fine tasks required expensive hardware. ACT achieves 80–90% success with ~10 min of demos on $5k arms.
   - **limit**: Cannot perform multi-finger coordination, high torque, or fingernail-dependent tasks. Failed at candy-unwrapping (0/10 success).

2. [[Chi2023_diffusion_policy]](../REFERENCES/MAIN.md#Chi2023_diffusion_policy) — Chi, Xu, Feng, Cousineau, Du, Burchfiel, Tedrake, Song, "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion" (2023)
   - **DOI**: 10.1177/02783649241273668
   - **thesis**: Representing a policy as a conditional denoising diffusion process over action sequences consistently outperforms prior representations because diffusion naturally handles multimodality and high-dimensional action spaces.
   - **core**: Diffusion formulation (DDPM/DDIM over action sequences) with receding-horizon prediction. Handles multimodal distributions inherently.
   - **diff**: Prior policies (BC, IBC, LSTM-GMM) struggle with multimodal demonstrations. Diffusion Policy yields 46.9% average improvement over state-of-the-art.
   - **limit**: Inherits behavior-cloning limitations with insufficient data. Higher inference latency (insufficient for sub-10ms control).

3. [[Shridhar2023_peract]](../REFERENCES/MAIN.md#Shridhar2023_peract) — Shridhar, Manuelli, Fox, "PerAct: A Multi-Task Transformer for Robotic Manipulation" (2023)
   - **arXiv**: 2209.05451
   - **thesis**: Formulating manipulation as "next best voxel action" detection provides sufficient structural prior for a single language-conditioned transformer to learn 18 diverse 6-DoF tasks data-efficiently.
   - **core**: Voxelized 3D observation and action space encoding with Perceiver Transformer and language conditioning.
   - **diff**: Prior approaches use 2D images or separate task-specific policies. PerAct unifies 18 tasks via voxel-action detection.
   - **limit**: Relies on sampling-based motion planner (brittle for path-sensitive tasks). Discrete-time actions not applicable to real-time tasks. Not extensible to dexterous hands.

4. [[Goyal2023_rvt]](../REFERENCES/MAIN.md#Goyal2023_rvt) — Goyal, Xu, Guo, Blukis, Chao, Fox, "RVT: Robotic View Transformer for 3D Object Manipulation" (2023)
   - **arXiv**: 2306.14896
   - **thesis**: Re-rendering inputs from virtual viewpoints and aggregating via cross-view attention provides a scalable 3D representation that is 36× faster than voxel-based PerAct with superior performance.
   - **core**: Virtual viewpoint re-rendering replacing expensive 3D convolution with 2D attention over re-rendered views.
   - **diff**: PerAct and C2F-ARM use voxels that scale poorly. RVT achieves comparable success at 36× training and 2.3× inference speed.
   - **limit**: Virtual view layout manually designed. Requires calibrated camera-to-robot extrinsics.

### F. Surveys

2. [[Mavrakis2020_inertia_survey]](../REFERENCES/MAIN.md#Mavrakis2020_inertia_survey) — Mavrakis, Stolkin, "Estimation and Exploitation of Objects' Inertial Parameters in Robotic Grasping and Manipulation: A Survey" (2020)
   - **arXiv**: 1911.04397
   - **thesis**: Inertial parameters (mass, center of mass, inertia tensor) are a tractable prior for manipulation planning and control; existing estimation methods offer distinct trade-offs not yet systematically reconciled.
   - **core**: Taxonomic framework organizing estimation methods by interaction regime and linking to control tasks.
   - **diff**: No prior survey covered the full pipeline from inertial parameter estimation to exploitation across all interaction modes.
   - **limit**: limit not available (survey paper).

1. [[Ai2025_dynamics_review]](../REFERENCES/MAIN.md#Ai2025_dynamics_review) — Ai, Tian, Shi, Wang, Pfaff, Tan, Christensen, Su, Wu, Li, "A Review of Learning-Based Dynamics Models for Robotic Manipulation" (2025)
   - **DOI**: 10.1126/scirobotics.adt1497
   - **thesis**: Learning-based dynamics models have reached maturity to serve as a critical enabling layer for manipulation, but state representation is the central design bottleneck.
   - **core**: Representation-centric taxonomy organizing models by state representation, integrated with control and estimation interfaces.
   - **diff**: First systematic treatment of dynamics models spanning architecture, representations, and control integration for manipulation.
   - **limit**: limit not available (survey paper).

## Survey Methodology

### Search Review Checkpoint

- Papers presented to user: 35 (after deduplication from ~50 raw results)
- User additions: 0
- User removals: 4 (CAPTURE, Zhang CoRL contact-rich, PhyGrasp, Tobin visual DR)
- Target count adjustment: none (31 papers)
- Duplicates removed before checkpoint: ~10

### Search Log

#### Search Angle 1: Explicit Physical Properties for Manipulation

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | WebSearch | "explicit physical properties manipulation policy generalization" | ~10 | Found survey papers, PhysMem |
| 2 | WebSearch | "inertia friction conditioning robot manipulation learning" | ~10 | Friction modeling survey, contact-rich work |
| 3 | WebSearch | "physical parameter estimation manipulation policy" | ~10 | Found DREAM framework |
| 4 | WebSearch | "object physical properties robot grasping pushing generalization" | ~10 | Found PhyGrasp |
| 5 | WebSearch | "interpretable physical quantities robot learning manipulation" | ~10 | Neurosymbolic approaches |
| 6 | WebSearch | "Rapid Motor Adaptation" manipulation | ~10 | Found RMA, RMA2 |
| 7 | WebSearch | "domain randomization" physical parameters manipulation | ~10 | Found Peng 2018 |
| 8–42 | WebSearch | (various refinements — see full agent log) | ~10 each | Confirmed UP-OSI, OpenAI dexterous, ASID, CAPTURE, IMA, DensePhysNet |

#### Search Angle 2: Object-Centric and Pose-Based Policies

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | WebSearch | "6D pose manipulation policy imitation learning" | ~10 | PRISM-DP, SPOT, ActivePose |
| 2 | WebSearch | "object-centric representation robot manipulation generalization" | ~10 | OmniManip, GROOT |
| 3 | WebSearch | "point cloud manipulation policy transformer" | ~10 | DP3, PolarNet, PointMapPolicy |
| 4 | WebSearch | "ACT action chunking transformer manipulation" | ~10 | ACT confirmed |
| 5–12 | WebSearch | (refinements for SPOT, PerAct, SKIL, GenDP, NDF, DP3, Point Policy) | ~10 each | All confirmed |

#### Search Angle 3: Sim-to-Real and Physical Reasoning

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | WebSearch | "sim-to-real manipulation physical parameters adaptation" | ~10 | Peng 2018, Zhang CoRL |
| 2 | WebSearch | "system identification robot manipulation learning" | ~10 | UP-OSI, ASID |
| 3 | WebSearch | "physics-informed manipulation policy learning" | ~10 | PIN-WM |
| 4 | WebSearch | "pushing task object generalization robot learning" | ~10 | DensePhysNet, Push-Net |
| 5–28 | WebSearch | (refinements for all papers in group) | ~10 each | gradSim, DREAM, Phys2Real, Chen2025, Asymmetric AC confirmed |

#### API Searches

| # | Source | Query | Results | Notes |
|---|--------|-------|---------|-------|
| 1 | Semantic Scholar API | "explicit physical properties manipulation policy generalization inertia friction" | 484 total, 20 returned | Low relevance — query too broad |
| 2 | OpenAlex API | "physical properties conditioning manipulation policy object generalization" | 5883 total, 20 returned | Low relevance — query too broad |

**Source summary**: WebSearch (primary, ~90 queries across 3 angles), ar5iv (limit field retrieval, ~15 papers), arXiv API (supplementary), Semantic Scholar API (1 query, low yield), OpenAlex API (1 query, low yield), DBLP (DOI resolution, pending).

### DOI Resolution Log

- Papers with publisher DOI resolved: 18 / 31
- Papers remaining arXiv-only: 5 (SPOT, Point Policy, SKIL, PRISM-DP, PIN-WM — preprint or venue unconfirmed in metadata)
- Papers with proceedings URL only (no standard DOI): 5 (gradSim/ICLR, GROOT/CoRL, RVT/CoRL, ASID/ICLR, GenDP/CoRL — PMLR/OpenReview)
- Papers with OpenReview only: 1 (DREAM — venue pending)
- Resolution sources used: DBLP (12 queries), Semantic Scholar (8), Crossref (3), WebFetch DOI (15)

| Paper | arXiv ID | Publisher DOI | Source | Notes |
|-------|----------|---------------|--------|-------|
| UP-OSI | 1702.02453 | 10.15607/RSS.2017.XIII.048 | DBLP | RSS 2017 |
| Dynamics Rand. | 1710.06537 | 10.1109/ICRA.2018.8460528 | DBLP | ICRA 2018 |
| Push-Net | — | 10.15607/RSS.2018.XIV.024 | DBLP | RSS 2018 |
| Asymmetric AC | 1710.06542 | 10.15607/RSS.2018.XIV.008 | DBLP | RSS 2018 |
| DensePhysNet | 1906.03853 | 10.15607/RSS.2019.XV.046 | DBLP | RSS 2019 |
| Inertia Survey | 1911.04397 | 10.1016/j.robot.2019.103374 | DBLP | RAS 2020 |
| Dexterous | 1808.00177 | 10.1177/0278364919887447 | given | IJRR 2020 |
| RMA | 2107.04034 | 10.15607/RSS.2021.XVII.011 | DBLP | RSS 2021 |
| gradSim | 2104.02646 | — | — | ICLR 2021; OpenReview only |
| NDF | 2112.05124 | 10.1109/ICRA46639.2022.9812146 | given | ICRA 2022 |
| Cloth+PB | 2409.15635 | 10.3389/fnbot.2022.890695 | given | Frontiers 2022 |
| ACT | 2304.13705 | 10.15607/RSS.2023.XIX.016 | DBLP | RSS 2023 |
| Diffusion Policy | 2303.04137 | 10.1177/02783649241273668 | given | IJRR 2024 |
| GROOT | 2310.14386 | — | — | CoRL 2023; PMLR v229 |
| PerAct | 2209.05451 | — | — | **CoRL 2022** (corrected); PMLR v205 |
| RVT | 2306.14896 | — | — | CoRL 2023; PMLR v229 |
| ASID | 2404.12308 | — | — | ICLR 2024; OpenReview only |
| RMA2 | 2312.04670 | 10.1109/CVPR52733.2024.01552 | DBLP | **CVPR 2024** (corrected from arXiv-only) |
| SPOT | 2411.00965 | — | — | Preprint (venue unconfirmed) |
| DP3 | 2403.03954 | 10.15607/RSS.2024.XX.067 | DBLP | RSS 2024 |
| GenDP | 2410.17488 | — | — | CoRL 2024; PMLR v270 |
| IMA | 2412.11829 | 10.1177/02783649251344638 | given | IJRR 2025 |
| DREAM | — | — | — | OpenReview S0FmCZ6by5; venue pending |
| PIN-WM | 2504.16693 | — | — | RSS 2025 (per arXiv abstract) |
| Phys2Real | 2510.11689 | — | — | **ICRA 2026** (corrected; per arXiv v2) |
| Chen et al. | 2410.03920 | 10.1109/ICRA55743.2025.11127955 | DBLP | ICRA 2025 |
| OmniManip | 2501.03841 | 10.1109/CVPR52734.2025.01618 | DBLP | CVPR 2025 |
| Point Policy | 2502.20391 | — | — | Preprint (CoRL 2025 unconfirmed) |
| SKIL | 2501.14400 | — | — | Preprint (RSS 2025 unconfirmed) |
| PRISM-DP | 2504.20359 | — | — | Preprint |
| Ai et al. Review | — | 10.1126/scirobotics.adt1497 | given | Science Robotics 2025 |

### Hallucination Check Results

- Papers checked: 31
- Passed: 31
- Failed and re-searched: 0
- Removed (unverifiable): 0

**Venue corrections applied**: PerAct → CoRL 2022 (was CoRL 2023), RMA2 → CVPR 2024 (was arXiv-only), Phys2Real → ICRA 2026 (was arXiv preprint).

### Limit Field Coverage

- Papers with limit recorded: 20 / 31 (65%)
- Papers marked "limit not available": 6 (Peng2018, Push-Net, Pinto2018, DREAM, Chen2025, Ai2025 survey, Mavrakis2020 survey)
- Breakdown: 3 no formal limitations section (older papers), 2 survey papers (no Limitations expected), 1 paper removed from arXiv, 1 workshop paper
