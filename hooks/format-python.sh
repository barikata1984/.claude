#!/bin/bash
FILE_PATH=$(cat | jq -r '.tool_input.file_path // empty')
if [[ "$FILE_PATH" == *.py ]]; then
  ruff format --quiet "$FILE_PATH" 2>/dev/null
fi
exit 0
