# Report Template

Use this template when generating the survey report in Phase 7.

## File: `docs/SURVEYS/<topic_slug>.md`

```markdown
# Literature Survey: [Topic]

| | |
|---|---|
| **Date** | YYYY-MM-DD |
| **Scope** | [Brief description of what was covered] |
| **Papers found** | N |
| **Research Questions** | RQ1: ... / RQ2: ... / RQ3: ... |

## Abstract

[4 sentences following this structure:
1. Current state of the field (1-2 sentences)
2. What this survey contributes (1 sentence)
3. Key findings — concrete results, not vague claims (1 sentence)
4. How the findings were validated — search scope and method (1 sentence)]

## Research Landscape Overview

[2-3 paragraphs of factual background: major trends, how the area has evolved,
key venues and research groups. This orients a reader unfamiliar with the topic.
This section is descriptive, not argumentative.]

## Terminology and Background

[Map the terminology variations used across the surveyed papers. Many research
areas use multiple terms for the same concept, or the same term with different
meanings depending on context. Clarifying these upfront prevents reader
confusion and documents the keyword mapping used during search.]

| Term | Synonyms / Variants | Scope in this survey |
|------|---------------------|----------------------|
| [term 1] | [variant A, variant B, abbreviation] | [how this term is used here] |
| [term 2] | ... | ... |

## Survey Findings

### Thesis

[The survey's central claim about the field's fundamental unsolved problem,
derived from cross-cutting paper-level theses. 1-2 paragraphs.]

### Foundation

[Shared technical building blocks and assumptions that the surveyed methods
rely on. Derived from aggregating paper-level cores.]

1. **[Foundation element]**: [Description and which papers depend on it]

2. ...

### Progress

[Trajectory of significant advances, derived from aggregating paper-level
diffs chronologically. Show the major capability transitions.]

1. **[Advance]**: [What limitation was overcome, by which paper(s), when]

2. ...

### Gap

[Each gap is a self-contained paragraph. Reference Paper Catalogue categories
and prior sections to avoid redundancy. Close with the engineering consequence.]

1. **[Gap title]**

   [Paragraph: state the gap → reference categories/sections for evidence →
   add only NEW details not covered elsewhere → engineering consequence.]

2. ...

### Seed

**Include this section only when the user requests research proposals, next
steps, or seed ideas.** If the user asks for a reading list, reference
collection, or background survey without mentioning research directions,
omit the Seed section entirely.

When included, read `references/seed_format.md` for the detailed structure.

## Paper Catalogue

### Category Overview

[Narrative explaining how the surveyed papers cluster into categories.
Describe what characterizes each category and how they relate to each other.]

| Category | Description | Count |
|----------|-------------|-------|
| [Cat 1]  | [One-line description] | N |
| [Cat 2]  | [One-line description] | N |
| ...      | ...         | ... |

### Comparison Table

[Cross-cutting comparison of key papers. Adapt the columns to the topic
domain. The purpose is to enable at-a-glance comparison across the most
important dimensions — a reader should be able to identify which papers
are most relevant to their specific needs.]

| Paper | Method Category | System Type | Sensors | Metrics | Environment | Real HW | Code |
|-------|----------------|-------------|---------|---------|-------------|---------|------|
| A et al. (2024) | [cat] | [type] | [sensors] | [metrics] | [env] | Yes/No | Yes/No |
| B et al. (2023) | ... | ... | ... | ... | ... | ... | ... |

Evidence level column (simplified from Shaw 2003):
- **R**: Real-world experiment with comparison
- **S**: Simulation-only experiment
- **B**: Both simulation and real-world
- **T**: Theoretical / analytical only

### Quantitative Trends

[Tabulate from paper metadata — no new searches needed.]

#### Publication Count by Year

| Year | Count |
|------|-------|
| 2026 | N |
| 2025 | N |
| ... | ... |

#### Method Category Distribution

| Category | Count | % |
|----------|-------|---|
| [Cat 1] | N | X% |
| ... | ... | ... |

#### Experimental Setting Breakdown

| Setting | Count | % |
|---------|-------|---|
| Simulation only | N | X% |
| Real hardware only | N | X% |
| Both | N | X% |

### Concept Matrix

[Maps key concepts (rows) to papers (columns). Derive concepts from
category assignments and thesis/core annotations.]

| Concept | Paper A | Paper B | Paper C | ... |
|---------|---------|---------|---------|-----|
| [concept 1] | X | | X | |
| [concept 2] | | X | X | |
| ... | | | | |

### Foundational Works

| # | Paper | Year | Venue | Significance |
|---|-------|------|-------|-------------|
| N | [Title] | YYYY | [Venue] | [Brief significance in this field] |
| ... | ... | ... | ... | ... |

The `#` column corresponds to the paper's number within its category section,
enabling cross-reference from this table to the detailed entry.

### [Category 1 Name]

[Brief narrative connecting the papers in this category]

1. [[Key]](references/main.md#Key) — Authors, "Title" (Year)
   - **DOI**: [Publisher DOI, e.g., `10.1109/ICRA.2024.XXXXXXX`] | **arXiv**: [ID if no publisher DOI]
   - **thesis**: [The author's central claim — what they argue is true, not what the method does]
   - **core**: [The essential element(s) without which the method would not work]
   - **diff**: [Explicit contrast with prior work — what is new, what limitation is overcome]
   - **limit**: [Constraints the authors acknowledge — from Limitations/Future Work sections]

2. ...

### [Category 2 Name]
...

## Survey Methodology

### Search Review Checkpoint

[Record the checkpoint interaction from Phase 2.5.]

- Papers presented to user: N
- User additions: N ([list titles if any])
- User removals: N ([list titles/directions if any])
- Target count adjustment: [none / changed from X to Y]
- Duplicates removed before checkpoint: N

### Search Log

[Record the actual searches performed during this survey. Each entry is one
search action (a WebSearch query, an arXiv API call, etc.).
Group by search angle/subagent.]

#### [Search Angle 1 Name]

| # | Source | Query / URL | Results | Notes |
|---|--------|-------------|---------|-------|
| 1 | WebSearch | `"exact query string used"` | N hits, M relevant | [brief note on what was found/not found] |
| 2 | arXiv API | `search_query=all:...` | N results | [note] |
| 3 | ar5iv | `https://ar5iv.labs.arxiv.org/html/XXXX.XXXXX` | success/fail | [used for limit field of Key] |
| ... | ... | ... | ... | ... |

#### [Search Angle 2 Name]
...

**Source summary**: [List all distinct information sources used (e.g., Google
via WebSearch, arXiv API, ar5iv, DBLP, Semantic Scholar, Crossref, IEEE Xplore
via fetch_with_auth, OpenReview, specific project websites) and the approximate
number of queries to each.]

### DOI Resolution Log

- Papers with publisher DOI resolved: N / M
- Papers remaining arXiv-only: N (preprint: N, DOI not found: N)
- Resolution sources used: [e.g., DBLP (N queries), Semantic Scholar (N), Crossref (N)]

| Paper | arXiv ID | Publisher DOI | Source | Notes |
|-------|----------|---------------|--------|-------|
| [Short title] | XXXX.XXXXX | 10.XXXX/... | DBLP | [venue] |
| [Short title] | XXXX.XXXXX | — | — | Preprint (not yet published) |
| ... | ... | ... | ... | ... |

### Hallucination Check Results

- Papers checked: N
- Passed: N
- Failed and re-searched: N
- Removed (unverifiable): N ([list titles if any])

### Limit Field Coverage

- Papers with limit recorded: N / M (X%)
- Papers marked "limit not available": N, breakdown:

| Category | Count | Papers | Action taken |
|----------|-------|--------|-------------|
| Paywall (fetched in 3b) | N | [list keys] | Cookies provided, fetch_with_auth succeeded |
| Paywall (skipped) | N | [list keys] | User chose to skip publisher group |
| Rendering failure | N | [list keys] | [e.g., retried with alternative methods / user declined] |
| Survey/review paper | N | [list keys] | N/A (no Limitations section expected) |

### Threats to Validity

[Discuss limitations of this survey itself — not the surveyed papers'
limitations, but constraints on how this survey was conducted.]

- **Search scope**: Which databases were searched, which were not. Language
  restrictions applied (e.g., English-only). Time period covered.
- **Publication bias**: The degree to which preprints and grey literature
  were included to counter positive-result bias in peer-reviewed venues.
- **Selection bias**: How inclusion/exclusion criteria may have systematically
  excluded relevant work (e.g., excluding certain robot types or venues).
- **Analysis limitations**: Single-reviewer analysis (AI-assisted), potential
  for misinterpretation of papers not read in full text (paywall).

## Conclusion

[Structured conclusion addressing each Research Question posed in Phase 1:]

1. **RQ1**: [1-2 sentence answer summarizing what the survey found]
2. **RQ2**: [...]
3. **RQ3**: [...]

[1 paragraph on practical implications — what practitioners should take away.]

[1 paragraph on the most promising research directions identified.]
```
