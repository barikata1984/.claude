---
paths:
  - "**/*.py"
  - "**/pyproject.toml"
  - "**/ruff.toml"
---

# Python コーディング規約

- **Formatter**: `ruff format`
- **Linter**: `ruff check`
- **Type hints**: Python 3.10+ annotations required
- **Line length**: 100 characters
- **Import order**: stdlib → third-party → local (enforced by ruff isort)
- **Docstrings**: Google style, only for non-obvious functions
