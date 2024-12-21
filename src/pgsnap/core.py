"""pgsnap: Snapshot databases fast

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
