# OSX-UR: Claude Code Instructions

UR5e object manipulation imitation learning with physical properties using ROS1.

## Workspace Layout

```
(TBD — update for current project)
```

## Coding Standards

- **Formatter**: `ruff format` (configured in `/root/osx-ur/pyproject.toml`)
- **Linter**: `ruff check`
- **Type hints**: Python 3.10+ annotations required
- **Line length**: 100 characters
- **Import order**: stdlib, third-party, local `src` imports (enforced by ruff isort)
- **Error handling**: Use custom exceptions from `src/core/exceptions.py`
- **Docstrings**: Google style, only for non-obvious functions

## Testing

```bash
python -m pytest tests/ -v                         # all tests
python -m pytest tests/src/refactoring/ -v         # refactoring phase tests (176)
python -m pytest tests/src/models/ -v              # model tests
python -m pytest tests/ -v -k "keyword"            # keyword filter
```

All tests are pure Python -- no ROS or hardware required.
Always run relevant tests before committing.

## Git Workflow

- **Commit format**: Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`)
- **Branch naming**: `feature/ISSUE_ID-description`, `fix/ISSUE_ID-description`
- **Main branch**: `ros-o`

## Key Technologies

- Python 3.10.12, ROS One Ninjemys (ROS1)
- PyTorch, LeRobot, wandb
- CLI: Tyro (dataclass-based)
- Object pose: BundleSDF
- Point cloud: PointNet (pretrained)
