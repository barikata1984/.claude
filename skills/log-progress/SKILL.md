# log-progress

Update documentation based on conversation content at session end.

## Procedure

1. Analyze the conversation to identify progress, findings, and resolved issues
2. Locate documentation files by consulting the project's CLAUDE.md (look for a "参照先" or "ドキュメント構成" section) and the user-level CLAUDE.md "標準ドキュメント構成" table. If neither exists or the referenced files do not exist on disk, report that to the user and skip
3. Update each file according to its role:
   - **TODO** — Check off completed items with `[x]`. Add newly identified tasks
   - **LOGS** — Append results and findings to the relevant topic log (append to end). Create a new `log_<topic>.md` if no suitable log exists
   - **ISSUES** — Add newly discovered issues. Delete resolved issues entirely
   - **PLAN** — Update only if design decisions have changed

## Reference processing

If `.claude/rules/references.md` exists in the project, follow its citation conventions.

## Rules

- LOGS are **append-only**. Do not edit past records
- ISSUES: **delete** resolved items (do not archive)
- Maintain the existing format of each file
- Use ISO date format (YYYY-MM-DD)
- Do not touch files if there are no changes
