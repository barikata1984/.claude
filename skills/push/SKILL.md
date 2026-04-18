---
name: push
description: Push already-committed local commits to the remote repository. Checks which commits are ahead of upstream (git log @{u}..HEAD), confirms the branch, and runs git push (with -u origin <branch> if no tracking branch is set yet). Reports clearly when there is nothing to push or when push fails due to remote being ahead of local. Also used as a sub-step by /commit-and-push. Use this skill whenever the user asks to push already-committed changes, publish commits, sync a branch with the remote without making new commits, or says things like "push", "push to remote", "プッシュ", "push 済みのやつ", "publish these commits". Do NOT trigger if the user has uncommitted changes they want to include — suggest /commit-and-push instead.
---

# push

Push committed changes to the remote repository. Also used as part of `/commit-and-push`. Trigger on requests like "push", "push to remote", "sync with remote".

## Procedure

1. Check commits to push with `git log --oneline @{u}..HEAD`
   - If no tracking branch exists, show recent commits with `git log --oneline -5`
2. If there are no commits to push, notify the user and finish
3. Confirm the current branch name
4. Execute `git push`:
   - If a remote tracking branch exists: `git push`
   - If no remote tracking branch exists: `git push -u origin <branch>`
6. Display the push result

## Rules

- Push destination defaults to the current branch's remote unless otherwise specified by the user
- If push fails (e.g., remote is ahead), report the cause and consult the user on how to proceed
