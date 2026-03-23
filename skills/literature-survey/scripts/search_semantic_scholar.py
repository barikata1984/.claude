#!/usr/bin/env python3
"""Search Semantic Scholar Academic Graph API for papers.

Returns structured JSON with title, authors, year, venue, citation count,
and external IDs (DOI, ArXiv). Handles rate limiting (1 req/sec, retry on 429).

Usage:
    python search_semantic_scholar.py --query "robot manipulation" --limit 20
    python search_semantic_scholar.py --query "reinforcement learning" --year-from 2022 --year-to 2025
    python search_semantic_scholar.py --query "sim-to-real transfer" --fields title,year,citationCount
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.semanticscholar.org/graph/v1/paper/search"
DEFAULT_FIELDS = "title,authors,year,venue,citationCount,externalIds,abstract"
MAX_RETRIES = 5
BACKOFF_BASE = 2  # seconds
BACKOFF_MAX = 60  # seconds


def search(
    query: str,
    *,
    year_from: int | None = None,
    year_to: int | None = None,
    limit: int = 20,
    fields: str = DEFAULT_FIELDS,
    offset: int = 0,
    api_key: str | None = None,
) -> dict:
    """Query the Semantic Scholar paper search endpoint."""
    params: dict[str, str | int] = {
        "query": query,
        "limit": min(limit, 100),  # API max is 100 per request
        "offset": offset,
        "fields": fields,
    }
    if year_from or year_to:
        year_range = f"{year_from or ''}-{year_to or ''}"
        params["year"] = year_range

    url = f"{API_BASE}?{urllib.parse.urlencode(params)}"
    headers = {"User-Agent": "literature-survey-skill/1.0"}
    if api_key:
        headers["x-api-key"] = api_key
    req = urllib.request.Request(url, headers=headers)

    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_RETRIES - 1:
                # Exponential backoff with jitter: 2s, 4s, 8s, 16s, ...
                delay = min(BACKOFF_BASE * (2**attempt) + random.uniform(0, 1), BACKOFF_MAX)
                print(
                    f"Rate limited (429), retry {attempt + 1}/{MAX_RETRIES - 1}"
                    f" in {delay:.1f}s...",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue
            raise SystemExit(f"HTTP {e.code}: {e.reason}") from e
        except urllib.error.URLError as e:
            raise SystemExit(f"Connection error: {e.reason}") from e

    raise SystemExit("Max retries exceeded")


def format_paper(paper: dict) -> dict:
    """Normalize a paper record for output."""
    ext_ids = paper.get("externalIds") or {}
    authors = paper.get("authors") or []
    return {
        "title": paper.get("title", ""),
        "authors": [a.get("name", "") for a in authors],
        "year": paper.get("year"),
        "venue": paper.get("venue", ""),
        "citationCount": paper.get("citationCount", 0),
        "doi": ext_ids.get("DOI"),
        "arxivId": ext_ids.get("ArXiv"),
        "semanticScholarId": paper.get("paperId"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Search Semantic Scholar for papers")
    parser.add_argument("--query", "-q", required=True, help="Search query string")
    parser.add_argument("--year-from", type=int, default=None, help="Start year (inclusive)")
    parser.add_argument("--year-to", type=int, default=None, help="End year (inclusive)")
    parser.add_argument("--limit", "-n", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument(
        "--fields", default=DEFAULT_FIELDS, help=f"Comma-separated fields (default: {DEFAULT_FIELDS})"
    )
    parser.add_argument("--offset", type=int, default=0, help="Pagination offset")
    parser.add_argument(
        "--api-key", default=None, help="API key (default: S2_API_KEY env var)"
    )
    parser.add_argument("--raw", action="store_true", help="Output raw API response")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("S2_API_KEY")

    result = search(
        args.query,
        year_from=args.year_from,
        year_to=args.year_to,
        limit=args.limit,
        fields=args.fields,
        offset=args.offset,
        api_key=api_key,
    )

    if args.raw:
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    else:
        papers = [format_paper(p) for p in result.get("data", [])]
        output = {
            "total": result.get("total", 0),
            "offset": result.get("offset", 0),
            "count": len(papers),
            "papers": papers,
        }
        json.dump(output, sys.stdout, indent=2, ensure_ascii=False)

    print(file=sys.stdout)  # trailing newline


if __name__ == "__main__":
    main()
