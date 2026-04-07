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
descriptions, gap analyses, seed proposals, significance descriptions, and methodology notes.

Always keep the following in English regardless of output language:
chapter/section/subsection headings, paper titles, author names, venue names,
proposed method/architecture names (e.g., "Rapid Motor Adaptation", "Domain Contraction"),
DOI, URLs, BibTeX keys, and structural labels (thesis/core/diff/limit).

Do NOT mix languages within a single report. The template below contains
placeholder descriptions in English; translate them to match the output language.

## Workflow

### Subagent Model Policy

All subagents launched during the survey must use the **middle-class model**
(the tier between the highest-capability and lowest-cost models in the
current lineup). This balances annotation quality against cost and context
efficiency.

### Phase 1: Research Design

Before searching, establish the survey's scope and boundaries with the user:

- **Core topic**: The specific research question or area
- **Research Questions (RQs)**: Formulate 2-4 concrete questions the survey
  will answer. RQs give the survey a clear purpose beyond "collect papers"
  and guide search, analysis, and synthesis. Example:
  - RQ1: What algorithmic approaches have been proposed for [problem]?
  - RQ2: Under what conditions are these approaches evaluated?
  - RQ3: What are the unresolved technical challenges?
- **Breadth**: Should adjacent fields be included?
- **Time emphasis**: Default is recent-first with historical coverage (see Phase 2)
- **Target count**: Default 30-60 papers, adjustable
- **Inclusion / Exclusion criteria**: Define the scope boundary upfront:
  - Inclusion: e.g., peer-reviewed papers + major preprints, specific
    robot types, specific task domains
  - Exclusion: e.g., poster-only publications, non-English papers,
    papers outside the target domain

If the user's request is already specific enough, propose the RQs and
criteria for confirmation rather than asking open-ended questions.

### Phase 2: Search Strategy

Search systematically in three temporal tiers:

**Tier 1 — Recent (last 2-3 years): Exhaustive**
- Search for the latest preprints, conference papers, and journal articles
- Include workshop papers, technical reports, and theses if relevant
- Actively include preprints to counter publication bias (positive results
  are overrepresented in peer-reviewed venues)
- This tier gets the most effort — aim for near-complete coverage of the topic

**Tier 2 — Established (3-10 years): High-impact focus**
- Concentrate on highly-cited papers and key contributions
- Identify papers that introduced major techniques, datasets, or benchmarks
- Follow citation chains from Tier 1 papers backward

**Tier 3 — Foundational (10+ years): Seminal works only**
- Classic papers that defined the field or subfield
- Only include if they are still widely cited or conceptually essential

### Keyword Construction

Before executing searches, derive a structured keyword set from the RQs:

1. Extract key concepts from each RQ (population, intervention, outcome)
2. For each concept, list synonyms, abbreviations, and spelling variants
3. Combine with Boolean operators to form search strings

Example: `("multi-robot" OR "multi-agent" OR "swarm") AND ("task allocation"
OR "task assignment") AND ("cooperation" OR "coordination")`

Record the final search strings in the Search Log.

### Search Execution

Use multiple complementary search approaches to maximize coverage:

1. **Direct topic search**: Search the core topic and its synonyms/variants
2. **Survey discovery**: Search for existing survey papers on the topic — these are goldmines for finding references you might miss
3. **Citation chain following**: When you find a key paper, look at what it cites and what cites it
4. **Author tracking**: If a few researchers dominate the field, search their recent publications
5. **Venue-specific search**: Check top venues (conferences/journals) known for this area

WebSearch is the primary discovery tool — it is fast, has no rate limits, and
reliably finds papers across all venues. Use it alongside the structured
metadata tools (Semantic Scholar MCP, OpenAlex script) described in
`references/search_sources.md`. Read that file at the start of Phase 2 for
tool-specific details (API formats, MCP parameters, OA resolution priority).

Use subagents to parallelize searches across different queries and sources.
Each subagent should handle a distinct search angle (e.g., one for the main
topic, one for a related subtopic, one for survey papers).

**Search logging requirement**: Every subagent must return a structured search log
alongside its paper results. The log must record, for each search action performed:
(1) the information source (e.g., WebSearch, Semantic Scholar API, arXiv API, ar5iv,
IEEE Xplore), (2) the exact query string or URL used, (3) the number of results
obtained, and (4) a brief note on relevance. This log is aggregated into the
Survey Methodology → Search Log section of the final report.

**DOI/URL requirement**: Every paper collected must have at least one of:
publisher DOI (preferred), arXiv ID (fallback), or URL (last resort). See
`references/search_sources.md` § DOI Types for details. Papers for which
none of these can be found should be excluded.

### Deduplication

Multiple search angles will inevitably find the same paper. Deduplicate before
proceeding to Phase 2.5:

- **Primary match**: DOI or arXiv ID (normalize before comparing — strip URL
  prefixes like `https://doi.org/` or `https://arxiv.org/abs/`)
- **Fallback match**: Title comparison after normalization (lowercase, strip
  punctuation and whitespace)
- **Merge strategy**: When duplicates are found, keep the entry with the richest
  metadata (publisher DOI > arXiv ID > URL-only)
- **Logging**: Record the total number of duplicates removed in the search log

### Phase 2.5: Search Review Checkpoint

Before investing effort in paper-level analysis (Phase 3), present the search
results to the user for review. This checkpoint exists because Phase 3 is the
most token- and time-intensive part of the workflow — the paper list should be
confirmed before analysis begins.

**Present the following to the user:**

A paper list grouped by temporal tier, sorted within each tier by citation count
(descending):

```
## Search Results (N papers found, target: M)

### Tier 1 — Recent (2023-2026): N papers
| # | Title | Year | Venue | Citations |
|---|-------|------|-------|-----------|
| 1 | ...   | 2025 | NeurIPS | 42      |

### Tier 2 — Established (2016-2022): N papers
| # | Title | Year | Venue | Citations |
|---|-------|------|-------|-----------|

### Tier 3 — Foundational (~2015): N papers
| # | Title | Year | Venue | Citations |
|---|-------|------|-------|-----------|

### Coverage Summary
- Search angles used: N (list them)
- Top venues represented: ...
- Duplicates removed: N
```

**Scoring criteria** (used for sort order and for pruning when count exceeds target):

1. **Citation count** (primary) — from Semantic Scholar or OpenAlex
2. **Venue tier** (secondary) — top-tier conference/journal > workshop > preprint
3. **Recency** (tertiary) — newer papers first within the same tier

Before presenting, apply the inclusion/exclusion criteria defined in
Phase 1 and note any papers excluded with reasons.

**Ask the user:**
- Are there known papers that should be added?
- Should any subtopics or directions be excluded?
- Should the inclusion/exclusion criteria be adjusted?
- Should the target count be adjusted?

Do not proceed to Phase 3 until the user approves the paper list.

### Phase 3a: Open-Access Paper Analysis

Classify the approved papers by full-text accessibility, then process OA papers first.

**Step 1 — Classify papers:**

For each approved paper, determine full-text access status:

1. If `openAccessPdf` was returned by `search_semantic_scholar`, classify as **OA**.
2. Otherwise, call `resolve_oa_url` with the paper's DOI / arXiv ID / S2 ID.
   - If `best_url` is non-null → **OA**
   - If `best_url` is null → **Paywall**

Record the classification and the resolved URL for each paper.

**Step 2 — Extract key sections (deterministic):**

For arXiv papers, run the section extraction script to obtain structured
content without reading full text:

```bash
python3 scripts/extract_sections.py --input oa_papers.json --output sections.json
```

The script fetches ar5iv HTML and extracts: abstract, introduction,
conclusion, limitations, future work, tables (as Markdown), and figure
captions. This replaces full-text reading for most papers — the extracted
sections contain the information needed for all four annotation fields.

For non-arXiv OA papers (e.g., publisher HTML), fall back to WebFetch on
the OA URL, but instruct the subagent to focus on the same sections.

**Step 3 — Annotate via subagents:**

Distribute the extracted sections across subagents in batches of 15-20
papers each. Because each paper is now represented by its key sections
(~2,000-5,000 tokens) rather than full text (~10,000-15,000 tokens),
larger batches are feasible.

Each subagent receives the pre-extracted sections and returns **only** a
JSON array — no intermediate reasoning or raw content:

```json
[
  {
    "key": "Author2024_keyword",
    "title": "...", "authors": "...", "year": 2024,
    "venue": "...", "doi": "...", "arxiv_id": "...", "oa_url": "...",
    "thesis": "1-2 sentences",
    "core": "1-2 sentences",
    "diff": "1-2 sentences",
    "limit": "1-2 sentences"
  }
]
```

**Annotation field definitions:**

- **thesis**: The author's central claim — not what the method does, but what
  the author argues is true. Frame as an argumentative stance (e.g., "dense
  physical features from interaction are necessary for manipulation, visual
  appearance alone is insufficient" rather than "proposes a method to assign
  dense physical features").
- **core**: The essential, irreplaceable element(s) of the method. Without
  this, the approach would not work. Be specific (e.g., "differentiable
  rendering loss that back-propagates through the physics simulator" not
  just "differentiable rendering").
- **diff**: Explicit contrast with prior work. Name the predecessor(s) and
  state what limitation is overcome or what new capability is introduced.
  Avoid vague statements like "improves over previous methods".
- **limit**: Constraints or unsolved problems the authors explicitly
  acknowledge — from the extracted Limitations/Future Work sections.
  Record only what the authors themselves state. If the extraction script
  could not find a Limitations section, supplement with abstract hints or
  write "limit not available" rather than guessing.

  **No speculation**: Fabricated limitations are indistinguishable from
  real ones and undermine the survey's reliability.

After all subagents return, merge their JSON arrays into a unified paper
list. Then identify themes, trace the evolution, and highlight connections
across the full set.

**Step 3 — OA coverage analysis and paywall processing recommendation:**

After processing all OA papers, analyze coverage and present a recommendation
before proceeding to Phase 3b:

1. **Coverage analysis**: For each thematic category and RQ, count OA vs
   Paywall papers. Identify categories where Paywall papers are the sole
   or majority source.
2. **Annotation coverage**: Calculate the percentage of papers with complete
   annotations (all four fields filled) from OA alone.
3. **Recommendation**: Based on the above, propose one of:
   - **Skip all**: OA coverage is sufficient across all categories/RQs
   - **Selective fetch**: List specific Paywall papers that fill coverage
     gaps (e.g., sole paper in a category, high-citation foundational work)
   - **Full fetch**: OA coverage has significant gaps requiring most
     Paywall papers

Present the analysis and recommendation to the user:

```
## Paywall Processing Recommendation

### OA Coverage Analysis
- Total: N papers (OA: X, Paywall: Y)
- Categories with OA-only coverage: [list]
- Categories requiring Paywall papers: [list, with reason]
- Annotation completeness (OA only): Z%

### Recommendation: [Skip all / Selective fetch / Full fetch]
[1-2 sentence justification]

### Paywall Papers (Y papers, M publishers)

| Publisher | Count | Papers | Priority |
|-----------|-------|--------|----------|
| IEEE Xplore | 3 | [Title1], ... | [High/Low] |
| Elsevier | 2 | [Title4], ... | [High/Low] |

For publishers you want to fetch:
1. Log in via your browser
2. Export cookies via Cookie-Editor (Export → JSON → copies to clipboard)
3. Run: bash ~/.claude/mcp/academic-fetch/save-cookies.sh
4. Say "ready" to process that publisher's papers

You can also say "skip" for any publisher to mark those papers as
"limit not available (paywall)" and move on.
```

If there are no paywall papers, skip Phase 3b entirely and proceed to Phase 4.

### Phase 3b: Paywall Paper Analysis

Process paywall papers one publisher group at a time:

```
for each publisher group (IEEE, Elsevier, Springer, ACM, ...):
  1. Ask the user to export cookies for this publisher + run save-cookies.sh
  2. User says "ready" → process all papers from this publisher via fetch_with_auth
  3. Annotate with the same four fields (thesis/core/diff/limit)
  4. If fetch_with_auth returns session-expiry → ask user to re-export cookies
  5. User says "skip" → mark all papers from this publisher as
     "limit not available (paywall)"
```

After all publisher groups are processed (or skipped), merge Phase 3a and 3b
results into a unified set of annotated papers. Update the themes and connections
identified in Phase 3a to incorporate newly analyzed paywall papers.

### Phase 3 → 5 Transition: Context Consolidation

Before proceeding to Phase 4, consolidate the analysis state. At this point,
only the following information is needed for the remaining phases:

1. **Paper metadata table**: key, title, authors, year, venue, DOI/arXiv ID
2. **Annotations**: thesis/core/diff/limit per paper (1-2 sentences each)
3. **Category assignments**: which papers belong to which thematic category
4. **Unresolved DOIs**: list of papers needing Phase 4 resolution

All raw search results, full-text content, and intermediate reasoning from
Phase 2-3 subagents have already been consumed and should not be carried
forward. If the conversation context has grown large, summarize the above
into a compact working state before continuing.

### Phase 4: DOI Resolution

Many ML/AI papers first appear on arXiv but are later published at venues
with a separate publisher DOI. The arXiv DOI (`10.48550/arXiv.XXXX.XXXXX`)
is not the publisher DOI — the publisher DOI should appear in formal citations.

Run the DOI resolution script on all papers that currently only have an
arXiv ID or URL:

```bash
python3 scripts/resolve_dois.py --input papers.json --output resolved.json
```

The script queries DBLP, `resolve_oa_url` MCP tool, and Crossref in cascade,
respecting rate limits. Resolution priority: publisher DOI > arXiv ID > URL.

Record the resolution results in the DOI Resolution Log section of the
final report (see Phase 7 template).

### Phase 5: Survey-Level Synthesis

Derive survey-level findings by cross-cutting the paper-level annotations.
This is the primary intellectual contribution of the survey — it transforms
a collection of papers into actionable research insight.

Read `references/synthesis_guide.md` for detailed writing guidelines for
each section. The four paper-level axes aggregate into survey-level sections:

1. **thesis** — synthesize paper-level theses into the field's fundamental
   unsolved problem
2. **foundation** — aggregate paper-level cores into shared technical
   building blocks
3. **progress** — aggregate paper-level diffs chronologically into a
   trajectory of solved problems
4. **gap** — identify structural unsolved problems from the frontier of
   diffs and converging limits
5. **seed** (conditional) — include only when the user explicitly requests
   research proposals. Read `references/seed_format.md` for structure.

Additionally, produce these cross-cutting analyses from the consolidated
paper metadata (no new searches needed):

6. **Quantitative trends** — tabulate from paper metadata:
   - Publication count by year
   - Distribution across method categories
   - Experimental setting breakdown (simulation / real hardware / both)
   - Top venues by paper count
7. **Concept matrix** — a table mapping key concepts (rows) to papers
   (columns) showing which papers address which concepts. Derive concepts
   from the category assignments and thesis/core annotations.

### Phase 6: Reference Verification

Use the **reference-verify** skill to verify all collected papers and retrieve
missing `limit` fields. Invoke it with:

- **Papers**: the full list of papers collected in Phases 2-3
- **Metadata triage**: enabled, targeting the `limit` field
- **Output format**: structured data for embedding into the Survey Methodology section

The reference-verify skill will:
1. Run hallucination checks (DOI/URL existence verification) on all papers
2. Exclude unverifiable papers and report the count
3. Classify papers with missing `limit` fields by barrier type (paywall /
   rendering failure / no Limitations section expected) and ask the user
   per-category whether to attempt additional retrieval

Only proceed to Phase 7 after reference-verify completes and the user has
responded to any triage prompts.

### Phase 7: Output Generation

Produce the survey report in `docs/SURVEYS/<topic_slug>.md`.

Read `references/report_template.md` for the complete report structure.
If the user requested research proposals/seeds, also read
`references/seed_format.md` for the Seed section structure.

Generate the report in sections to avoid hitting output limits and to
maintain quality across the full document:

1. **Metadata + Research Landscape Overview + Survey Findings**
   (Thesis/Foundation/Progress/Gap, and conditionally Seed)
2. **Paper Catalogue** — generate one category at a time, appending each
3. **Survey Methodology** (Search Log, DOI Resolution Log, Hallucination
   Check, Limit Field Coverage)

## Reference Processing

Follow the citation conventions in `.claude/rules/references.md`.

Additional steps:
1. **Update MAIN.md**: Add all papers from the Paper Catalogue to MAIN.md
2. **Update SURVEYS/README.md**: Add a new entry to the table in `docs/SURVEYS/README.md`
   after the survey is complete
3. **Execution log**: Append to `docs/LOGS/literature-survey.md` with the search process,
   output file paths, and implications for the project

## Quality Checklist

Before delivering results, read `references/quality_checklist.md` and verify
all items.
