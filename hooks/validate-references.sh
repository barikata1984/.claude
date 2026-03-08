#!/usr/bin/env bash
# PostToolUse hook: validate MAIN.md entries and regenerate references.bib.
# Exit 0 = pass, Exit 2 = block (require fix).

set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.file // empty')

# Only act on docs/REFERENCES/MAIN.md
case "$FILE_PATH" in
  */docs/REFERENCES/MAIN.md) ;;
  *) exit 0 ;;
esac

# --- Validation: every ### entry must have DOI or URL ---
MISSING=()
CURRENT_KEY=""
HAS_REF=false

while IFS= read -r line; do
  if [[ "$line" =~ ^###[[:space:]]+(.+) ]]; then
    if [[ -n "$CURRENT_KEY" && "$HAS_REF" == false ]]; then
      MISSING+=("$CURRENT_KEY")
    fi
    CURRENT_KEY="${BASH_REMATCH[1]}"
    HAS_REF=false
  fi
  if [[ "$line" =~ DOI:|doi:|https?:// ]]; then
    HAS_REF=true
  fi
done < "$FILE_PATH"

if [[ -n "$CURRENT_KEY" && "$HAS_REF" == false ]]; then
  MISSING+=("$CURRENT_KEY")
fi

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo "REFERENCES validation failed: entries without DOI or URL:" >&2
  for key in "${MISSING[@]}"; do
    echo "  - $key" >&2
  done
  exit 2
fi

# --- BibTeX generation: parse MAIN.md → references.bib ---
BIB_FILE="$(dirname "$FILE_PATH")/references.bib"
{
  echo "% Auto-generated from MAIN.md — do not edit manually."
  echo ""

  KEY=""
  TITLE=""
  AUTHORS=""
  VENUE=""
  YEAR=""
  DOI=""
  URL=""

  flush_entry() {
    if [[ -z "$KEY" ]]; then return; fi
    # Determine entry type from venue name
    TYPE="misc"
    if [[ "$VENUE" =~ (ICRA|IROS|NeurIPS|ICML|ICLR|CoRL|RSS|CVPR|ICCV|ECCV|AAAI|IJCAI|Proceedings|Conference|Conf\.|Proc\.) ]]; then
      TYPE="inproceedings"
    elif [[ "$VENUE" =~ (Journal|Trans\.|Transactions|IEEE|ACM|Letters|Review|Magazine) ]]; then
      TYPE="article"
    elif [[ "$VENUE" =~ arXiv ]]; then
      TYPE="misc"
    fi

    echo "@${TYPE}{${KEY},"
    [[ -n "$TITLE" ]] && echo "  title = {${TITLE}},"
    [[ -n "$AUTHORS" ]] && echo "  author = {${AUTHORS}},"
    [[ -n "$YEAR" ]] && echo "  year = {${YEAR}},"
    if [[ "$TYPE" == "inproceedings" ]]; then
      [[ -n "$VENUE" ]] && echo "  booktitle = {${VENUE}},"
    elif [[ "$TYPE" == "article" ]]; then
      [[ -n "$VENUE" ]] && echo "  journal = {${VENUE}},"
    else
      [[ -n "$VENUE" ]] && echo "  howpublished = {${VENUE}},"
    fi
    [[ -n "$DOI" ]] && echo "  doi = {${DOI}},"
    [[ -n "$URL" ]] && echo "  url = {${URL}},"
    echo "}"
    echo ""

    KEY="" TITLE="" AUTHORS="" VENUE="" YEAR="" DOI="" URL=""
  }

  while IFS= read -r line; do
    # New entry: ### Key
    if [[ "$line" =~ ^###[[:space:]]+(.+) ]]; then
      flush_entry
      KEY="${BASH_REMATCH[1]}"
      continue
    fi

    [[ -z "$KEY" ]] && continue

    # Title line: **Title**
    if [[ "$line" =~ ^\*\*(.+)\*\*$ ]]; then
      TITLE="${BASH_REMATCH[1]}"
      continue
    fi

    # Authors — Venue, Year
    if [[ "$line" =~ ^(.+)[[:space:]]—[[:space:]](.+),[[:space:]]*([0-9]{4})$ ]]; then
      AUTHORS="${BASH_REMATCH[1]}"
      VENUE="${BASH_REMATCH[2]}"
      YEAR="${BASH_REMATCH[3]}"
      continue
    fi

    # DOI line
    if [[ "$line" =~ DOI:[[:space:]]*\`([^\`]+)\` ]]; then
      DOI="${BASH_REMATCH[1]}"
    fi

    # URL (standalone or after |)
    if [[ "$line" =~ \[([^\]]*)\]\((https?://[^)]+)\) ]]; then
      URL="${BASH_REMATCH[2]}"
    elif [[ "$line" =~ (https?://[^[:space:]]+) && -z "$URL" ]]; then
      URL="${BASH_REMATCH[1]}"
    fi
  done < "$FILE_PATH"

  flush_entry
} > "$BIB_FILE"

exit 0
