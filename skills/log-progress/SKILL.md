---
name: log-progress
description: Update project documentation (notes/TODO.md, notes/LOGS/log_*.md, notes/ISSUES.md, notes/PLAN.md — or docs/* for legacy projects) based on the current conversation's progress, findings, and resolved issues. Checks off completed TODOs, appends new findings to the relevant append-only topic log, adds newly discovered issues, deletes resolved issues, and updates PLAN only if design decisions changed. Also used as a sub-step by /wrap-up-session. Use this skill whenever the user wants to record session progress, update project docs from conversation, capture findings before stopping, or says things like "log progress", "update docs", "update notes", "record what we did", "進捗記録", "ログ更新", "TODO を更新", "ノート更新". Do NOT trigger if the user also wants to commit and push — suggest /wrap-up-session instead.
---

# log-progress

Update documentation based on conversation content via a sonnet subagent.

## Procedure

### 1. Build session summary (main agent)

Review the conversation to extract:
- Completed tasks and their outcomes
- New findings, experiment results, design decisions
- Newly discovered issues
- Resolved issues
- Any changes to project plan or architecture

### 2. Resolve docs base directory (main agent)

Detect which exists in the project — `notes/` (default) or `docs/` (legacy). If neither exists, consult project-level CLAUDE.md; otherwise default to `notes/`.

### 3. Spawn sonnet subagent

Use the Agent tool with `model: "sonnet"` to delegate the documentation updates. The subagent prompt must include:

1. **The session summary** from step 1
2. **The docs base directory** from step 2
3. **The update procedure and rules** below

#### Subagent update procedure (include in prompt)

1. Read each documentation file to understand current state:
   - `<base>/TODO.md`
   - `<base>/LOGS/` (list files, read relevant topic logs)
   - `<base>/ISSUES.md`
   - `<base>/PLAN.md`
2. If referenced files do not exist on disk, report and skip them
3. Update each file according to its role:
   - **TODO** (`<base>/TODO.md`) — Check off completed items with `[x]`. Add newly identified tasks
   - **LOGS** (`<base>/LOGS/log_<topic>.md`) — Append results and findings to the relevant topic log (append to end). Create a new `log_<topic>.md` if no suitable log exists
   - **ISSUES** (`<base>/ISSUES.md`) — Add newly discovered issues. Delete resolved issues entirely
   - **PLAN** (`<base>/PLAN.md`) — Update only if design decisions have changed

#### Reference processing (include in prompt)

If `.claude/rules/references.md` exists in the project, follow its citation conventions.

#### Rules (include in prompt)

- LOGS are **append-only** — do not edit past records
- ISSUES: **delete** resolved items (do not archive)
- Maintain the existing format of each file
- Use ISO date format (YYYY-MM-DD)
- Do not touch files if there are no changes

### 4. Report result (main agent)

Report which files the subagent updated to the user.
