# Contributing

Thanks for looking. This project is an early-stage snapshot-strategy
taxonomy, not a working pytest plugin yet — bug reports with a
reproduction, and notes on where this documentation or the `Snapshot`
class hierarchy misled you, are the most useful contributions right now.

How this project writes prose — README, `CHANGES`, commit messages,
docstrings, and source comments — is set out separately in
[WRITING.md](WRITING.md). Read that before changing any of it. The
constraints every change is held to, and the map of what is where, are in
[AGENTS.md](../AGENTS.md).

## Getting set up

```console
$ uv sync --all-extras --dev
```

## The gates

CI (`.github/workflows/tests.yml`) is the order of record; every gate it
runs has to pass before a change is done.

Lint:

```console
$ uv run ruff check .
```

Format:

```console
$ uv run ruff format . --check
```

Type-check:

```console
$ uv run mypy .
```

Test:

```console
$ uv run pytest
```

CI additionally runs the test gate with coverage capture:
`uv run pytest --cov=./ --cov-report=xml`.

Documentation is a gate, not a courtesy. Examples in docstrings and
documentation pages are executed by `pytest`; the doctest flags live in
`pyproject.toml`, so there is no separate doctest step and a green
`pytest` is the proof. Which blocks qualify, and the one mistake that
silently removes a test, are in
[WRITING.md](WRITING.md#documented-examples-that-run).

Before claiming a test or a gate works, show it failing. A gate that has
never been red is an assumption.

## Tests

The suite (`tests/test_core.py`) is pure Python: it asserts the
inheritance relationships of the `Snapshot` class taxonomy in
`src/pgsnap/core.py`. It needs no live PostgreSQL, no network access, and
no fixtures beyond what pytest provides by default — there is no
`conftest.py` anywhere in this repository.

The `dev` dependency group also installs `pytest-mock` and
`pytest-rerunfailures` for when the suite needs them, and
`pytest-watcher` for a watch loop:

```console
$ uv run ptw
```

## Documentation

Docs are Sphinx + MyST, themed with Furo, built from `docs/`:

```console
$ cd docs && uv run sphinx-build -b html . _build/html
```

`docs/index.md` includes `README.md` verbatim, so a README heading that
is deep-linked from the published site must keep its anchor. `AGENTS.md`
and `CLAUDE.md` are excluded from the build (`docs/conf.py`).

## Releasing

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow. See
[Release commits](WRITING.md#release-commits).

Pushing a version tag runs the `release` job in
`.github/workflows/tests.yml`: it builds the package with `uv build` and
publishes to PyPI through `pypa/gh-action-pypi-publish` using a repository
secret.

## Pull requests

One subject per pull request. Unrelated cleanup found along the way
belongs in its own commit, and usually in its own pull request.

Discuss a substantial change via an issue before making it.

Commit format is in [WRITING.md](WRITING.md#commits).

## Decorum

- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of
  personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should
  always assume good intentions.
- Behaviour which can be reasonably considered harassment will not be
  tolerated.

Based on [Ruby's Community Conduct Guideline](https://www.ruby-lang.org/en/conduct/).

## Security

Please do not open a public issue for a vulnerability. This repository
has no `SECURITY.md`; use GitHub's private vulnerability reporting (the
"Report a vulnerability" action under the repository's Security tab)
instead.
