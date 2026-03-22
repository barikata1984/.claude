# Phase Transitions

Rules for determining when a phase is complete and which phase comes next.
SKILL.md uses this reference to manage phase progression and loop detection.

## Phase Completion Conditions

| Phase | Completion condition | Next phase |
| ----- | -------------------- | ---------- |
| 0 | Problem defined in one sentence (human decision, outside skill scope) | 1 |
| 1 | Gap between existing work and proposed approach is clearly articulated | 2 |
| 2 | Experiment plan approved by user (approval gate) | 3 |
| 3 | All implementation tasks done, external verification (pytest/ruff/pyright) passes | 4 |
| 4 | Experiment data collected (human + compute, outside skill scope) | 5 |
| 5 | Analysis report complete with statistical summary | 6 or loop |
| 6 | Output draft (paper or product) complete | 7 |
| 7 | All critiques resolved to PASS | 8 or loop |
| 8 | Published / deployed (human decision, outside skill scope) | — |

## Approval Gates

Some transitions require explicit user approval before proceeding.

| Transition | Gate type | Rationale |
| ---------- | --------- | --------- |
| 2 → 3 | User approves experiment plan | Cost/time tradeoff is a human judgment |
| 5 → 6 | User confirms hypothesis verdict | Interpretation of results requires domain insight |
| 7 → 8 | User approves final deliverable | Publication/release is an irreversible decision |

## Loop Structures

Loops represent rework triggered by results or reviews.
SKILL.md tracks loop counts to detect runaway iterations.

### Loop A — Hypothesis Revision

| Field | Value |
| ----- | ----- |
| Trigger | Phase 5 analysis rejects the hypothesis |
| Path | 5 → 2 → 3 → 4 → 5 |
| Expected count | 1–3 |
| Escalation | If count > 3, propose revisiting Phase 0 (problem definition) |

### Loop B — Additional Experiments

| Field | Value |
| ----- | ----- |
| Trigger | Phase 5 results are inconclusive (no significance, insufficient samples) |
| Path | 5 → 4 → 5 |
| Expected count | 1–2 |
| Escalation | If count > 2, propose redesigning experiment (return to Phase 2) |

### Loop C — Critical Defect

| Field | Value |
| ----- | ----- |
| Trigger | Phase 7 review returns BLOCK verdict |
| Path | 7 → 3/4 → 5 → 6 → 7 |
| Expected count | 0–1 |
| Escalation | If count > 1, indicates a fundamental design problem |

### Loop D — Minor Revision

| Field | Value |
| ----- | ----- |
| Trigger | Phase 7 review returns REVISE verdict |
| Path | Within Phase 7 (original agent fixes, re-review) |
| Expected count | 1–3 |
| Escalation | None — self-contained within Phase 7 |

## State File Format

SKILL.md persists phase state in the project state file.

```markdown
# Project State

- Mode: [academic | startup]
- Current phase: [0-8]
- Loop counts: (A)0 (B)0 (C)0 (D)0

## Phase [N] Task Queue

| ID | Task | Agent | Mode | Dependencies | Status | Completed |
| -- | ---- | ----- | ---- | ------------ | ------ | --------- |
```

## Phases Without Definition Files

| Phase | Reason |
| ----- | ------ |
| 0 (Ideation) | No agent involvement — skill has no role |
| 4 (Experiments) | Human + compute work — delegate to `/sweep run` |
| 8 (Publication) | Human decision — delegate to `/commit-and-push` |
