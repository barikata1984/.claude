---
name: commit-and-push
description: Commit session changes AND push them to the remote in one flow. Runs /commit to group and commit changes by topic, then /push to publish them to origin, finally displaying git status and recent log. Use this skill whenever the user wants to finish and publish a chunk of work, sync their branch with remote, or says things like "commit and push", "push my changes", "sync with remote", "publish these changes", "wrap this up and push", "コミットしてプッシュ", "変更を上げて". Prefer this over invoking /commit and /push separately whenever both actions are intended — this skill orchestrates them and shows the final state.
---

# commit-and-push

Commit session changes and push to remote. Both sub-steps delegate to haiku subagents.

## Procedure

1. Follow `.claude/skills/commit/SKILL.md` to commit changes (spawns haiku subagent)
2. If the commit succeeds, follow `.claude/skills/push/SKILL.md` to push (spawns haiku subagent)
3. Display `git status` and `git log --oneline -5` as the final result

## Context

- Commit logic (haiku subagent): see `.claude/skills/commit/SKILL.md`
- Push logic (haiku subagent): see `.claude/skills/push/SKILL.md`
