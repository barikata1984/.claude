---
name: research-proposal
description: >
  Create or review research proposals in ML, deep learning, AI, robot learning, and embodied AI —
  designed for lab-internal sharing with PIs, mentors, and research groups (not grant applications).
  Use this skill whenever the user mentions writing a 研究計画書, research proposal, or research plan;
  structuring a research idea; preparing for an advisor or supervisor meeting; organizing thoughts before
  a lab meeting; or wanting feedback on a draft research concept. Don't skip this skill just because the
  user hasn't said "research proposal" explicitly — if they're trying to articulate a research idea to
  share with someone in their lab or group, this skill applies. Handles Japanese and English output.
  Specialized for ML, DL, AI, reinforcement learning, robot learning, manipulation, locomotion, and
  embodied AI. TRIGGER even for vague early-stage ideas like "I have a rough idea I want to discuss
  with my PI" or "先生に研究アイデアを見せたい".
---

# Research Proposal — Interactive Guide

This skill helps create or review research proposals in ML/AI/robot learning for **lab-internal sharing**
(PI, mentor, research group). The goal is not a polished grant application — it's a document that makes
the user's thinking clear enough to have a productive conversation with their supervisor.

## 0. Session Setup

Determine three things before proceeding:

1. **Mode**: Starting from scratch, or reviewing an existing draft?
2. **Output language**: Japanese, English, or mixed?
3. **Subfield**: General ML/DL/AI — or does this involve physical robots, sim-to-real, manipulation,
   locomotion, or embodied agents? If yes, activate the Robot Learning Module (Section 5).

Then open with: "まず一文でいいので、取り組もうとしている問題や研究アイデアを教えてください" (or English
equivalent). Even a rough sentence is enough to start — don't wait for a polished summary.

If the user's opening message already contains enough context to infer the research topic, skip this
opener and proceed directly to the first section's questions.

---

## 1. Interactive Design Mode

Walk through sections one at a time. For each section:

- Ask 2–3 targeted questions (full question bank in `references/sections.md`)
- After the user responds, reflect back in 2–3 sentences: "つまり〜ということですね。合ってますか？"
- Correct misunderstandings before moving on
- Once confirmed, produce a short written summary of that section in the target language
- Offer to move to the next section

Take as many turns as needed on a hard section. It's better to spend three turns getting the research
motivation right than to rush through all seven sections with shallow answers.

### Section Order

Go through these in order. Adapt depth based on how much the user already knows — a student who just
had an idea needs more scaffolding than a PI with a concrete plan.

| # | Section | Core question |
|---|---------|---------------|
| 1 | Research Motivation | Why this problem? Why now? Who cares? |
| 2 | Current State & Gaps | What exists, and where does it fall short? |
| 3 | Contribution Type | What *kind* of contribution is this? |
| 4 | Proposed Approach | What's the core idea, and why should it work? |
| 5 | Evaluation Plan | Benchmarks, baselines, metrics, ablations |
| 6 | Timeline & Milestones | Phases with intermediate checkpoints |
| 7 | Risks & Alternatives | Failure scenarios and fallback plans |

Robot learning adds sections 8–9 (see Section 5 below).

See `references/sections.md` for the full question set and guidance for each section.

---

## 2. Draft Review Mode

When the user provides an existing draft, give structured feedback organized by section.

**Per-section assessment:**
- **Clarity** — Is the point clear to a non-expert reader (e.g., a new lab member)?
- **Specificity** — Are claims concrete? (named methods, benchmark names, numbers)
- **Logic** — Does this section support the overall argument coherently?
- **Completeness** — What's missing that a PI would immediately ask about?

**Summary at the end:**
- Top 2–3 strengths (what's already working)
- Top 2–3 issues in priority order
- Specific, actionable suggestions for the weakest 1–2 sections

Avoid giving a wall of feedback on everything at once — prioritize. A student can fix 2–3 things; they
cannot fix 15 things simultaneously.

See `references/review-rubric.md` for the full section-by-section rubric.

---

## 3. Output Template

When producing the written document, use this 3-part structure. Keep it to **2–4 pages** for a
lab-internal document. Cut padding, not content.

```
# [Research Title]

## Part 1: Motivation
1.1  Plain-language summary (no jargon — readable by a non-specialist)
1.2  Problem statement
1.3  Current methods and their specific limitations
1.4  What's new in the proposed approach
1.5  Expected impact (concrete, not "advance the field")

## Part 2: Technical Content
2.1  Background and notation (only what's needed)
2.2  Related work (each citation positioned: how it relates and how this work differs)
2.3  Proposed method
2.4  Why it should work (theoretical reasoning or preliminary evidence)

## Part 3: Validation Plan
3.1  Hypotheses in falsifiable form
3.2  Experimental design (benchmarks, baselines, metrics)
3.3  Ablation design
3.4  Milestones and intermediate checkpoints
3.5  Risks and mitigation
3.6  Negative result scenarios
3.7  Tiered success criteria (minimum / standard / stretch)

## Appendix (optional)
- Preliminary results or proof-of-concept
- References
```

---

## 4. Principles to Apply Throughout

**Specificity is everything**
"Our method improves performance" → "Our method achieves ≥90% success on Push-T while reducing
planning time from 1 s to <0.1 s, matching CEM accuracy." Help the user add numbers wherever possible.

**Honest uncertainty beats false confidence**
For early-stage proposals: "We hypothesize X because Y. If X fails, we will try Z" is more credible
than pretending certainty. Encourage students to write this way.

**Falsifiable hypotheses**
Every testable claim should be writable as: "We predict [measurable outcome] under [specific conditions]
using [specific method] compared to [specific baseline]." If the prediction can't fail, it isn't a
hypothesis.

**Tiered success criteria**
Design for partial success. Three levels:
- Minimum (論文化可能): what counts as a publishable contribution even if things go wrong
- Standard (目標): the expected outcome
- Stretch (ベストケース): if everything works

This protects against all-or-nothing proposals and gives the PI a realistic picture.

**Risk = credibility**
A proposal without risks looks naive. A proposal that identifies risks *and* addresses them looks
mature. Help students write risks honestly — PIs respect this.

**Part 1 must be jargon-free**
The Heilmeier test: can a non-specialist understand the motivation after reading Part 1.1? If the user
can't explain the problem without jargon, they may not fully understand it yet. Use this as a
diagnostic, not a criticism.

---

## 5. Robot Learning Module

Activate when the research involves physical robots, sim-to-real transfer, manipulation, locomotion,
embodied agents, or any system that interacts with the physical world.

Add these two sections after Section 7 (Risks):

**Section 8: Sim-to-Real Strategy** (if simulation is involved)
Questions to ask:
- Where does training happen — simulation, real world, or both?
- What simulation environment? (Isaac Gym, MuJoCo, Gazebo, custom?)
- What's the expected sim-to-real gap, and how will you bridge it?
  (domain randomization, real2sim2real, online adaptation, etc.)
- How will you validate that the policy transfers before investing in real-robot experiments?

**Section 9: Hardware & Safety**
Questions to ask:
- What robot platform? What are its constraints (DOF, payload, sensors, onboard compute)?
- Is the task quasi-static (lower risk) or dynamic (higher risk of hardware damage)?
- What safety measures are in place for real-robot experiments?
- What's the cost and access situation for hardware time?

When reviewing robot learning drafts, additionally check:
- Is the sim-to-real gap acknowledged and addressed?
- Are hardware constraints treated as design inputs (not afterthoughts)?
- Is there a safety protocol for real-world experiments?
- Is the computational cost of real-robot data collection addressed?
