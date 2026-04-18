---
name: commit
description: Create git commits from session file changes grouped by topic using Conventional Commits format (feat/fix/refactor/docs/chore/style/test/perf/build/ci). Reviews conversation history to identify what was changed and why, categorizes changes into logical groups, generates accurate commit messages without requiring user confirmation when intent is clear from session context, stages files individually (never git add -A or git add .), and handles submodules/secrets with care. Also used as a sub-step by /commit-and-push. Use this skill whenever the user asks to commit changes, stage changes, create a commit, group changes into commits, or says things like "commit this", "commit the work", "make a commit", "コミット", "これコミットして". Do NOT trigger for "commit and push" — /commit-and-push handles that case.
---

# commit

Create commits from session file changes or git diffs. Categorize changes by topic and commit using Conventional Commits format. Also used as part of `/commit-and-push`. Trigger on requests like "commit", "stage changes", "group changes".

## Procedure

### 1. Inspect session history

Review the conversation history to identify files changed during this session via Edit / Write / Bash tools.

### 2-A. When there are session changes

The conversation context provides "what was changed and why", so commit messages are highly accurate.

1. Check actual file state with `git status` and `git diff`
2. If changes across different topics are clearly distinguishable, group them by topic
3. Generate a Conventional Commits format message for each group
4. Stage and commit (no user confirmation needed since intent is clear from session context)

If there are uncommitted changes beyond session changes, notify the user and ask whether to include them.

### 2-B. When there are no session changes

Without conversation context about the changes, commit messages are based solely on git information.

1. List changed files with `git status`
2. Examine change details with `git diff` (staged + unstaged)
3. Check recent commit history with `git log --oneline -10` to match message style
4. Analyze changes and group by topic
5. Generate a Conventional Commits format message for each group
6. **Present commit messages to the user and obtain approval before** staging and committing

### 3. Execute commits

For each topic group:

1. Stage relevant files individually with `git add <file1> <file2> ...`
2. Commit with the message passed via HEREDOC format:
   ```bash
   git commit -m "$(cat <<'EOF'
   <type>: <description>

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```
3. Verify the result with `git status` after committing
4. If there are multiple groups, proceed to the next group

## Rules

- Commit messages use Conventional Commits format: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`
- Commit messages in English, imperative mood
- Match the style of recent `git log`
- Exclude files containing secrets (`.env`, credentials, API keys, etc.) from commits and warn
- Do not use `git add -A` or `git add .`; specify files individually
- If a pre-commit hook fails, do not use `--amend`; fix the issue and create a new commit
- Do not create empty commits
- For submodule changes (shown as `Subproject commit` in `git diff`), explicitly confirm with the user
