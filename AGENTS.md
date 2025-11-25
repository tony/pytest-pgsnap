# AGENTS.md

This file provides guidance to AI agents (including Claude Code, Cursor, and other LLM-powered tools) when working with code in this repository.

## CRITICAL REQUIREMENTS

### Test Success
- ALL tests MUST pass for code to be considered complete and working
- Never describe code as "working as expected" if there are ANY failing tests
- Even if specific feature tests pass, failing tests elsewhere indicate broken functionality
- Changes that break existing tests must be fixed before considering implementation complete
- A successful implementation must pass linting, type checking, AND all existing tests

## Project Overview

pytest-pgsnap is an experimental pytest plugin and snapshot toolkit in the gp-libs ecosystem. It combines a doctest/docutils-aware pytest plugin with early abstractions for caching side effects—especially small PostgreSQL databases—to speed up repeatable tests and documentation examples.

Key features:
- Pytest plugin (`src/pytest_pgsnap.py`) that collects doctests from `.rst`/`.md` files and selected `.py` modules via `doctest-docutils`, while blocking pytest's built-in doctest plugin to avoid double collection.
- pgsnap core module (`src/pgsnap/core.py`) sketching pluggable snapshot strategies for files and PostgreSQL (SQL emission, dumps, and template-based copies) plus pytest-oriented cache markers.
- Strict typing (`mypy --strict`) and Ruff-powered formatting/linting.
- Documentation built with Sphinx/Furo; shared tooling pulled from `gp-libs`.

## Development Environment

This project uses:
- Python 3.9+ (tool-versions lists interpreters up to 3.14)
- [uv](https://github.com/astral-sh/uv) for dependency management and running commands
- [ruff](https://github.com/astral-sh/ruff) for linting and formatting
- [mypy](https://github.com/python/mypy) for type checking
- [pytest](https://docs.pytest.org/) for testing
- [Sphinx](https://www.sphinx-doc.org/) + [furo](https://pradyunsg.me/furo/) for docs

## Common Commands

### Setting Up Environment
```bash
uv sync --all-extras --dev
```

### Running Tests
```bash
uv run py.test
make test           # helper
make start          # pytest-watcher
make watch_test     # requires entr(1)
```

### Linting and Formatting
```bash
uv run ruff check .
uv run ruff format .
uv run ruff check . --fix
make ruff           # lint
make ruff_format    # format
make watch_ruff     # requires entr(1)
```

### Type Checking
```bash
uv run mypy .
make mypy
make watch_mypy     # requires entr(1)
```

### Documentation
```bash
make start_docs     # live reload at http://localhost:8034
(cd docs && make start)  # same from docs/
make build_docs
make watch_docs     # requires entr(1)
make dev_docs       # concurrent rebuild+serve (GNU make -J)
```

### Development Workflow

1. **Format**: `uv run ruff format .`
2. **Lint**: `uv run ruff check . --fix`
3. **Type Check**: `uv run mypy .`
4. **Test**: `uv run py.test`
5. **Repeat tests** after fixes

## Code Architecture

- **Pytest plugin** (`src/pytest_pgsnap.py`): custom collector for doctest-docutils; disables default pytest doctest plugin; provides `PytestDoctestRunner` that accumulates failures instead of aborting on first error.
- **Snapshot core** (`src/pgsnap/core.py`): abstract bases for side-effect snapshots (files and PostgreSQL) including SQL emission, dump/restore, and template strategies, plus pytest fixture cache markers.
- **Package metadata** (`src/pgsnap/__about__.py`): central metadata for packaging, docs, and distribution.
- **Documentation** (`docs/`): Sphinx project with developing guide and placeholder API stubs.

## Testing Strategy

- Primary framework: pytest; doctests collected through `doctest-docutils` integration.
- Favor real doctest examples in `.rst`/`.md`/`.py` to cover plugin behavior and snapshot helpers.
- Add targeted pytest tests when modifying collection logic, option flags, or snapshot abstractions; keep fixtures minimal and deterministic.
- Use `make start` (pytest-watcher) for tight feedback; ensure `uv run py.test` passes before shipping changes.

## Coding Standards

- Ruff handles formatting and linting; run the formatter before committing.
- mypy runs in strict mode—annotate new code thoroughly and prefer `import typing as t` with namespace access.
- Docstrings follow NumPy style (pydocstyle via Ruff); keep complex examples in dedicated tests instead of long doctests.
- Prefer `pathlib.Path` over `os.path`; use f-strings for interpolation; keep Python ≥3.9 compatibility in mind.

## References

- Docs: https://pytest-pgsnap.git-pull.com
- Repository: https://github.com/tony/pytest-pgsnap
- PyPI: https://pypi.org/project/pytest-pgsnap/
- Shared tooling: https://gp-libs.git-pull.com
