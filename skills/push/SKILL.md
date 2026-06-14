---
name: push
description: Push already-committed local commits to the remote repository. Checks which commits are ahead of upstream (git log @{u}..HEAD), confirms the branch, and runs git push (with -u origin <branch> if no tracking branch is set yet). Reports clearly when there is nothing to push or when push fails due to remote being ahead of local. Also used as a sub-step by /commit-and-push. Use this skill whenever the user asks to push already-committed changes, publish commits, sync a branch with the remote without making new commits, or says things like "push", "push to remote", "プッシュ", "push 済みのやつ", "publish these commits". Do NOT trigger if the user has uncommitted changes they want to include — suggest /commit-and-push instead.
---

# push

Push committed changes to the remote repository via a haiku subagent.

## Procedure

Spawn a subagent using the Agent tool with `model: "haiku"`. The subagent prompt must include the procedure and rules below.

### Subagent push procedure (include in prompt)

1. Run `git log --oneline @{u}..HEAD` to check commits to push
   - If no tracking branch exists, run `git log --oneline -5` to show recent commits
2. If there are no commits to push, return "nothing to push"
3. Confirm the current branch name with `git branch --show-current`
4. Execute push:
   - If a remote tracking branch exists: `git push`
   - If no remote tracking branch: `git push -u origin <branch>`
5. Return the push result (success/failure and details)

### Rules (include in prompt)

- Push destination defaults to the current branch's remote unless otherwise specified
- If push fails (e.g., remote is ahead), return the error details — do not attempt force push

## Handle result (main agent)

Report the subagent's result to the user. If push failed, consult the user on how to proceed.
