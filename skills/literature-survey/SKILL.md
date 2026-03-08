---
name: literature-survey
description: "Conduct a comprehensive academic literature survey on a given research topic. Searches the web systematically for papers from recent to historical, producing a structured Markdown report with summaries. Use this skill whenever the user asks for a literature review, survey, related work search, prior art investigation, or wants to know what research exists on X. Also trigger when the user says things like papers about, survey the field of, what is the state of the art in, find relevant publications, prior work, related work, or any request to systematically gather academic references."
---

# Literature Survey Skill

You are conducting a comprehensive academic literature survey. Your goal is to produce
a well-organized, citable reference collection that gives the user a clear picture of
the research landscape on their topic.

## Language Rule

**The entire report must be written in a single language, determined by the language
of the user's topic description:**

- User provides topic in **Japanese** → all prose in **Japanese**
- User provides topic in **English** → all prose in **English**

"Prose" means: section narratives, thesis/core/diff/limit annotations, category
descriptions, gap analyses, significance descriptions, and methodology notes.

Always keep the following in English regardless of output language:
paper titles, author names, venue names, DOI, URLs, BibTeX keys, and
structural labels (thesis/core/diff/limit).

Do NOT mix languages within a single report. The template below contains
placeholder descriptions in English; translate them to match the output language.

## Workflow

### Phase 1: Scope Definition

Before searching, clarify the survey scope with the user if not already clear:

- **Core topic**: The specific research question or area
- **Breadth**: Should adjacent fields be included?
- **Time emphasis**: Default is recent-first with historical coverage (see Phase 2)
- **Target count**: Default 30-60 papers, adjustable

If the user's request is already specific enough, skip the clarification and proceed.

### Phase 2: Search Strategy

Search systematically in three temporal tiers:

**Tier 1 — Recent (last 2-3 years): Exhaustive**
- Search for the latest preprints, conference papers, and journal articles
- Include workshop papers and technical reports if relevant
- This tier gets the most effort — aim for near-complete coverage of the topic

**Tier 2 — Established (3-10 years): High-impact focus**
- Concentrate on highly-cited papers and key contributions
- Identify papers that introduced major techniques, datasets, or benchmarks
- Follow citation chains from Tier 1 papers backward

**Tier 3 — Foundational (10+ years): Seminal works only**
- Classic papers that defined the field or subfield
- Only include if they are still widely cited or conceptually essential

### Search Execution

Use multiple complementary search approaches to maximize coverage:

1. **Direct topic search**: Search the core topic and its synonyms/variants
2. **Survey discovery**: Search for existing survey papers on the topic — these are goldmines for finding references you might miss
3. **Citation chain following**: When you find a key paper, look at what it cites and what cites it
4. **Author tracking**: If a few researchers dominate the field, search their recent publications
5. **Venue-specific search**: Check top venues (conferences/journals) known for this area

For each search, use WebSearch to find papers and WebFetch to access abstracts,
Semantic Scholar API pages, or arXiv pages for details.

**Semantic Scholar API** is particularly useful:
- Search: `https://api.semanticscholar.org/graph/v1/paper/search?query=TOPIC&limit=20&fields=title,authors,year,abstract,citationCount,url,venue,externalIds`
- Paper details: `https://api.semanticscholar.org/graph/v1/paper/PAPER_ID?fields=title,authors,year,abstract,citationCount,references,citations,url,venue,externalIds`
- Use citation counts to gauge impact and prioritize papers

**arXiv search** for preprints:
- `https://export.arxiv.org/api/query?search_query=all:TOPIC&sortBy=submittedDate&sortOrder=descending&max_results=20`

**ar5iv** for full-text access (arXiv papers only):
- `https://ar5iv.labs.arxiv.org/html/PAPER_ID` (e.g., `https://ar5iv.labs.arxiv.org/html/2206.15469`)
- HTML rendering of arXiv PDFs — use to access Limitations/Future Work sections for the `limit` field
- Not all papers are available; fall back to abstract/Semantic Scholar if ar5iv returns an error

Use subagents to parallelize searches across different queries and sources when possible.
Each subagent should handle a distinct search angle (e.g., one for the main topic,
one for a related subtopic, one for survey papers).

**DOI/URL requirement**: Every paper collected must have at least one of:
- DOI (preferred): e.g., `10.1109/ICRA.2024.XXXXXXX`
- URL: arXiv page, Semantic Scholar page, or publisher page

Papers for which neither DOI nor URL can be found should be excluded.

### Phase 3: Paper-Level Analysis

After collecting papers, analyze each individually and organize into themes:

1. **Identify themes**: Group papers by subtopic, methodology, or contribution type
2. **Trace the evolution**: Show how the field progressed over time
3. **Highlight connections**: Note where papers build on, extend, or contradict each other
4. **Annotate each paper** with four structured fields:
   - **thesis**: The author's central claim — not what the method does, but what the
     author argues is true. Frame as an argumentative stance (e.g., "dense physical
     features from interaction are necessary for manipulation, visual appearance alone
     is insufficient" rather than "proposes a method to assign dense physical features").
   - **core**: The essential, irreplaceable element(s) of the method. Without this, the
     approach would not work. Be specific (e.g., "differentiable rendering loss that
     back-propagates through the physics simulator" not just "differentiable rendering").
   - **diff**: Explicit contrast with prior work. Name the predecessor(s) and state what
     limitation is overcome or what new capability is introduced. This is a factual record
     of accomplished advances. Avoid vague statements like "improves over previous methods".
   - **limit**: Constraints or unsolved problems the authors explicitly acknowledge —
     typically from the Limitations or Future Work sections. Record only what the authors
     themselves state; do not mix in the reviewer's subjective critique. Where diff records
     limitations that *were* overcome, limit records those that *remain*.
     When the full text is unavailable, supplement with: (a) Semantic Scholar TLDR or
     abstract hints, (b) limitations noted by citing papers. If no limit information can
     be found from any source, write "limit not available" rather than guessing.

### Phase 4: Survey-Level Synthesis

Derive survey-level findings by cross-cutting the paper-level annotations. This is the
primary intellectual contribution of the survey — it transforms a collection of papers
into actionable research insight.

The four paper-level axes (thesis/core/diff/limit) aggregate into four survey-level
sections via the following logic:

1. **thesis** — the field's fundamental unsolved problem:
   Paper-level theses will reveal agreements, contradictions, and tensions. Synthesize
   these into a central claim about what the field's fundamental unsolved problem is.
   Example: "The core tension is between pre-task estimation accuracy and interaction
   cost — no existing approach resolves this without compromising one or the other."

2. **foundation** — the shared technical substrate:
   Aggregate paper-level cores to identify what technical building blocks the field
   relies on. These are the shared substrates — methods, representations, or
   assumptions — without which the majority of surveyed approaches would not function.
   For each stated foundation, verify that it genuinely holds across the surveyed papers;
   if a paper contradicts it, narrow the claim accordingly.

3. **progress** — the trajectory of solved problems:
   Aggregate paper-level diffs chronologically to trace how the field has advanced.
   Identify the most significant capability transitions — where a limitation of earlier
   work was definitively overcome. This section shows the trajectory of solved problems.

4. **gap** — structural unsolved problems and engineering consequences:
   Identify what remains unsolved by examining two sources:
   (a) the frontier of paper-level diffs — limitations that the most recent papers
       still have not overcome, and
   (b) paper-level limits — constraints that multiple papers independently acknowledge.
   Converging limits across papers are stronger evidence of structural gaps than
   isolated mentions. For each gap:
   - State the gap concretely (what is not yet achieved)
   - State the engineering consequence (what becomes possible if this gap is closed)
   - Trace which paper-level diffs and/or limits point toward this gap as evidence

### Phase 5: Hallucination Check

Follow the hallucination check procedure in `.claude/rules/references.md`.
Exclude papers that fail verification and record the exclusion count in the
Survey Methodology section.

### Phase 6: Output Generation

Produce the following file in `docs/SURVEYS/`:

#### Main Report: `docs/SURVEYS/<topic_slug>.md`

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

[Structural unsolved problems, derived from converging paper-level limits
and the frontier of paper-level diffs.]

1. **[Gap]**
   - Evidence: [Paper-level diffs and/or limits that point to this gap]
   - Engineering consequence: [What becomes possible if resolved]

2. ...

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
   - **thesis**: [The author's central claim — what they argue is true, not what the method does]
   - **core**: [The essential element(s) without which the method would not work]
   - **diff**: [Explicit contrast with prior work — what is new, what limitation is overcome]
   - **limit**: [Constraints the authors acknowledge — from Limitations/Future Work sections]

2. ...

### [Category 2 Name]
...

## Survey Methodology

[What sources were searched, what queries were used, any limitations]

### Hallucination Check Results

- Papers checked: N
- Passed: N
- Failed and re-searched: N
- Removed (unverifiable): N ([list titles if any])

### Limit Field Coverage

- Papers with limit recorded: N / M (X%)
- Papers marked "limit not available": N ([list titles if any])
- Primary cause of unavailability: [e.g., paywall, no Limitations section, preprint without full text]
```

## Reference Processing

Follow the citation conventions in `.claude/rules/references.md`.

Additional steps:
1. **Update MAIN.md**: Add all papers from the Paper Catalogue to MAIN.md
2. **Update SURVEYS/README.md**: Add a new entry to the table in `docs/SURVEYS/README.md`
   after the survey is complete
3. **Execution log**: Append to `docs/LOGS/literature-survey.md` with the search process,
   output file paths, and implications for the project

## Quality Checklist

Before delivering results, verify:

- [ ] All three temporal tiers are represented
- [ ] Each paper has: title, authors, year, venue/source, DOI or URL, and thesis/core/diff/limit
- [ ] Papers are organized by category, not just listed chronologically
- [ ] The overview section gives a reader unfamiliar with the topic a clear starting point
- [ ] Survey Findings section contains thesis, foundation, progress, and gap (with engineering consequences)
- [ ] Survey-level claims are traceable to specific paper-level annotations
- [ ] Foundational works table includes #, paper, year, venue, and significance
- [ ] Hallucination check completed — all papers verified via DOI/URL
- [ ] Search methodology is documented so the user can extend the survey later
- [ ] Output language is consistent throughout — no mixing of languages
