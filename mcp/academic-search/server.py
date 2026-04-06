# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp[cli]>=1.0", "httpx>=0.27"]
# ///
"""MCP server for academic paper search and open-access URL resolution.

Provides two tools:
  - search_semantic_scholar: Search the Semantic Scholar Academic Graph API
  - resolve_oa_url: Resolve a paper identifier to the best open-access URL
    via Unpaywall, S2 openAccessPdf, and arXiv PDF fallback

API keys are injected by start.sh (via pass) and never exposed to the agent.
"""
from __future__ import annotations

import asyncio
import json
import os
import random
import time
import urllib.parse

import httpx
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Configuration (read at module load time — before agent has access)
# ---------------------------------------------------------------------------

S2_API_KEY: str | None = os.environ.get("S2_API_KEY") or None
UNPAYWALL_EMAIL: str | None = os.environ.get("UNPAYWALL_EMAIL") or None

S2_BASE = "https://api.semanticscholar.org/graph/v1"
UNPAYWALL_BASE = "https://api.unpaywall.org/v2"

S2_DEFAULT_FIELDS = (
    "title,authors,year,venue,citationCount,externalIds,abstract,openAccessPdf"
)

# Rate limiting
S2_INTERVAL = 1.0 if S2_API_KEY else 3.0  # seconds between S2 requests
MAX_RETRIES = 5
BACKOFF_BASE = 2  # seconds
BACKOFF_MAX = 60  # seconds
REQUEST_TIMEOUT = 30.0

USER_AGENT = "academic-search-mcp/1.0"

# ---------------------------------------------------------------------------
# Rate limiter (stateful — persists across tool calls within a session)
# ---------------------------------------------------------------------------

_last_s2_request_time: float = 0.0
_s2_rate_lock = asyncio.Lock()


async def _s2_rate_limit() -> None:
    """Enforce minimum interval between Semantic Scholar API requests."""
    global _last_s2_request_time
    async with _s2_rate_lock:
        now = time.monotonic()
        elapsed = now - _last_s2_request_time
        if elapsed < S2_INTERVAL:
            await asyncio.sleep(S2_INTERVAL - elapsed)
        _last_s2_request_time = time.monotonic()


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def _s2_headers() -> dict[str, str]:
    headers = {"User-Agent": USER_AGENT}
    if S2_API_KEY:
        headers["x-api-key"] = S2_API_KEY
    return headers


async def _s2_request(client: httpx.AsyncClient, url: str) -> dict:
    """Rate-limited S2 API request with exponential backoff on 429."""
    for attempt in range(MAX_RETRIES):
        await _s2_rate_limit()
        resp = await client.get(url, headers=_s2_headers(), timeout=REQUEST_TIMEOUT)
        if resp.status_code == 429 and attempt < MAX_RETRIES - 1:
            delay = min(BACKOFF_BASE * (2**attempt) + random.uniform(0, 1), BACKOFF_MAX)
            await asyncio.sleep(delay)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("Max retries exceeded for Semantic Scholar API")


def _format_paper(paper: dict) -> dict:
    """Normalize an S2 paper record for output."""
    ext_ids = paper.get("externalIds") or {}
    authors = paper.get("authors") or []
    oa_pdf = paper.get("openAccessPdf")
    return {
        "title": paper.get("title", ""),
        "authors": [a.get("name", "") for a in authors],
        "year": paper.get("year"),
        "venue": paper.get("venue", ""),
        "citationCount": paper.get("citationCount", 0),
        "doi": ext_ids.get("DOI"),
        "arxivId": ext_ids.get("ArXiv"),
        "semanticScholarId": paper.get("paperId"),
        "abstract": paper.get("abstract"),
        "openAccessPdf": {"url": oa_pdf["url"], "status": oa_pdf.get("status")}
        if oa_pdf
        else None,
    }


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP("academic-search")


@mcp.tool()
async def search_semantic_scholar(
    query: str,
    year_from: int | None = None,
    year_to: int | None = None,
    limit: int = 20,
    offset: int = 0,
    fields: str | None = None,
) -> str:
    """Search the Semantic Scholar Academic Graph API for papers.

    Args:
        query: Search query string (e.g., "robot manipulation reinforcement learning")
        year_from: Start year filter (inclusive). Optional.
        year_to: End year filter (inclusive). Optional.
        limit: Maximum number of results (default 20, max 100).
        offset: Pagination offset.
        fields: Comma-separated S2 fields. Defaults include openAccessPdf.

    Returns:
        JSON with total count and paper list (title, authors, year, venue,
        citationCount, doi, arxivId, abstract, openAccessPdf).
    """
    params: dict[str, str | int] = {
        "query": query,
        "limit": min(limit, 100),
        "offset": offset,
        "fields": fields or S2_DEFAULT_FIELDS,
    }
    if year_from or year_to:
        params["year"] = f"{year_from or ''}-{year_to or ''}"

    url = f"{S2_BASE}/paper/search?{urllib.parse.urlencode(params)}"

    async with httpx.AsyncClient() as client:
        data = await _s2_request(client, url)

    papers = [_format_paper(p) for p in data.get("data", [])]
    result = {
        "total": data.get("total", 0),
        "offset": data.get("offset", 0),
        "count": len(papers),
        "papers": papers,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def resolve_oa_url(
    doi: str | None = None,
    s2_paper_id: str | None = None,
    arxiv_id: str | None = None,
) -> str:
    """Resolve a paper identifier to the best open-access full-text URL.

    Tries multiple sources in cascade: Unpaywall → S2 openAccessPdf → arXiv PDF.
    At least one identifier must be provided.

    Args:
        doi: Paper DOI (e.g., "10.1109/ICRA.2024.1234567").
        s2_paper_id: Semantic Scholar paper ID.
        arxiv_id: arXiv paper ID (e.g., "2401.12345").

    Returns:
        JSON with resolved URLs from each source and a best_url recommendation.
    """
    if not doi and not s2_paper_id and not arxiv_id:
        return json.dumps({"error": "At least one of doi, s2_paper_id, or arxiv_id is required."})

    result: dict = {
        "doi": doi,
        "arxiv_id": arxiv_id,
        "unpaywall": None,
        "s2_open_access_pdf": None,
        "arxiv_pdf": None,
        "best_url": None,
    }

    # --- 1. Unpaywall (DOI required, email required) ---
    if doi and UNPAYWALL_EMAIL:
        try:
            encoded_doi = urllib.parse.quote(doi, safe="")
            uw_url = f"{UNPAYWALL_BASE}/{encoded_doi}?email={urllib.parse.quote(UNPAYWALL_EMAIL)}"
            async with httpx.AsyncClient() as client:
                resp = await client.get(uw_url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                uw_data = resp.json()
                best_loc = uw_data.get("best_oa_location")
                if best_loc:
                    result["unpaywall"] = {
                        "url": best_loc.get("url"),
                        "pdf_url": best_loc.get("url_for_pdf"),
                        "host_type": best_loc.get("host_type"),
                        "version": best_loc.get("version"),
                        "oa_status": uw_data.get("oa_status"),
                    }
        except httpx.HTTPError:
            pass  # Unpaywall failure is non-fatal

    # --- 2. S2 openAccessPdf (via paper detail endpoint) ---
    s2_lookup_id = None
    if s2_paper_id:
        s2_lookup_id = s2_paper_id
    elif arxiv_id:
        s2_lookup_id = f"ArXiv:{arxiv_id}"
    elif doi:
        s2_lookup_id = f"DOI:{doi}"

    if s2_lookup_id:
        try:
            s2_url = f"{S2_BASE}/paper/{urllib.parse.quote(s2_lookup_id, safe=':')}?fields=openAccessPdf,externalIds"
            async with httpx.AsyncClient() as client:
                s2_data = await _s2_request(client, s2_url)
            oa_pdf = s2_data.get("openAccessPdf")
            if oa_pdf:
                result["s2_open_access_pdf"] = {
                    "url": oa_pdf.get("url"),
                    "status": oa_pdf.get("status"),
                }
            # Fill in arxiv_id if we didn't have it
            if not arxiv_id:
                ext_ids = s2_data.get("externalIds") or {}
                arxiv_id = ext_ids.get("ArXiv")
                result["arxiv_id"] = arxiv_id
        except (httpx.HTTPError, RuntimeError):
            pass  # S2 failure is non-fatal

    # --- 3. arXiv PDF fallback ---
    if arxiv_id:
        result["arxiv_pdf"] = f"https://arxiv.org/pdf/{arxiv_id}"

    # --- Determine best_url ---
    uw = result.get("unpaywall")
    s2_oa = result.get("s2_open_access_pdf")
    if uw and (uw.get("pdf_url") or uw.get("url")):
        result["best_url"] = uw.get("pdf_url") or uw.get("url")
    elif s2_oa and s2_oa.get("url"):
        result["best_url"] = s2_oa["url"]
    elif result.get("arxiv_pdf"):
        result["best_url"] = result["arxiv_pdf"]

    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
