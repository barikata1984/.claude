# Literature Search Log: Foundation Models, Language-Conditioned Policies, and VLA Models for Manipulation

**Date**: 2026-04-06
**Topic**: Foundation models, language-conditioned policies, and vision-language-action models applied to manipulation tasks (pick-and-place focus)
**Scope**: 2020--2026, top venues (RSS, CoRL, ICRA, IROS, NeurIPS, ICML, ICLR, CVPR, AAAI, Science Robotics, IJRR, RA-L, T-ASE)

---

## 1. Search Log

| # | Source | Exact Query | Results | Relevance Note |
|---|--------|-------------|---------|----------------|
| 1 | Semantic Scholar | "foundation model robot manipulation" (year_from=2020, limit=40) | 11,253 total / 40 returned | High relevance. Top results include RDT-1B, SAM-E, Magma, General Flow, Distilled Feature Fields, GNFactor, and several VLA foundation models. Good coverage of 2023-2026 papers. |
| 2 | Semantic Scholar | "language conditioned robot manipulation pick place" (year_from=2020, limit=40) | 1,140 total / 40 returned | High relevance. Includes RFST (fast/slow thinking), A^2 pick-and-place alignment, CALVIN benchmark, language-conditioned IL (NeurIPS 2020), CLIPort descendants, and several language-grounded policy papers. |
| 3 | Semantic Scholar | "vision language action model robot" (year_from=2020, limit=40) | 5,830 total / 40 returned | Very high relevance. Dominated by VLA papers: OpenVLA, pi0, pi0.5, RT-2, ChatVLA, FAST tokenization, fine-tuning VLAs, RoboMamba, and many 2025 VLA variants. |
| 4 | WebSearch | "foundation model robotic manipulation survey 2024 2025" | 10 links | Found 4 major survey papers: Firoozi et al. (IJRR 2025), Li et al. (IJRR 2025), Xiao et al. (Neurocomputing 2025), diffusion models survey (Frontiers 2025). |
| 5 | WebSearch | "language conditioned manipulation policy pick and place" | 10 links | Found A^2 (T-ASE 2025), RFST (ICRA 2024), language-conditioned IL survey (arXiv 2312.10807), HULC/CALVIN line of work. |
| 6 | WebSearch | "VLA vision language action model robot 2024 2025" | 10 links | Found VLA survey papers, OpenVLA, RT-2, pi0, SmolVLA, CoA-VLA (ICCV 2025), Wikipedia entry on VLAs, and deployment notes (Figure AI at BMW). |
| 7 | WebSearch | "survey robotic manipulation learning 2023 2024" | 10 links | Found surveys on in-hand manipulation (Frontiers 2024), diffusion models for manipulation (Frontiers 2025), embodied learning for object-centric manipulation (MIR 2025), interactive IL for dexterous manipulation. |
| 8 | Semantic Scholar | "CLIPort language grounding transporter network manipulation" (year_from=2020, limit=10) | 21 total / 10 returned | Found CLIPort (CoRL 2021, 872 citations) directly. Also related grounding works. |
| 9 | Semantic Scholar | "RT-1 robotics transformer real world manipulation" (year_from=2022, limit=10) | 558 total / 10 returned | Found RT-1 (RSS 2022, 2019 citations), BAKU (NeurIPS 2024), and other real-world manipulation works. |
| 10 | Semantic Scholar | "SayCan grounding language models affordances" (year_from=2022, limit=10) | 84 total / 10 returned | Found SayCan (CoRL 2022, 2905 citations), HULC2, AffordanceLLM, 3D-LLM. |
| 11 | Semantic Scholar | "Octo generalist robot policy transformer" (year_from=2023, limit=10) | 27 total / 10 returned | Found Octo (RSS 2024, 1113 citations), Dita, RLDG, Diffusion Transformer Policy, REGENT. |
| 12 | Semantic Scholar | "diffusion policy visuomotor robot manipulation" (year_from=2023, limit=10) | 554 total / 10 returned | Found Diffusion Policy (RSS 2023, 2755 citations), ScaleDP (ICRA 2025), Dreamitate (CoRL 2024), ManiFlow. |
| 13 | Semantic Scholar | "survey foundation model robotic manipulation" (year_from=2023, limit=10) | 660 total / 10 returned | Found GAI in robotic manipulation survey (2025), VLA survey for embodied manipulation, OpenHelix dual-system VLA survey, SAM2Act. |

---

## 2. Collected Papers (De-duplicated, sorted by category)

### 2.1 Landmark / Highly-Cited Foundation Papers

| # | Title | First Author | Year | Venue | Citations | arXiv / DOI | Relevance |
|---|-------|-------------|------|-------|-----------|-------------|-----------|
| 1 | **Diffusion Policy: Visuomotor Policy Learning via Action Diffusion** | Cheng Chi et al. | 2023 | RSS / IJRR | 2,755 | 2303.04137 | Foundational diffusion-based policy; de facto standard for manipulation policy learning |
| 2 | **Do As I Can, Not As I Say: Grounding Language in Robotic Affordances (SayCan)** | Michael Ahn et al. | 2022 | CoRL | 2,905 | 2204.01691 | Seminal work connecting LLMs to robot affordances for task planning |
| 3 | **RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control** | Anthony Brohan et al. | 2023 | CoRL | 2,686 | 2307.15818 | First large-scale VLA; showed web-scale VLM knowledge transfers to robot actions |
| 4 | **RT-1: Robotics Transformer for Real-World Control at Scale** | Anthony Brohan et al. | 2022 | RSS | 2,019 | 2212.06817 | Pioneered transformer-based robot policies at scale with 130k real demos |
| 5 | **OpenVLA: An Open-Source Vision-Language-Action Model** | Moo Jin Kim et al. | 2024 | CoRL | 1,883 | 2406.09246 | 7B open-source VLA; became community standard baseline |
| 6 | **pi0: A Vision-Language-Action Flow Model for General Robot Control** | Kevin Black et al. | 2024 | arXiv / RSS 2025 | 1,380+77 | 2410.24164 | Flow-matching VLA from Physical Intelligence; strong generalist capabilities |
| 7 | **Octo: An Open-Source Generalist Robot Policy** | Octo Model Team et al. | 2024 | RSS | 1,113 | 2405.12213 | Large open-source transformer policy trained on Open X-Embodiment (800k trajs) |
| 8 | **CLIPort: What and Where Pathways for Robotic Manipulation** | Mohit Shridhar et al. | 2021 | CoRL | 872 | 2109.12098 | Combined CLIP semantics with Transporter spatial precision; influential for language-conditioned manipulation |
| 9 | **pi0.5: A Vision-Language-Action Model with Open-World Generalization** | Physical Intelligence et al. | 2025 | arXiv | 680 | 2504.16054 | Extended pi0 with hierarchical policy; first generalization to unseen real-world environments |
| 10 | **RDT-1B: A Diffusion Foundation Model for Bimanual Manipulation** | Songming Liu et al. | 2024 | ICLR | 499 | 2410.07864 | 1B-param diffusion transformer for bimanual tasks; pioneered diffusion FM for dual-arm |
| 11 | **CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks** | Oier Mees et al. | 2021 | RA-L | 494 | 2112.03227 | Standard benchmark for language-conditioned long-horizon manipulation |
| 12 | **FAST: Efficient Action Tokenization for Vision-Language-Action Models** | Karl Pertsch et al. | 2025 | RSS | 353 | 2501.09747 | Frequency-space action tokenization enabling 5x faster VLA training |
| 13 | **Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success** | Moo Jin Kim et al. | 2025 | RSS | 364 | 2502.19645 | OpenVLA-OFT; systematic study of VLA fine-tuning strategies |
| 14 | **Language-Conditioned Imitation Learning for Robot Manipulation Tasks** | Simon Stepputtis et al. | 2020 | NeurIPS | 238 | 2010.12083 | Early language-conditioned IL; showed language grounding in demonstration learning |
| 15 | **Learning Language-Conditioned Robot Behavior from Offline Data and Crowd-Sourced Annotation** | Suraj Nair et al. | 2021 | CoRL | 183 | 2109.01115 | Efficient language annotation; less than 1% pairing cost via multicontext IL |

### 2.2 VLA Models (2024--2026)

| # | Title | First Author | Year | Venue | Citations | arXiv / DOI | Relevance |
|---|-------|-------------|------|-------|-----------|-------------|-----------|
| 16 | **Distilled Feature Fields Enable Few-Shot Language-Guided Manipulation** | William Shen et al. | 2023 | CoRL | 156 | 2308.07931 | Feature field distillation for language-guided manipulation; few-shot capability |
| 17 | **GNFactor: Multi-Task Real Robot Learning with Generalizable Neural Feature Fields** | Yanjie Ze et al. | 2023 | CoRL | 145 | 2308.16891 | Neural feature fields for generalizable multi-task learning |
| 18 | **Video Prediction Policy: A Generalist Robot Policy with Predictive Visual Representations** | Yucheng Hu et al. | 2024 | ICML | 139 | 2412.14803 | Video prediction as representation for generalist robot policy |
| 19 | **Gen2Act: Human Video Generation in Novel Scenarios enables Generalizable Robot Manipulation** | Homanga Bharadhwaj et al. | 2024 | arXiv | 118 | 2409.16283 | Video generation for robot manipulation generalization |
| 20 | **Magma: A Foundation Model for Multimodal AI Agents** | Jianwei Yang et al. | 2025 | CVPR | 117 | 2502.13130 | Multimodal FM for embodied agents; broad action capabilities |
| 21 | **RoboMamba: Efficient Vision-Language-Action Model for Robotic Reasoning and Manipulation** | Jiaming Liu et al. | 2024 | NeurIPS | 97 | 2406.04339 | Mamba-based VLA; efficient reasoning architecture |
| 22 | **ChatVLA: Unified Multimodal Understanding and Robot Control** | Zhongyi Zhou et al. | 2025 | EMNLP | 94 | 2502.14420 | Unified multimodal understanding + action generation |
| 23 | **DreamVLA: A VLA Model Dreamed with Comprehensive World Knowledge** | Wenyao Zhang et al. | 2025 | arXiv | 89 | 2507.04447 | World knowledge integration into VLA |
| 24 | **General Flow as Foundation Affordance for Scalable Robot Learning** | Chengbo Yuan et al. | 2024 | CoRL | 83 | 2401.11439 | Flow-based affordance representation for scalable learning |
| 25 | **OneTwoVLA: A Unified VLA Model with Adaptive Reasoning** | Fanqi Lin et al. | 2025 | arXiv | 74 | 2505.11917 | Adaptive reasoning in VLA |
| 26 | **A Careful Examination of Large Behavior Models for Multitask Dexterous Manipulation** | Tri LBM Team et al. | 2025 | arXiv | 76 | 2507.05331 | Large behavior model analysis for dexterous manipulation |
| 27 | **OpenHelix: A Short Survey, Empirical Analysis, and Open-Source Dual-System VLA Model** | Can Cui et al. | 2025 | arXiv | 62 | 2505.03912 | Dual-system VLA survey + open-source model |
| 28 | **VLA-Adapter: An Effective Paradigm for Tiny-Scale VLA Model** | Yihao Wang et al. | 2025 | AAAI | 57 | 2509.09372 | Parameter-efficient VLA via adapters |
| 29 | **X-VLA: Soft-Prompted Transformer as Scalable Cross-Embodiment VLA Model** | Jinliang Zheng et al. | 2025 | arXiv | 54 | 2510.10274 | Cross-embodiment VLA with soft prompts |
| 30 | **Dita: Scaling Diffusion Transformer for Generalist VLA Policy** | Zhi Hou et al. | 2025 | arXiv | 54 | 2503.19757 | Diffusion transformer for generalist VLA; in-context conditioning |
| 31 | **MoLe-VLA: Dynamic Layer-skipping VLA via Mixture-of-Layers** | Rongyu Zhang et al. | 2025 | AAAI | 50 | 2503.20384 | Efficient VLA inference via layer skipping |
| 32 | **VLAS: VLA Model With Speech Instructions** | Wei Zhao et al. | 2025 | ICLR | 50 | 2502.13508 | Speech-conditioned VLA for customized manipulation |
| 33 | **SAM2Act: Integrating Visual Foundation Model with Memory Architecture** | Haoquan Fang et al. | 2025 | ICML | 47 | 2501.18564 | SAM2-based visual FM for manipulation with memory; 86.8% on RLBench |
| 34 | **Interleave-VLA: Enhancing Robot Manipulation with Interleaved Image-Text Instructions** | Cunxin Fan et al. | 2025 | arXiv | 44 | 2505.02152 | Interleaved multimodal instruction following |
| 35 | **Scaling Diffusion Policy in Transformer to 1B Parameters** (ScaleDP) | Minjie Zhu et al. | 2024 | ICRA 2025 | 44 | 2409.14411 | Demonstrated scaling laws for diffusion policy |
| 36 | **VidBot: Learning Generalizable 3D Actions from In-the-Wild 2D Human Videos** | Hanzhi Chen et al. | 2025 | CVPR | 41 | 2503.07135 | Zero-shot robotic manipulation from human videos |
| 37 | **VTLA: Vision-Tactile-Language-Action Model with Preference Learning** | Chaofan Zhang et al. | 2025 | arXiv | 40 | 2505.09577 | Added tactile modality to VLA for insertion tasks |
| 38 | **TLA: Tactile-Language-Action Model for Contact-Rich Manipulation** | Peng Hao et al. | 2025 | CoRL | 40 | 2503.08548 | Tactile-language-action for contact-rich tasks |

### 2.3 Language-Conditioned Manipulation Policies

| # | Title | First Author | Year | Venue | Citations | arXiv / DOI | Relevance |
|---|-------|-------------|------|-------|-----------|-------------|-----------|
| 39 | **Grounding Language with Visual Affordances over Unstructured Data** (HULC2) | Oier Mees et al. | 2022 | ICRA 2023 | 153 | 2210.01911 | Language-conditioned skills from unstructured data; 25+ tasks single policy |
| 40 | **Pave the Way to Grasp Anything: Transferring Foundation Models for Universal Pick-Place Robots** | Jiange Yang et al. | 2023 | arXiv | 30 | 2306.05716 | Foundation model transfer for universal pick-and-place |
| 41 | **SAM-E: Leveraging Visual Foundation Model with Sequence Imitation for Embodied Manipulation** | Junjie Zhang et al. | 2024 | ICML | 29 | 2405.19586 | SAM-based visual FM for manipulation |
| 42 | **Modularity through Attention: Efficient Training and Transfer of Language-Conditioned Policies** | Yifan Zhou et al. | 2022 | CoRL | 28 | 2212.04573 | Modular attention for language-conditioned policy transfer |
| 43 | **Language-Conditioned Robotic Manipulation with Fast and Slow Thinking** (RFST) | Minjie Zhu et al. | 2024 | ICRA | 26 | 2401.04181 | Dual-process cognitive architecture for language-conditioned manipulation |
| 44 | **FP3: A 3D Foundation Policy for Robotic Manipulation** | Rujia Yang et al. | 2025 | arXiv | 28 | 2503.08950 | 3D foundation policy for manipulation |
| 45 | **RoboGround: Robotic Manipulation with Grounded Vision-Language Priors** | Haifeng Huang et al. | 2025 | CVPR | 25 | 2504.21530 | Grounding masks as intermediate representation for manipulation |
| 46 | **Transferring Foundation Models for Generalizable Robotic Manipulation** | Jiange Yang et al. | 2023 | WACV 2025 | 23 | 2306.05716 | FM transfer strategies for robotic manipulation |
| 47 | **Learning Language-Conditioned Deformable Object Manipulation with Graph Dynamics** | Kaichun Mo et al. | 2023 | ICRA 2024 | 21 | 2303.01310 | Language-conditioned deformable object manipulation |
| 48 | **ManiFlow: A General Robot Manipulation Policy via Consistency Flow Training** | Ge Yan et al. | 2025 | arXiv | 19 | 2509.01819 | Flow matching with consistency training for 1-2 step inference |
| 49 | **Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation** | Hongkuan Zhou et al. | 2023 | arXiv | 18 | 2312.10807 | Survey: language-conditioned manipulation landscape |
| 50 | **ManiFoundation Model for General-Purpose Robotic Manipulation of Contact Synthesis** | Zhixuan Xu et al. | 2024 | IROS | 17 | 2405.06964 | General-purpose contact synthesis FM |
| 51 | **ERRA: Embodied Representation and Reasoning Architecture for Long-Horizon Language-Conditioned Tasks** | Chao Zhao et al. | 2023 | RA-L | 17 | 2304.02251 | Embodied reasoning for long-horizon manipulation |
| 52 | **LEMMA: Learning Language-Conditioned Multi-Robot Manipulation** | Ran Gong et al. | 2023 | RA-L | 15 | 2308.00937 | Multi-robot language-conditioned manipulation |
| 53 | **Efficient Alignment of Unconditioned Action Prior for Language-Conditioned Pick and Place in Clutter** (A^2) | Kechun Xu et al. | 2025 | T-ASE | 2 | 2503.09423 | Directly relevant: efficient language-conditioned pick-and-place |
| 54 | **Closed-Loop Open-Vocabulary Mobile Manipulation with GPT-4V** | Peiyuan Zhi et al. | 2024 | ICRA 2025 | 60 | 2404.10220 | GPT-4V for open-vocabulary mobile manipulation |

### 2.4 Generalist Robot Policies and Diffusion Models

| # | Title | First Author | Year | Venue | Citations | arXiv / DOI | Relevance |
|---|-------|-------------|------|-------|-----------|-------------|-----------|
| 55 | **Dreamitate: Real-World Visuomotor Policy Learning via Video Generation** | Junbang Liang et al. | 2024 | CoRL | 77 | 2406.16862 | Video diffusion for visuomotor policy; cross-embodiment |
| 56 | **BAKU: An Efficient Transformer for Multi-Task Policy Learning** | Siddhant Haldar et al. | 2024 | NeurIPS | 87 | 2406.07539 | Efficient multi-task transformer; 91% real-world success |
| 57 | **Robot Learning in the Era of Foundation Models: A Survey** | Xuan Xiao et al. | 2023 | arXiv (Neurocomputing 2025) | 51 | 2311.14379 | Comprehensive survey of FM for robot learning |
| 58 | **RLDG: Robotic Generalist Policy Distillation via Reinforcement Learning** | Charles Xu et al. | 2024 | arXiv | 38 | 2412.09858 | RL-generated data for FM fine-tuning; up to 40% gain over human demos |
| 59 | **Diffusion Transformer Policy** | Zhi Hou et al. | 2024 | arXiv | 28 | 2410.15959 | Precursor to Dita; diffusion transformer for continuous actions |
| 60 | **NVSPolicy: Adaptive Novel-View Synthesis for Generalizable Language-Conditioned Policy** | Le Shi et al. | 2025 | arXiv | 3 | 2505.10359 | Novel-view synthesis for policy generalization |

### 2.5 Survey Papers

| # | Title | First Author | Year | Venue | Citations | arXiv / DOI | Relevance |
|---|-------|-------------|------|-------|-----------|-------------|-----------|
| 61 | **Foundation Models in Robotics: Applications, Challenges, and the Future** | Roya Firoozi et al. | 2025 | IJRR | -- | 10.1177/02783649241281508 | Comprehensive FM in robotics survey (Stanford group) |
| 62 | **What Foundation Models Can Bring for Robot Learning in Manipulation: A Survey** | Dingzhe Li et al. | 2025 | IJRR | -- | 10.1177/02783649251390579 | FM specifically for manipulation learning |
| 63 | **Robot Learning in the Era of Foundation Models: A Survey** | Xuan Xiao et al. | 2023/2025 | Neurocomputing | 51 | 2311.14379 | Broad FM for robot learning survey |
| 64 | **Generative Artificial Intelligence in Robotic Manipulation: A Survey** | Kun Zhang et al. | 2025 | arXiv | 17 | 2503.03464 | GAI (GANs, VAEs, diffusion, flow, AR) for manipulation |
| 65 | **Diffusion Models for Robotic Manipulation: A Survey** | -- | 2025 | Frontiers in Robotics and AI | -- | 10.3389/frobt.2025.1606247 | Focused survey on diffusion models for manipulation |
| 66 | **Survey of Vision-Language-Action Models for Embodied Manipulation** | Haoran Li et al. | 2025 | arXiv | 7 | 2508.15201 | VLA models survey: architecture, training, evaluation |
| 67 | **Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation** | Hongkuan Zhou et al. | 2023 | arXiv | 18 | 2312.10807 | Language-conditioned manipulation survey |
| 68 | **Survey of Learning-Based Approaches for Robotic In-Hand Manipulation** | -- | 2024 | Frontiers in Robotics and AI | -- | 10.3389/frobt.2024.1455431 | In-hand manipulation learning survey |
| 69 | **A Survey of Embodied Learning for Object-Centric Robotic Manipulation** | -- | 2025 | Machine Intelligence Research | -- | 10.1007/s11633-025-1542-8 | Object-centric embodied learning survey |

### 2.6 Additional Notable Papers (from WebSearch / cross-references)

| # | Title | First Author | Year | Venue | Citations | Identifier | Relevance |
|---|-------|-------------|------|-------|-----------|------------|-----------|
| 70 | **SmolVLA: A Vision-Language-Action Model** | HuggingFace | 2025 | arXiv | -- | 2506.01844 | 450M compact open-source VLA |
| 71 | **CoA-VLA: Improving VLA via Visual-Text Chain-of-Affordance** | Li et al. | 2025 | ICCV | -- | ICCV 2025 | Chain-of-affordance reasoning in VLA |
| 72 | **NaVILA: Legged Robot VLA Model for Navigation** | An-Chieh Cheng et al. | 2024 | arXiv | 160 | 2412.04453 | VLA for legged robot navigation |
| 73 | **ABot-M0: VLA Foundation Model with Action Manifold Learning** | Yandan Yang et al. | 2026 | arXiv | 6 | 2602.11236 | Action manifold learning in VLA |
| 74 | **A Pragmatic VLA Foundation Model** | Wei Wu et al. | 2026 | arXiv | 10 | 2601.18692 | Pragmatic design for VLA |
| 75 | **LaDi-WM: A Latent Diffusion-based World Model for Predictive Manipulation** | Yuhang Huang et al. | 2025 | arXiv | 13 | 2505.11528 | World model for predictive manipulation |
| 76 | **RynnVLA-001: Using Human Demonstrations to Improve Robot Manipulation** | Yuming Jiang et al. | 2025 | arXiv | 13 | 2509.15212 | Human demo improvement for VLA |
| 77 | **DreamArrangement: Learning Language-Conditioned Robotic Rearrangement via Denoising Diffusion** | Wenkai Chen et al. | 2025 | IEEE T-SMC | 3 | T-SMC 2025 | Language-conditioned rearrangement (placement-relevant) |
| 78 | **Scalable Real2Sim: Physics-Aware Asset Generation Via Robotic Pick-and-Place Setups** | Nicholas Pfaff et al. | 2025 | IROS | 33 | 2503.00370 | Pick-and-place for sim asset generation |
| 79 | **From Grounding to Manipulation: Case Studies of FM Integration in Embodied Robotic Systems** | Xiuchao Sui et al. | 2025 | EMNLP | 4 | 2505.15685 | Comparing VLA vs VLM vs LLM paradigms for manipulation |

---

## 3. Summary Statistics

- **Total unique papers collected**: ~79
- **Landmark papers (>500 citations)**: 8 (Diffusion Policy, SayCan, RT-2, RT-1, OpenVLA, pi0, Octo, CLIPort)
- **VLA-specific papers**: ~25
- **Language-conditioned manipulation**: ~16
- **Survey papers**: ~9
- **Year distribution**: 2020 (1), 2021 (3), 2022 (4), 2023 (12), 2024 (15), 2025 (35+), 2026 (5+)
- **Top venues represented**: RSS, CoRL, ICRA, IROS, NeurIPS, ICML, ICLR, CVPR, AAAI, RA-L, T-ASE, IJRR, Science Robotics, EMNLP

## 4. Key Observations

1. **VLA explosion in 2024-2025**: After RT-2 (2023) and OpenVLA (2024), the field saw a rapid proliferation of VLA variants (pi0, ChatVLA, DreamVLA, X-VLA, MoLe-VLA, etc.), with 30+ VLA papers in 2025 alone.

2. **Diffusion-based policies dominate**: Diffusion Policy (Chi et al., 2023) has become the de facto backbone, with variants scaling to 1B parameters (ScaleDP, RDT-1B) and integrating with VLAs (Dita, pi0).

3. **Language conditioning is standard**: Almost all recent manipulation policies accept language instructions; the CALVIN benchmark remains the standard evaluation.

4. **Pick-and-place specific work is sparse**: Despite being a fundamental task, relatively few papers focus specifically on stable placement. Most treat pick-and-place as a subtask within broader manipulation benchmarks.

5. **Gap identified**: Stable object placement (pose-aware, physics-informed placement) under language conditioning is under-explored compared to grasping.

6. **Survey saturation**: Multiple comprehensive surveys appeared in 2025, covering FM for manipulation (Firoozi, Li), generative AI for manipulation (Zhang), VLA models (Li), and diffusion models for manipulation.
