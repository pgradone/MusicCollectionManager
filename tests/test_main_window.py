"""
=========================================================
Music Collection Manager
MainWindow Smoke Tests
=========================================================

Milestone 4A (1/N)

pytest tests for main.py's MainWindow - specifically the
schema-driven _related_relationships(), which replaced a
hardcoded per-table dict with core.relationships.
discover_relationships().

Read-only against the application's configured database
(the same one MainWindow itself connects to). No INSERT,
UPDATE, or DELETE operations are performed.

Requires a QApplication instance, since PySide6 widgets
cannot be constructed without one - even headlessly, with
QT_QPA_PLATFORM=offscreen set.
"""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from PySide6.QtWidgets import QApplication

from main import MainWindow


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture(scope="module")
def qapp() -> Iterator[QApplication]:
    """Provide a single QApplication instance for this module."""

    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture()
def window(qapp: QApplication) -> MainWindow:
    """Provide a constructed MainWindow, connected to the real database."""

    return MainWindow()


# ============================================================
# _related_relationships: junction relationships are discovered
# ============================================================


@pytest.mark.parametrize(
    ("table", "expected"),
    [
        ("Artists", {("Songs", "Sing")}),
        (
            "Songs",
            {
                ("Artists", "Sing"),
                ("Records", "Contain"),
                ("Styles", "Belong"),
                ("Programs scheduling this Song", "ScheduledPrograms"),
            },
        ),
        ("Records", {("Songs", "Contain")}),
        ("Styles", {("Songs", "Belong")}),
        ("Programs", {("Schedule", "Schedule")}),
    ],
)
def test_related_relationships_matches_expected_set(
    window: MainWindow,
    table: str,
    expected: set[tuple[str, str]],
) -> None:
    window.current_table = table

    assert set(window._related_relationships()) == expected


def test_related_relationships_empty_before_table_selected(
    window: MainWindow,
) -> None:
    window.current_table = ""

    assert window._related_relationships() == []


# ============================================================
# Full load path: tabs build without error for every main table
# ============================================================


@pytest.mark.parametrize(
    ("table", "expected_tab_titles"),
    [
        ("Artists", {"Songs"}),
        (
            "Songs",
            {"Styles", "Records", "Artists", "Programs scheduling this Song"},
        ),
        ("Records", {"Songs"}),
        ("Styles", {"Songs"}),
        ("Programs", {"Schedule"}),
    ],
)
def test_load_table_data_builds_expected_tabs(
    window: MainWindow,
    table: str,
    expected_tab_titles: set[str],
) -> None:
    window.load_table_data(table)

    tab_titles = {
        window.related_tabs.tabText(i)
        for i in range(window.related_tabs.count())
    }

    assert tab_titles == expected_tab_titles
    assert len(window.table_rows) > 0