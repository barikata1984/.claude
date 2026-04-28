# Draft Review Rubric

Use this when the user provides an existing draft (Review Mode). Evaluate each section present in the
draft. Skip sections that don't exist yet — note their absence instead.

---

## How to Score

For each section, assess four dimensions (same four as SKILL.md Section 2):

| Dimension | What to look for |
|-----------|-----------------|
| **Clarity** | Is the point understandable to a non-expert — a new lab member from an adjacent field? If jargon is unavoidable, is it explained? |
| **Specificity** | Named methods, named benchmarks, numbers. "Existing methods are insufficient" scores 0. "Method X achieves 60% on benchmark Y but fails under condition Z" scores high. |
| **Logic** | Does this section support the overall argument? Does it follow from the previous section? |
| **Completeness** | What would a PI ask that isn't answered here? |

Don't give numeric scores — give qualitative assessment and concrete suggestions.

---

## Section-by-Section Rubric

### Part 1: Motivation

**Strong indicators:**
- Problem explained in plain language without loss of meaning
- Specific stakeholder identified (not "the community" — which researchers? which engineers?)
- Concrete impact articulated (what changes, by how much, for whom)
- Timing justified (why is this tractable now?)

**Red flags:**
- "This is an important and open problem" — everyone says this; it doesn't argue anything
- No plain-language summary — Part 1.1 is supposed to be jargon-free
- Motivation is purely academic ("we want to understand X") without any connection to why X matters

**Suggested feedback framing:**
- "Part 1.1 still has jargon — try rewriting as if explaining to a lab member from a different field"
- "The impact is described abstractly — can you add a concrete example of what changes if this works?"

---

### Current State & Gaps

**Strong indicators:**
- 3+ specific prior works cited with paper names and years
- Limitations of each cited work described quantitatively or with specific failure cases
- Clear gap identified: what the existing methods cannot do that this work will address

**Red flags:**
- "Existing methods struggle with X" without naming which methods or where they struggle
- Only citing survey papers instead of primary sources
- Gap is presented as "no one has tried X" — this may be true, but why hasn't anyone? Is there a
  good reason? The proposal should address this.
- Cherry-picking only weak baselines to position against

**Suggested feedback framing:**
- "Section 2 mentions 'existing methods' without naming them — which specific papers?"
- "The limitations listed are qualitative. Can you add numbers? e.g., 'achieves X% under standard
  conditions but drops to Y% under condition Z?'"

---

### Contribution Type

**Strong indicators:**
- Contribution type explicitly stated (new method? efficiency? new problem? benchmark?)
- One primary contribution type identified, with secondary ones acknowledged if present
- Novelty claim is precise: "we are the first to..." or "unlike X which does Y, we do Z"

**Red flags:**
- Contribution type implied but never stated — the reader has to guess
- "We combine X and Y in a novel way" — combination alone is not novelty; what's the insight?
- Multiple contribution types claimed equally — usually dilutes the impact of each

---

### Proposed Approach

**Strong indicators:**
- Intuitive explanation that comes before the technical description
- Reason given for why the approach should work (theory, preliminary experiment, or analogy)
- Clear statement of what's new vs. what's reused from prior work

**Red flags:**
- Method described only in technical detail without an intuitive explanation
- "We use a Transformer" — architecture choice without justification of *why* this architecture
  addresses the specific limitations identified in Section 2
- No reason given for why the approach should work — "we will try it and see" is not a plan

**Suggested feedback framing:**
- "Part 2.3 goes straight into technical detail. Can you add one paragraph before it that explains
  the core idea intuitively?"
- "Why will this approach succeed where Method X failed? The connection between the gap identified
  in Section 2 and the proposed solution in Section 4 isn't explicit yet."

---

### Evaluation Plan

This is often the weakest section in student drafts. Be thorough here.

**Strong indicators:**
- Specific benchmark names (e.g., Push-T, D4RL, IsaacGym-Ant, MuJoCo HalfCheetah)
- At least 3 baselines named, including the strongest competing method
- Primary metric specified (success rate, return, accuracy, FLOPs, inference time...)
- Numerical target stated when relevant
- Ablation plan: what components will be removed to isolate contributions?
- Addressed what happens if the main benchmark is saturated

**Red flags:**
- "We will evaluate on standard benchmarks" — which ones?
- Only weak baselines chosen — is the strongest competing method included?
- No ablation plan — for a method paper, this is a significant omission
- No metric defined — what does "better" mean in this context?
- Evaluation plan claims more than the method can deliver (scope mismatch)

**Suggested feedback framing:**
- "The evaluation section mentions 'several benchmarks' — please name them specifically"
- "Which is the strongest existing method in this area? Is it included as a baseline?"
- "How will you demonstrate that Component A specifically contributes? What's removed in the ablation?"

---

### Timeline & Milestones

**Strong indicators:**
- Clear phases that build on each other
- Each phase has a concrete exit criterion (not "finish implementation")
- Intermediate checkpoints: what result at the end of Phase N tells you it's worth proceeding to N+1?
- Realistic time estimates (not all experiments in the last 2 weeks)

**Red flags:**
- All experiments compressed into the final phase — this is the most common mistake
- No intermediate checkpoints — the proposal assumes everything works until the end
- Implementation time underestimated (data prep, debugging, infrastructure often take 2–3× longer
  than expected)
- No contingency time

**Suggested feedback framing:**
- "The timeline puts all evaluations in Phase 4. What happens if Phase 3 takes longer than expected?"
- "What's the exit criterion for Phase 2? 'Complete the model implementation' isn't measurable."

---

### Risks & Alternatives

**Strong indicators:**
- At least 2–3 specific technical risks identified (not "the project might fail")
- Concrete mitigation or fallback for each risk
- Negative result scenario: if the main hypothesis fails, what's the publishable story?
- Tiered success criteria: minimum / standard / stretch

**Red flags:**
- No risks listed — the proposal looks naive
- Risks listed but no mitigation — worse than not listing them (shows awareness without response)
- "We'll handle it if it happens" — not a plan
- No negative result scenario — all-or-nothing proposals are fragile

**ML-specific risks to check for:**
- Benchmark saturation: does the chosen benchmark have headroom for meaningful improvement?
- Silent training failures: how will they detect bugs that don't crash but degrade quality?
- Compute cost: what if training is more expensive than estimated?
- Data pipeline issues: how will they validate the data before committing to large runs?

**Suggested feedback framing:**
- "The risks section is missing. A proposal without risks looks like it hasn't been stress-tested."
- "If the approach in Section 4 doesn't work, what happens? Is there still a contribution to report?"

---

### Robot Learning Additions (if applicable)

**Sim-to-Real:**
- Is the sim-to-real gap acknowledged?
- Is a specific strategy named (domain randomization, real2sim2real, online adaptation)?
- How will transfer be validated before committing to real-robot experiments?

**Hardware & Safety:**
- Platform specified with relevant constraints?
- Task regime identified (quasi-static vs. dynamic)?
- Safety protocol described?
- Hardware access situation addressed?

---

## Summary Feedback Template

After section-by-section assessment, give a structured summary:

```
**Strengths** (2–3 things working well):
- ...

**Priority Issues** (2–3 most important to fix, in order):
1. [Most critical issue] — [specific suggestion]
2. [Second issue] — [specific suggestion]
3. [Third issue] — [specific suggestion]

**Recommendation for next draft:**
[One paragraph: what to focus on first and why]
```

Keep the summary actionable. A student can address 2–3 concrete issues; they cannot address 15 items
of equal priority.
