# Survey-Level Synthesis Guide

This file contains detailed instructions for Phase 4 (Synthesize).
SKILL.md specifies the overall aggregation logic; this file provides the
writing guidelines for each axis.

## Synthesis Inputs

The synthesis draws on **two distinct sources**:

1. **Hub-paper deep reads** (5–10 papers): the rich material from
   `/paper-summary` notes — full Executive Summary, the 6 standardized
   questions (problem, approach-and-core-elements, novelty vs prior work,
   training/optimization, validation, discussion), and the BibTeX.
   These are the **primary evidence** for thesis / foundation / progress / gap.
2. **Concept matrix** (all mapped papers): broad coverage of the field —
   1-line contribution per paper plus 3-5 concept tags. This provides the
   **statistical view**: which concepts are dense, which are sparse, where
   the empty cells are.

Cite hub papers via Obsidian wikilink (`[[papers/{citekey}/{slug}|Author+ Year]]`)
when referencing their deep reads in synthesis prose.

## Axes

### 1. thesis — the field's fundamental unsolved problem

Read across the hub deep reads' "問い・課題" (problem) and "議論" (discussion)
sections. Identify recurring tensions, contradictions, or shared assumptions.
Synthesize into a single central claim about what the field's fundamental
unsolved problem is. Validate against the concept matrix: if the claimed
tension does not show up as a sparse / contested column, narrow the claim.

Example: "The core tension is between pre-task estimation accuracy and
interaction cost — no surveyed approach resolves this without compromising
one or the other (see hub papers [[Author1+]], [[Author2+]], [[Author3+]])."

### 2. foundation — the shared technical substrate

Aggregate from two sources in hub deep reads:

(a) The **「アプローチと根幹をなす要素」セクション** — extract the strategy
    and the irreplaceable building blocks (methods, representations,
    architectural patterns, assumptions).
(b) The **「訓練・最適化」セクション** — extract shared loss functions,
    objectives, and datasets. In ML/robotics surveys, "all hubs use
    diffusion loss on teleoperation demos" is a substantive foundation
    observation, not a trivia item.

Identify elements that recur across multiple hubs. For each stated
foundation, verify it genuinely holds across the surveyed papers via the
concept matrix; if a paper contradicts it, narrow the claim.

### 3. progress — the trajectory of solved problems

Order hub papers chronologically. From each hub's "新規性 vs 既存研究"
(novelty vs prior work) section, extract what limitation was overcome.
Trace the trajectory of solved problems. The concept matrix supplements
this by showing when concepts entered the field (first paper with `●`
in a column).

### 4. gap — structural unsolved problems

Three input sources, in order of evidence strength:

(a) **Converging discussion sections** across hub deep reads — limitations
    that multiple authors independently acknowledge. Strongest evidence.
(b) **Concept matrix gaps** — empty columns (no paper addresses a concept)
    or sparse rows (concept rarely combined with others).
(c) **Frontier diffs** — limitations of the most recent papers that have
    not yet been addressed.

**Writing style**: Each gap is a self-contained paragraph (not a bulleted
list). The paragraph should:

- Open with a concise statement of what is not yet achieved
- Reference the Concept Matrix or prior Survey Findings sections
  (e.g., "As the matrix shows, no surveyed approach combines X with Y...")
  to avoid re-explaining what individual papers do
- Mention specific papers only when adding NEW information not covered
  elsewhere — e.g., a specific failure mode relevant to the gap. Cite hub
  papers via wikilink.
- Close with the engineering consequence — what becomes possible if the gap
  is closed
- Avoid redundancy with Thesis, Foundation, and Progress; if a point was
  already made, reference it rather than restating it

### 5. seed (conditional)

**Include only when the user explicitly requests research proposals.**
For reading lists, reference collections, or background surveys, omit and
end Survey Findings at Gap.

When included, read `references/seed_format.md` for the structure
(academic contribution, required components, readiness assessment).
Each seed must be grounded in the gap analysis above and cite specific
hub papers as evidence for the readiness assessment.
