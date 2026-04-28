# Draft Review: "Improving Few-Shot Classification with Contrastive Representation Learning"

> Reviewed under: **Draft Review Mode** (SKILL.md Section 2)
> Rubric applied: `references/review-rubric.md`

---

## Section-by-Section Feedback

### 1. Research Motivation / Background

**Clarity:** Low. The single sentence "Few-shot learning is an important problem" gives a reader no sense of *why* it is important or to whom.

**Specificity:** None. No stakeholder is named, no concrete scenario is described, and no number anchors the claim. Compare: "existing methods have limitations" — which methods? What limitations? The rubric explicitly flags "This is an important and open problem" as a red flag because everyone says it without arguing anything.

**Logic:** The background paragraph does not build a case. It asserts importance, asserts limitations, and jumps to a solution — skipping the reasoning that connects them.

**Completeness:** Missing entirely:
- A plain-language summary (required by Part 1.1 of the output template)
- Identification of a specific stakeholder (which researchers? which practitioners? which applications?)
- A timing argument: why is this tractable now, with contrastive learning?
- Any concrete impact statement (what changes, by how much, for whom?)

**Priority action:** Rewrite Background as two short paragraphs: (1) What is few-shot classification and why does it matter in a concrete application? (2) Where do current best methods fail, with at least one specific example and a number.

---

### 2. Current State & Gaps

**Clarity:** Unclear. "Existing methods have limitations" is the entirety of the gap analysis. A new lab member cannot learn anything from this.

**Specificity:** Zero. The rubric scores "Existing methods are insufficient" at 0. No paper is named, no year is cited, no metric is given. This is the single most glaring specificity failure in the draft.

**Logic:** There is no logic to evaluate — the section is one sentence with no structure.

**Completeness:** The rubric requires:
- 3+ specific prior works cited with names and years (e.g., Prototypical Networks (Snell et al., 2017), MAML (Finn et al., 2017), SimCLR (Chen et al., 2020))
- Limitations of each cited work, ideally with numbers or specific failure conditions
- A clear, named gap: what specifically cannot the best current methods do?

The phrase "existing methods" without names is a critical gap. If the advisor reads this, their first question will be "which methods?" — and this draft has no answer.

**Priority action:** Replace "Existing methods have limitations" with at least three named prior works, each accompanied by one concrete limitation (a number, a failure case, or a distribution shift it cannot handle).

---

### 3. Contribution Type

**Clarity:** Not stated. The reader must infer that this is a new method paper, but it is never declared.

**Specificity:** None. "A new contrastive learning framework" does not position this against anything. The rubric requires a precise novelty claim: "we are the first to..." or "unlike X which does Y, we do Z."

**Logic:** Without a stated contribution type, the reader cannot judge whether the proposed approach actually delivers on a contribution.

**Completeness:** Missing:
- Explicit statement of contribution type (new method? new problem formulation? efficiency gain? benchmark contribution?)
- What is new vs. reused from prior work (e.g., which contrastive loss? which meta-learning protocol?)

**Priority action:** Add one sentence of the form: "Our primary contribution is [X]. Unlike [Method A], which [does Y], our approach [does Z] because [reason]."

---

### 4. Proposed Method

**Clarity:** Low. Three sentences describe the method at a high level, but there is no intuitive explanation before the technical description. The rubric flags this: "Method described only in technical detail without an intuitive explanation."

**Specificity:** Insufficient. Key unresolved questions:
- What contrastive objective is used? (NT-Xent? SupCon? InfoNCE? Something new?)
- What does "meta-learning episodes" mean here? (N-way K-shot? Standard Prototypical setup?)
- What is the architecture — image encoder, projection head?
- Why does contrastive pretraining specifically improve few-shot generalization? The *why* is entirely missing.

**Logic:** There is no causal chain from the identified gap (unspecified) to the proposed solution. The rubric's key question — "Why will this approach succeed where Method X failed?" — is completely unanswered.

**Completeness:** Missing:
- Intuitive one-paragraph explanation before any technical detail
- Justification for why contrastive learning addresses the limitations named in Section 2 (which were themselves not named)
- A clear statement of what is new versus borrowed from prior work

**Priority action:** Add one paragraph that explains the core idea non-technically: "The intuition is that [X]. This addresses the limitation of [Method Y] because [Z]." Then specify which contrastive objective and meta-learning protocol you are using.

---

### 5. Evaluation Plan

**Clarity:** Vague. "Several benchmarks" and "existing methods" give the reader nothing to evaluate.

**Specificity:** Zero. The rubric explicitly flags "We will evaluate on standard benchmarks" as a red flag and asks "which ones?" Specific benchmark names are required (e.g., miniImageNet, tieredImageNet, CUB-200, CIFAR-FS, Meta-Dataset). Specific baselines must be named (e.g., Prototypical Networks, MAML, FEAT, Meta-Baseline, the strongest concurrent method).

**Logic:** Without named benchmarks, it is impossible to judge whether the evaluation is appropriate for the stated problem. "Compare with existing methods" does not constitute a plan.

**Completeness:** Missing:
- Named benchmarks (at minimum 2, ideally 3–4)
- Named baselines including the strongest competing method
- Primary metric (1-shot accuracy? 5-shot accuracy? Both?)
- Numerical target ("we aim to exceed X% on miniImageNet 5-way 5-shot")
- **Ablation plan** — completely absent. For a method paper, this is a significant omission. The rubric states this explicitly. Without an ablation, there is no way to show which component of the framework drives the improvement. Minimum: one ablation removing the contrastive objective, one replacing meta-learning episodes with standard training.
- What happens if the primary benchmark is already saturated?

**Priority action (highest urgency for this section):** Name at least three benchmarks, name at least three baselines (including the strongest current state-of-the-art), specify the primary metric, and add an ablation plan with at least two ablation conditions.

---

### 6. Timeline & Milestones

**Clarity:** Low. "4 months to implement, run experiments, and write the paper" is a single undifferentiated block with no phases.

**Specificity:** None. There are no phases, no intermediate checkpoints, no exit criteria per phase.

**Logic:** A single-phase 4-month plan provides no signal to the advisor about whether the project is on track at any point before the final deadline.

**Completeness:** Missing:
- Phase breakdown (e.g., Month 1: data pipeline + baseline reimplementation; Month 2: method implementation; Month 3: experiments + ablations; Month 4: writing)
- Exit criterion per phase: "At the end of Month 2, we should be able to reproduce [Baseline X] within 1% of reported accuracy"
- Intermediate checkpoints the advisor can use to evaluate progress
- Contingency time (infrastructure and data prep routinely take 2–3× longer than estimated)

**Priority action:** Break the 4 months into at least 3 phases with one measurable exit criterion each. Move experiments into Month 3, not Month 4.

---

### 7. Risks & Alternatives

**Status:** This section does not exist in the draft.

The rubric states: "The risks section is missing. A proposal without risks looks like it hasn't been stress-tested." A proposal that identifies risks *and* addresses them looks mature; one without any risks looks naive to a PI.

**What is missing:**
- At least 2–3 specific technical risks (not "the project might fail")
- A concrete mitigation or fallback for each risk
- A negative result scenario: if the main hypothesis fails, is there still a contribution?
- Tiered success criteria: minimum / standard / stretch

**ML-specific risks the draft should address (per rubric):**
- Benchmark saturation: does few-shot classification on miniImageNet still have headroom for meaningful improvement?
- Silent training failures: how will you detect bugs that don't crash but quietly degrade quality?
- Compute cost: contrastive pretraining on large datasets (e.g., ImageNet) can be expensive — what is the fallback if GPU budget is insufficient?
- Data pipeline: how will the episode sampling be validated before committing to full runs?

**Priority action:** Add a Risks section with at least 2 risks, each with a named mitigation, plus a one-sentence tiered success description (minimum publishable result / standard goal / stretch).

---

## Structured Summary

**Strengths (2–3 things working):**

1. **Topic relevance and direction.** Few-shot learning combined with contrastive representation learning is a meaningful research direction with active literature. The high-level framing points toward a real problem area.
2. **Compact scope.** The 4-month framing suggests the student is aiming for a contained, single-paper contribution rather than an overambitious multi-year project — this is appropriate for a lab-internal proposal stage.

**Priority Issues (2–3 most important to fix, in order):**

1. **[Highest priority] Name every unnamed entity.** "Existing methods," "several benchmarks," and "existing methods" as baselines are placeholders, not content. Before anything else: name at least 3 prior works in the gap analysis with specific limitations, name 3+ benchmarks in the evaluation plan, name the primary metric and at least 3 baselines. The rubric scores these at 0 specificity and a PI will stop reading here.

2. **[High priority] Add an ablation plan.** For a method paper, the absence of an ablation design is a significant omission. Add at minimum: (a) training without the contrastive objective, (b) training without meta-learning episodes. These two ablations directly test the two claims in the proposal.

3. **[Medium priority] Add a Risks section with tiered success criteria.** The section does not exist. A proposal without risks looks like it hasn't been stress-tested. Add 2 specific risks with mitigations, and state the minimum publishable result if the main hypothesis partially fails.

**Recommendation for next draft:**

Start by filling in the blanks: open the draft, find every use of "existing methods," "several benchmarks," and "limitations," and replace each with a proper name and a number. That one pass will double the credibility of the proposal without requiring new ideas. Then add a five-bullet ablation plan and a two-paragraph Risks section. These three changes address the gaps a PI will notice in the first read.

---

*Review generated under Draft Review Mode (SKILL.md §2) using the section-by-section rubric in `references/review-rubric.md`.*
