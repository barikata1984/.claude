# wrap-up-session

Standard end-of-session routine. Performs documentation update → commit → push in sequence. Trigger on requests like "done", "finished", "end session", "wrap up", "let's call it". Since this is the skill to call at the end of a session, proactively suggest it when the user indicates work is complete.

## Procedure

1. Follow the procedure in `.claude/skills/log-progress/SKILL.md` to update documentation
2. Once documentation updates are complete, follow `.claude/skills/commit-and-push/SKILL.md` to commit and push changes

## Rules

- Execute each step strictly in order (log-progress → commit-and-push)
- Even if log-progress produces no changes, run commit-and-push if there are uncommitted changes from the session
- If there is nothing to commit, notify the user and finish

## Context

- Documentation update logic: see `.claude/skills/log-progress/SKILL.md`
- Commit and push logic: see `.claude/skills/commit-and-push/SKILL.md`
