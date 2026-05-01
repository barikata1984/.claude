#!/bin/bash
# start.sh — Inject credentials and launch the MCP server.
#
# Credential resolution order (first hit wins):
#   1. Already-set environment variable (caller-supplied)
#   2. Doppler (per-machine token in ~/.config/doppler.env)
#   3. pass (legacy fallback)
#
# The API key exists only in this server process's environment.
# The Claude Code agent never sees the key.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---------------------------------------------------------------------------
# Pull secrets from Doppler if available. No-op when CLI is missing or
# ~/.config/doppler.env is absent. Existing env vars are preserved (Doppler
# secrets only fill in unset names) so the caller can always override.
# ---------------------------------------------------------------------------
if command -v doppler >/dev/null 2>&1 && [ -r "$HOME/.config/doppler.env" ]; then
    DOPPLER_TOKEN="$(grep -E '^DOPPLER_TOKEN=' "$HOME/.config/doppler.env" | cut -d= -f2-)"
    export DOPPLER_TOKEN
    if _doppler_env="$(doppler secrets download --no-file --format=env --silent 2>/dev/null)"; then
        while IFS='=' read -r _key _val; do
            [ -z "$_key" ] && continue
            [ -n "${!_key:-}" ] && continue
            _val="${_val#\"}"; _val="${_val%\"}"
            export "$_key=$_val"
        done <<< "$_doppler_env"
        unset _key _val _doppler_env
    fi
    unset DOPPLER_TOKEN
fi

# Semantic Scholar API key (optional — without it, stricter rate limits apply)
export S2_API_KEY="${S2_API_KEY:-$(pass show api/semantic-scholar 2>/dev/null || true)}"
if [[ -z "$S2_API_KEY" ]]; then
    echo "Warning: S2_API_KEY not available. Rate limits will be stricter." >&2
fi

# Unpaywall email (required for Unpaywall API access; identifier, not a secret)
export UNPAYWALL_EMAIL="${UNPAYWALL_EMAIL:-franche1984@gmail.com}"

exec uv run "$SCRIPT_DIR/server.py"
