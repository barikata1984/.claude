# Search Sources Reference

This file contains tool-specific details for Phase 2 (Search Execution).
SKILL.md specifies *what* to search and *when*; this file specifies *how* to
use each tool.

## arXiv API

Search for preprints:

```
https://export.arxiv.org/api/query?search_query=all:TOPIC&sortBy=submittedDate&sortOrder=descending&max_results=20
```

## ar5iv (Full-Text Access)

HTML rendering of arXiv PDFs — useful for extracting Limitations/Future Work
sections for the `limit` field.

- URL format: `https://ar5iv.labs.arxiv.org/html/PAPER_ID`
  (e.g., `https://ar5iv.labs.arxiv.org/html/2206.15469`)
- Not all papers are available; fall back to abstract/Semantic Scholar if
  ar5iv returns an error

## Semantic Scholar MCP Tool

`search_semantic_scholar` — Semantic Scholar Academic Graph API

- Parameters: `query`, `year_from`, `year_to`, `limit` (default 20), `offset`
- Returns: title, authors, year, venue, citationCount, doi, arxivId, abstract,
  openAccessPdf
- Rate limiting and API authentication handled internally by the MCP server
- Do NOT call the S2 API directly or use `scripts/search_semantic_scholar.py`

## OpenAlex Script

`scripts/search_openalex.py` — OpenAlex API (250M+ works)

```bash
python scripts/search_openalex.py --query "TOPIC" --year-from 2022 --sort cited_by_count:desc
```

Returns: title, authors, year, venue, citedByCount, doi, arxivId

Run Semantic Scholar and OpenAlex early in the search process to obtain
citation counts for all candidate papers. The counts are used for scoring
in Phase 2.5.

## Open-Access Full-Text Resolution

When you need to read a paper's full text, try these sources in priority order:

1. **openAccessPdf from search results** — already available in
   `search_semantic_scholar` output at no additional cost. Check this first.
2. **`resolve_oa_url` MCP tool** — resolves a DOI/arXiv ID/S2 ID to the best
   open-access URL via Unpaywall + S2 openAccessPdf + arXiv PDF fallback.
   Call this when `openAccessPdf` is null in the search results.
   - Parameters: `doi`, `s2_paper_id`, `arxiv_id` (at least one required)
   - Returns: JSON with resolved URLs from each source and a `best_url`
     recommendation
3. **ar5iv** — `https://ar5iv.labs.arxiv.org/html/PAPER_ID` (arXiv papers
   only). Provides structured HTML with headings, useful for extracting
   Limitations sections.
4. **`fetch_with_auth` MCP tool** — last resort for paywalled papers (IEEE,
   Elsevier, Springer, ACM). Uses institutional authentication cookies.
   - If the tool returns a session-expiry error, inform the user that cookie
     re-export is needed (see `.claude/mcp/academic-fetch/README.md`)

In Phase 3a, sources 1-3 are used to classify papers as OA or Paywall.
Source 4 (`fetch_with_auth`) is used only in Phase 3b for paywall papers.

## DOI Types

- **Publisher DOI** (preferred): e.g., `10.1109/ICRA.2024.XXXXXXX`,
  `10.1007/...` — assigned by the publisher (IEEE, ACM, Springer, PMLR, etc.),
  NOT the arXiv DOI (`10.48550/arXiv.XXXX.XXXXX`). Many ML papers appear
  first on arXiv but are later published at conferences with a different,
  authoritative DOI.
- **arXiv ID**: e.g., `2407.04620` — acceptable as a fallback, but always
  attempt to resolve to a publisher DOI in Phase 4.
- **URL**: Publisher page, OpenReview page, or project page — use only when
  neither publisher DOI nor arXiv ID is available.
