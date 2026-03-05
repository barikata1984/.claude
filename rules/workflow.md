# Development Workflow Rules

All paths below are relative to `catkin_ws/src/osx_bilateral/`.

- Test after code changes: `python -m pytest tests/ -v -k "relevant_keyword"`
- Commit only after passing tests
- When completing a task: update `docs/TODO.md` (check off item)
- When completing a topic: append results to relevant `docs/LOGS/log_*.md`
- When discovering a new issue: add entry to `docs/ISSUES.md`
- When resolving an issue: delete the entry from `docs/ISSUES.md`
- Commit message: English, imperative mood, Conventional Commits format
