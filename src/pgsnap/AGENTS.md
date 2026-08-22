# AGENTS.md — `src/pgsnap`

Logging conventions for this package. These rules guide future logging
changes; existing code may not yet conform. Everything else that applies
here is set by the root [AGENTS.md](../../AGENTS.md).

## Logger setup

- Use `logging.getLogger(__name__)` in every module.
- Add `NullHandler` in library `__init__.py` files.
- Never configure handlers, levels, or formatters in library code — that
  is the application's job.

## Structured context via `extra`

Pass structured data on every log call where useful for filtering,
searching, or test assertions.

**Core keys** (stable, scalar, safe at any log level):

| Key | Type | Context |
| --- | --- | --- |
| `pgsnap_fixture` | `str` | fixture name |
| `pgsnap_snapshot_type` | `str` | snapshot type (file, postgres) |
| `pgsnap_db_name` | `str` | database name |

Treat established keys as compatibility-sensitive — downstream users may
build dashboards and alerts on them. Change deliberately.

## Key naming rules

- `snake_case`, not dotted; `pgsnap_` prefix.
- Prefer stable scalars; avoid ad-hoc objects.

## Lazy formatting

`logger.debug("msg %s", val)` not f-strings. Two rationales:

- Deferred string interpolation: skipped entirely when the level is
  filtered.
- Aggregator message template grouping: `"Running %s"` is one signature
  grouped ×10,000; f-strings make each line unique.

When computing `val` itself is expensive, guard with
`if logger.isEnabledFor(logging.DEBUG)`.

## `stacklevel` for wrappers

Increment for each wrapper layer so `%(filename)s:%(lineno)d` and OTel
`code.filepath` point to the real caller. Verify whenever call depth
changes.

## Log levels

| Level | Use for | Examples |
| --- | --- | --- |
| `DEBUG` | Internal mechanics | Snapshot comparison steps, fixture setup |
| `INFO` | Lifecycle, user-visible operations | Snapshot created, database restored |
| `WARNING` | Recoverable issues, deprecation | Missing snapshot file, deprecated option |
| `ERROR` | Failures that stop an operation | Database connection failed, snapshot mismatch |

## Message style

- Lowercase, past tense for events: `"snapshot created"`,
  `"database restored"`.
- No trailing punctuation.
- Keep messages short; put details in `extra`, not the message string.

## Exception logging

- Use `logger.exception()` only inside `except` blocks when **not**
  re-raising.
- Use `logger.error(..., exc_info=True)` when the traceback is needed
  outside an `except` block.
- Avoid `logger.exception()` followed by `raise` — this duplicates the
  traceback. Either add context via `extra` that would otherwise be lost,
  or let the exception propagate.

## Testing logs

Assert on `caplog.records` attributes, not string matching on
`caplog.text`:

- Scope capture: `caplog.at_level(logging.DEBUG, logger="pgsnap")`.
- Filter records rather than index by position:
  `[r for r in caplog.records if hasattr(r, "pgsnap_fixture")]`.
- Assert on schema: `record.pgsnap_db_name == "testdb"`, not
  `"testdb" in caplog.text`.
- `caplog.record_tuples` cannot access extra fields — always use
  `caplog.records`.

## Avoid

- f-strings/`.format()` in log calls.
- Unguarded logging in hot loops (guard with `isEnabledFor()`).
- Catch-log-reraise without adding new context.
- `print()` for diagnostics.
- Logging secret env var values (log key names only).
- Non-scalar ad-hoc objects in `extra`.
- Requiring custom `extra` fields in format strings without safe defaults
  (missing keys raise `KeyError`).
