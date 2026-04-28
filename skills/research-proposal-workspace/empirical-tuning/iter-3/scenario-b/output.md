# Draft Review: Improving Few-Shot Classification with Contrastive Representation Learning

> Review generated using the `research-proposal` skill — Draft Review Mode (SKILL.md Section 2)
> Rubric: `references/review-rubric.md`

---

## Section-by-Section Feedback

### Background (maps to: Motivation + Current State & Gaps)

**Clarity** — The topic is recognizable, but the section reads as three disconnected assertions. A new lab member from an adjacent field would not understand *why* few-shot learning matters, for whom, or in what deployment context. There is no plain-language sentence that a non-specialist could follow.

**Specificity** — This is the most critical weakness in the entire draft. "Existing methods have limitations" names no methods. The rubric is explicit: "Existing methods are insufficient" scores 0. Which methods? Prototypical Networks? MAML? SimpleShot? Where specifically do they fail — low-resource languages, medical imaging, cross-domain shift? Without named methods, there is no gap to fill, and the proposed solution cannot be evaluated as a response to anything concrete.

**Logic** — The three sentences do not build an argument. The jump from "few-shot learning is important" to "our approach uses contrastive learning" skips the reasoning step entirely: *why* is contrastive learning the right response to the limitations of existing methods?

**Completeness** — Missing: (1) a stakeholder or application context, (2) a timing justification (why is this tractable now?), (3) specific prior works with named limitations, (4) a clear gap statement distinguishing what existing methods cannot do from what this work will do.

**Suggested fix:** Rewrite as two distinct paragraphs. First: explain the problem in plain language and identify a concrete application where few-shot classification currently falls short. Second: name 2–3 specific prior methods, state their measurable limitations (e.g., "MAML achieves X% on miniImageNet but requires Y inner-gradient steps and degrades to Z% under domain shift"), and state the gap this work addresses.

---

### Proposed Method

**Clarity** — The section has three sentences, all at the same level of abstraction. There is no intuitive explanation before the technical description. A reader cannot form a mental model of what is actually being proposed.

**Specificity** — "A new contrastive learning framework" is undefined. Contrastive learning is a large family: SimCLR, MoCo, SupCon, CLIP-style, episode-level contrastive objectives — which design choices are being made and why? "Meta-learning episodes" is mentioned without specifying the episode structure (N-way K-shot, number of query examples, whether episodes are class-balanced). "The model learns better representations" is a hoped-for outcome, not a method description.

**Logic** — The connection between the gap identified in the Background and the proposed solution is entirely implicit. Why does contrastive representation learning address the specific limitations of existing few-shot methods? This is the core intellectual claim of the paper and it is currently missing.

**Completeness** — Missing: (1) an intuitive explanation of the core idea, (2) what is new versus what is reused from prior contrastive or meta-learning work, (3) a theoretical or empirical reason to believe the approach will work, (4) any architectural or training detail that distinguishes this from prior combinations of contrastive + meta-learning (which already exist, e.g., FEAT, DeepEMD variants, ProtoNet with contrastive pretraining).

**Suggested fix:** Add one paragraph before technical details: "The key idea is that [plain-language description]. Unlike [Method X] which does [Y], we do [Z] because [reason]." Then specify the episode structure, the contrastive objective, and what component is novel.

---

### Evaluation

**Clarity** — The intent is clear, but no information is conveyed.

**Specificity** — "Several benchmarks" names none. Standard few-shot classification benchmarks include miniImageNet, tieredImageNet, CUB-200, CIFAR-FS, Meta-Dataset — which will be used? "Existing methods" names no baselines. The rubric flags this directly: "We will evaluate on standard benchmarks" scores the same as writing nothing.

**Logic** — Without knowing what is being claimed in the method section, it is impossible to assess whether the evaluation plan would actually test that claim.

**Completeness** — Missing: (1) named benchmarks, (2) named baselines (including the strongest competing method — not just weak ones), (3) primary metric (1-shot accuracy? 5-shot accuracy? mean and 95% confidence interval?), (4) numerical target or threshold, (5) **ablation plan** — this is a significant omission for a method paper. If the contribution is a new contrastive framework applied to meta-learning, the ablation must isolate which components drive the improvement (e.g., contrastive objective alone vs. episode design vs. both combined).

**Suggested fix:** Replace with: "We evaluate on [miniImageNet, tieredImageNet, CUB-200] under the standard 5-way 1-shot and 5-way 5-shot protocols. Baselines: [ProtoNet, MAML, DeepEMD, FEAT, and the strongest current method]. Primary metric: mean accuracy ± 95% CI over 600 test episodes. Ablation: we remove the contrastive objective (Ablation A), replace episode-level training with standard supervised pretraining (Ablation B), and combine both (Ablation C) to isolate each contribution."

---

### Timeline

**Clarity** — The single-sentence timeline is clear in what it is trying to say.

**Specificity** — 4 months with three phases described in four words each. No phase boundaries, no intermediate checkpoints, no exit criteria.

**Logic** — The ordering (implement → experiment → write) is conventional but the allocation is unspecified. In practice, writing a paper takes longer than "writing the paper" implies, and experiments rarely fit neatly into a single phase.

**Completeness** — Missing: (1) phase breakdown with durations, (2) exit criterion for each phase (what result at the end of Phase N tells you it's safe to proceed to Phase N+1?), (3) intermediate checkpoints (e.g., "by end of Month 2, achieve at least baseline-level performance to confirm the training pipeline is correct"), (4) contingency buffer, (5) any acknowledgment that debugging and infrastructure often take 2–3× longer than expected.

**Suggested fix:** Structure as three or four phases with explicit duration, an exit criterion per phase, and a 2-week contingency buffer. For example: "Phase 1 (Weeks 1–4): implement contrastive episode training pipeline. Exit criterion: reproduce ProtoNet baseline ±1% on miniImageNet. Phase 2 (Weeks 5–10): ..."

---

### Missing Sections

The following sections from the skill's standard structure are entirely absent. A PI reviewing this draft would ask about all of them immediately.

| Missing Section | Why It Matters |
|---|---|
| **Contribution Type** | The reader must guess whether this is a new method, a new training recipe, a new benchmark, or a systems contribution. The novelty claim is undefined. |
| **Why the approach should work** | No theoretical reasoning, no preliminary result, no analogy. "We will train and see" is not a plan. |
| **Risks & Alternatives** | A proposal without risks looks unstressed. At minimum: what if contrastive pretraining doesn't help over supervised pretraining? What if the approach is not competitive with SOTA? What is the publishable story if the main hypothesis fails? |
| **Tiered success criteria** | Minimum / Standard / Stretch. This protects against an all-or-nothing framing that makes the proposal fragile. |

---

## Structured Summary

**Strengths** (2 things working):
- The research topic (few-shot classification + contrastive learning) is coherent and addresses an active area with real open questions. The general direction is defensible.
- The structural skeleton is present — Background, Method, Evaluation, Timeline are all named, which gives a clear revision target for each section.

**Priority Issues** (in order of importance to fix first):

1. **Name the prior methods — this is blocking everything else.** "Existing methods have limitations" and "compare with existing methods" are placeholders, not content. Until specific papers are named with specific limitations, the proposal has no argument. This affects the Background, the Method (can't claim novelty without naming what came before), and the Evaluation (can't name baselines without knowing the comparison space). Fix this first.

2. **Add an ablation plan to the Evaluation section.** For a method paper proposing a new training framework, the absence of an ablation plan is a significant omission that a PI will ask about in the first read. The ablation design needs to appear in the draft before the advisor meeting.

3. **Add a Risks section with a fallback story.** Currently there is no section addressing what happens if contrastive learning does not improve over a supervised pretraining baseline, or if the approach is not competitive with current SOTA. A one-paragraph risks section with 2–3 specific technical risks and a "negative result still publishable because..." statement would substantially increase the proposal's credibility.

**Recommendation for next draft:**

Focus the next revision on Priority Issue 1 entirely. Sit down with a few-shot learning survey (e.g., Tian et al. 2020 "Rethinking Few-Shot Image Classification," Triantafillou et al. 2020 "Meta-Dataset") and identify 3 specific papers that represent the current state of the art in your setting, write one sentence about each describing a concrete measurable limitation, and then state in one sentence what gap your work fills. Once those named methods are in the draft, the method section's novelty claim and the evaluation section's baseline list will follow naturally. The other issues (ablation, risks) are easier to fix once the core argument is established.
