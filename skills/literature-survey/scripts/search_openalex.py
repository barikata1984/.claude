#!/usr/bin/env python3
"""Search OpenAlex API for academic papers.

Returns structured JSON with title, authors, year, venue, citation count, and DOI.
Uses the polite pool (faster rate limits) when --mailto is provided.

Usage:
    python search_openalex.py --query "robot manipulation" --limit 20
    python search_openalex.py --query "reinforcement learning" --year-from 2022 --sort cited_by_count:desc
    python search_openalex.py --query "sim-to-real" --mailto user@example.com
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.openalex.org/works"


def search(
    query: str,
    *,
    year_from: int | None = None,
    year_to: int | None = None,
    limit: int = 20,
    sort: str = "relevance_score:desc",
    mailto: str | None = None,
    page: int = 1,
) -> dict:
    """Query the OpenAlex works endpoint."""
    params: dict[str, str | int] = {
        "search": query,
        "per_page": min(limit, 200),  # API max is 200
        "page": page,
        "sort": sort,
    }

    # Build filter string
    filters: list[str] = []
    if year_from and year_to:
        filters.append(f"publication_year:{year_from}-{year_to}")
    elif year_from:
        filters.append(f"publication_year:{year_from}-")
    elif year_to:
        filters.append(f"publication_year:-{year_to}")
    if filters:
        params["filter"] = ",".join(filters)

    if mailto:
        params["mailto"] = mailto

    url = f"{API_BASE}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "literature-survey-skill/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.reason}") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"Connection error: {e.reason}") from e


def format_paper(work: dict) -> dict:
    """Normalize an OpenAlex work record for output."""
    authorships = work.get("authorships") or []
    authors = []
    for a in authorships:
        author_info = a.get("author") or {}
        name = author_info.get("display_name", "")
        if name:
            authors.append(name)

    # Extract venue from primary_location or host_venue
    venue = ""
    primary_loc = work.get("primary_location") or {}
    source = primary_loc.get("source") or {}
    venue = source.get("display_name", "")

    # Extract DOI (strip https://doi.org/ prefix)
    doi_url = work.get("doi") or ""
    doi = doi_url.replace("https://doi.org/", "") if doi_url else None

    # Extract arXiv ID from locations
    arxiv_id = None
    for loc in work.get("locations") or []:
        loc_source = loc.get("source") or {}
        if loc_source.get("display_name") == "arXiv":
            landing_url = loc.get("landing_page_url") or ""
            if "arxiv.org/abs/" in landing_url:
                arxiv_id = landing_url.split("arxiv.org/abs/")[-1]
                break

    return {
        "title": work.get("display_name", ""),
        "authors": authors,
        "year": work.get("publication_year"),
        "venue": venue,
        "citedByCount": work.get("cited_by_count", 0),
        "doi": doi,
        "arxivId": arxiv_id,
        "openAlexId": work.get("id", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Search OpenAlex for papers")
    parser.add_argument("--query", "-q", required=True, help="Search query string")
    parser.add_argument("--year-from", type=int, default=None, help="Start year (inclusive)")
    parser.add_argument("--year-to", type=int, default=None, help="End year (inclusive)")
    parser.add_argument("--limit", "-n", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument(
        "--sort",
        default="relevance_score:desc",
        help="Sort order (default: relevance_score:desc). Options: cited_by_count:desc, publication_date:desc",
    )
    parser.add_argument(
        "--mailto", default=None, help="Email for polite pool (faster rate limits)"
    )
    parser.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    parser.add_argument("--raw", action="store_true", help="Output raw API response")
    args = parser.parse_args()

    result = search(
        args.query,
        year_from=args.year_from,
        year_to=args.year_to,
        limit=args.limit,
        sort=args.sort,
        mailto=args.mailto,
        page=args.page,
    )

    if args.raw:
        json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    else:
        papers = [format_paper(w) for w in result.get("results", [])]
        output = {
            "total": result.get("meta", {}).get("count", 0),
            "page": result.get("meta", {}).get("page", 1),
            "count": len(papers),
            "papers": papers,
        }
        json.dump(output, sys.stdout, indent=2, ensure_ascii=False)

    print(file=sys.stdout)  # trailing newline


if __name__ == "__main__":
    main()
