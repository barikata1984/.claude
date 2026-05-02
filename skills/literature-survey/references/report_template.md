# Report Template

Use this template when generating the survey report in Phase 5.

## File: `./literature/surveys/{survey_slug}.md`

```markdown
# Literature Survey: [Topic]

| | |
|---|---|
| **Date** | YYYY-MM-DD |
| **Scope** | [Brief description of what was covered] |
| **Papers mapped** | N |
| **Hub papers (deep-read)** | M |
| **Research Questions** | RQ1: ... / RQ2: ... / RQ3: ... |

## Abstract

[4 sentences:
1. Current state of the field
2. What this survey contributes
3. Key findings — concrete results, not vague claims
4. How findings were validated — search scope and method]

## Research Landscape Overview

[2-3 paragraphs of factual background: major trends, how the area has evolved,
key venues and research groups. Descriptive, not argumentative.]

## Terminology and Background

[Map terminology variations across the surveyed papers. Many areas use multiple
terms for the same concept. Clarifying upfront prevents reader confusion.]

| Term | Synonyms / Variants | Scope in this survey |
|------|---------------------|----------------------|
| [term 1] | [variant A, variant B, abbreviation] | [how this term is used here] |
| [term 2] | ... | ... |

## Survey Findings

### Thesis

[The survey's central claim about the field's fundamental unsolved problem,
derived from cross-cutting hub-paper deep reads + concept matrix patterns.
1-2 paragraphs. Cite hub papers via wikilink.]

### Foundation

[Shared technical building blocks the surveyed methods rely on. Aggregated
from hub-paper deep reads.]

1. **[Foundation element]**: [Description and which papers depend on it,
   with wikilinks to hub notes where applicable]
2. ...

### Progress

[Trajectory of significant advances, derived from hub-paper diffs in
chronological order. Show major capability transitions.]

1. **[Advance]**: [What limitation was overcome, by which paper(s), when]
2. ...

### Gap

[Each gap is a self-contained paragraph. Reference Concept Matrix and
prior sections to avoid redundancy. Close with the engineering consequence.]

1. **[Gap title]**

   [Paragraph: state the gap → reference matrix/sections for evidence →
   add only NEW details not covered elsewhere → engineering consequence.]
2. ...

### Seed

**Include only when the user requested research proposals.** If the user asked
for a reading list, reference collection, or background survey without
mentioning research directions, omit this section entirely.

When included, follow `references/seed_format.md`.

## Concept Matrix

This is the survey's primary at-a-glance artifact. Rows = papers (sorted by
relevance / centrality), columns = key concepts. Cells: `●` (central use),
`○` (mentioned), blank (absent). Empty columns or sparse rows indicate gaps.

**Column derivation rule** — pick 4-6 concepts as follows:

1. Aggregate all `concept tags` collected during Phase 2 Map across the entire
   paper set
2. Count tag frequency. Drop tags that appear in <2 papers (too sparse to
   discriminate) and tags that appear in >80% of papers (too universal — they
   define the survey scope, not differentiate within it)
3. From the remaining ranked list, pick the **top 4-6** that span the field's
   key axes (method family, problem domain, evaluation setting, etc.)
4. If the natural count is 4-6, take it; if more, prioritize concepts that
   appear in hub-paper deep reads' "アプローチと根幹要素" sections (these are
   the field's foundation per `synthesis_guide.md`)
5. Concepts appearing in synthesis Thesis / Foundation / Gap sections must
   appear as columns (otherwise the matrix can't ground the synthesis)

| Paper | [Concept 1] | [Concept 2] | [Concept 3] | [Concept 4] | [Concept 5] | [Concept 6] |
|-------|---|---|---|---|---|---|
| [[papers/{citekey}/{slug}\|Author1+ 2024]] | ● | ○ | | ● | | |
| Author2+ 2023 | | ● | ● | | ○ | |
| ... | | | | | | |

(Hub papers shown as wikilinks; non-hub papers as plain text.)

## Quantitative Trends

### Publication Count by Year

| Year | Count |
|------|-------|
| 2026 | N |
| 2025 | N |
| ... | ... |

### Concept Distribution

| Concept | Count of papers | % |
|---------|-----------------|---|
| [Concept 1] | N | X% |
| ... | ... | ... |

### Experimental Setting Breakdown

| Setting | Count | % |
|---------|-------|---|
| Simulation only | N | X% |
| Real hardware only | N | X% |
| Both | N | X% |
| Theoretical / analytical only | N | X% |

### Top Venues

| Venue | Count |
|-------|-------|
| [Venue 1] | N |
| ... | ... |

## Hub Papers

Papers selected for deep read via `/paper-summary`. Each entry links to the
generated note in `./literature/papers/{citekey}/`.

| # | Citekey | Title | Year | Venue | Code | Why hub |
|---|---------|-------|------|-------|------|---------|
| 1 | [[papers/{citekey1}/{slug1}\|{Citekey1}]] | [Title] | YYYY | [Venue] | [GitHub](url) / — | [bridges clusters X+Y; central to gap Z] |
| 2 | ... | ... | ... | ... | ... | ... |

(`Code` 列は各 hub の `Repository` frontmatter から取得。未公開なら `—`。)

## Paper Catalogue

Non-hub papers are listed here as 1-line entries. Hub papers are shown above
in the Hub Papers section; their entries here are minimal pointers.

### [Category 1 Name]

[1-2 sentence narrative connecting the papers in this category]

1. **Author1+ 2024**, "Title" ([DOI](...) | [arXiv](...))
   — [1-line contribution from Map phase]
2. **Author2+ 2023**, "Title" ([DOI](...))
   — [1-line contribution]
3. **Author3+ 2022** *(hub — see [[papers/{citekey3}/{slug3}|deep read]])*

### [Category 2 Name]
...

## Survey Methodology

### Frame

- Core topic: [topic]
- Depth: focused / broad
- Inclusion criteria: [list]
- Exclusion criteria: [list]
- Known abbreviations declared by user: [list, if any]

### Map

| Search angle | Source(s) | Sample query | Results |
|---|---|---|---|
| Direct topic | WebSearch + Semantic Scholar | `"..."` | N |
| Snowballing forward | Semantic Scholar citations | seeds: [list] | N |
| Snowballing backward | OpenAlex references | seeds: [list] | N |
| Survey discovery | WebSearch | `"survey of ..."` | N |
| Venue-specific | [venue list] | filter by venue | N |

- Total mapped: N
- Duplicates removed: N
- Excluded by I/E criteria: N
- DOI resolution: N papers had publisher DOI resolved from arXiv ID

### Hub Selection

- Selection criteria applied: B (cluster bridging + top-tertile citations)
  AND/OR C (synthesis centrality)
- Candidates considered: N
- Final hubs: M
- PDFs successfully acquired: M' (of M)
- Acquisition failures: [list with reasons]

### Verify

- Papers checked via reference-verify: N
- Passed: N
- Excluded as unverifiable: N ([list titles if any])
```
