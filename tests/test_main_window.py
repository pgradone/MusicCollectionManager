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
from pathlib import Path
from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QApplication, QDialog, QListWidget, QTableWidget

from core.relationship_operations import link, list_related, unlink
from core.relationships import JUNCTION, discover_relationships
from main import SOFT_FOREIGN_KEYS, MainWindow
from core.repository import repository_for

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATABASE = PROJECT_ROOT / "tests" / "Musi_crud_test.db"


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture(scope="module")
def qapp() -> Iterator[QApplication]:
    """Provide a single QApplication instance for this module."""

    app = QApplication.instance()

    if not isinstance(app, QApplication):
        app = QApplication([])

    yield app


@pytest.fixture()
def window(qapp: QApplication) -> MainWindow:
    """Provide a constructed MainWindow, connected to the real database."""

    return MainWindow()


@pytest.fixture()
def crud_window(qapp: QApplication) -> Iterator[MainWindow]:
    """
    Provide a constructed MainWindow redirected to the dedicated CRUD
    test database, restoring the singleton's original database path
    afterwards so later tests are unaffected.
    """

    if not TEST_DATABASE.exists():
        raise FileNotFoundError(
            f"Test database not found:\n{TEST_DATABASE}"
        )

    win = MainWindow()
    original_path = win.db.database

    win.db.database = TEST_DATABASE
    win.context.refresh_schema()

    try:
        yield win
    finally:
        win.db.database = original_path


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

# ============================================================
# Junction UI write paths (Milestone 4A (2/N))
# ============================================================
#
# These run against the dedicated CRUD test database and clean up
# whatever they create, exactly like tests/test_services.py.


def _sing_relationship(window: MainWindow):
    return next(
        r
        for r in discover_relationships(
            window.context, "Artists", soft_foreign_keys=SOFT_FOREIGN_KEYS
        )
        if r.kind == JUNCTION and r.target_table == "Songs"
    )


def _contain_relationship(window: MainWindow):
    return next(
        r
        for r in discover_relationships(
            window.context, "Records", soft_foreign_keys=SOFT_FOREIGN_KEYS
        )
        if r.kind == JUNCTION and r.target_table == "Songs"
    )


def test_add_junction_relation_creates_link(
    crud_window: MainWindow,
) -> None:
    artists = repository_for(crud_window.context, "Artists")
    songs = repository_for(crud_window.context, "Songs")
    existing_song = songs.all(limit=1)[0]

    artist_id = artists.insert({"Surname": "AddViaUI"}, commit=True)
    relationship = _sing_relationship(crud_window)

    def fake_exec(dialog: QDialog) -> QDialog.DialogCode:
        list_widget = dialog.findChild(QListWidget)
        assert list_widget is not None
        # The dialog lists every song ordered by SongID - select
        # whichever row corresponds to our known existing_song.
        for i in range(list_widget.count()):
            if list_widget.item(i).text().startswith(
                str(existing_song["SongID"])
            ):
                list_widget.setCurrentRow(i)
                break
        return QDialog.DialogCode.Accepted

    try:
        crud_window.load_table_data("Artists")
        row_idx = next(
            r
            for r in range(len(crud_window.table_rows))
            if crud_window.table_rows[r]["ArtistID"] == artist_id
        )
        crud_window.table_widget.selectRow(row_idx)

        tab_widget = crud_window.related_tabs.widget(0)
        assert tab_widget is not None
        table_widget = tab_widget.findChild(QTableWidget)
        assert table_widget is not None

        with patch.object(QDialog, "exec", fake_exec):
            crud_window._add_junction_relation(
                relationship, artist_id, False, table_widget
            )

        linked = list_related(crud_window.context, relationship, artist_id)
        assert [row["SongID"] for row in linked] == [
            existing_song["SongID"]
        ]
    finally:
        unlink(
            crud_window.context, relationship, artist_id, existing_song["SongID"]
        )
        artists.delete(artist_id, commit=True)


def test_delete_junction_relation_removes_link(
    crud_window: MainWindow,
) -> None:
    artists = repository_for(crud_window.context, "Artists")
    songs = repository_for(crud_window.context, "Songs")
    existing_song = songs.all(limit=1)[0]

    artist_id = artists.insert({"Surname": "DeleteViaUI"}, commit=True)
    relationship = _sing_relationship(crud_window)
    link(crud_window.context, relationship, artist_id, existing_song["SongID"])

    try:
        crud_window.load_table_data("Artists")
        row_idx = next(
            r
            for r in range(len(crud_window.table_rows))
            if crud_window.table_rows[r]["ArtistID"] == artist_id
        )
        crud_window.table_widget.selectRow(row_idx)

        tab_widget = crud_window.related_tabs.widget(0)
        assert tab_widget is not None
        table_widget = tab_widget.findChild(QTableWidget)
        assert table_widget is not None
        table_widget.selectRow(0)

        display_columns = ["SongID", "Title", "BPM", "Year", "Time"]
        crud_window._delete_junction_relation(
            relationship, artist_id, display_columns, table_widget
        )

        assert (
            list_related(crud_window.context, relationship, artist_id) == []
        )
    finally:
        artists.delete(artist_id, commit=True)


def test_swap_junction_position_exchanges_positions(
    crud_window: MainWindow,
) -> None:
    records = repository_for(crud_window.context, "Records")
    songs = repository_for(crud_window.context, "Songs")
    song_a, song_b = songs.all(limit=2)

    record_id = records.insert({"Title": "SwapViaUI"}, commit=True)
    relationship = _contain_relationship(crud_window)
    link(
        crud_window.context, relationship, record_id, song_a["SongID"],
        extra_values={"Position": "1"},
    )
    link(
        crud_window.context, relationship, record_id, song_b["SongID"],
        extra_values={"Position": "2"},
    )

    try:
        crud_window.load_table_data("Records")
        row_idx = next(
            r
            for r in range(len(crud_window.table_rows))
            if crud_window.table_rows[r]["RecordID"] == record_id
        )
        crud_window.table_widget.selectRow(row_idx)

        tab_widget = crud_window.related_tabs.widget(0)
        assert tab_widget is not None
        table_widget = tab_widget.findChild(QTableWidget)
        assert table_widget is not None
        table_widget.selectRow(0)  # song_a, currently Position "1"

        crud_window._swap_junction_position(
            relationship, record_id, table_widget, 1
        )

        positions = {
            row["SongID"]: str(row["Position"])
            for row in list_related(crud_window.context, relationship, record_id)
        }
        assert positions[song_a["SongID"]] == "2"
        assert positions[song_b["SongID"]] == "1"
    finally:
        unlink(crud_window.context, relationship, record_id, song_a["SongID"])
        unlink(crud_window.context, relationship, record_id, song_b["SongID"])
        records.delete(record_id, commit=True)


def test_renumber_junction_positions_assigns_sequential_values(
    crud_window: MainWindow,
) -> None:
    records = repository_for(crud_window.context, "Records")
    songs = repository_for(crud_window.context, "Songs")
    song_a, song_b = songs.all(limit=2)

    record_id = records.insert({"Title": "RenumberViaUI"}, commit=True)
    relationship = _contain_relationship(crud_window)
    # Deliberately non-sequential, unsorted-looking starting positions.
    link(
        crud_window.context, relationship, record_id, song_a["SongID"],
        extra_values={"Position": "5"},
    )
    link(
        crud_window.context, relationship, record_id, song_b["SongID"],
        extra_values={"Position": "10"},
    )

    try:
        crud_window.load_table_data("Records")
        row_idx = next(
            r
            for r in range(len(crud_window.table_rows))
            if crud_window.table_rows[r]["RecordID"] == record_id
        )
        crud_window.table_widget.selectRow(row_idx)

        tab_widget = crud_window.related_tabs.widget(0)
        assert tab_widget is not None
        table_widget = tab_widget.findChild(QTableWidget)
        assert table_widget is not None

        crud_window._renumber_junction_positions(
            relationship, record_id, table_widget
        )

        positions = {
            row["SongID"]: str(row["Position"])
            for row in list_related(crud_window.context, relationship, record_id)
        }
        assert sorted(positions.values()) == ["1", "2"]
    finally:
        unlink(crud_window.context, relationship, record_id, song_a["SongID"])
        unlink(crud_window.context, relationship, record_id, song_b["SongID"])
        records.delete(record_id, commit=True)


# ============================================================
# Direct-relationship (FK) double-click navigation (Milestone 4A (3/N))
# ============================================================


def test_direct_cell_links_matches_expected_per_table(
    window: MainWindow,
) -> None:
    expected = {
        "Artists": {},
        "Songs": {},
        "Records": {"ArtistID": "Artists"},
        "Styles": {},
        "Programs": {},
    }

    for table, links in expected.items():
        window.current_table = table
        assert window._direct_cell_links() == links


def _select_table_via_combo(window: MainWindow, table: str) -> None:
    """
    Switch tables the way a real user would - through the combo box -
    so window.table_combo and window.current_table stay in sync.
    Calling load_table_data() directly leaves the combo pointed at
    its old selection, which breaks _navigate_to_related_value()'s
    own findText()-based lookup.
    """

    index = window.table_combo.findText(table)
    assert index >= 0
    window.table_combo.setCurrentIndex(index)


def test_grid_double_click_navigates_to_linked_artist(
    window: MainWindow,
) -> None:
    _select_table_via_combo(window, "Records")

    row_index, artist_id = next(
        (r, row["ArtistID"])
        for r, row in enumerate(window.table_rows)
        if row.get("ArtistID")
    )
    col = window.column_names.index("ArtistID")

    window._on_main_table_double_clicked(row_index, col)

    assert window.current_table == "Artists"
    assert window.current_row is not None
    assert window.current_row["ArtistID"] == artist_id


def test_form_field_double_click_navigates_to_linked_artist(
    window: MainWindow,
) -> None:
    _select_table_via_combo(window, "Records")

    row_index, artist_id = next(
        (r, row["ArtistID"])
        for r, row in enumerate(window.table_rows)
        if row.get("ArtistID")
    )
    window.table_widget.selectRow(row_index)

    window._on_form_field_double_clicked("ArtistID", "Artists")

    assert window.current_table == "Artists"
    assert window.current_row is not None
    assert window.current_row["ArtistID"] == artist_id
