#!/usr/bin/env python3
"""Normalize Japanese typography in Markdown to a half-width-punctuation style.

Deterministic, mask-protected transforms ONLY. The rules here are the subset that
can be applied without lexical judgment; spacing rules (和欧 boundary, number+unit)
and em-dash removal are deliberately left to generation time (the prompt tier),
because they require knowledge a regex cannot recover safely
(e.g. Tシャツ / Jリーグ / 5GHz vs GPT4 / 図3).

Applied conversions (full-width source marks only; ASCII is never touched):
    。  -> ". "      、 -> ", "      ！ -> "! "     ？ -> "? "     ：  -> ": "
    「 」 -> " "       『 』 -> ' '      （ -> (        ） -> )

Preserved (never converted):   〜 (range)   ・ (nakaguro)   ；
Detected and warned (not auto-fixed):   — (em dash),   spaced en dash " – "

Protected (masked out, never modified):
    YAML/TOML front matter, fenced code blocks, inline code, math ($...$, $$...$$,
    \\(..\\), \\[..\\]), LaTeX environments/commands, Markdown link targets,
    autolinks, bare URLs.

Idempotent (full-width marks are consumed; ASCII is untouched) and fail-safe
(any exception => original text returned unchanged).
"""

from __future__ import annotations

import re
import sys

# Sentinel unlikely to occur in Markdown. {} holds the store index.
_PH = "\x00\x00JT{}\x00\x00"
_PH_RE = re.compile(r"\x00\x00JT(\d+)\x00\x00")

# Masking patterns, applied in this order. Block constructs first so their inner
# backticks/dollars are already hidden before inline patterns run.
_MASK_PATTERNS = [
    # YAML / TOML front matter, only at the very start of the file.
    re.compile(r"\A---\n.*?\n---\n", re.DOTALL),
    re.compile(r"\A\+\+\+\n.*?\n\+\+\+\n", re.DOTALL),
    # Fenced code blocks (``` or ~~~).
    re.compile(r"(?ms)^[ \t]*`{3,}[^\n]*\n.*?^[ \t]*`{3,}[ \t]*$"),
    re.compile(r"(?ms)^[ \t]*~{3,}[^\n]*\n.*?^[ \t]*~{3,}[ \t]*$"),
    # Inline code (run of N backticks ... matching run).
    re.compile(r"(`+)(.+?)\1"),
    # Display math.
    re.compile(r"\$\$.+?\$\$", re.DOTALL),
    re.compile(r"(?s)\\\[.*?\\\]"),
    # LaTeX environments and inline math / commands.
    re.compile(r"(?s)\\begin\{[^}]*\}.*?\\end\{[^}]*\}"),
    re.compile(r"\\\(.*?\\\)"),
    re.compile(r"\$(?!\$)[^\n$]+?\$"),
    re.compile(r"\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})*"),
    # Markdown link / image targets: keep the visible text convertible, hide URL.
    re.compile(r"(?<=\])\([^)\n]*\)"),
    # Autolinks and bare URLs. The bare-URL class is restricted to ASCII URL
    # characters so it stops at the first CJK char / full-width mark that
    # commonly follows a URL in Japanese without an intervening space.
    re.compile(r"<[A-Za-z][A-Za-z0-9+.\-]*:[^>\s]*>"),
    re.compile(r"(?:https?://|ftp://|www\.)[A-Za-z0-9\-._~:/?#@!$&'*+,;=%]+"),
]

# Full-width -> half-width + trailing space.
_PUNCT = {"。": ". ", "、": ", ", "！": "! ", "？": "? ", "：": ": "}
_PUNCT_RE = re.compile("[" + "".join(_PUNCT) + "]")

# Brackets / quotes (straight quotes are not directional, so open==close).
_BRACKETS = {"「": '"', "」": '"', "『": "'", "』": "'", "（": "(", "）": ")"}
_BRACKETS_RE = re.compile("[" + "".join(_BRACKETS) + "]")

# Surgical space cleanup, only right after a mark we just produced. The inserted
# space is dropped before a line end, the file end, or a closing delimiter.
_DOUBLE_SP = re.compile(r"([.,!?:]) {2,}")
_TRAIL_SP = re.compile(r"([.,!?:]) +(?=[)\]\"'）】」』\n]|$)")


class _Masker:
    def __init__(self) -> None:
        self.store: list[str] = []

    def mask(self, text: str) -> str:
        for pat in _MASK_PATTERNS:
            text = pat.sub(self._stash, text)
        return text

    def _stash(self, m: "re.Match[str]") -> str:
        idx = len(self.store)
        self.store.append(m.group(0))
        return _PH.format(idx)

    def unmask(self, text: str) -> str:
        # Repeat until stable in case a stored span contained a sentinel-like run
        # (it never should, but this keeps restoration total and safe).
        def repl(m: "re.Match[str]") -> str:
            return self.store[int(m.group(1))]

        prev = None
        while prev != text and _PH_RE.search(text):
            prev = text
            text = _PH_RE.sub(repl, text)
        return text


def _convert(text: str) -> str:
    text = _PUNCT_RE.sub(lambda m: _PUNCT[m.group(0)], text)
    text = _BRACKETS_RE.sub(lambda m: _BRACKETS[m.group(0)], text)
    text = _DOUBLE_SP.sub(r"\1 ", text)
    text = _TRAIL_SP.sub(r"\1", text)
    return text


def warnings(text: str) -> list[str]:
    """Return human-readable warnings for marks that need manual judgment."""
    out: list[str] = []
    masker = _Masker()
    visible = masker.mask(text)
    if "—" in visible:
        out.append(f"em dash (—) x{visible.count('—')}: replace with (), comma, or colon")
    if " – " in visible:
        out.append(f"spaced en dash ( – ) x{visible.count(' – ')}: parenthetical use is banned")
    return out


def normalize(text: str) -> str:
    """Return text with deterministic typography conversions applied.

    Fail-safe: on any error the original text is returned unchanged.
    """
    try:
        masker = _Masker()
        masked = masker.mask(text)
        converted = _convert(masked)
        return masker.unmask(converted)
    except Exception:  # never corrupt a file on a parser/regex edge case
        return text


def _main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: format_ja_typography.py <file.md>", file=sys.stderr)
        return 0  # never block the caller
    path = argv[1]
    try:
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
    except (OSError, UnicodeDecodeError):
        return 0
    for w in warnings(original):
        print(f"[ja-typography] {path}: {w}", file=sys.stderr)
    new = normalize(original)
    if new != original:
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)
        except OSError:
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
