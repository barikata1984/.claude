# Development Workflow Rules

- Test after code changes: `python -m pytest tests/ -v -k "relevant_keyword"`
- Commit only after passing tests
- When completing a task: update `notes/TODO.md` (or `docs/TODO.md` if the project uses legacy `docs/`; check off item)
- When completing a topic: append results to relevant `notes/LOGS/log_*.md` (or `docs/LOGS/log_*.md` for legacy)
- When discovering a new issue: add entry to `notes/ISSUES.md` (or `docs/ISSUES.md` for legacy)
- When resolving an issue: delete the entry from `notes/ISSUES.md` (or `docs/ISSUES.md` for legacy)
- Directory resolution (`notes/` default vs `docs/` legacy): see CLAUDE.md「標準ドキュメント構成」
- Commit message: English, imperative mood, Conventional Commits format
