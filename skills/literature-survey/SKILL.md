---
name: literature-survey
description: >
  Conduct a comprehensive academic literature survey on a given research topic.
  Searches the web systematically for papers from recent to historical, producing
  a structured Markdown report with summaries and a BibTeX file.
  Use this skill whenever the user asks for a literature review, survey, related work
  search, prior art investigation, or wants to know "what research exists on X".
  Also trigger when the user says things like "papers about", "survey the field of",
  "what's the state of the art in", "find relevant publications", "先行研究", "文献調査",
  "サーベイ", "論文を探して", or any request to systematically gather academic references.
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

### Phase 3: Synthesis and Organization

After collecting papers, organize them into a coherent narrative:

1. **Identify themes**: Group papers by subtopic, methodology, or contribution type
2. **Trace the evolution**: Show how the field progressed over time
3. **Highlight connections**: Note where papers build on, extend, or contradict each other
4. **Spot gaps**: Identify areas with limited research or open questions
5. **Deep annotation per paper**: For each paper, write three structured fields:
   - **summary**: Concise description of the proposed method (2-3 sentences). What problem does it solve and how?
   - **core**: The essential, irreplaceable element(s) of the method. Without this, the approach would not work. Be specific (e.g., "differentiable rendering loss that back-propagates through the physics simulator" not just "differentiable rendering").
   - **diff**: Explicit contrast with prior work. Name the predecessor(s) and state what limitation is overcome or what new capability is introduced. Avoid vague statements like "improves over previous methods".

### Phase 4: Output Generation

Produce two files in the user's specified directory (default: current directory):

#### Main Report: `survey_<topic_slug>.md`

```markdown
# Literature Survey: [Topic]

**Date**: YYYY-MM-DD
**Scope**: [Brief description of what was covered]
**Papers found**: N

## Research Landscape Overview

[2-3 paragraphs summarizing the field: major trends, key debates,
how the area has evolved, and where it's heading]

## Thematic Sections

### [Theme 1 Name]

[Brief narrative connecting the papers in this theme]

1. **[Paper Title]** — Authors (Year)
   Venue | [Citations: N] | [URL]
   - **summary**: [提案手法の概要を2-3文で記述。何をどのように解決するか]
   - **core**: [提案手法の中核要素。これが欠けると手法が成立しない本質的な要素を端的に記述]
   - **diff**: [先行研究との対比。何が新しいか、どの既存手法の限界を克服したか]

2. ...

### [Theme 2 Name]
...

## Foundational Works

[Papers from Tier 3 that underpin the field]

## Research Gaps and Future Directions

[What's missing, what's emerging, what opportunities exist]

## Survey Methodology

[What sources were searched, what queries were used, any limitations]
```

#### BibTeX File: `survey_<topic_slug>.bib`

Generate a BibTeX entry for every paper in the report. Use the format:
```bibtex
@article{AuthorYear_keyword,
  title = {Full Paper Title},
  author = {Author1 and Author2 and Author3},
  year = {2024},
  journal = {Venue or ArXiv ID},
  url = {https://...},
  note = {Citations: N}
}
```

Use `@inproceedings` for conference papers, `@article` for journals,
`@misc` for preprints/arXiv.

## Quality Checklist

Before delivering results, verify:

- [ ] All three temporal tiers are represented
- [ ] Each paper has: title, authors, year, venue/source, URL, and summary
- [ ] BibTeX file has an entry for every paper in the report
- [ ] Papers are organized thematically, not just listed chronologically
- [ ] The overview section gives a reader unfamiliar with the topic a clear starting point
- [ ] Search methodology is documented so the user can extend the survey later
- [ ] No hallucinated papers — every entry was found via actual web search
