#!/usr/bin/env bash
# PostToolUse hook: normalize Japanese typography in Markdown files in place.
# Skips the ~/.claude config tree and any file carrying the opt-out marker
# (e.g. LaTeX-source Markdown). Always exits 0 so it never blocks Claude.
FILE_PATH=$(cat | jq -r '.tool_input.file_path // .tool_input.file // empty')

[[ "$FILE_PATH" == *.md ]] || exit 0

# Rules/instruction files must keep their own punctuation and examples.
case "$FILE_PATH" in
  "$HOME"/.claude/*) exit 0 ;;
esac

# Per-file opt-out: place "<!-- no-ja-typography -->" in LaTeX-source Markdown etc.
if [[ -f "$FILE_PATH" ]] && grep -q '<!-- no-ja-typography -->' "$FILE_PATH"; then
  exit 0
fi

python3 "$HOME/.claude/hooks/format_ja_typography.py" "$FILE_PATH" || true
exit 0
