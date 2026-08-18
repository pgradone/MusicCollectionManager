"""
=========================================================
Music Collection Manager
Logger Tests
=========================================================

pytest tests for core/logger.py.

initialise_logger() mutates the root logger, a process-wide
singleton, so every test here restores the root logger's original
handlers/level afterwards - otherwise a handler added by one test
would leak into every later test's logging output for the rest of
the session.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from pathlib import Path

import pytest

import config
from core.logger import initialise_logger


@pytest.fixture()
def clean_root_logger() -> Iterator[None]:
    """Snapshot the root logger's handlers/level and restore them after."""

    root = logging.getLogger()
    original_handlers = list(root.handlers)
    original_level = root.level

    yield

    for handler in list(root.handlers):
        if handler not in original_handlers:
            root.removeHandler(handler)
            handler.close()

    root.setLevel(original_level)


def test_initialise_logger_creates_log_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    clean_root_logger: None,
) -> None:
    monkeypatch.setattr(config, "LOG_FOLDER", tmp_path / "logs")

    initialise_logger()

    logfile = tmp_path / "logs" / "music_collection.log"
    assert logfile.exists()
    assert "Music Collection Manager started." in logfile.read_text(
        encoding="utf-8"
    )


def test_initialise_logger_sets_configured_level(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    clean_root_logger: None,
) -> None:
    monkeypatch.setattr(config, "LOG_FOLDER", tmp_path / "logs")
    monkeypatch.setattr(config, "LOG_LEVEL", "WARNING")

    logger = initialise_logger()

    assert logger.level == logging.WARNING


def test_initialise_logger_adds_file_and_console_handlers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    clean_root_logger: None,
) -> None:
    monkeypatch.setattr(config, "LOG_FOLDER", tmp_path / "logs")

    root_before = len(logging.getLogger().handlers)
    logger = initialise_logger()

    assert len(logger.handlers) == root_before + 2