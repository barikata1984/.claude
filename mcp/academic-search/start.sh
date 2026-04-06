#!/bin/bash
# start.sh — Inject credentials from pass and launch the MCP server.
#
# This script is the credential isolation boundary:
# - pass is called once at startup
# - The API key exists only in this server process's environment
# - The Claude Code agent never sees the key
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Semantic Scholar API key (optional — without it, stricter rate limits apply)
export S2_API_KEY="${S2_API_KEY:-$(pass show api/semantic-scholar 2>/dev/null || true)}"
if [[ -z "$S2_API_KEY" ]]; then
    echo "Warning: S2_API_KEY not available. Rate limits will be stricter." >&2
fi

# Unpaywall email (required for Unpaywall API access)
export UNPAYWALL_EMAIL="${UNPAYWALL_EMAIL:-$(pass show api/unpaywall-email 2>/dev/null || true)}"
if [[ -z "$UNPAYWALL_EMAIL" ]]; then
    echo "Warning: UNPAYWALL_EMAIL not set. resolve_oa_url will skip Unpaywall." >&2
fi

exec uv run "$SCRIPT_DIR/server.py"
