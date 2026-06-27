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
- Python 3.10+ (tool-versions lists interpreters up to 3.14)
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
- Prefer `pathlib.Path` over `os.path`; use f-strings for interpolation; keep Python ≥3.10 compatibility in mind.

## Doctests

**All functions and methods MUST have working doctests.** Doctests serve as both documentation and tests.

**CRITICAL RULES:**
- Doctests MUST actually execute - never comment out function calls or similar
- Doctests MUST NOT be converted to `.. code-block::` as a workaround (code-blocks don't run)
- If you cannot create a working doctest, **STOP and ask for help**

**Available tools for doctests:**
- `doctest_namespace` fixtures: `tmp_path`
- Ellipsis for variable output: `# doctest: +ELLIPSIS`
- Update `conftest.py` to add new fixtures to `doctest_namespace`

**`# doctest: +SKIP` is NOT permitted** - it's just another workaround that doesn't test anything. Use fixtures properly.

**Note:** This project has abstract snapshot base classes. Keep complex examples in dedicated tests under `tests/` rather than long doctests. For PostgreSQL-specific examples, use fixtures that mock or stub database operations.

## Logging Standards

These rules guide future logging changes; existing code may not yet conform.

### Logger setup

- Use `logging.getLogger(__name__)` in every module
- Add `NullHandler` in library `__init__.py` files
- Never configure handlers, levels, or formatters in library code — that's the application's job

### Structured context via `extra`

Pass structured data on every log call where useful for filtering, searching, or test assertions.

**Core keys** (stable, scalar, safe at any log level):

| Key | Type | Context |
|-----|------|---------|
| `pgsnap_fixture` | `str` | fixture name |
| `pgsnap_snapshot_type` | `str` | snapshot type (file, postgres) |
| `pgsnap_db_name` | `str` | database name |

Treat established keys as compatibility-sensitive — downstream users may build dashboards and alerts on them. Change deliberately.

### Key naming rules

- `snake_case`, not dotted; `pgsnap_` prefix
- Prefer stable scalars; avoid ad-hoc objects

### Lazy formatting

`logger.debug("msg %s", val)` not f-strings. Two rationales:
- Deferred string interpolation: skipped entirely when level is filtered
- Aggregator message template grouping: `"Running %s"` is one signature grouped ×10,000; f-strings make each line unique

When computing `val` itself is expensive, guard with `if logger.isEnabledFor(logging.DEBUG)`.

### stacklevel for wrappers

Increment for each wrapper layer so `%(filename)s:%(lineno)d` and OTel `code.filepath` point to the real caller. Verify whenever call depth changes.

### Log levels

| Level | Use for | Examples |
|-------|---------|----------|
| `DEBUG` | Internal mechanics | Snapshot comparison steps, fixture setup |
| `INFO` | Lifecycle, user-visible operations | Snapshot created, database restored |
| `WARNING` | Recoverable issues, deprecation | Missing snapshot file, deprecated option |
| `ERROR` | Failures that stop an operation | Database connection failed, snapshot mismatch |

### Message style

- Lowercase, past tense for events: `"snapshot created"`, `"database restored"`
- No trailing punctuation
- Keep messages short; put details in `extra`, not the message string

### Exception logging

- Use `logger.exception()` only inside `except` blocks when you are **not** re-raising
- Use `logger.error(..., exc_info=True)` when you need the traceback outside an `except` block
- Avoid `logger.exception()` followed by `raise` — this duplicates the traceback. Either add context via `extra` that would otherwise be lost, or let the exception propagate

### Testing logs

Assert on `caplog.records` attributes, not string matching on `caplog.text`:
- Scope capture: `caplog.at_level(logging.DEBUG, logger="pytest_pgsnap")`
- Filter records rather than index by position: `[r for r in caplog.records if hasattr(r, "pgsnap_fixture")]`
- Assert on schema: `record.pgsnap_db_name == "testdb"` not `"testdb" in caplog.text`
- `caplog.record_tuples` cannot access extra fields — always use `caplog.records`

### Avoid

- f-strings/`.format()` in log calls
- Unguarded logging in hot loops (guard with `isEnabledFor()`)
- Catch-log-reraise without adding new context
- `print()` for diagnostics
- Logging secret env var values (log key names only)
- Non-scalar ad-hoc objects in `extra`
- Requiring custom `extra` fields in format strings without safe defaults (missing keys raise `KeyError`)

## Git Commit Standards

Format commit messages as:
```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject ≤50 chars (excluding any trailing `(#NN)` PR ref); wrap
body lines at ≤72 chars. Separate the `why:` and `what:` blocks with a
blank line.

Common commit types:
- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev Dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (CLAUDE.md)
- **ai(claude[command])**: Claude Code command changes

## Changelog Conventions

These rules apply when authoring entries in `CHANGES`, which is rendered as the Sphinx changelog page. Modeled on Django's release-notes shape — deliverables get titles and prose, not bullets. Older entries used a flat `### Section` + bullet shape; new entries follow the Django shape below.

**Release entry boilerplate.** Every release header is `## pytest-pgsnap X.Y.Z (YYYY-MM-DD)`. The file opens with a `## pytest-pgsnap X.Y.Z (unreleased)` placeholder block fenced by `<!-- KEEP THIS PLACEHOLDER ... -->` and `<!-- END PLACEHOLDER ... -->` HTML comments — new release entries land immediately below the END marker, never above it.

**Open with a multi-sentence lead paragraph.** Plain prose, no italic. Open with the version as sentence subject (*"pytest-pgsnap X.Y.Z ships …"*) so the lead is self-contained when excerpted. Two to four sentences telling the reader what shipped and who cares — user-visible takeaways, not internal mechanism. Cross-reference detail docs with `{ref}` to keep the lead compact.

**Each deliverable is a section, not a bullet.** Inside `### What's new`, every distinct deliverable gets a `#### Deliverable title (#NN)` heading naming it in user vocabulary, followed by 1-3 prose paragraphs explaining what shipped. Don't wrap a paragraph in `- ` — bullets are for enumerable lists, not paragraph containers. Cross-link detail docs (`See {ref}\`foo\` for details.`) so prose stays focused.

**The deliverable test.** Before writing an entry, ask: "What's the deliverable, in user vocabulary?" If you can't answer in one sentence, the entry isn't ready. Mechanism (helper internals, byte counters, schema-validation locations) belongs in PR descriptions and code comments, not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`, `### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`, `### Development`. Dev tooling (helper scripts, internal automation) lives under `### Development`. For breaking changes, show the migration path with concrete inline code (e.g. a `# Before` / `# After` fenced code block). Dependency floor bumps use the form ``Minimum `pkg>=X.Y.Z` (was `>=X.Y.W`)``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`, occasionally `### Documentation`) with 3+ genuinely small items use bullets — one line each, never paragraphs. If a bullet swells past two lines, promote it to a `#### Title (#NN)` heading with prose body.

**Anti-patterns.**

- Fragile metrics: token ceilings, third-party version pins, percent benchmarks, exact byte counts. Describe the *capability*, not the math.
- Internal jargon: private symbols (leading-underscore identifiers), algorithm names exposed for the first time, backend scaffolding.
- Walls of text dressed up as bullets.
- Buried breaking changes — they get their own subheading at the top of the entry.

**Always link autodoc'd APIs.** Any class, method, function, exception, or attribute that has its own rendered page must be cited via the appropriate role (`{class}`, `{meth}`, `{func}`, `{exc}`, `{attr}`) — never with plain backticks. Doc pages without explicit ref labels use `{doc}`. Plain backticks are correct for code syntax, env vars, parameter names, and file paths that aren't doc pages — anything without an autodoc destination.

**MyST roles.** Class references use `{class}`, methods use `{meth}`, functions use `{func}`, exceptions use `{exc}`, attributes use `{attr}`, internal anchors use `{ref}`, doc-path links use `{doc}`.

**Summarization style.** When a user asks "what changed in the latest version?" or similar, lead with the entry's lead paragraph (paraphrased if needed), followed by each `####` deliverable heading under `### What's new` with a one-sentence summary. Cite `(#NN)` only if the user asks for source links. Don't invent versions, dates, or numbers not present in `CHANGES`. Don't quote line numbers or file offsets — those shift as the file evolves.

## References

- Docs: https://pytest-pgsnap.git-pull.com
- Repository: https://github.com/tony/pytest-pgsnap
- PyPI: https://pypi.org/project/pytest-pgsnap/
- Shared tooling: https://gp-libs.git-pull.com

## AI Slop Prevention

Treat AI slop as **review-hostile noise**, not as proof that text or
code is wrong. The goal is to maximize information density by removing
artifacts that make the repository harder to trust or navigate.

### The Anti-Slop Rubric

Before committing, audit all AI-assisted changes for these noise
patterns:

- **AI Signatures:** Remove "Generated by", footers, conversational
  filler ("Certainly!", "Here is..."), unexplained emojis (🤖, ✨), and
  AI-tool metadata.
- **Brittle References:** Avoid hard-coded line numbers, fragile
  file/test counts, dated "as of" claims, bare SHAs, and local
  absolute paths unless they are strict evidentiary artifacts (e.g.,
  benchmark logs).
- **Diff Narration:** Do not restate what moved, was renamed, or was
  removed in artifacts the downstream reader holds: code, docstrings,
  README, CHANGES, PR descriptions, or release notes. The diff and
  commit message already carry this history.
- **Branch-Internal Narrative:** Do not mention intermediate branch
  states, abandoned approaches, or "no longer" behavior unless users
  of a published release actually experienced the old state (**The
  Published-Release Test**).
- **Low-Value Scaffolding:** Remove ownerless TODOs (`TODO: revisit`),
  unused future-proofing, debug artifacts, and defensive wrappers that
  do not protect a currently reachable failure mode.
- **Prose Inflation:** Replace generic AI "tells" like *comprehensive,
  robust, seamless, production-ready, leverage, delve, tapestry,* and
  *best practices* with concrete descriptions of behavior,
  constraints, or trade-offs.

### Preservation & Context

**When unsure, leave the text in place and ask.** Subjective cleanup
must never be a reason to remove load-bearing rationale.

- **Preserve the "Why":** You MUST NOT delete comments that document
  invariants, protocol constraints, platform quirks, security
  boundaries, and upstream workarounds.
- **Evidence is Immune:** Preserve exact counts, dates, and SHAs when
  they serve as evidence in benchmark results, release notes, stack
  traces, or lockfiles.
- **Behavior Over Inventory:** A useful description explains what
  changed for the *system or user*; it does not provide an inventory
  of files or functions the diff already shows.

### The Published-Release Test

Long-running branches accumulate tactical decisions — renames,
refactors, attempts-then-reverts. When deciding what counts as
branch-internal, use trunk or the parent branch as the baseline — not
intermediate states inside the current branch. Ask:

> Did users of the most recently published release ever experience
> this old name, old behavior, or bug?

If the answer is **no**, it is branch-internal narrative. Move it to
the commit message and describe only the final state in the artifact.

**Keep in shipped artifacts:**
- Deprecations and migration guides for symbols that actually shipped.
- `### Fixes` entries for bugs that affected users of a published
  release.
- Comments explaining *why the current code looks this way*
  (invariants, platform quirks) that make sense to a reader who never
  saw the previous version.

### Cleanup in Hindsight

When applying these rules retroactively from inside a feature branch,
first establish scope by diffing against the parent branch (or trunk)
to identify which commits this branch actually introduced. Then:

- **In-branch commits:** Prompt the user with two options: `fixup!`
  commits with `git rebase --autosquash` to address each causal commit
  at its source, or a single cleanup commit at branch tip.
- **Trunk/Parent commits:** Default to leaving them alone. Act only on
  explicit user instruction. If the user opts in, fold the cleanup
  into a single commit at branch tip; do not rewrite shared history.
- **Scope guard:** If cleaning prior slop would touch a colleague's
  work or expand the branch beyond its stated goal, stay in lane:
  protect the current goal and leave prior slop alone.

