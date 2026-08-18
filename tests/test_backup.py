"""
=========================================================
Music Collection Manager
Backup Tests
=========================================================

pytest tests for core/backup.py.

Every test isolates itself from the real project folder by
monkeypatching config.DATABASE_FILE / config.BACKUP_FOLDER to a
pytest tmp_path - none of these touch the real Musi.db or backups/
folder.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import config
from core.backup import backup_database


@pytest.fixture()
def isolated_backup_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path]:
    """
    Point config.DATABASE_FILE and config.BACKUP_FOLDER at a fresh
    tmp_path, with a real (small, fake) database file already in
    place. Returns (database_file, backup_folder).
    """

    database_file = tmp_path / "Musi.db"
    database_file.write_bytes(b"fake sqlite content")

    backup_folder = tmp_path / "backups"

    monkeypatch.setattr(config, "DATABASE_FILE", database_file)
    monkeypatch.setattr(config, "BACKUP_FOLDER", backup_folder)
    monkeypatch.setattr(config, "AUTO_BACKUP", True)
    monkeypatch.setattr(config, "MAX_BACKUPS", 30)

    return database_file, backup_folder


def test_backup_disabled_creates_nothing(
    isolated_backup_env: tuple[Path, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, backup_folder = isolated_backup_env
    monkeypatch.setattr(config, "AUTO_BACKUP", False)

    backup_database()

    assert not backup_folder.exists()


def test_backup_skipped_when_database_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    missing_database = tmp_path / "DoesNotExist.db"
    backup_folder = tmp_path / "backups"

    monkeypatch.setattr(config, "DATABASE_FILE", missing_database)
    monkeypatch.setattr(config, "BACKUP_FOLDER", backup_folder)
    monkeypatch.setattr(config, "AUTO_BACKUP", True)

    backup_database()

    assert not any(backup_folder.glob("Musi_*.db"))


def test_backup_creates_timestamped_copy(
    isolated_backup_env: tuple[Path, Path],
) -> None:
    database_file, backup_folder = isolated_backup_env

    backup_database()

    backups = list(backup_folder.glob("Musi_*.db"))
    assert len(backups) == 1
    assert backups[0].read_bytes() == database_file.read_bytes()


def test_backup_keeps_only_max_backups(
    isolated_backup_env: tuple[Path, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, backup_folder = isolated_backup_env
    monkeypatch.setattr(config, "MAX_BACKUPS", 2)
    backup_folder.mkdir(exist_ok=True)

    # Pre-seed 3 fake older backups with distinct, sortable names -
    # more than MAX_BACKUPS, so the very next backup_database() call
    # must prune down to 2 total.
    for name in ["Musi_20200101_000000.db", "Musi_20200102_000000.db", "Musi_20200103_000000.db"]:
        (backup_folder / name).write_bytes(b"old backup")

    backup_database()

    remaining = sorted(backup_folder.glob("Musi_*.db"))
    assert len(remaining) == 2


def test_backup_prunes_oldest_first(
    isolated_backup_env: tuple[Path, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, backup_folder = isolated_backup_env
    monkeypatch.setattr(config, "MAX_BACKUPS", 2)
    backup_folder.mkdir(exist_ok=True)

    # Both of these are in the past relative to any real "now" this
    # test could run in, so the fresh backup backup_database() is
    # about to create is always the newest of the three - keeping
    # this test's outcome independent of the actual current date.
    older = backup_folder / "Musi_20200101_000000.db"
    newer = backup_folder / "Musi_20240101_000000.db"
    older.write_bytes(b"older")
    newer.write_bytes(b"newer")

    backup_database()

    remaining = {p.name for p in backup_folder.glob("Musi_*.db")}
    assert older.name not in remaining
    assert newer.name in remaining
    assert len(remaining) == 2