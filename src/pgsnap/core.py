"""pgsnap: Snapshot databases fast.

Intended for small databases.

Abstracts different DB snapshot methods. The fastest one is templates, but it requires
a parallel DB.
"""


class Snapshot:
    """Base class for a way to snapshot a third party side effect.

    When do I know when I need it? Cost-benefit analysis:

    - If it's worth the storage of caching, repetively used, with stable state.
    - How complex the data is detect cache of

      Example:
      - Direct cache key
      - Hash of pytest fixture and ancestor fixtures
    """


class FileSnapshot(Snapshot):
    """Base class for a way to snapshot a file state.

    Example case:
    - Downloaded files
    - Initialized or clone VCS repositories
    - Encoded images or videos
    """


class DBSnapshot(Snapshot):
    """Base class for a way to snapshot a database state."""


"""
# Types of caching
Type of caching, simple to complex.

2 main types:
- Output
  - Instrumentation: Happens at end of tests
  - Types of storage:
    - File / folders
    - Database storage
  - On cache hit: Copies or imports (with fast strategies like TEMPLATE on postgres)
- Playback
  - Instrumentation: Records queries within test
  - Cache hit: Runs / publishes queries
"""


class PostgresDBSnapshotSQLEmission(DBSnapshot):
    """Record SQL generated. On cache hit, execute SQL directly.

    Upsides: Incremental deltas.
    Downsides: Potentially fragile.

    Record behavior: All SQL insert, update queries
    Cache hit behavior: Runs SQL
    Special notes: Recorder. Monitors SQL throughout test.
    """


class PostgresDBSnapshotDump(DBSnapshot):
    """Snapshot DB. On cache hit, pg_restore(1), SQL.

    Upsides: Guaranteed state of whole DB
    Downsides: Stores whole db to dump, has to be restored

    Cache set behavior: pg_dump
    Cache hit behavior: pg_restore
    """


class PostgresDBSnapshotTemplate(DBSnapshot):
    """Snapshot DB via Template.

    Upsides: Fast, premier solution
    Downsides:
    - Overhead: Must be stored in postgres DB for access
    - Pruning / nuking old DBs

    Cache set behavior: Saves DB in a new db, named after cache hit
    Cache hit behavior: Creates DB from template
    """
