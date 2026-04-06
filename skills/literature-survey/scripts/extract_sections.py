#!/usr/bin/env python3
"""Extract key sections from ar5iv HTML papers.

Fetches ar5iv HTML and extracts Abstract, Introduction, Conclusion,
Limitations, Future Work, table contents (as Markdown), and figure captions.
Uses stdlib only (no pip deps).

Input JSON format (array of objects):
    [{"arxiv_id": "2309.10312", "title": "..."}, ...]

Output JSON format:
    {
        "papers": [
            {
                "arxiv_id": "2309.10312",
                "title": "...",
                "status": "ok",
                "sections": {
                    "abstract": "...",
                    "introduction": "...",
                    "conclusion": "...",
                    "limitations": "...",
                    "future_work": "..."
                },
                "tables": [{"caption": "...", "content": "..."}],
                "figure_captions": ["Figure 1: ...", ...]
            }
        ],
        "summary": {"total": N, "ok": N, "failed": N}
    }

Usage:
    python3 extract_sections.py --input papers.json --output extracted.json
    python3 extract_sections.py --input papers.json  # stdout
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser

AR5IV_BASE = "https://ar5iv.labs.arxiv.org/html"
USER_AGENT = "literature-survey-skill/1.0"

# Section heading patterns (case-insensitive)
TARGET_SECTIONS: dict[str, list[str]] = {
    "introduction": [r"^introduction$"],
    "conclusion": [r"^conclusions?$", r"^concluding\s+remarks$", r"^summary$"],
    "limitations": [
        r"^limitations?$",
        r"^limitations?\s+and\s+future\s+work$",
        r"^limitations?\s+and\s+discussion$",
    ],
    "future_work": [
        r"^future\s+work$",
        r"^future\s+directions?$",
        r"^future\s+work\s+and\s+limitations?$",
    ],
}

# Sections to stop collecting at (avoid collecting References, Appendix, etc.)
STOP_SECTIONS: list[str] = [
    r"^references?$",
    r"^bibliography$",
    r"^acknowledg",
    r"^supplementary",
    r"^appendi",
]


def _strip_tags(html_text: str) -> str:
    """Remove HTML tags and normalize whitespace."""
    text = re.sub(r"<[^>]+>", " ", html_text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&#\d+;", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _match_heading(text: str, patterns: list[str]) -> bool:
    """Check if heading text matches any pattern."""
    clean = text.strip().lower()
    # Remove leading section numbers like "6" or "6."
    clean = re.sub(r"^\d+\.?\s*", "", clean)
    return any(re.match(p, clean, re.IGNORECASE) for p in patterns)


def _is_stop_section(text: str) -> bool:
    """Check if heading indicates we should stop collecting."""
    clean = text.strip().lower()
    clean = re.sub(r"^\d+\.?\s*", "", clean)
    return any(re.match(p, clean, re.IGNORECASE) for p in STOP_SECTIONS)


class _TableParser(HTMLParser):
    """Extract table content as Markdown."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self.current_row: list[str] = []
        self.current_cell: list[str] = []
        self.in_cell = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self.current_row = []
        elif tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = []

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.current_cell.append(data.strip())

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th"):
            self.in_cell = False
            self.current_row.append(" ".join(self.current_cell))
        elif tag == "tr":
            if self.current_row:
                self.rows.append(self.current_row)

    def to_markdown(self) -> str:
        if not self.rows:
            return ""
        # Determine column count
        max_cols = max(len(r) for r in self.rows)
        lines: list[str] = []
        for i, row in enumerate(self.rows):
            # Pad row to max_cols
            padded = row + [""] * (max_cols - len(row))
            lines.append("| " + " | ".join(padded) + " |")
            if i == 0:
                lines.append("| " + " | ".join(["---"] * max_cols) + " |")
        return "\n".join(lines)


def _table_to_markdown(table_html: str) -> str:
    """Convert an HTML table to Markdown."""
    parser = _TableParser()
    parser.feed(table_html)
    return parser.to_markdown()


def _extract_abstract(html: str) -> str:
    """Extract abstract from ltx_abstract div."""
    match = re.search(
        r'<div[^>]*class="ltx_abstract"[^>]*>(.*?)</div>',
        html,
        re.DOTALL,
    )
    if not match:
        return ""
    content = match.group(1)
    # Remove the title tag
    content = re.sub(r"<h\d[^>]*>.*?</h\d>", "", content, flags=re.DOTALL)
    return _strip_tags(content)


def _detect_section_tag(html: str) -> str:
    """Detect which heading level is used for top-level sections.

    ar5iv uses <h2> in some papers and <h3> in others. We detect the
    level by checking which tag contains known section names like
    'Introduction' or 'Conclusion'.
    """
    for tag in ("h2", "h3"):
        headings = re.findall(f"<{tag}[^>]*>(.*?)</{tag}>", html, re.DOTALL)
        for h in headings:
            text = _strip_tags(h).lower()
            text = re.sub(r"^\d+\.?\s*", "", text)
            if text in ("introduction", "conclusion", "related work", "method"):
                return tag
    return "h2"  # default fallback


def _extract_sections(html: str) -> dict[str, str]:
    """Extract target sections by splitting on section-level headings."""
    sections: dict[str, str] = {}

    tag = _detect_section_tag(html)

    # Split HTML by the detected heading tag
    parts = re.split(rf"(<{tag}[^>]*>.*?</{tag}>)", html, flags=re.DOTALL)

    current_key: str | None = None
    current_content: list[str] = []

    for part in parts:
        heading_match = re.match(rf"<{tag}[^>]*>(.*?)</{tag}>", part, re.DOTALL)
        if heading_match:
            # Save previous section if it was a target
            if current_key and current_content:
                sections[current_key] = _strip_tags("".join(current_content))

            heading_text = _strip_tags(heading_match.group(1))
            current_key = None
            current_content = []

            # Check if this heading matches a target section
            if _is_stop_section(heading_text):
                current_key = None
                continue

            for key, patterns in TARGET_SECTIONS.items():
                if key not in sections and _match_heading(heading_text, patterns):
                    current_key = key
                    break
        elif current_key is not None:
            current_content.append(part)

    # Don't forget the last section
    if current_key and current_content:
        sections[current_key] = _strip_tags("".join(current_content))

    return sections


def _extract_tables(html: str) -> list[dict[str, str]]:
    """Extract tables with their captions."""
    tables: list[dict[str, str]] = []

    # Find all <figure> blocks containing <table>
    figure_pattern = re.compile(
        r"<figure[^>]*>(.*?)</figure>",
        re.DOTALL,
    )
    for fig_match in figure_pattern.finditer(html):
        fig_content = fig_match.group(1)
        if "<table" not in fig_content:
            continue

        # Extract caption
        cap_match = re.search(
            r"<figcaption[^>]*>(.*?)</figcaption>",
            fig_content,
            re.DOTALL,
        )
        caption = _strip_tags(cap_match.group(1)) if cap_match else ""

        # Extract table
        table_match = re.search(r"(<table[^>]*>.*?</table>)", fig_content, re.DOTALL)
        if table_match:
            md = _table_to_markdown(table_match.group(1))
            if md:
                tables.append({"caption": caption, "content": md})

    return tables


def _extract_figure_captions(html: str) -> list[str]:
    """Extract figure captions (excluding tables)."""
    captions: list[str] = []

    figure_pattern = re.compile(
        r"<figure[^>]*>(.*?)</figure>",
        re.DOTALL,
    )
    for fig_match in figure_pattern.finditer(html):
        fig_content = fig_match.group(1)
        # Skip figures that contain tables (those are handled separately)
        if "<table" in fig_content:
            continue

        cap_match = re.search(
            r"<figcaption[^>]*>(.*?)</figcaption>",
            fig_content,
            re.DOTALL,
        )
        if cap_match:
            caption = _strip_tags(cap_match.group(1))
            if caption:
                captions.append(caption)

    return captions


def fetch_and_extract(arxiv_id: str) -> dict:
    """Fetch ar5iv HTML and extract all sections."""
    url = f"{AR5IV_BASE}/{arxiv_id}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
        return {"status": "error", "error": str(e)}

    abstract = _extract_abstract(html)
    sections = _extract_sections(html)
    tables = _extract_tables(html)
    figure_captions = _extract_figure_captions(html)

    all_sections = {"abstract": abstract, **sections}

    return {
        "status": "ok",
        "sections": all_sections,
        "tables": tables,
        "figure_captions": figure_captions,
    }


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
        description="Extract key sections from ar5iv papers"
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
        help="Delay between fetches in seconds (default: 1.0)",
    )
    args = parser.parse_args()

    papers = load_papers(args.input)
    results: list[dict] = []
    ok_count = 0
    fail_count = 0

    for i, paper in enumerate(papers):
        arxiv_id = paper.get("arxiv_id") or paper.get("arxivId")
        title = paper.get("title", "")

        if not arxiv_id:
            results.append({**paper, "status": "skipped", "error": "no arxiv_id"})
            fail_count += 1
            continue

        # Normalize arxiv_id (strip URL prefixes)
        arxiv_id = (
            arxiv_id.replace("https://arxiv.org/abs/", "")
            .replace("http://arxiv.org/abs/", "")
            .strip()
        )

        extraction = fetch_and_extract(arxiv_id)
        result = {
            "arxiv_id": arxiv_id,
            "title": title,
            **extraction,
        }
        results.append(result)

        if extraction["status"] == "ok":
            ok_count += 1
        else:
            fail_count += 1

        # Rate limiting
        if i < len(papers) - 1:
            time.sleep(args.delay)

    output = {
        "papers": results,
        "summary": {"total": len(papers), "ok": ok_count, "failed": fail_count},
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
