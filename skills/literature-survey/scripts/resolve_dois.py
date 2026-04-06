#!/usr/bin/env python3
"""Resolve arXiv-only papers to publisher DOIs.

Queries DBLP and Crossref APIs in cascade to find publisher DOIs for papers
that currently only have an arXiv ID or URL. Uses stdlib only (no pip deps).

Input JSON format (array of objects, or object with "papers" key):
    [{"title": "...", "arxiv_id": "2407.04620", "doi": null}, ...]

Output JSON format:
    {
        "resolved": [...],  // papers with updated DOIs
        "summary": {"total": N, "resolved": N, "unresolved": N}
    }

Usage:
    python resolve_dois.py --input papers.json --output resolved.json
    python resolve_dois.py --input papers.json  # stdout
    cat papers.json | python resolve_dois.py    # stdin/stdout
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "literature-survey-skill/1.0 (mailto:noreply@example.com)"
DBLP_API = "https://dblp.org/search/publ/api"
CROSSREF_API = "https://api.crossref.org/works"


def _fetch_json(url: str, *, timeout: int = 30, retries: int = 2) -> dict | None:
    """Fetch JSON from a URL with retries and backoff."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries:
                wait = (2**attempt) + random.uniform(0, 1)
                time.sleep(wait)
                continue
            return None
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries:
                time.sleep(1)
                continue
            return None
    return None


def _normalize_title(title: str) -> str:
    """Lowercase, strip punctuation and extra whitespace for comparison."""
    import re

    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)
    return " ".join(title.split())


def _titles_match(a: str, b: str, threshold: float = 0.85) -> bool:
    """Check if two titles match after normalization."""
    na, nb = _normalize_title(a), _normalize_title(b)
    if na == nb:
        return True
    # Simple word overlap ratio
    words_a, words_b = set(na.split()), set(nb.split())
    if not words_a or not words_b:
        return False
    overlap = len(words_a & words_b)
    ratio = overlap / max(len(words_a), len(words_b))
    return ratio >= threshold


def resolve_via_dblp(title: str) -> str | None:
    """Search DBLP for a publisher DOI by title."""
    params = urllib.parse.urlencode({"q": title, "format": "json", "h": 3})
    url = f"{DBLP_API}?{params}"
    data = _fetch_json(url)
    if not data:
        return None

    hits = data.get("result", {}).get("hits", {}).get("hit", [])
    for hit in hits:
        info = hit.get("info", {})
        hit_title = info.get("title", "")
        doi = info.get("doi")
        if doi and _titles_match(title, hit_title):
            return doi
    return None


def resolve_via_crossref(title: str) -> str | None:
    """Search Crossref for a publisher DOI by title."""
    params = urllib.parse.urlencode({"query.title": title, "rows": 3})
    url = f"{CROSSREF_API}?{params}"
    data = _fetch_json(url, timeout=45)
    if not data:
        return None

    items = data.get("message", {}).get("items", [])
    for item in items:
        item_titles = item.get("title", [])
        doi = item.get("DOI")
        if doi and item_titles and _titles_match(title, item_titles[0]):
            return doi
    return None


def is_arxiv_doi(doi: str) -> bool:
    """Check if a DOI is an arXiv DOI (not a publisher DOI)."""
    return doi.startswith("10.48550/arXiv.") or doi.startswith("10.48550/arxiv.")


def needs_resolution(paper: dict) -> bool:
    """Check if a paper needs DOI resolution."""
    doi = paper.get("doi")
    if doi and not is_arxiv_doi(doi):
        return False  # already has publisher DOI
    return True


def resolve_paper(paper: dict) -> dict:
    """Attempt to resolve a paper's DOI via DBLP then Crossref."""
    title = paper.get("title", "")
    if not title:
        return {**paper, "_resolution": "skipped", "_resolution_source": None}

    # Try DBLP first (fast, no auth)
    doi = resolve_via_dblp(title)
    if doi:
        return {
            **paper,
            "doi": doi,
            "_resolution": "resolved",
            "_resolution_source": "DBLP",
        }

    # Rate-limit between API calls
    time.sleep(0.5)

    # Fallback to Crossref
    doi = resolve_via_crossref(title)
    if doi:
        return {
            **paper,
            "doi": doi,
            "_resolution": "resolved",
            "_resolution_source": "Crossref",
        }

    # Could not resolve
    arxiv_id = paper.get("arxiv_id") or paper.get("arxivId")
    status = "preprint" if arxiv_id else "unresolved"
    return {**paper, "_resolution": status, "_resolution_source": None}


def load_papers(path: str | None) -> list[dict]:
    """Load papers from a file or stdin."""
    if path:
        with open(path) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "papers" in data:
        return data["papers"]
    raise ValueError("Input must be a JSON array or object with 'papers' key")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve arXiv papers to publisher DOIs"
    )
    parser.add_argument(
        "--input", "-i", default=None, help="Input JSON file (default: stdin)"
    )
    parser.add_argument(
        "--output", "-o", default=None, help="Output JSON file (default: stdout)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between papers in seconds (default: 1.0)",
    )
    args = parser.parse_args()

    papers = load_papers(args.input)
    results: list[dict] = []
    resolved_count = 0
    skipped_count = 0

    for i, paper in enumerate(papers):
        if not needs_resolution(paper):
            results.append(
                {**paper, "_resolution": "already_resolved", "_resolution_source": None}
            )
            skipped_count += 1
            continue

        result = resolve_paper(paper)
        results.append(result)
        if result["_resolution"] == "resolved":
            resolved_count += 1

        # Rate limiting between papers
        if i < len(papers) - 1:
            time.sleep(args.delay)

    output = {
        "papers": results,
        "summary": {
            "total": len(papers),
            "already_had_doi": skipped_count,
            "resolved": resolved_count,
            "unresolved": len(papers) - skipped_count - resolved_count,
        },
    }

    if args.output:
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
            f.write("\n")
    else:
        json.dump(output, sys.stdout, indent=2, ensure_ascii=False)
        print(file=sys.stdout)


if __name__ == "__main__":
    main()
