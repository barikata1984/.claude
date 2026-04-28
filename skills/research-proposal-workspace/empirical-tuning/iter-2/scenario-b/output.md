# Research Proposal Review

**Draft:** Improving Few-Shot Classification with Contrastive Representation Learning
**Reviewed under:** Draft Review Mode (SKILL.md Section 2) + review-rubric.md

---

## Session Setup (Section 0)

- **Mode:** Draft Review
- **Output language:** English
- **Subfield:** General ML/DL — no physical robots, sim-to-real, or embodied agents mentioned. Robot Learning Module (Section 5) is NOT activated.

---

## Section-by-Section Feedback

---

### Background (maps to: Research Motivation + Current State & Gaps)

**Clarity:** Low. "Few-shot learning is an important problem" is the entire motivation statement. A new lab member from an adjacent field would not learn what few-shot classification is, who is harmed by current limitations, or why this matters right now.

**Specificity:** Very low. "Existing methods have limitations" — which methods? ProtoNets (Snell et al., 2017)? MAML (Finn et al., 2017)? MatchingNets? Under what conditions do they fail, and by how much? "Existing methods struggle with X" without naming them scores near zero on the rubric.

**Logic:** The gap between "limitations exist" and "therefore use contrastive learning" is not established. The reader cannot evaluate whether contrastive learning is a principled response to the identified gap, or an arbitrary choice.

**Completeness:** A PI would immediately ask:
- Which specific methods are you positioning against?
- What is the concrete failure mode — poor cross-domain generalization? Low accuracy on fine-grained tasks? Sensitivity to episode construction?
- Why is contrastive learning the right solution to that specific failure mode?
- Why is this problem tractable now (new data, new compute, new theoretical tools)?

**Priority issues in this section:**
1. Name at least 3 prior works with paper names and failure cases described quantitatively or with concrete failure conditions.
2. State a specific gap — not "limitations exist" but "Method X achieves Y% on benchmark Z under standard conditions but degrades to W% under condition C."
3. Justify the timing: what has changed recently that makes this approach now viable?

---

### Proposed Method

**Clarity:** Low. "A new contrastive learning framework" is a category, not an idea. A reader cannot form a mental model of what is novel or how it works.

**Specificity:** Very low. No architectural choices, no loss function (SimCLR-style? SupCon? custom?), no description of how meta-learning episodes are structured or what role they play in the contrastive objective.

**Logic:** The connection between the gap identified in Background and this solution is not explicit. Why does contrastive learning address the stated limitation? The rubric flags this directly: "Why will this approach succeed where Method X failed? The connection between the gap identified in Section 2 and the proposed solution isn't explicit yet."

**Completeness:** Missing:
- Intuitive explanation of the core idea (should precede technical detail)
- Reason why this approach should work — theory, analogy, or preliminary evidence
- What is reused from prior contrastive learning work vs. what is new
- Contribution type: is this a new method? A new training objective? An efficiency improvement? A new combination? The rubric requires this to be stated explicitly.

**Priority issues in this section:**
1. Add one paragraph before the technical description that explains the core idea intuitively — "the key insight is that..."
2. State what is new: "unlike SimCLR which operates on image augmentations, our framework constructs episode-aware positive pairs by..." This makes the novelty claim precise.
3. Explain why this approach addresses the specific gap from Background. The connection must be explicit.

---

### Evaluation

**Clarity:** Moderate. "Evaluate on several benchmarks and compare with existing methods" is syntactically clear but informationally empty.

**Specificity:** Very low. No benchmark is named (miniImageNet? tieredImageNet? CUB? Meta-Dataset?). No baseline is named. No metric is specified (5-way 1-shot accuracy? 5-way 5-shot?). No numerical target given. This is the rubric's red-flag case: "We will evaluate on standard benchmarks."

**Logic:** Cannot assess whether the evaluation would actually validate the method's claims, because the claims are not precise enough and the benchmarks are unnamed.

**Completeness:** The rubric treats the Evaluation section as "often the weakest section in student drafts" and requires thorough treatment. Everything is missing:
- Benchmark names (specific datasets and episode configurations)
- At least 3 baselines, including the strongest current method in the area
- Primary metric with a target value
- Ablation plan: which components will be removed to isolate the contribution of the contrastive objective vs. the meta-learning episode structure vs. the backbone?
- What happens if the main benchmark is saturated (e.g., miniImageNet 5-way 5-shot is near ceiling for many methods)?

**Priority issues in this section:**
1. Name the benchmarks specifically. Standard choices in few-shot classification include miniImageNet, tieredImageNet, CUB-200, CIFAR-FS, and Meta-Dataset — choose and justify.
2. Name the baselines, including the strongest competing method (e.g., current SOTA on the chosen benchmark).
3. Add an ablation plan. Example: "We will ablate (a) the contrastive loss alone without meta-learning episodes, (b) meta-learning episodes without contrastive loss, and (c) the full model — to isolate which component drives the improvement."

---

### Timeline

**Clarity:** Moderate. Three phases can be inferred (implement, experiment, write), though not stated as phases.

**Specificity:** Low. "4 months to implement, run experiments, and write the paper" — no phase boundaries, no intermediate deliverables, no exit criteria per phase.

**Logic:** Compressed timeline without contingency is a structural risk. The rubric flags: "All experiments compressed into the final phase" and "implementation time underestimated."

**Completeness:** Missing:
- Phase breakdown with approximate durations
- Exit criterion for each phase (what result at end of Phase N confirms it's worth proceeding to N+1?)
- Intermediate checkpoints (e.g., "by end of Month 2, we expect baseline reproduction + initial contrastive training to show positive signal on validation split")
- Contingency buffer
- No mention of when the writing phase begins relative to experiments

**Priority issues in this section:**
1. Break the 4 months into phases with concrete exit criteria. Example: Phase 1 (Month 1): Reproduce a strong baseline. Exit criterion: match reported numbers ±1%. Phase 2 (Month 2–3): Implement and run ablations. Exit criterion: at least one ablation variant outperforms baseline on validation. Phase 3 (Month 4): Full evaluation and writing.
2. Build in at least 2 weeks of contingency — student proposals almost always underestimate debugging and infrastructure time.

---

### Missing Sections (not present in the draft)

The following sections from the SKILL.md template are entirely absent. A PI would notice immediately:

- **Contribution Type** — What kind of contribution is claimed? New method, new training objective, benchmark, efficiency improvement? This must be stated explicitly.
- **Risks & Alternatives** — No risks are listed. The rubric is unambiguous: "A proposal without risks looks naive." At minimum, identify 2–3 technical risks (benchmark saturation, contrastive collapse, compute cost) and a fallback for each.
- **Tiered success criteria** — Minimum publishable outcome / Standard expected outcome / Stretch goal. Without this, the proposal is all-or-nothing.
- **Negative result scenario** — If the contrastive framework does not outperform the strongest baseline, is there still a publishable story?

---

## Structured Summary

**Strengths** (what is already working):

1. The title is specific enough to identify the subproblem (few-shot classification) and the technique (contrastive representation learning) — a good starting point for a more detailed proposal.
2. The combination of meta-learning episodes with contrastive learning is a reasonable research direction; it is neither trivially obvious nor implausible, which means there is a real proposal to develop here.

**Priority Issues** (in order — fix these first):

1. **No named prior works and no concrete gap** — The entire motivation rests on "existing methods have limitations." This is the single most urgent fix. Without it, the advisor cannot evaluate whether this is a real gap or a gap in the student's literature reading. Action: cite 3+ specific papers, describe their failure conditions with numbers, state the precise gap.

2. **No named benchmarks and no ablation plan** — The evaluation section is currently unfalsifiable. "Several benchmarks" and "existing methods" give the advisor nothing to push back on constructively. Action: name the benchmarks, name the strongest baseline, write out the ablation design.

3. **Missing Risks, Contribution Type, and Tiered Success Criteria sections** — These three sections are entirely absent and together represent the difference between a draft and a proposal. Action: add a one-paragraph Risks section with 2–3 specific technical risks and mitigations; state the contribution type in one sentence; add three-tier success criteria.

**Recommendation for next draft:**

Before touching the method description, invest one revision pass entirely on Background and Evaluation. Read 5–8 papers in the few-shot + contrastive learning intersection, identify the strongest existing result on your target benchmark, and write one sentence that explains precisely what that method cannot do and why. Everything else in the proposal — the method choice, the evaluation design, the contribution claim — will become much easier to write once that gap sentence is clear and specific.
