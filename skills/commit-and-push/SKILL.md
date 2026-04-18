---
name: commit-and-push
description: Commit session changes AND push them to the remote in one flow. Runs /commit to group and commit changes by topic, then /push to publish them to origin, finally displaying git status and recent log. Use this skill whenever the user wants to finish and publish a chunk of work, sync their branch with remote, or says things like "commit and push", "push my changes", "sync with remote", "publish these changes", "wrap this up and push", "コミットしてプッシュ", "変更を上げて". Prefer this over invoking /commit and /push separately whenever both actions are intended — this skill orchestrates them and shows the final state.
---

# commit-and-push

An integrated command that runs `/commit` followed by `/push` in sequence. Commits session changes or git diffs and pushes to the remote. Trigger on requests like "commit and push", "push changes", "sync changes".

## Usage

```
/commit-and-push    → Run commit + push in sequence
/commit             → Commit only (no push)
/push               → Push only (targets already committed changes)
```

## Procedure

1. Follow `.claude/skills/commit/SKILL.md` to commit changes
2. If the commit succeeds, follow `.claude/skills/push/SKILL.md` to push to the remote
3. Display `git status` and `git log --oneline -5` as the final result

## Context

- Commit logic: see `.claude/skills/commit/SKILL.md`
- Push logic: see `.claude/skills/push/SKILL.md`
