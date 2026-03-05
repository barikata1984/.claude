---
name: literature-survey
description: "Conduct a comprehensive academic literature survey on a given research topic. Searches the web systematically for papers from recent to historical, producing a structured Markdown report with summaries and a BibTeX file. Use this skill whenever the user asks for a literature review, survey, related work search, prior art investigation, or wants to know what research exists on X. Also trigger when the user says things like papers about, survey the field of, what is the state of the art in, find relevant publications, 先行研究, 文献調査, サーベイ, 論文を探して, or any request to systematically gather academic references."
---

# Literature Survey Skill

You are conducting a comprehensive academic literature survey. Your goal is to produce
a well-organized, citable reference collection that gives the user a clear picture of
the research landscape on their topic.

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
4. **Annotate each paper** with three structured fields:
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

### Phase 4: Survey-Level Synthesis

Derive survey-level findings by cross-cutting the paper-level annotations. This is the
primary intellectual contribution of the survey — it transforms a collection of papers
into actionable research insight.

1. **thesis** (この分野の本質的問題):
   Paper-level theses will reveal agreements, contradictions, and tensions. Synthesize
   these into a central claim about what the field's fundamental unsolved problem is.
   Example: "The core tension is between pre-task estimation accuracy and interaction
   cost — no existing approach resolves this without compromising one or the other."

2. **core** (分野の共通前提・暗黙の制約):
   Identify assumptions shared across the surveyed papers — these are the field's
   implicit constraints that bound what current methods can achieve.

   **Counter-example check (required)**: For each stated core assumption, search the
   surveyed papers for violations. If a counter-example exists, narrow the claim until
   no paper in the survey contradicts it. Document the check:
   - "Assumption: X. Counter-examples: [Paper A] partially violates this by doing Y.
     Refined: X, except when Z."

3. **diff** (未踏領域と工学的帰結):
   Identify what remains unsolved by examining the frontier of paper-level diffs — the
   limitations that the most recent papers still have not overcome. For each gap:
   - State the gap concretely (what is not yet achieved)
   - State the engineering consequence (what becomes possible if this gap is closed)
   - Trace which paper-level diffs point toward this gap as evidence

### Phase 5: Hallucination Check

Before generating the final report, verify that every paper actually exists.

Launch a subagent to batch-check all papers in parallel. For each paper, the subagent
should attempt to access the paper's DOI or URL using WebFetch:

- **DOI**: Fetch `https://doi.org/<DOI>` and confirm it resolves (HTTP 200/302)
- **URL**: Fetch the URL and confirm the page contains the paper title or authors

Report format from the subagent:
```
PASS: [Paper Title] — DOI/URL confirmed
FAIL: [Paper Title] — DOI/URL returned error or title mismatch
```

- Papers that FAIL must be re-searched via WebSearch to find a valid DOI/URL.
- If no valid reference can be found after re-search, remove the paper from the report.
- Document any removals in the Survey Methodology section.

### Phase 6: Output Generation

Produce two files in the user's specified directory (default: current directory):

#### Main Report: `survey_<topic_slug>.md`

```markdown
# Literature Survey: [Topic]

**Date**: YYYY-MM-DD
**Scope**: [Brief description of what was covered]
**Papers found**: N

## Research Landscape Overview

[2-3 paragraphs of factual background: major trends, how the area has evolved,
key venues and research groups. This orients a reader unfamiliar with the topic.
This section is descriptive, not argumentative.]

## Survey Findings

### Thesis

[The survey's central claim about the field's fundamental unsolved problem,
derived from cross-cutting paper-level theses. 1-2 paragraphs.]

### Core Assumptions

[Shared assumptions and implicit constraints across the field. Each assumption
includes a counter-example check against surveyed papers.]

1. **[Assumption]**
   Counter-examples: [Papers that partially violate this, if any]
   Refined: [Narrowed statement if needed]

2. ...

### Frontier Gaps

[Unsolved problems at the frontier, with engineering consequences.]

1. **[Gap]**
   - Evidence: [Paper-level diffs that point to this gap]
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
| N | [Title] | YYYY | [Venue] | [この分野における意義を端的に記述] |
| ... | ... | ... | ... | ... |

The `#` column corresponds to the paper's number within its category section,
enabling cross-reference from this table to the detailed entry.

### [Category 1 Name]

[Brief narrative connecting the papers in this category]

1. **[Paper Title]** — Authors (Year)
   Venue | [Citations: N] | DOI: `10.xxxx/xxxxx` or [URL]
   - **thesis**: [著者の中心的主張。手法の記述ではなく、何が真であると論じているか]
   - **core**: [手法の中核要素。これが欠けると手法が成立しない本質的な要素]
   - **diff**: [先行研究との対比（事実の記述）。何が新しいか、どの限界を克服したか]

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
```

#### BibTeX File: `survey_<topic_slug>.bib`

Generate a BibTeX entry for every paper in the report. Use the format:
```bibtex
@article{AuthorYear_keyword,
  title = {Full Paper Title},
  author = {Author1 and Author2 and Author3},
  year = {2024},
  journal = {Venue or ArXiv ID},
  doi = {10.xxxx/xxxxx},
  url = {https://...},
  note = {Citations: N}
}
```

Use `@inproceedings` for conference papers, `@article` for journals,
`@misc` for preprints/arXiv. Always include `doi` field when available.

## Quality Checklist

Before delivering results, verify:

- [ ] All three temporal tiers are represented
- [ ] Each paper has: title, authors, year, venue/source, DOI or URL, and thesis/core/diff
- [ ] BibTeX file has an entry for every paper in the report
- [ ] Papers are organized by category, not just listed chronologically
- [ ] The overview section gives a reader unfamiliar with the topic a clear starting point
- [ ] Survey Findings section contains thesis, core (with counter-example checks), and diff (with engineering consequences)
- [ ] Survey-level claims are traceable to specific paper-level annotations
- [ ] Foundational works table includes #, paper, year, venue, and significance
- [ ] Hallucination check completed — all papers verified via DOI/URL
- [ ] Search methodology is documented so the user can extend the survey later
