# Literature Search Log: Sim-to-Real, RL Pick-and-Place, Imitation Learning for Manipulation

**Date**: 2026-04-06
**Topic**: Robotic grasping and stable object placement -- sim-to-real transfer, RL for pick-and-place, imitation learning for manipulation
**Scope**: 2020-2026, top venues

---

## Search Log

### Search 1: Semantic Scholar -- "sim-to-real transfer robot manipulation"
- **Source**: Semantic Scholar API (search_semantic_scholar)
- **Query**: `sim-to-real transfer robot manipulation`
- **Filters**: year_from=2020, limit=40
- **Results returned**: 40 / 1714 total
- **Relevance**: High. Returned papers on action space design for sim-to-real, contact-rich manipulation transfer, domain randomization, visual sim-to-real, dexterous in-hand manipulation. Strong coverage of ICRA, CoRL, RSS, RA-L venues.

### Search 2: Semantic Scholar -- "reinforcement learning pick and place"
- **Source**: Semantic Scholar API (search_semantic_scholar)
- **Query**: `reinforcement learning pick and place`
- **Filters**: year_from=2020, limit=40
- **Results returned**: 40 / 230 total
- **Relevance**: Medium-high. Many results are from lower-tier venues (MDPI journals, regional conferences). A few high-quality papers on hierarchical RL, task decomposition, sim-to-real pick-and-place. Notable survey paper (Lobbezoo et al. 2021, 63 citations).

### Search 3: Semantic Scholar -- "imitation learning robot manipulation grasping"
- **Source**: Semantic Scholar API (search_semantic_scholar)
- **Query**: `imitation learning robot manipulation grasping`
- **Filters**: year_from=2020, limit=40
- **Results returned**: 40 / 1715 total
- **Relevance**: High. Returned seminal papers on language-conditioned IL (Stepputtis et al. 2020, NeurIPS, 238 cites), coarse-to-fine IL (Johns 2021, ICRA, 160 cites), continual IL (LOTUS, ICRA 2024, 64 cites), dual-arm IL (Kim et al., T-RO, 61 cites), diffusion policy (Chi et al. 2023, RSS, 2755 cites).

### Search 4: Semantic Scholar -- "diffusion policy robot manipulation"
- **Source**: Semantic Scholar API (search_semantic_scholar)
- **Query**: `diffusion policy robot manipulation`
- **Filters**: year_from=2023, limit=10
- **Results returned**: 10 / 2909 total
- **Relevance**: High. Captured the foundational Diffusion Policy paper (Chi et al. 2023, 2755 cites) and multiple follow-ups including hierarchical, equivariant, and long-horizon variants.

### Search 5: Semantic Scholar -- "EquiBot equivariant diffusion policy manipulation"
- **Source**: Semantic Scholar API (search_semantic_scholar)
- **Query**: `EquiBot equivariant diffusion policy manipulation`
- **Filters**: year_from=2024, limit=5
- **Results returned**: 5 / 9 total
- **Relevance**: High. Captured EquiBot (CoRL 2024, 77 cites) and related equivariant diffusion policy works.

### Search 6: Semantic Scholar -- "SimPLE simulation pick localize place regrasp"
- **Source**: Semantic Scholar API (search_semantic_scholar)
- **Query**: `SimPLE simulation pick localize place regrasp`
- **Filters**: year_from=2024, limit=5
- **Results returned**: 5 / 33 total (1 relevant)
- **Relevance**: Found the target paper: SimPLE (Bauza et al. 2024, Science Robotics, 23 cites). Other results irrelevant.

### Search 7: Semantic Scholar -- "SimplerEnv simulated evaluation real-world robot manipulation policies"
- **Source**: Semantic Scholar API (search_semantic_scholar)
- **Query**: `SimplerEnv simulated evaluation real-world robot manipulation policies`
- **Filters**: year_from=2024, limit=5
- **Results returned**: 5 / 619 total
- **Relevance**: Found SIMPLER (Li et al. 2024, CoRL, 316 cites) and related real-to-sim evaluation frameworks.

### Search 8: WebSearch -- "sim-to-real manipulation policy learning 2023 2024 2025 ICRA CoRL"
- **Source**: WebSearch
- **Query**: `sim-to-real manipulation policy learning 2023 2024 2025 ICRA CoRL`
- **Results returned**: 10 links
- **Relevance**: Medium. Surfaced EquiBot (CoRL 2024), ManiFlow (CoRL 2025), SimplerEnv (CoRL 2024), foundation model surveys. Helped confirm venue/year metadata. Also pointed to VLA model trend.

### Search 9: WebSearch -- "imitation learning pick and place robot 2024 2025"
- **Source**: WebSearch
- **Query**: `imitation learning pick and place robot 2024 2025`
- **Results returned**: 10 links
- **Relevance**: Medium-high. Found the one-shot visual IL paper (Lu et al. 2025, Scientific Reports), SimPLE (MIT/Science Robotics), LeRobot framework, and a survey on IL for contact-rich tasks.

### Search 10: WebSearch -- "reinforcement learning robotic grasping placement 2022 2023"
- **Source**: WebSearch
- **Query**: `reinforcement learning robotic grasping placement 2022 2023`
- **Results returned**: 10 links
- **Relevance**: Medium. Pointed to survey papers on learning-based grasping and RL for manipulation. Confirmed that most RL grasping work optimizes grasp stability in isolation, with post-grasp placement under-explored.

---

## Collected Papers (Deduplicated, Filtered for Relevance)

Papers are grouped by theme. Only papers with clear relevance to robotic grasping/placement, sim-to-real transfer, or pick-and-place demonstration tasks are included. Papers on non-manipulation domains (mobile robots, surgery-only, non-robotics) are excluded.

### A. Sim-to-Real Transfer for Manipulation

| # | Title | First Author | Year | Venue | Cites | DOI | arXiv | Relevance Note |
|---|-------|-------------|------|-------|-------|-----|-------|----------------|
| A1 | On the Role of the Action Space in Robot Manipulation Learning and Sim-to-Real Transfer | Aljalbout et al. | 2023 | RA-L | 30 | 10.1109/LRA.2024.3398428 | 2312.03673 | Systematic study of action space design for sim-to-real RL transfer in reaching/pushing |
| A2 | DrEureka: Language Model Guided Sim-To-Real Transfer | Ma et al. | 2024 | RSS | 82 | 10.48550/arXiv.2406.01967 | 2406.01967 | LLM-guided domain randomization and reward tuning for sim-to-real |
| A3 | TRANSIC: Sim-to-Real Policy Transfer by Learning from Online Correction | Jiang et al. | 2024 | CoRL | 65 | 10.48550/arXiv.2405.10315 | 2405.10315 | Human-in-the-loop online correction for sim-to-real gap closure |
| A4 | Efficient Sim-to-real Transfer of Contact-Rich Manipulation Skills with Online Admittance Residual Learning | Zhang et al. | 2023 | CoRL | 45 | 10.48550/arXiv.2310.10509 | 2310.10509 | Admittance residual policy for contact-rich assembly transfer |
| A5 | Grasp Stability Prediction with Sim-to-Real Transfer from Tactile Sensing | Si et al. | 2022 | IROS | 45 | 10.1109/IROS47612.2022.9981863 | 2208.02885 | Tactile-based grasp stability prediction with sim-to-real |
| A6 | Robust Visual Sim-to-Real Transfer for Robotic Manipulation | Garcia Pinel et al. | 2023 | IROS | 10 | 10.1109/IROS55552.2023.10342471 | 2307.15320 | Visual domain adaptation for robust sim-to-real manipulation |
| A7 | Sim-to-Real Learning for Humanoid Box Loco-Manipulation | Dao et al. | 2023 | ICRA | 61 | 10.1109/ICRA57147.2024.10610977 | 2310.03191 | Sim-to-real for whole-body humanoid pick-and-carry |
| A8 | Bridging the Sim-to-Real Gap with Dynamic Compliance Tuning for Industrial Insertion | Zhang et al. | 2023 | ICRA | 27 | 10.1109/ICRA57147.2024.10610707 | 2311.07499 | Dynamic compliance for contact-rich insertion sim-to-real |
| A9 | Learning Sim-to-Real Dense Object Descriptors for Robotic Manipulation | Cao et al. | 2023 | ICRA | 3 | 10.1109/ICRA48891.2023.10161477 | 2304.08703 | Dense descriptor learning for generalizable sim-to-real grasping |
| A10 | DemoStart: Demonstration-Led Auto-Curriculum Applied to Sim-to-Real with Multi-Fingered Robots | Bauza et al. | 2024 | ICRA | 12 | 10.1109/ICRA55743.2025.11127813 | 2409.06613 | Auto-curriculum from demos for dexterous sim-to-real |
| A11 | Modularity through Attention: Efficient Training and Transfer of Language-Conditioned Policies for Robot Manipulation | Zhou et al. | 2022 | CoRL | 28 | 10.48550/arXiv.2212.04573 | 2212.04573 | Modular attention for language-conditioned sim-to-real transfer |
| A12 | A Sim-to-Real Learning-Based Framework for Contact-Rich Assembly by Utilizing CycleGAN and Force Control | Shi et al. | 2023 | T-CDS | 31 | 10.1109/TCDS.2023.3237734 | N/A | CycleGAN visual adaptation + force control for assembly sim-to-real |
| A13 | Re3Sim: Generating High-Fidelity Simulation Data via 3D-Photorealistic Real-to-Sim for Robotic Manipulation | Han et al. | 2025 | arXiv | 29 | 10.48550/arXiv.2502.08645 | 2502.08645 | Real-to-sim 3D reconstruction for high-fidelity training data |
| A14 | X-Sim: Cross-Embodiment Learning via Real-to-Sim-to-Real | Dan et al. | 2025 | arXiv | 13 | 10.48550/arXiv.2505.07096 | 2505.07096 | Cross-embodiment policy transfer through real-to-sim-to-real pipeline |
| A15 | A Recipe for Efficient Sim-to-Real Transfer in Manipulation with Online Imitation-Pretrained World Models | Wang et al. | 2025 | arXiv | 2 | 10.48550/arXiv.2510.02538 | 2510.02538 | World-model-based approach for efficient sim-to-real manipulation |
| A16 | Sim-to-Real Deep Reinforcement Learning with Manipulators for Pick-and-Place | Liu et al. | 2023 | TAROS | 1 | 10.1007/978-3-031-43360-3_20 | 2309.09247 | Directly addresses sim-to-real RL for pick-and-place |
| A17 | Pixel2Catch: Multi-Agent Sim-to-Real Transfer for Agile Manipulation with a Single RGB Camera | Kim et al. | 2026 | arXiv | 0 | 10.48550/arXiv.2602.22733 | 2602.22733 | Multi-agent agile catching with single RGB, sim-to-real |
| A18 | One-shot sim-to-real transfer policy for robotic assembly via RL with visual demonstration | Xiao et al. | 2024 | Robotica | 7 | 10.1017/S0263574724000092 | N/A | One-shot transfer for assembly tasks |
| A19 | Evaluating Real-World Robot Manipulation Policies in Simulation (SIMPLER) | Li et al. | 2024 | CoRL | 316 | 10.48550/arXiv.2405.05941 | 2405.05941 | Benchmark for evaluating real manipulation policies in sim; real-to-sim evaluation |

### B. Reinforcement Learning for Pick-and-Place

| # | Title | First Author | Year | Venue | Cites | DOI | arXiv | Relevance Note |
|---|-------|-------------|------|-------|-------|-----|-------|----------------|
| B1 | Reinforcement Learning for Pick and Place Operations in Robotics: A Survey | Lobbezoo et al. | 2021 | Robotics (MDPI) | 63 | 10.3390/robotics10030105 | N/A | Comprehensive survey of RL approaches for pick-and-place |
| B2 | Towards Hierarchical Task Decomposition using Deep RL for Pick and Place Subtasks | Marzari et al. | 2021 | ICAR | 36 | 10.1109/ICAR53236.2021.9659344 | 2102.04022 | Hierarchical RL decomposition for pick-and-place |
| B3 | Reinforcement Learning for Collaborative Robots Pick-and-Place Applications: A Case Study | Gomes et al. | 2022 | Automation | 30 | 10.3390/automation3010011 | N/A | RL for collaborative robot pick-and-place |
| B4 | Simulated and Real Robotic Reach, Grasp, and Pick-and-Place Using Combined RL and Traditional Controls | Lobbezoo et al. | 2023 | Robotics (MDPI) | 25 | 10.3390/robotics12010012 | N/A | Hybrid RL + classical control for pick-and-place |
| B5 | Learning Needle Pick-and-Place Without Expert Demonstrations | Bendikas et al. | 2023 | RA-L | 22 | 10.1109/LRA.2023.3266720 | N/A | Self-supervised RL for needle pick-and-place (surgical) |
| B6 | Prehensile and Non-Prehensile Robotic Pick-and-Place of Objects in Clutter Using Deep RL | Imtiaz et al. | 2023 | Sensors (MDPI) | 20 | 10.3390/s23031513 | N/A | Deep RL for cluttered pick-and-place with prehensile/non-prehensile actions |
| B7 | Pick and Place Objects in a Cluttered Scene Using Deep Reinforcement Learning | Mohammed et al. | 2020 | N/A | 19 | N/A | N/A | Early deep RL for cluttered pick-and-place |
| B8 | Towards Intelligent Pick and Place Assembly Using RL | Neef et al. | 2020 | IHSED | 4 | 10.1007/978-3-030-58282-1_51 | 2002.08333 | RL for individualized product assembly |
| B9 | Multiagent Hierarchical RL With Asynchronous Termination Applied to Robotic Pick and Place | Lan et al. | 2024 | IEEE Access | 4 | 10.1109/ACCESS.2024.3409076 | N/A | Multi-agent hierarchical RL for coordinated pick-and-place |
| B10 | PolyDexFrame: Deep RL-Based Pick-and-Place of Objects in Clutter | Imtiaz et al. | 2024 | Machines | 1 | 10.3390/machines12080547 | N/A | Dexterous RL framework for cluttered pick-and-place |

### C. Imitation Learning for Manipulation (with Grasping/Placement)

| # | Title | First Author | Year | Venue | Cites | DOI | arXiv | Relevance Note |
|---|-------|-------------|------|-------|-------|-----|-------|----------------|
| C1 | Diffusion Policy: Visuomotor Policy Learning via Action Diffusion | Chi et al. | 2023 | RSS / IJRR | 2755 | 10.1177/02783649241273668 | 2303.04137 | Foundational diffusion-based IL; benchmarked on manipulation including pick-and-place |
| C2 | Language-Conditioned Imitation Learning for Robot Manipulation Tasks | Stepputtis et al. | 2020 | NeurIPS | 238 | N/A | 2010.12083 | Language-conditioned IL for manipulation; seminal work |
| C3 | Coarse-to-Fine Imitation Learning: Robot Manipulation from a Single Demonstration | Johns | 2021 | ICRA | 160 | 10.1109/ICRA48506.2021.9560942 | 2105.06411 | One-shot IL framework for manipulation tasks |
| C4 | NeRF in the Palm of Your Hand: Corrective Augmentation for Robotics via Novel-View Synthesis | Zhou et al. | 2023 | CVPR | 85 | 10.1109/CVPR52729.2023.01717 | 2301.08556 | NeRF-based data augmentation for manipulation IL |
| C5 | EquiBot: SIM(3)-Equivariant Diffusion Policy for Generalizable and Data Efficient Learning | Yang et al. | 2024 | CoRL | 77 | 10.48550/arXiv.2407.01479 | 2407.01479 | Equivariant diffusion policy for data-efficient manipulation |
| C6 | Transformer-based Deep Imitation Learning for Dual-Arm Robot Manipulation | Kim et al. | 2021 | IROS | 67 | 10.1109/IROS51168.2021.9636301 | 2108.00385 | Transformer architecture for dual-arm manipulation IL |
| C7 | LOTUS: Continual Imitation Learning for Robot Manipulation Through Unsupervised Skill Discovery | Wan et al. | 2023 | ICRA | 64 | 10.1109/ICRA57147.2024.10611129 | 2311.02058 | Continual learning with unsupervised skill discovery for manipulation |
| C8 | Goal-Conditioned Dual-Action Imitation Learning for Dexterous Dual-Arm Robot Manipulation | Kim et al. | 2022 | T-RO | 61 | 10.1109/TRO.2024.3372778 | 2203.09749 | Goal-conditioned IL for dual-arm dexterous manipulation |
| C9 | Generalization Guarantees for Imitation Learning | Ren et al. | 2020 | CoRL | 33 | N/A | N/A | Theoretical analysis of IL generalization for manipulation |
| C10 | Imitation of Manipulation Skills Using Multiple Geometries | Ti et al. | 2022 | IROS | 3 | 10.1109/IROS47612.2022.9981683 | 2203.01171 | Multi-geometry representation for manipulation skill transfer |
| C11 | Imitation Learning for Nonprehensile Manipulation Through Self-Supervised Learning Considering Motion Speed | Saigusa et al. | 2022 | IEEE Access | 18 | 10.1109/ACCESS.2022.3185651 | 2206.10289 | Self-supervised IL for non-prehensile manipulation |
| C12 | On the Effectiveness of Retrieval, Alignment, and Replay in Manipulation | Di Palo et al. | 2023 | RA-L | 15 | 10.1109/LRA.2024.3349832 | 2312.12345 | Retrieval-augmented IL for manipulation |
| C13 | Memory-based Gaze Prediction in Deep Imitation Learning for Robot Manipulation | Kim et al. | 2022 | ICRA | 17 | 10.1109/icra46639.2022.9812087 | 2202.04877 | Gaze-guided IL for manipulation with memory |
| C14 | Learning Robot Manipulation from Cross-Morphology Demonstration | Salhotra et al. | 2023 | CoRL | 14 | N/A | 2304.03833 | Cross-embodiment IL for manipulation |
| C15 | RoboCopilot: Human-in-the-loop Interactive Imitation Learning for Robot Manipulation | Wu et al. | 2025 | arXiv | 18 | 10.48550/arXiv.2503.07771 | 2503.07771 | Interactive IL with human correction for manipulation |
| C16 | Visual imitation learning from one-shot demonstration for multi-step robot pick and place tasks | Lu et al. | 2025 | Scientific Reports | 2 | 10.1038/s41598-025-30938-x | N/A | One-shot visual IL specifically for multi-step pick-and-place |

### D. Diffusion Policy Extensions (Relevant to Manipulation/Pick-and-Place)

| # | Title | First Author | Year | Venue | Cites | DOI | arXiv | Relevance Note |
|---|-------|-------------|------|-------|-------|-----|-------|----------------|
| D1 | ManiFlow: A General Robot Manipulation Policy via Consistency Flow Training | Yan et al. | 2025 | arXiv | 19 | 10.48550/arXiv.2509.01819 | 2509.01819 | Flow-matching-based IL for general manipulation |
| D2 | Hierarchical Diffusion Policy: Manipulation Trajectory Generation via Contact Guidance | Wang et al. | 2025 | T-RO | 19 | 10.1109/TRO.2025.3547272 | N/A | Contact-guided diffusion for manipulation |
| D3 | ET-SEED: Efficient Trajectory-Level SE(3) Equivariant Diffusion Policy | Tie et al. | 2024 | ICLR | 19 | 10.48550/arXiv.2411.03990 | 2411.03990 | Trajectory-level equivariant diffusion for data-efficient manipulation |
| D4 | Diffusion Trajectory-Guided Policy for Long-Horizon Robot Manipulation | Fan et al. | 2025 | RA-L | 14 | 10.1109/LRA.2025.3619794 | 2502.10040 | Diffusion trajectory guidance for long-horizon manipulation |

### E. Precise Pick-and-Place / Visuotactile

| # | Title | First Author | Year | Venue | Cites | DOI | arXiv | Relevance Note |
|---|-------|-------------|------|-------|-------|-----|-------|----------------|
| E1 | SimPLE: A Visuotactile Method Learned in Simulation to Precisely Pick, Localize, Regrasp, and Place Objects | Bauza et al. | 2024 | Science Robotics | 23 | 10.1126/scirobotics.adi8808 | N/A | Sim-to-real visuotactile for precise pick-and-place with regrasping; directly on topic |
| E2 | AnyRotate: Gravity-Invariant In-Hand Object Rotation with Sim-to-Real Touch | Yang et al. | 2024 | CoRL | 43 | 10.48550/arXiv.2405.07391 | 2405.07391 | Tactile sim-to-real for in-hand rotation (related to placement orientation) |

### F. Surveys and Evaluation Frameworks

| # | Title | First Author | Year | Venue | Cites | DOI | arXiv | Relevance Note |
|---|-------|-------------|------|-------|-------|-----|-------|----------------|
| F1 | A Survey of Embodied Learning for Object-centric Robotic Manipulation | Zheng et al. | 2024 | MIR | 33 | 10.1007/s11633-025-1542-8 | 2408.11537 | Comprehensive survey covering RL/IL for object manipulation |
| F2 | Guided Reinforcement Learning for Robust Multi-Contact Loco-Manipulation | Sleiman et al. | 2024 | CoRL | 17 | 10.48550/arXiv.2410.13817 | 2410.13817 | Guided RL framework for contact-rich loco-manipulation |

---

## Summary Statistics

- **Total unique papers collected**: 53
- **By theme**: Sim-to-Real (19), RL Pick-and-Place (10), Imitation Learning (16), Diffusion Policy (4), Precise Pick-and-Place (2), Surveys (2)
- **By venue tier** (approximate):
  - Top venues (ICRA, IROS, CoRL, RSS, NeurIPS, CVPR, ICLR, T-RO, RA-L, Science Robotics, IJRR): 33
  - Mid-tier / workshops / arXiv: 14
  - Lower-tier: 6
- **Searches executed**: 10 (7 Semantic Scholar, 3 WebSearch)
- **Total S2 hits scanned**: 40 + 40 + 40 + 10 + 5 + 5 + 5 = 145 papers scanned, 53 retained after relevance filtering and deduplication
