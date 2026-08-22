# AGENTS.md

pytest-pgsnap: an early-stage toolkit for caching side effects — especially
small PostgreSQL databases — across pytest runs instead of rebuilding them
every time.

Follow the conventions already in the tree, and keep a change scoped to what
was asked for.

## What is here

| Path | What it is |
| ---- | ---------- |
| `src/pgsnap/core.py` | `Snapshot` strategy taxonomy: file and PostgreSQL (SQL emission, dump/restore, template copy) base classes, plus unimplemented pytest-integration stubs |
| `src/pgsnap/AGENTS.md` | Logging conventions scoped to this package |
| `tests/test_core.py` | Inheritance tests for the `Snapshot` taxonomy |
| `docs/` | Sphinx + MyST site (Furo theme), published at pytest-pgsnap.git-pull.com |
| `CHANGES` | Changelog; rendered as the docs history page |
| `.github/workflows/` | CI: `tests.yml` (lint/type/test matrix, PyPI release on tag push), `docs.yml` (docs publish) |

## Which policy applies

- Documentation, user-facing text, `CHANGES`, commit messages, docstrings,
  and source comments: [.github/WRITING.md](.github/WRITING.md)
- Environment, the gates, tests, documentation builds, releases, and pull
  requests: [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

Each of those is the single home for its subject. Where a rule seems to be
stated twice, the file listed above is the one that governs.

## Change discipline

- Make the smallest coherent change that solves the verified problem; keep
  unrelated cleanup out of it.
- Reuse an existing file, helper, API, or test before adding a new one.
- Keep new APIs private until a caller outside the module needs them.
- Add a file only for a durable boundary — a distinct responsibility,
  independent reuse, or splitting an oversized module — not for a
  single-use helper or a one-line re-export.
- Add a test for every user-visible behaviour change, and a `CHANGES` entry
  for every change to the public API, CLI, configuration, or output.
- A passing gate is evidence only once it has been shown capable of
  failing. Pair a new test with a deliberate break that proves it bites.

This package registers no pytest plugin, fixture, or marker as of this
version (CHANGES: "The bundled doctest collector is gone"). Do not document
or invent one until it is wired into pytest and tested — see
[Documenting fixtures and markers](.github/WRITING.md#documenting-fixtures-and-markers).
`.md`/`.rst` doctest collection under `docs/` comes from the `gp-libs` dev
dependency, not from this package. The distribution name `pytest-pgsnap`
differs from the import name `pgsnap`.

## References

- Docs: https://pytest-pgsnap.git-pull.com
- Repository: https://github.com/tony/pytest-pgsnap
- PyPI: https://pypi.org/project/pytest-pgsnap/
- Shared tooling: https://gp-libs.git-pull.com
