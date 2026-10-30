"""
=========================================================
Music Collection Manager
Startup Tests
=========================================================

Milestone 6C (1/N)

pytest tests for main.run_startup_tasks() and the order main()
runs things in: logging and the automatic backup first, then the
window (which opens the database).

Every test points config at pytest's tmp_path, so no real backups/
or logs/ folder is touched, and restores the root logger afterwards
(initialise_logger() adds handlers to a process-wide singleton).
No QApplication is created: main()'s Qt pieces are replaced.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import config
import main as app_main


@pytest.fixture()
def startup_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Iterator[dict[str, Path]]:
    """A throwaway database, backup folder and log folder."""

    database_file = tmp_path / "Musi.db"
    database_file.write_bytes(b"fake sqlite content")

    paths = {
        "database": database_file,
        "backups": tmp_path / "backups",
        "logs": tmp_path / "logs",
    }

    monkeypatch.setattr(config, "DATABASE_FILE", paths["database"])
    monkeypatch.setattr(config, "BACKUP_FOLDER", paths["backups"])
    monkeypatch.setattr(config, "LOG_FOLDER", paths["logs"])
    monkeypatch.setattr(config, "AUTO_BACKUP", True)
    monkeypatch.setattr(config, "MAX_BACKUPS", 30)

    root = logging.getLogger()
    original_handlers = list(root.handlers)
    original_level = root.level

    yield paths

    for handler in list(root.handlers):
        if handler not in original_handlers:
            root.removeHandler(handler)
            handler.close()

    root.setLevel(original_level)


def read_log(paths: dict[str, Path]) -> str:
    return (paths["logs"] / "music_collection.log").read_text(encoding="utf-8")


def test_startup_creates_log_and_backup(startup_env: dict[str, Path]) -> None:
    app_main.run_startup_tasks()

    backups = list(startup_env["backups"].glob("Musi_*.db"))
    assert len(backups) == 1
    assert backups[0].read_bytes() == b"fake sqlite content"

    log_text = read_log(startup_env)
    assert "Music Collection Manager started." in log_text
    assert f"Database backed up to {backups[0].name}" in log_text


def test_startup_with_backups_disabled_logs_that_it_skipped(
    startup_env: dict[str, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(config, "AUTO_BACKUP", False)

    app_main.run_startup_tasks()

    assert not startup_env["backups"].exists()
    assert "Automatic backup skipped" in read_log(startup_env)


def test_startup_without_a_database_file_skips_the_backup(
    startup_env: dict[str, Path],
) -> None:
    startup_env["database"].unlink()

    app_main.run_startup_tasks()

    assert not list(startup_env["backups"].glob("Musi_*.db"))
    assert "Automatic backup skipped" in read_log(startup_env)


def test_a_failed_backup_is_logged_and_does_not_stop_startup(
    startup_env: dict[str, Path],
) -> None:
    with patch(
        "main.backup_database", side_effect=PermissionError("disk is read-only")
    ):
        app_main.run_startup_tasks()  # must not raise

    log_text = read_log(startup_env)
    assert "Automatic backup failed: disk is read-only" in log_text
    assert "Database backed up" not in log_text


def test_main_runs_startup_tasks_before_the_window_is_created() -> None:
    order: list[str] = []

    with patch(
        "main.run_startup_tasks", side_effect=lambda: order.append("startup")
    ), patch(
        "main.MainWindow", side_effect=lambda: order.append("window") or MagicMock()
    ), patch("main.QApplication") as qapplication:
        qapplication.instance.return_value.exec.return_value = 0

        assert app_main.main() == 0

    # The backup has to copy a database nothing has opened yet.
    assert order == ["startup", "window"]
