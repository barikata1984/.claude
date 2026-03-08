# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp[cli]>=1.0", "httpx>=0.27", "beautifulsoup4>=4.12", "lxml>=5.0"]
# ///
"""MCP server for authenticated academic paper fetching.

Uses browser cookies exported via Cookie-Editor to access paywalled papers
through institutional authentication (Shibboleth/SAML).
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup, Tag
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

COOKIE_FILE = Path(os.environ.get("ACADEMIC_COOKIE_FILE", "~/.academic_cookies.json")).expanduser()
MIN_REQUEST_INTERVAL = 3.0  # seconds between requests
REQUEST_TIMEOUT = 30.0
MAX_OUTPUT_CHARS = 50_000
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

# Headings that indicate Limitations / Future Work sections
FOCUS_HEADINGS = re.compile(
    r"limitation|future\s*work|discussion|conclusion|concluding", re.IGNORECASE
)

# Shibboleth / SAML login page indicators
SHIBBOLETH_INDICATORS = re.compile(
    r"shibboleth|saml|idp.*login|wayf|discovery.*service|"
    r"institutionalsignin|federation.*login",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------

_last_request_time: float = 0.0
_rate_lock = asyncio.Lock()


async def _rate_limit() -> None:
    global _last_request_time
    async with _rate_lock:
        now = time.monotonic()
        elapsed = now - _last_request_time
        if elapsed < MIN_REQUEST_INTERVAL:
            await asyncio.sleep(MIN_REQUEST_INTERVAL - elapsed)
        _last_request_time = time.monotonic()


# ---------------------------------------------------------------------------
# Cookie loading
# ---------------------------------------------------------------------------


def _load_cookies(url: str) -> dict[str, str]:
    """Load cookies from Cookie-Editor JSON export, filtered by domain."""
    if not COOKIE_FILE.exists():
        raise FileNotFoundError(
            f"Cookie file not found: {COOKIE_FILE}\n"
            "Please export cookies from your browser using the Cookie-Editor extension\n"
            f"and save them to {COOKIE_FILE}"
        )

    raw = json.loads(COOKIE_FILE.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError(
            f"Expected a JSON array in {COOKIE_FILE} (Cookie-Editor export format)"
        )

    target_domain = urlparse(url).hostname or ""
    cookies: dict[str, str] = {}
    for entry in raw:
        cookie_domain = entry.get("domain", "").lstrip(".")
        # Match if the request domain ends with the cookie domain
        if target_domain == cookie_domain or target_domain.endswith(f".{cookie_domain}"):
            cookies[entry["name"]] = entry["value"]
    return cookies


# ---------------------------------------------------------------------------
# Session expiry detection
# ---------------------------------------------------------------------------


def _check_session_expired(response: httpx.Response) -> None:
    """Raise an error if the response indicates a Shibboleth/SAML redirect."""
    # Check redirect chain
    for r in response.history:
        if SHIBBOLETH_INDICATORS.search(str(r.url)):
            raise RuntimeError(
                "Session expired: redirected to institutional login page.\n"
                "Please log in again via your browser and re-export cookies to "
                f"{COOKIE_FILE}"
            )

    # Check final URL
    if SHIBBOLETH_INDICATORS.search(str(response.url)):
        raise RuntimeError(
            "Session expired: landed on institutional login page.\n"
            "Please log in again via your browser and re-export cookies to "
            f"{COOKIE_FILE}"
        )

    # Check response body for login form indicators
    if response.status_code == 200:
        body_start = response.text[:5000]
        if re.search(r'<form[^>]*action="[^"]*shibboleth', body_start, re.IGNORECASE):
            raise RuntimeError(
                "Session expired: response contains Shibboleth login form.\n"
                "Please log in again via your browser and re-export cookies to "
                f"{COOKIE_FILE}"
            )


# ---------------------------------------------------------------------------
# Publisher-specific parsers
# ---------------------------------------------------------------------------

# Each parser returns (full_text, focused_sections) where focused_sections
# contains Limitations/Future Work content if found.


def _extract_focused_sections(soup: BeautifulSoup) -> str:
    """Extract sections with headings matching FOCUS_HEADINGS."""
    sections: list[str] = []
    for heading in soup.find_all(re.compile(r"^h[1-6]$")):
        if FOCUS_HEADINGS.search(heading.get_text()):
            parts = [heading.get_text(strip=True)]
            for sibling in heading.find_next_siblings():
                if isinstance(sibling, Tag) and sibling.name and re.match(r"^h[1-6]$", sibling.name):
                    break
                text = sibling.get_text(strip=True)
                if text:
                    parts.append(text)
            sections.append("\n".join(parts))
    return "\n\n---\n\n".join(sections)


def _parse_ieee(soup: BeautifulSoup) -> str:
    """Parse IEEE Xplore article page."""
    # Abstract
    abstract = ""
    abstract_div = soup.find("div", class_=re.compile(r"abstract"))
    if abstract_div:
        abstract = f"## Abstract\n\n{abstract_div.get_text(strip=True)}"

    # Full text sections
    body = soup.find("div", class_=re.compile(r"document-main-content|article-content"))
    if body:
        return f"{abstract}\n\n{body.get_text(separator='\n', strip=True)}"

    # Fallback: all section elements
    sections = soup.find_all("section")
    if sections:
        text = "\n\n".join(s.get_text(separator="\n", strip=True) for s in sections)
        return f"{abstract}\n\n{text}"

    return abstract or soup.get_text(separator="\n", strip=True)


def _parse_elsevier(soup: BeautifulSoup) -> str:
    """Parse Elsevier / ScienceDirect article page."""
    body = soup.find("div", id="body") or soup.find("div", class_=re.compile(r"Body"))
    if body:
        return body.get_text(separator="\n", strip=True)

    article = soup.find("article")
    if article:
        return article.get_text(separator="\n", strip=True)

    return soup.get_text(separator="\n", strip=True)


def _parse_springer(soup: BeautifulSoup) -> str:
    """Parse Springer article page."""
    body = (
        soup.find("div", class_=re.compile(r"c-article-body"))
        or soup.find("div", id="body")
        or soup.find("article")
    )
    if body:
        return body.get_text(separator="\n", strip=True)
    return soup.get_text(separator="\n", strip=True)


def _parse_acm(soup: BeautifulSoup) -> str:
    """Parse ACM Digital Library article page."""
    body = (
        soup.find("div", class_=re.compile(r"article__body"))
        or soup.find("div", class_=re.compile(r"hlFld-Fulltext"))
        or soup.find("article")
    )
    if body:
        return body.get_text(separator="\n", strip=True)
    return soup.get_text(separator="\n", strip=True)


def _parse_fallback(soup: BeautifulSoup) -> str:
    """Generic parser: extract text from the largest content div."""
    # Remove nav, header, footer, script, style
    for tag_name in ("nav", "header", "footer", "script", "style", "noscript"):
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Find largest div by text length
    best: Tag | None = None
    best_len = 0
    for div in soup.find_all("div"):
        text_len = len(div.get_text())
        if text_len > best_len:
            best_len = text_len
            best = div

    if best:
        return best.get_text(separator="\n", strip=True)
    return soup.get_text(separator="\n", strip=True)


# Publisher detection: (url_pattern, parser_function)
_PUBLISHERS: list[tuple[re.Pattern[str], callable]] = [
    (re.compile(r"ieeexplore\.ieee\.org"), _parse_ieee),
    (re.compile(r"sciencedirect\.com|elsevier\.com"), _parse_elsevier),
    (re.compile(r"link\.springer\.com"), _parse_springer),
    (re.compile(r"dl\.acm\.org"), _parse_acm),
]


def _select_parser(url: str) -> callable:
    for pattern, parser in _PUBLISHERS:
        if pattern.search(url):
            return parser
    return _parse_fallback


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP("academic-fetch")


@mcp.tool()
async def fetch_with_auth(url: str) -> str:
    """Fetch an academic paper page using institutional authentication cookies.

    Uses cookies exported from the browser via Cookie-Editor extension to access
    paywalled content. Extracts article text with a focus on Limitations and
    Future Work sections.

    Args:
        url: Full URL to an academic paper page (IEEE, Elsevier, Springer, ACM, etc.)

    Returns:
        Extracted article text. Limitations/Future Work sections are shown first
        when available.
    """
    # Load domain-filtered cookies
    try:
        cookies = _load_cookies(url)
    except (FileNotFoundError, ValueError) as e:
        return f"Error: {e}"

    if not cookies:
        return (
            f"No cookies found for domain of {url}.\n"
            "Make sure you exported cookies while logged in to this publisher."
        )

    # Rate limit
    await _rate_limit()

    # Fetch
    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=REQUEST_TIMEOUT,
        headers={"User-Agent": USER_AGENT},
    ) as client:
        try:
            response = await client.get(url, cookies=cookies)
        except httpx.HTTPError as e:
            return f"HTTP error fetching {url}: {e}"

    # Check session expiry
    try:
        _check_session_expired(response)
    except RuntimeError as e:
        return str(e)

    if response.status_code != 200:
        return f"HTTP {response.status_code} for {url}"

    # Parse
    soup = BeautifulSoup(response.text, "lxml")
    parser = _select_parser(url)
    full_text = parser(soup)

    # Extract focused sections
    focused = _extract_focused_sections(soup)

    # Build output
    parts: list[str] = []
    if focused:
        parts.append("## Limitations / Future Work (extracted)\n")
        parts.append(focused)
        parts.append("\n\n---\n\n## Full Article Text\n")

    parts.append(full_text)

    output = "\n".join(parts)

    # Truncate if needed
    if len(output) > MAX_OUTPUT_CHARS:
        output = output[:MAX_OUTPUT_CHARS] + f"\n\n[Truncated at {MAX_OUTPUT_CHARS} characters]"

    return output


if __name__ == "__main__":
    mcp.run(transport="stdio")
