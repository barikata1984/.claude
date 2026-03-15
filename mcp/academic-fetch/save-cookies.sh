#!/usr/bin/env bash
# save-cookies.sh — Merge Cookie-Editor clipboard export into ~/.academic_cookies.json
#
# Usage:
#   1. Export cookies from Cookie-Editor (JSON → clipboard)
#   2. Run: bash .claude/mcp/academic-fetch/save-cookies.sh
#
# The script reads JSON from the clipboard, merges with existing cookies
# (deduplicating by domain+name+path), and saves to the cookie file.

set -euo pipefail

COOKIE_FILE="${ACADEMIC_COOKIE_FILE:-$HOME/.academic_cookies.json}"

# ---------------------------------------------------------------------------
# Read clipboard
# ---------------------------------------------------------------------------
if command -v xclip &>/dev/null; then
    clip="$(xclip -selection clipboard -o 2>/dev/null)" || clip=""
elif command -v xsel &>/dev/null; then
    clip="$(xsel --clipboard --output 2>/dev/null)" || clip=""
elif command -v wl-paste &>/dev/null; then
    clip="$(wl-paste 2>/dev/null)" || clip=""
elif command -v pbpaste &>/dev/null; then
    clip="$(pbpaste 2>/dev/null)" || clip=""
elif command -v powershell.exe &>/dev/null; then
    clip="$(powershell.exe -Command Get-Clipboard 2>/dev/null)" || clip=""
else
    echo "Error: No clipboard tool found (xclip, xsel, wl-paste, pbpaste)." >&2
    exit 1
fi

if [[ -z "$clip" ]]; then
    echo "Error: Clipboard is empty." >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Validate clipboard JSON
# ---------------------------------------------------------------------------
if ! echo "$clip" | python3 -c "import sys,json; d=json.load(sys.stdin); assert isinstance(d,list)" 2>/dev/null; then
    echo "Error: Clipboard does not contain a valid JSON array." >&2
    echo "Make sure you exported cookies via Cookie-Editor → Export → JSON." >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Merge and save
# ---------------------------------------------------------------------------
python3 -c "
import json, sys, os

cookie_file = os.path.expanduser('${COOKIE_FILE}')
new_cookies = json.loads(sys.stdin.read())

# Load existing cookies
existing = []
if os.path.exists(cookie_file):
    with open(cookie_file, 'r') as f:
        try:
            existing = json.load(f)
            if not isinstance(existing, list):
                existing = []
        except json.JSONDecodeError:
            existing = []

# Deduplicate: (domain, name, path) as key — new cookies take precedence
def cookie_key(c):
    return (c.get('domain', ''), c.get('name', ''), c.get('path', '/'))

merged = {}
for c in existing:
    merged[cookie_key(c)] = c
for c in new_cookies:
    merged[cookie_key(c)] = c

result = list(merged.values())

with open(cookie_file, 'w') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

# Summary
new_domains = sorted(set(c.get('domain', '').lstrip('.') for c in new_cookies))
all_domains = sorted(set(c.get('domain', '').lstrip('.') for c in result))
nd = ', '.join(new_domains)
ad = len(all_domains)
print(f'Added {len(new_cookies)} cookies from: {nd}')
print(f'Total: {len(result)} cookies across {ad} domains')
print(f'Saved to: {cookie_file}')
" <<< "$clip"
