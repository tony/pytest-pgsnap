# pytest-pgsnap &middot; [![Python Package](https://img.shields.io/pypi/v/pytest-pgsnap.svg)](https://pypi.org/project/pytest-pgsnap/) [![License](https://img.shields.io/github/license/tony/pytest-pgsnap.svg)](https://github.com/tony/pytest-pgsnap/blob/main/LICENSE) [![Code Coverage](https://codecov.io/gh/tony/pytest-pgsnap/branch/main/graph/badge.svg)](https://codecov.io/gh/tony/pytest-pgsnap)

pytest-pgsnap is an early-stage toolkit for caching side effects — especially
small PostgreSQL databases — across pytest runs instead of rebuilding them
every time.

At this version it ships a `Snapshot` class taxonomy and nothing that runs
yet: no pytest entry point, no fixture, and no marker is registered.
Installing this package does not add a pytest plugin. See "What this ships
today" below.

## Install

```console
$ pip install --user pytest-pgsnap
```

The distribution is `pytest-pgsnap`; the package imports as `pgsnap`.

### Developmental releases

You can test the unpublished version of pytest-pgsnap before it is
released.

- [pip](https://pip.pypa.io/en/stable/):

  ```console
  $ pip install --user --upgrade --pre pytest-pgsnap
  ```

## What this ships today

`pgsnap.core` sketches a strategy ladder for caching a side effect instead
of recreating it on every test run: `Snapshot` is the base, with
`FileSnapshot` and `DBSnapshot` as the two storage families, and three
PostgreSQL-specific `DBSnapshot` strategies underneath:

- **SQL emission** (`PostgresDBSnapshotSQLEmission`) — records the SQL a
  test issues and replays it on a cache hit. Incremental, but fragile if
  the recorded statements drift from what actually runs.
- **Dump/restore** (`PostgresDBSnapshotDump`) — `pg_dump` on cache set,
  `pg_restore` on cache hit. Guarantees the whole database's state, at the
  cost of storing and restoring it in full.
- **Template copy** (`PostgresDBSnapshotTemplate`) — saves the database as
  a template and creates new databases from it. The fastest cache hit, but
  requires a parallel database and its own pruning.

`PytestFixtureCache` and `SideEffectMark` sketch how a caller would consume
these strategies as a pytest fixture and a cache marker, but neither is
wired into pytest: there is no `pytest11` entry point, and importing
`pgsnap` registers nothing with a running test session.

## More information

- Python support: `>=3.10,<4.0`
- Source: <https://github.com/tony/pytest-pgsnap>
- Docs: <https://pytest-pgsnap.git-pull.com>
- Changelog: <https://pytest-pgsnap.git-pull.com/history.html>
- Issues: <https://github.com/tony/pytest-pgsnap/issues>
- Test Coverage: <https://codecov.io/gh/tony/pytest-pgsnap>
- pypi: <https://pypi.python.org/pypi/pytest-pgsnap>
- License: [MIT](https://opensource.org/licenses/MIT).

[![Docs](https://github.com/tony/pytest-pgsnap/workflows/docs/badge.svg)](https://pytest-pgsnap.git-pull.com)
[![Build Status](https://github.com/tony/pytest-pgsnap/workflows/tests/badge.svg)](https://github.com/tony/pytest-pgsnap/actions?query=workflow%3A%22tests%22)
