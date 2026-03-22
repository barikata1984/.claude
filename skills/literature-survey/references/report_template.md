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

## Research Landscape Overview

[2-3 paragraphs of factual background: major trends, how the area has evolved,
key venues and research groups. This orients a reader unfamiliar with the topic.
This section is descriptive, not argumentative.]

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

### Foundational Works

| # | Paper | Year | Venue | Significance |
|---|-------|------|-------|-------------|
| N | [Title] | YYYY | [Venue] | [Brief significance in this field] |
| ... | ... | ... | ... | ... |

The `#` column corresponds to the paper's number within its category section,
enabling cross-reference from this table to the detailed entry.

### [Category 1 Name]

[Brief narrative connecting the papers in this category]

1. [[Key]](../REFERENCES/MAIN.md#Key) — Authors, "Title" (Year)
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
| Paywall barrier | N | [list keys] | [e.g., fetch_with_auth attempted / user declined] |
| Rendering failure | N | [list keys] | [e.g., retried with alternative methods / user declined] |
| Survey/review paper | N | [list keys] | N/A (no Limitations section expected) |
```
