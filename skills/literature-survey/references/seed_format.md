# Seed Section Format

This file defines the structure for the Seed section of a literature survey.
**Only include seeds when the user explicitly requests research proposals,
next steps, or seed ideas.** Omit entirely for reading lists, reference
collections, or background surveys.

## When to include seeds

Include when the user says things like:
- "suggest research directions"
- "what are the open problems worth pursuing"
- "propose next steps based on the survey"
- Any explicit mention of wanting research ideas or seeds

Do NOT include when the user says things like:
- "just the key papers"
- "I want a reading list"
- "survey the literature on X" (without mentioning research directions)
- "what papers should I read"

When in doubt, ask the user.

## Seed structure

Each seed is a self-contained subsection with three required parts:

**(a) Academic contribution** — why this idea constitutes a research seed:
Articulate the specific academic contribution. Reference the gap(s) it addresses
and explain why the contribution would be novel relative to the surveyed literature.
The argument must be grounded in the survey evidence (thesis/foundation/progress/gap),
not speculation.

**(b) Required components** — what building blocks are needed:
Enumerate the concrete technical components (algorithms, representations, datasets,
hardware, theoretical results, etc.) required to realize the idea. Be specific
enough that a researcher could use this as a project planning checklist.

**(c) Readiness assessment** — what exists vs. what must be developed:
For each component listed in (b), classify it as:
- **Available**: already demonstrated in surveyed papers (cite the specific paper(s))
- **Adaptable**: exists in a related context but requires non-trivial modification
  (state what modification is needed)
- **New development required**: does not exist and must be created (state the
  core technical challenge)

This three-part structure ensures each seed is not merely a wish-list item but
a grounded, actionable research direction with a clear feasibility profile.

## Seed Overview (before individual seeds)

Before the individual seed subsections, write a **Seed Overview** that:
- Presents a table summarizing each seed's **premise** (what it assumes about the
  current state of the field) and **approach** (what strategy it takes)
- Explains the relationships between seeds: which are independent, which are
  complementary, which are mutually exclusive
- Proposes a **staged progression** — a concrete sequence in which the seeds could
  be pursued, with rationale for the ordering (e.g., which seed provides foundations
  for others, which can start immediately, which requires results from a prior seed)

## Template

```markdown
### Seed

#### Seed Overview

| Seed | Premise | Approach |
|------|---------|----------|
| 1 | [What this seed assumes about the current state] | [What strategy it takes] |
| 2 | ... | ... |

[Narrative: relationships between seeds, staged progression with rationale.]

#### Seed 1: [Descriptive title]

##### Seed 1 — Academic Contribution

[Why this idea is a viable research seed. Reference gap(s) and argue novelty.]

##### Seed 1 — Required Components

1. [Component 1]
2. [Component 2]
3. ...

##### Seed 1 — Readiness Assessment

| Component | Status | Detail |
|-----------|--------|--------|
| [Component 1] | Available | [Paper(s) where demonstrated] |
| [Component 2] | Adaptable | [What exists and what modification is needed] |
| [Component 3] | New development required | [Core technical challenge] |

#### Seed 2: [Descriptive title]
...
```
