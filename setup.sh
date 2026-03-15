#!/usr/bin/env bash
# Setup script for .claude/ submodule.
# Creates symlinks from project root to .claude/ managed files.
#
# Usage: bash .claude/setup.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Symlink definitions: target (relative to project root) -> source (relative to .claude/)
declare -A LINKS=(
    ["CLAUDE.md"]=".claude/CLAUDE.md"
    [".mcp.json"]=".claude/mcp.json"
)

create_symlink() {
    local link_name="$1"
    local link_target="$2"
    local link_path="$PROJECT_ROOT/$link_name"

    if [ -L "$link_path" ]; then
        local current_target
        current_target="$(readlink "$link_path")"
        if [ "$current_target" = "$link_target" ]; then
            echo "  [skip] $link_name -> $link_target (already exists)"
            return 0
        fi
        echo "  [update] $link_name: $current_target -> $link_target"
        ln -snf "$link_target" "$link_path"
    elif [ -e "$link_path" ]; then
        echo "  [warn] $link_name exists as a regular file, skipping (remove it manually to create symlink)"
        return 0
    else
        echo "  [create] $link_name -> $link_target"
        ln -s "$link_target" "$link_path"
    fi
}

echo "Setting up .claude/ symlinks in $PROJECT_ROOT"
echo ""

# Verify .claude/ exists
if [ ! -d "$SCRIPT_DIR" ]; then
    echo "Error: .claude/ directory not found at $SCRIPT_DIR"
    exit 1
fi

# Create symlinks
for link_name in "${!LINKS[@]}"; do
    source_file="$SCRIPT_DIR/${LINKS[$link_name]#.claude/}"
    if [ ! -e "$source_file" ]; then
        echo "  [warn] Source not found: ${LINKS[$link_name]}, skipping"
        continue
    fi
    create_symlink "$link_name" "${LINKS[$link_name]}"
done

echo ""

# Check for uv (needed by MCP server)
if ! command -v uv &> /dev/null; then
    echo "Warning: 'uv' is not installed. The academic-fetch MCP server requires it."
    echo "  Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

echo "Done."
