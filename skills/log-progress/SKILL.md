---
name: log-progress
description: Update project documentation (notes/TODO.md, notes/LOGS/log_*.md, notes/ISSUES.md, notes/PLAN.md — or docs/* for legacy projects) based on the current conversation's progress, findings, and resolved issues. Checks off completed TODOs, appends new findings to the relevant append-only topic log, adds newly discovered issues, deletes resolved issues, and updates PLAN only if design decisions changed. Also used as a sub-step by /wrap-up-session. Use this skill whenever the user wants to record session progress, update project docs from conversation, capture findings before stopping, or says things like "log progress", "update docs", "update notes", "record what we did", "進捗記録", "ログ更新", "TODO を更新", "ノート更新". Do NOT trigger if the user also wants to commit and push — suggest /wrap-up-session instead.
---

# log-progress

Update documentation based on conversation content at session end.

## Procedure

1. Analyze the conversation to identify progress, findings, and resolved issues
2. **Resolve docs base directory**: detect which exists in the project — `notes/` (default) or `docs/` (legacy). If neither exists, consult project-level CLAUDE.md for an explicit choice; otherwise default to `notes/`. The 4 standard files live directly under this base directory
3. Locate documentation files by consulting the project's CLAUDE.md (look for a "参照先" or "ドキュメント構成" section) and the user-level CLAUDE.md "標準ドキュメント構成" table. If the referenced files do not exist on disk, report that to the user and skip
4. Update each file according to its role:
   - **TODO** (`<base>/TODO.md`) — Check off completed items with `[x]`. Add newly identified tasks
   - **LOGS** (`<base>/LOGS/log_<topic>.md`) — Append results and findings to the relevant topic log (append to end). Create a new `log_<topic>.md` if no suitable log exists
   - **ISSUES** (`<base>/ISSUES.md`) — Add newly discovered issues. Delete resolved issues entirely
   - **PLAN** (`<base>/PLAN.md`) — Update only if design decisions have changed

`<base>` = `notes/` (default) or `docs/` (legacy), determined per step 2.

## Reference processing

If `.claude/rules/references.md` exists in the project, follow its citation conventions.

## Rules

- LOGS are **append-only**. Do not edit past records
- ISSUES: **delete** resolved items (do not archive)
- Maintain the existing format of each file
- Use ISO date format (YYYY-MM-DD)
- Do not touch files if there are no changes
