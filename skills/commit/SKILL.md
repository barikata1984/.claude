---
name: commit
description: Create git commits from session file changes grouped by topic using Conventional Commits format (feat/fix/refactor/docs/chore/style/test/perf/build/ci). Reviews conversation history to identify what was changed and why, categorizes changes into logical groups, generates accurate commit messages without requiring user confirmation when intent is clear from session context, stages files individually (never git add -A or git add .), and handles submodules/secrets with care. Also used as a sub-step by /commit-and-push. Use this skill whenever the user asks to commit changes, stage changes, create a commit, group changes into commits, or says things like "commit this", "commit the work", "make a commit", "コミット", "これコミットして". Do NOT trigger for "commit and push" — /commit-and-push handles that case.
---

# commit

Create commits from session file changes or git diffs via a haiku subagent. The main agent gathers context; a haiku subagent executes the git operations.

## Procedure

### 1. Build change summary (main agent)

Review conversation history. Extract:
- Which files were changed via Edit / Write / Bash during this session
- What was done to each file and why

Determine whether session changes exist (changes you can trace to this conversation).

If there are uncommitted changes beyond session changes, note them separately.

### 2. Spawn haiku subagent

Use the Agent tool with `model: "haiku"` to delegate the commit work. The subagent prompt must include:

1. **The change summary** from step 1 (list of files, what changed, why), or state "no session changes — user approval required before committing"
2. **All rules** from the Rules section below (copy them into the prompt)
3. **The commit execution procedure** below

#### Subagent commit procedure (include in prompt)

1. Run `git status` and `git diff` (staged + unstaged) to see current state
2. Run `git log --oneline -10` to match existing commit message style
3. Group changes by topic
4. Generate a Conventional Commits message for each group

**If session changes exist** (intent is clear):
5. Stage files individually: `git add <file1> <file2> ...`
6. Commit using HEREDOC format:
   ```
   git commit -m "$(cat <<'EOF'
   <type>: <description>

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```
7. Run `git status` to verify
8. Return a summary of all commits made

**If no session changes** (intent unclear):
5. Return a structured list of proposed commits (files and messages for each group) — do NOT stage or commit

### 3. Handle result (main agent)

- **Session changes existed**: Report the subagent's commit summary to the user.
- **No session changes**: Present the proposed commits to the user. If approved, spawn another haiku subagent (or execute directly) to stage and commit.
- **Extra uncommitted changes** noted in step 1: Ask the user whether to include them.

## Rules

- Conventional Commits format: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`, `style:`, `perf:`, `build:`, `ci:`
- Commit messages in English, imperative mood
- Match the style of recent `git log`
- Exclude files containing secrets (`.env`, credentials, API keys) — warn the user
- Never use `git add -A` or `git add .`; stage files individually
- If a pre-commit hook fails, do not use `--amend`; fix the issue and create a new commit
- Do not create empty commits
- For submodule changes (`Subproject commit` in `git diff`), flag them for user confirmation — do not commit automatically
