---
name: reference-verify
description: "Verify that academic references actually exist (not hallucinated) and retrieve missing metadata. Use this skill whenever you need to confirm that papers are real before citing them, check DOI/URL validity, or populate missing fields (e.g., limit/limitations) for a set of papers. Also trigger when the user says things like verify references, check citations, hallucination check, are these papers real, validate bibliography, or when any workflow requires confirming paper existence before adding to MAIN.md."
---

# Reference Verify Skill

You are verifying that academic references are real (not hallucinated) and optionally
retrieving missing metadata. This skill is used both as a standalone tool and as a
subprocess within literature-survey.

## Language Rule

Match the language of the invoking context. If called from a Japanese-language survey
or conversation, write prose in Japanese. If English, write in English. Keep paper
titles, author names, DOI, URLs, BibTeX keys, and structural labels in English
regardless.

## Input

This skill expects one of:

1. **A list of papers to verify** — provided inline or as a file path (e.g., a draft
   survey, a section of MAIN.md, or a plain list of titles/DOIs/URLs)
2. **A reference to an existing survey or document** — in which case, extract all
   cited papers and verify them

Each paper should ideally have at least: title, author(s), and one of DOI or URL.
Papers with only a title can still be checked via search.

## Workflow

### Step 1: Existence Verification (Hallucination Check)

Follow the procedure in `.claude/rules/references.md` § ハルシネーションチェック.

For each paper:

1. **If DOI is available**: WebFetch `https://doi.org/<DOI>` and confirm HTTP 200/302
   resolution
2. **If URL is available (no DOI)**: WebFetch the URL and confirm that the page
   contains the paper's title or author name
3. **If neither resolves**: WebSearch for the paper title + authors. If found, update
   the DOI/URL. If not found after search, mark as FAIL

**Scale-appropriate execution**:
- 1-5 papers: verify inline
- 6+ papers: spawn subagents to batch-verify in parallel (group by ~10 papers each)

Record each result:
- `PASS`: DOI/URL confirmed — paper is real
- `FAIL + RE-SEARCHED`: original DOI/URL failed but paper found via search — update
  the reference with correct DOI/URL
- `REMOVED`: paper not found via any method — exclude from output

### Step 2: Missing Metadata Triage (optional)

When the invoking context requests metadata retrieval (e.g., populating `limit` fields
for a literature survey), classify papers with missing metadata into three categories:

1. **Paywall barrier**: Papers behind publisher paywalls (IEEE, Elsevier, Springer,
   ACM, etc.) where full text was inaccessible. Potentially resolvable with
   `fetch_with_auth` MCP tool
2. **Rendering failure**: arXiv papers where ar5iv failed to render. Potentially
   resolvable by retrying ar5iv, alternative mirrors, or careful Semantic Scholar
   abstract extraction
3. **No Limitations section expected**: Survey/review/textbook papers that inherently
   lack a Limitations/Future Work section. No retrieval will help

Present these categories to the user with paper counts and titles, and ask
per-category whether to attempt additional retrieval:

- **Paywall**: offer to use `fetch_with_auth` (requires valid cookies)
- **Rendering failure**: offer to retry with alternative access methods
- **No Limitations section**: inform the user these will remain as-is (no action)

Proceed only after the user responds. If declined, move on.

**Retrieval sources** (in priority order):
- **ar5iv**: `https://ar5iv.labs.arxiv.org/html/<PAPER_ID>` for arXiv paper full text
- **fetch_with_auth**: MCP tool for paywalled publisher access (IEEE, Elsevier,
  Springer, ACM) — uses institutional authentication cookies
- **Semantic Scholar**: `https://api.semanticscholar.org/graph/v1/paper/<ID>?fields=abstract,tldr`
  for TLDR or abstract hints when full text is unavailable
- **Citing papers**: limitations noted by papers that cite the target paper

If `fetch_with_auth` returns a session-expiry error, inform the user that cookie
re-export is needed (see `.claude/mcp/academic-fetch/README.md`).

### Step 3: Report

Produce a verification summary. The format depends on context:

**Standalone invocation** — print the report directly:

```
## Reference Verification Report

- Papers checked: N
- Passed: N
- Failed and re-searched: N
- Removed (unverifiable): N
  - [list titles if any]
```

If metadata triage was performed, append:

```
## Metadata Coverage

- Papers with metadata retrieved: N / M (X%)
- Papers with metadata unavailable: N, breakdown:

| Category | Count | Papers | Action taken |
|----------|-------|--------|-------------|
| Paywall barrier | N | [list keys] | [action] |
| Rendering failure | N | [list keys] | [action] |
| No Limitations section | N | [list keys] | N/A |
```

**Called from literature-survey** — return structured data so the survey can embed
the results into its Survey Methodology section. The survey skill specifies the
exact output format it expects.

## Usage from Other Skills

Other skills can invoke this skill by including an instruction like:

> Use the reference-verify skill to verify all papers before adding them to MAIN.md.

The calling skill should specify:
- The list of papers (or point to the file containing them)
- Whether metadata triage is needed (and which fields)
- The desired output format (inline report vs. structured data for embedding)
