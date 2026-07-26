"""Tests for the :mod:`pgsnap.core` snapshot taxonomy."""

from __future__ import annotations

import pytest

from pgsnap import core


def test_file_snapshot_is_a_snapshot() -> None:
    """File snapshots share the base snapshot contract."""
    assert issubclass(core.FileSnapshot, core.Snapshot)


def test_db_snapshot_is_a_snapshot() -> None:
    """Database snapshots share the base snapshot contract."""
    assert issubclass(core.DBSnapshot, core.Snapshot)


def test_file_and_db_snapshots_are_siblings() -> None:
    """Neither storage family derives from the other."""
    assert not issubclass(core.FileSnapshot, core.DBSnapshot)
    assert not issubclass(core.DBSnapshot, core.FileSnapshot)


@pytest.mark.parametrize(
    "strategy",
    [
        core.PostgresDBSnapshotSQLEmission,
        core.PostgresDBSnapshotDump,
        core.PostgresDBSnapshotTemplate,
    ],
    ids=["sql-emission", "dump", "template"],
)
def test_postgres_strategies_are_db_snapshots(strategy: type[core.DBSnapshot]) -> None:
    """Every PostgreSQL strategy is selectable wherever a DB snapshot is."""
    assert issubclass(strategy, core.DBSnapshot)


def test_pytest_fixture_cache_is_not_a_snapshot() -> None:
    """The pytest integration consumes snapshots rather than being one."""
    assert not issubclass(core.PytestFixtureCache, core.Snapshot)


def test_side_effect_mark_is_not_a_snapshot() -> None:
    """A side-effect mark labels a snapshot; it does not implement one."""
    assert not issubclass(core.SideEffectMark, core.Snapshot)
