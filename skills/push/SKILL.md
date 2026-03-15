# push

Push committed changes to the remote repository. Also used as part of `/commit-and-push`. Trigger on requests like "push", "push to remote", "sync with remote".

## Procedure

1. Check commits to push with `git log --oneline @{u}..HEAD`
   - If no tracking branch exists, show recent commits with `git log --oneline -5`
2. If there are no commits to push, notify the user and finish
3. Confirm the current branch name
4. For pushes to the main branch (`ros-o`):
   - Warn the user and obtain explicit confirmation
   - Force push is prohibited
5. Execute `git push`:
   - If a remote tracking branch exists: `git push`
   - If no remote tracking branch exists: `git push -u origin <branch>`
6. Display the push result

## Rules

- Push destination defaults to the current branch's remote unless otherwise specified by the user
- `--force` push to `ros-o` (main branch) is prohibited
- If push fails (e.g., remote is ahead), report the cause and consult the user on how to proceed
