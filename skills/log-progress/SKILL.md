# log-progress

Update documentation based on conversation content at session end.

## Procedure

1. Analyze the conversation to identify progress, findings, and resolved issues
2. Update the following files as appropriate:
   - `docs/TODO.md` — Check off completed items with `[x]`. Add newly identified tasks
   - `docs/LOGS/log_*.md` — Append results and findings to the relevant topic log (append to end)
   - `docs/ISSUES.md` — Add newly discovered issues. Delete resolved issues entirely
   - `docs/PLAN.md` — Update only if design decisions have changed

## Reference processing

Follow the citation conventions in `.claude/rules/references.md`.

## Rules

- LOGS are **append-only**. Do not edit past records
- ISSUES: **delete** resolved items (do not archive)
- Maintain the existing format of each file
- Use ISO date format (YYYY-MM-DD)
- Do not touch files if there are no changes
