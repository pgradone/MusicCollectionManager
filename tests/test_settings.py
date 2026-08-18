"""
=========================================================
Music Collection Manager
Settings Tests
=========================================================

pytest tests for core/settings.py.

Every test isolates itself by monkeypatching config.SETTINGS_FILE
to a pytest tmp_path - none of these touch the real project's
settings.json.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import config
from core.settings import Settings


@pytest.fixture()
def settings_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Path:
    path = tmp_path / "settings.json"
    monkeypatch.setattr(config, "SETTINGS_FILE", path)
    return path


def test_first_run_creates_defaults_and_saves_file(
    settings_file: Path,
) -> None:
    settings = Settings()

    assert settings_file.exists()
    assert settings.get("theme") == "light"
    assert settings.get("window_width") == config.WINDOW_WIDTH
    assert settings.get("window_height") == config.WINDOW_HEIGHT
    assert settings.get("maximized") is False


def test_existing_file_is_loaded_as_is(settings_file: Path) -> None:
    settings_file.write_text(
        json.dumps({"theme": "dark", "custom_key": "custom_value"}),
        encoding="utf-8",
    )

    settings = Settings()

    assert settings.get("theme") == "dark"
    assert settings.get("custom_key") == "custom_value"
    # Defaults are only applied on first run (no file yet) - an
    # existing file is trusted as-is, so a key that was never
    # written is simply absent, not backfilled.
    assert settings.get("window_width") is None


def test_get_returns_default_for_missing_key(
    settings_file: Path,
) -> None:
    settings = Settings()

    assert settings.get("does_not_exist") is None
    assert settings.get("does_not_exist", "fallback") == "fallback"


def test_set_persists_to_file(settings_file: Path) -> None:
    settings = Settings()

    settings.set("theme", "dark")

    reloaded = json.loads(settings_file.read_text(encoding="utf-8"))
    assert reloaded["theme"] == "dark"


def test_set_is_visible_to_a_new_instance(settings_file: Path) -> None:
    first = Settings()
    first.set("theme", "dark")
    first.set("custom_key", "custom_value")

    second = Settings()

    assert second.get("theme") == "dark"
    assert second.get("custom_key") == "custom_value"