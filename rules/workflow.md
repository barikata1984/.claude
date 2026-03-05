# Development Workflow Rules

- Test after code changes: `python -m pytest tests/ -v -k "relevant_keyword"`
- Commit only after passing tests
- When completing a task: update `catkin_ws/src/osx_bilateral/docs/TODO.md` (check off item)
- When completing a topic: append results to relevant `catkin_ws/src/osx_bilateral/docs/LOGS/log_*.md`
- When discovering a new issue: add entry to `catkin_ws/src/osx_bilateral/docs/ISSUES.md`
- When resolving an issue: delete the entry from `catkin_ws/src/osx_bilateral/docs/ISSUES.md`
- Commit message: English, imperative mood, Conventional Commits format
