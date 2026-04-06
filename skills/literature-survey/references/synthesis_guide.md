# Survey-Level Synthesis Guide

This file contains detailed instructions for Phase 5 (Survey-Level Synthesis).
SKILL.md specifies the overall aggregation logic; this file provides the
writing guidelines for each section.

## Axis Descriptions

### 1. thesis — the field's fundamental unsolved problem

Paper-level theses will reveal agreements, contradictions, and tensions.
Synthesize these into a central claim about what the field's fundamental
unsolved problem is.

Example: "The core tension is between pre-task estimation accuracy and
interaction cost — no existing approach resolves this without compromising
one or the other."

### 2. foundation — the shared technical substrate

Aggregate paper-level cores to identify what technical building blocks the
field relies on. These are the shared substrates — methods, representations,
or assumptions — without which the majority of surveyed approaches would not
function. For each stated foundation, verify that it genuinely holds across
the surveyed papers; if a paper contradicts it, narrow the claim accordingly.

### 3. progress — the trajectory of solved problems

Aggregate paper-level diffs chronologically to trace how the field has
advanced. Identify the most significant capability transitions — where a
limitation of earlier work was definitively overcome. This section shows
the trajectory of solved problems.

### 4. gap — structural unsolved problems and engineering consequences

Identify what remains unsolved by examining two sources:

(a) the frontier of paper-level diffs — limitations that the most recent
    papers still have not overcome, and
(b) paper-level limits — constraints that multiple papers independently
    acknowledge. Converging limits across papers are stronger evidence of
    structural gaps than isolated mentions.

**Writing style**: Each gap is a self-contained paragraph (not a bulleted
list). The paragraph should:

- Open with a concise statement of what is not yet achieved
- Reference the Paper Catalogue categories or prior Survey Findings sections
  (e.g., "As Category D shows, ...") to avoid re-explaining what individual
  papers do — the reader has already encountered those details
- Mention specific papers only when adding NEW information not covered
  elsewhere (e.g., a specific metric, a specific failure mode relevant to
  the gap)
- Close with the engineering consequence — what becomes possible if the gap
  is closed
- Avoid redundancy with Thesis, Foundation, and Progress sections; if a
  point was already made, reference it rather than restating it

### 5. seed (conditional)

**Include only when the user explicitly requests research proposals, next
steps, or seed ideas.** For reading lists, reference collections, or
background surveys, omit this section and end Survey Findings at Gap.

When included, read `references/seed_format.md` for the detailed structure
(academic contribution, required components, readiness assessment for each
seed).
