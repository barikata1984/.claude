---
name: literature-survey
description: >
  Use this skill for any request to systematically find, collect, or synthesize
  academic papers on a topic. This skill MUST be used — do not attempt literature
  surveys by running ad-hoc web searches without this skill.

  Trigger on any of the following, even if the user does not use the word "survey":
  - Asks for a literature review, related work, or prior art on any topic
  - Wants to know what research exists on X, or what the state of the art is
  - Wants to find papers to cite, or needs a reference list for a paper section
  - Says things like "survey the field", "find relevant papers", "what has been done on",
    "are there papers about", "who else has worked on", "what are the key papers in"
  - Needs to identify research gaps or open problems in a field
  - Wants to understand how a field has evolved or what the current trends are
  - Is preparing a Related Work section and needs systematic coverage
  - Needs to verify novelty of a research idea against existing work

  Produces a structured report in docs/SURVEYS/ with paper catalogue, survey-level
  findings (thesis, foundation, progress, gap), and optionally research seed proposals.
  For robotics topics, automatically applies venue-prioritized search using
  references/venues_robotics.md (CoRL, ICRA, IROS, RA-L, RSS, etc.).
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

### Phase 1: Scope Definition

**Read the conversation context first.**

Before asking the user anything, check whether the following parameters are
already established in the conversation history:

- **Core topic**: A research description, take-home message, or problem statement
- **Depth**: Whether adjacent fields should be included (broad) or the core topic
  only (focused)
- **Seed**: Whether research proposals / next-step ideas are needed
- **Constraints**: Experimental environment, hardware, or resource limits relevant
  to feasibility assessment

If all four are present and unambiguous, output a single confirmation line
(e.g., "Surveying [topic], focused depth, no seed — proceeding to search.")
and move directly to Phase 2.

If some are missing, ask only about the missing ones. Do not re-ask what is
already established.

If invoked standalone with no prior context, clarify the full scope
interactively:

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
5. **Venue-specific search**: Check top venues (conferences/journals) known for this area.
   If the topic falls in robotics, robot learning, manipulation, or adjacent fields
   (e.g., sim-to-real transfer, physical property estimation, human-robot interaction),
   read `references/venues_robotics.md` before executing venue-specific searches.
   Use the venue lists, search strategy notes, and DOI patterns defined there.

For each search, use WebSearch to find papers and WebFetch to access abstracts
or arXiv pages for details. WebSearch is the primary discovery tool — it is
fast, has no rate limits, and reliably finds papers across all venues.

**arXiv search** for preprints:
- `https://export.arxiv.org/api/query?search_query=all:TOPIC&sortBy=submittedDate&sortOrder=descending&max_results=20`

**ar5iv** for full-text access (arXiv papers only):
- `https://ar5iv.labs.arxiv.org/html/PAPER_ID` (e.g., `https://ar5iv.labs.arxiv.org/html/2206.15469`)
- HTML rendering of arXiv PDFs — use to access Limitations/Future Work sections for the `limit` field
- Not all papers are available; fall back to abstract/Semantic Scholar if ar5iv returns an error

**Authenticated publisher access** (paywalled papers):
- Use the `fetch_with_auth` MCP tool to access full-text HTML from IEEE, Elsevier, Springer, and ACM
- The tool uses institutional authentication cookies exported from the user's browser
- Use this primarily to populate the `limit` field for papers where ar5iv and abstracts are insufficient
- If the tool returns a session-expiry error, inform the user that cookie re-export is needed
  (see `.claude/mcp/academic-fetch/README.md` for the workflow)

**Structured metadata retrieval** via bundled scripts (in `scripts/`):

The skill includes two API search scripts that return structured JSON with citation
counts, DOIs, and venue information. Use these alongside WebSearch — WebSearch is
better for broad discovery, while the scripts provide precise metadata for scoring
and deduplication.

- `scripts/search_semantic_scholar.py` — Semantic Scholar Academic Graph API
  ```bash
  python scripts/search_semantic_scholar.py --query "TOPIC" --year-from 2022 --limit 30
  ```
  Returns: title, authors, year, venue, citationCount, doi, arxivId

- `scripts/search_openalex.py` — OpenAlex API (250M+ works)
  ```bash
  python scripts/search_openalex.py --query "TOPIC" --year-from 2022 --sort cited_by_count:desc
  ```
  Returns: title, authors, year, venue, citedByCount, doi, arxivId

Run these scripts early in the search process to obtain citation counts for all
candidate papers. The counts are used for scoring in Phase 2.5.

Use subagents to parallelize searches across different queries and sources when possible.
Each subagent should handle a distinct search angle (e.g., one for the main topic,
one for a related subtopic, one for survey papers).

**Search logging requirement**: Every subagent must return a structured search log
alongside its paper results. The log must record, for each search action performed:
(1) the information source (e.g., WebSearch, Semantic Scholar API, arXiv API, ar5iv,
IEEE Xplore), (2) the exact query string or URL used, (3) the number of results
obtained, and (4) a brief note on relevance. This log is aggregated into the
Survey Methodology → Search Log section of the final report.

**DOI/URL requirement**: Every paper collected must have at least one of:
- **Publisher DOI** (preferred): e.g., `10.1109/ICRA.2024.XXXXXXX`, `10.1007/...`
  This is the DOI assigned by the publisher (IEEE, ACM, Springer, PMLR, etc.),
  NOT the arXiv DOI (`10.48550/arXiv.XXXX.XXXXX`). Many ML papers appear first
  on arXiv but are later published at conferences with a different, authoritative DOI.
- **arXiv ID**: e.g., `2407.04620` — acceptable as a fallback, but always attempt
  to resolve to a publisher DOI in Phase 4 (DOI Resolution).
- **URL**: Publisher page, OpenReview page, or project page — use only when
  neither publisher DOI nor arXiv ID is available.

Papers for which none of these can be found should be excluded.

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

**Ask the user:**
- Are there known papers that should be added?
- Should any subtopics or directions be excluded?
- Should the target count be adjusted?

Do not proceed to Phase 3 until the user approves the paper list.

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

     **No speculation**: The limit field must contain only what the authors themselves
     explicitly state in the paper. Do not infer, deduce, or generate limitations
     based on general knowledge of the method or field. This rule exists because
     fabricated limitations are indistinguishable from real ones and undermine the
     survey's reliability.

### Phase 4: DOI Resolution

Many ML/AI papers first appear on arXiv but are later published at conferences
(ICML, NeurIPS, ICLR, CoRL, IROS, etc.) or in journals (JMLR, Science Robotics,
IJRR, etc.) with a separate, authoritative publisher DOI. The arXiv DOI
(`10.48550/arXiv.XXXX.XXXXX`) is not the same as the publisher DOI — the
publisher DOI is what should appear in formal citations.

After collecting and analyzing papers (Phases 2-3), resolve each paper's
identifier to its best available DOI. Process papers **sequentially** (not in
parallel) to respect API rate limits.

For each paper that currently only has an arXiv ID or URL:

1. **DBLP API** (first choice — fast, no authentication, generous rate limit):
   - `https://dblp.org/search/publ/api?q=TITLE&format=json`
   - Returns venue, year, and DOI for conference/journal publications
   - Match on title similarity (DBLP normalizes titles)

2. **Semantic Scholar API** (second choice — richer metadata, stricter rate limit):
   - `https://api.semanticscholar.org/graph/v1/paper/ArXiv:ARXIV_ID?fields=externalIds,venue,year,citationCount`
   - The `externalIds` field contains both `ArXiv` and `DOI` keys when available
   - Also useful for citation counts to gauge impact
   - **Rate limit**: 1 request/second without API key. Process one paper at a time
     with a brief pause between requests. If you receive a 429 error, wait 3 seconds
     and retry once. Do not retry more than once per paper — fall back to DBLP or
     Crossref instead.

3. **Crossref API** (fallback — broadest coverage, slower):
   - `https://api.crossref.org/works?query.title=TITLE&rows=3`
   - Returns publisher DOI for most published works
   - Match carefully on title and authors to avoid false positives

**Resolution priority**: Publisher DOI > arXiv ID > URL-only.

Record the resolution results in the DOI Resolution Log section of the final
report (see Phase 7 template). For papers that remain arXiv-only after this
phase, note whether the paper is a preprint (not yet published at a venue) or
whether the publisher DOI simply could not be found.

### Phase 5: Survey-Level Synthesis

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
   isolated mentions.

   **Writing style**: Each gap is a self-contained paragraph (not a bulleted list).
   The paragraph should:
   - Open with a concise statement of what is not yet achieved
   - Reference the Paper Catalogue categories or prior Survey Findings sections
     (e.g., "As Category D shows, ...") to avoid re-explaining what individual
     papers do — the reader has already encountered those details
   - Mention specific papers only when adding NEW information not covered
     elsewhere (e.g., a specific metric, a specific failure mode relevant to the gap)
   - Close with the engineering consequence — what becomes possible if the gap
     is closed
   - Avoid redundancy with Thesis, Foundation, and Progress sections; if a point
     was already made, reference it rather than restating it

5. **seed** (conditional) — novel research directions derived from the survey:
   **Include only when the user explicitly requests research proposals, next steps,
   or seed ideas.** For reading lists, reference collections, or background surveys,
   omit this section and end Survey Findings at Gap.

   When included, read `references/seed_format.md` for the detailed structure
   (academic contribution, required components, readiness assessment for each seed).

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

Read `references/report_template.md` for the complete report structure. The
template includes all sections: metadata table, Research Landscape Overview,
Survey Findings (Thesis/Foundation/Progress/Gap, and conditionally Seed),
Paper Catalogue with category overview and per-paper annotations, and
Survey Methodology (Search Log, DOI Resolution Log, Hallucination Check,
Limit Field Coverage).

If the user requested research proposals/seeds, also read
`references/seed_format.md` for the Seed section structure.

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
- [ ] Search Review Checkpoint (Phase 2.5) completed — user approved the paper list before analysis
- [ ] Duplicates removed and count recorded in search log
- [ ] Each paper has: title, authors, year, venue/source, publisher DOI (or arXiv ID if unpublished), and thesis/core/diff/limit
- [ ] limit fields contain only author-stated limitations (no LLM speculation)
- [ ] DOI Resolution phase completed — arXiv-only papers checked against DBLP/Semantic Scholar/Crossref for publisher DOIs
- [ ] Papers are organized by category, not just listed chronologically
- [ ] The overview section gives a reader unfamiliar with the topic a clear starting point
- [ ] Survey Findings section contains thesis, foundation, progress, and gap
- [ ] If user requested research proposals: seed section included (see `references/seed_format.md`)
- [ ] Survey-level claims are traceable to specific paper-level annotations
- [ ] Foundational works table includes #, paper, year, venue, and significance
- [ ] Hallucination check completed — all papers verified via DOI/URL
- [ ] Search Log records every search action: source, exact query/URL, result count, and notes
- [ ] Source summary lists all information sources used and query counts
- [ ] Output language is consistent throughout — no mixing of languages
