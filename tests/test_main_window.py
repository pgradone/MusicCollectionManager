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

import csv
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
from openpyxl import load_workbook
from pypdf import PdfReader
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QTableWidget,
)

from core.relationship_operations import link, list_related, unlink
from core.relationships import JUNCTION, discover_relationships
from main import REPORT_DEFINITIONS, SOFT_FOREIGN_KEYS, MainWindow
from services.discogs_service import DiscogsService
from services.program_service import ProgramService
from services.record_service import RecordService
from services.report_service import ReportService
from services.song_service import SongService
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


def test_contain_has_no_swap_or_renumber_controls(
    crud_window: MainWindow,
) -> None:
    """
    Contain.Position is free text (vinyl-side labels like "A1"), not
    a number - the generic subform must not offer numeric-only Move
    Up/Down/Renumber controls for it, since blindly swapping such
    values would silently corrupt them.
    """

    records = repository_for(crud_window.context, "Records")
    songs = repository_for(crud_window.context, "Songs")
    existing_song = songs.all(limit=1)[0]

    record_id = records.insert({"Title": "NoSwapButtonsUITest"}, commit=True)
    relationship = _contain_relationship(crud_window)
    link(
        crud_window.context, relationship, record_id, existing_song["SongID"],
        extra_values={"Position": "A1"},
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
        buttons = {
            b.text() for b in tab_widget.findChildren(QPushButton)
        }
        assert "Move Up" not in buttons
        assert "Move Down" not in buttons
        assert "Renumber" not in buttons
        assert "Add" in buttons
        assert "Remove" in buttons
    finally:
        unlink(crud_window.context, relationship, record_id, existing_song["SongID"])
        records.delete(record_id, commit=True)


def test_contain_position_cell_is_directly_editable(
    crud_window: MainWindow,
) -> None:
    """
    Since Position is free text, a user must be able to type
    directly into the cell - editing it should save through
    _set_junction_field the same way the old numeric spinbox did.
    """

    records = repository_for(crud_window.context, "Records")
    songs = repository_for(crud_window.context, "Songs")
    existing_song = songs.all(limit=1)[0]

    record_id = records.insert({"Title": "EditPositionUITest"}, commit=True)
    relationship = _contain_relationship(crud_window)
    link(
        crud_window.context, relationship, record_id, existing_song["SongID"],
        extra_values={"Position": "A1"},
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

        position_col = 0  # "Position" is the sole extra column, first
        item = table_widget.item(0, position_col)
        assert item is not None
        assert bool(item.flags() & Qt.ItemFlag.ItemIsEditable)

        item.setText("B7")  # simulates the user typing a new label

        positions = {
            row["SongID"]: row["Position"]
            for row in list_related(crud_window.context, relationship, record_id)
        }
        assert positions[existing_song["SongID"]] == "B7"
    finally:
        unlink(crud_window.context, relationship, record_id, existing_song["SongID"])
        records.delete(record_id, commit=True)


def test_schedule_has_move_up_and_move_down_controls(
    crud_window: MainWindow,
) -> None:
    """
    Schedule.Position is a genuine integer and part of the primary
    key - unlike Contain, it should have real Move Up/Down controls.
    """

    programs_repo = repository_for(crud_window.context, "Programs")
    songs = repository_for(crud_window.context, "Songs")
    existing_song = songs.all(limit=1)[0]
    program_id = programs_repo.insert(
        {"ProgName": "MoveButtonsUITest"}, commit=True
    )
    program_service = ProgramService(crud_window.context)
    program_service.add_song(program_id, 1.0, song_id=existing_song["SongID"])

    try:
        idx = crud_window.table_combo.findText("Programs")
        crud_window.table_combo.setCurrentIndex(idx)
        row_idx = next(
            r
            for r in range(len(crud_window.table_rows))
            if crud_window.table_rows[r]["ProgramID"] == program_id
        )
        crud_window.table_widget.selectRow(row_idx)

        tab_widget = crud_window.related_tabs.widget(0)
        assert tab_widget is not None
        buttons = {
            b.text() for b in tab_widget.findChildren(QPushButton)
        }
        assert "Move Up" in buttons
        assert "Move Down" in buttons
    finally:
        for entry in program_service.schedule_for_program(program_id):
            program_service.remove_song(program_id, entry["Position"])
        programs_repo.delete(program_id, commit=True)


def _select_schedule_rows_by_song(
    table_widget: QTableWidget, song_ids: set[Any]
) -> None:
    """Select every row in a Schedule table whose SongID (col 1) matches."""

    selection_model = table_widget.selectionModel()
    target_texts = {str(s) for s in song_ids}
    for row in range(table_widget.rowCount()):
        item = table_widget.item(row, 1)
        if item is not None and item.text() in target_texts:
            selection_model.select(
                table_widget.model().index(row, 0),
                selection_model.SelectionFlag.Select
                | selection_model.SelectionFlag.Rows,
            )


def _schedule_table_widget(
    crud_window: MainWindow, program_id: Any
) -> QTableWidget:
    idx = crud_window.table_combo.findText("Programs")
    crud_window.table_combo.setCurrentIndex(idx)
    row_idx = next(
        r
        for r in range(len(crud_window.table_rows))
        if crud_window.table_rows[r]["ProgramID"] == program_id
    )
    crud_window.table_widget.selectRow(row_idx)

    tab_widget = crud_window.related_tabs.widget(0)
    assert tab_widget is not None
    table_widget = tab_widget.findChild(QTableWidget)
    assert table_widget is not None
    return table_widget


def test_move_selected_schedule_rows_single_row(
    crud_window: MainWindow,
) -> None:
    programs_repo = repository_for(crud_window.context, "Programs")
    songs = repository_for(crud_window.context, "Songs")
    song_a, song_b = songs.all(limit=2)

    program_id = programs_repo.insert(
        {"ProgName": "MoveScheduleSingleUITest"}, commit=True
    )
    program_service = ProgramService(crud_window.context)
    program_service.add_song(program_id, 1.0, song_id=song_a["SongID"])
    program_service.add_song(program_id, 2.0, song_id=song_b["SongID"])

    try:
        table_widget = _schedule_table_widget(crud_window, program_id)
        table_widget.selectRow(0)  # song_a, currently Position 1

        crud_window._move_selected_schedule_rows(program_id, table_widget, 1)

        positions = {
            entry["SongID"]: entry["Position"]
            for entry in program_service.schedule_for_program(program_id)
        }
        assert positions[song_a["SongID"]] == 2.0
        assert positions[song_b["SongID"]] == 1.0
    finally:
        for entry in program_service.schedule_for_program(program_id):
            program_service.remove_song(program_id, entry["Position"])
        programs_repo.delete(program_id, commit=True)


def test_move_selected_schedule_rows_non_adjacent_selection(
    crud_window: MainWindow,
) -> None:
    """
    Selecting two non-adjacent rows (e.g. the 2nd and 4th of five)
    and clicking Move Up must move each independently, matching
    ProgramService.move_selected()'s own behaviour - not just move
    whichever row happened to be first in the selection.
    """

    programs_repo = repository_for(crud_window.context, "Programs")
    songs = repository_for(crud_window.context, "Songs")
    labelled = songs.all(limit=5)

    program_id = programs_repo.insert(
        {"ProgName": "MoveScheduleNonAdjacentUITest"}, commit=True
    )
    program_service = ProgramService(crud_window.context)
    for index, song in enumerate(labelled, start=1):
        program_service.add_song(program_id, float(index), song_id=song["SongID"])

    try:
        table_widget = _schedule_table_widget(crud_window, program_id)

        # Select rows 1 and 3 (0-indexed) - the 2nd and 4th songs.
        _select_schedule_rows_by_song(
            table_widget, {labelled[1]["SongID"], labelled[3]["SongID"]}
        )

        crud_window._move_selected_schedule_rows(program_id, table_widget, -1)

        schedule = sorted(
            program_service.schedule_for_program(program_id),
            key=lambda e: e["Position"],
        )
        song_id_order = [entry["SongID"] for entry in schedule]
        expected_order = [
            labelled[1]["SongID"],  # B moved to position 1
            labelled[0]["SongID"],  # A displaced to position 2
            labelled[3]["SongID"],  # D moved to position 3
            labelled[2]["SongID"],  # C displaced to position 4
            labelled[4]["SongID"],  # E untouched
        ]
        assert song_id_order == expected_order
    finally:
        for entry in program_service.schedule_for_program(program_id):
            program_service.remove_song(program_id, entry["Position"])
        programs_repo.delete(program_id, commit=True)


def test_move_selected_schedule_rows_keeps_selection_after_reload(
    crud_window: MainWindow,
) -> None:
    """
    After Move Up/Down triggers a reload, the same rows (at their
    new positions) must remain selected - otherwise the user has to
    re-select before every click, which is exactly what was reported.
    """

    programs_repo = repository_for(crud_window.context, "Programs")
    songs = repository_for(crud_window.context, "Songs")
    song_a, song_b = songs.all(limit=2)

    program_id = programs_repo.insert(
        {"ProgName": "MoveScheduleReselectUITest"}, commit=True
    )
    program_service = ProgramService(crud_window.context)
    program_service.add_song(program_id, 1.0, song_id=song_a["SongID"])
    program_service.add_song(program_id, 2.0, song_id=song_b["SongID"])

    try:
        table_widget = _schedule_table_widget(crud_window, program_id)
        table_widget.selectRow(1)  # song_b, currently Position 2

        crud_window._move_selected_schedule_rows(program_id, table_widget, -1)

        # The subform was rebuilt by the reload - fetch the new table.
        tab_widget = crud_window.related_tabs.widget(0)
        assert tab_widget is not None
        rebuilt_table = tab_widget.findChild(QTableWidget)
        assert rebuilt_table is not None

        selected_rows = {
            index.row()
            for index in rebuilt_table.selectionModel().selectedRows()
        }
        assert len(selected_rows) == 1
        selected_row = next(iter(selected_rows))
        song_id_item = rebuilt_table.item(selected_row, 1)
        assert song_id_item is not None
        assert int(song_id_item.text()) == song_b["SongID"]
    finally:
        for entry in program_service.schedule_for_program(program_id):
            program_service.remove_song(program_id, entry["Position"])
        programs_repo.delete(program_id, commit=True)


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


def _set_form_field_text(window: MainWindow, field_name: str, text: str) -> None:
    """
    Set text on a form field, narrowing the QWidget type first.
    form_fields is typed dict[str, QWidget] since fields can be
    QLineEdit, QSpinBox, QDoubleSpinBox, or QDateEdit - every real
    field used by these tests is a QLineEdit.
    """

    field = window.form_fields[field_name]
    assert isinstance(field, QLineEdit)
    field.setText(text)


# ============================================================
# Master-table CRUD (Milestone 4A (4/N))
# ============================================================
#
# These run against the dedicated CRUD test database and clean up
# whatever they create, exactly like the junction UI tests above.


def test_save_record_inserts_new_row(crud_window: MainWindow) -> None:
    artists = repository_for(crud_window.context, "Artists")

    crud_window.load_table_data("Artists")
    crud_window.start_new_record()
    _set_form_field_text(crud_window, "Surname", "InsertUITest")
    _set_form_field_text(crud_window, "Name", "Alex")
    crud_window.save_record()

    try:
        new_row = next(
            row
            for row in crud_window.table_rows
            if row["Surname"] == "InsertUITest"
        )
        assert new_row["Name"] == "Alex"
    finally:
        row = artists.find({"Surname": "InsertUITest"})
        if row:
            artists.delete(row[0]["ArtistID"], commit=True)


def test_save_record_updates_existing_row(crud_window: MainWindow) -> None:
    artists = repository_for(crud_window.context, "Artists")
    artist_id = artists.insert({"Surname": "UpdateUITest"}, commit=True)

    try:
        crud_window.load_table_data("Artists")
        row_idx = next(
            r
            for r in range(len(crud_window.table_rows))
            if crud_window.table_rows[r]["ArtistID"] == artist_id
        )
        crud_window.table_widget.selectRow(row_idx)
        assert crud_window.current_row is not None
        assert crud_window.current_row["ArtistID"] == artist_id

        _set_form_field_text(crud_window, "Surname", "UpdateUITestChanged")
        crud_window.save_record()

        updated = artists.require(artist_id)
        assert updated["Surname"] == "UpdateUITestChanged"
    finally:
        artists.delete(artist_id, commit=True)


def test_delete_record_removes_row(crud_window: MainWindow) -> None:
    artists = repository_for(crud_window.context, "Artists")
    artist_id = artists.insert({"Surname": "DeleteUITest"}, commit=True)

    crud_window.load_table_data("Artists")
    row_idx = next(
        r
        for r in range(len(crud_window.table_rows))
        if crud_window.table_rows[r]["ArtistID"] == artist_id
    )
    crud_window.table_widget.selectRow(row_idx)

    crud_window.delete_record()

    assert artists.get(artist_id) is None


# ============================================================
# Schedule UI (Milestone 4B): add/delete/reposition + reverse lookup
# ============================================================
#
# Schedule doesn't fit the generic junction/direct model (its own PK
# includes Position, and SongID is a soft FK), so this stays on
# ProgramService/SongService rather than the generic relationship
# layer - these tests run against the CRUD test database.


def test_add_schedule_song_auto_fills_bpm_and_year(
    crud_window: MainWindow,
) -> None:
    programs_repo = repository_for(crud_window.context, "Programs")
    songs_repo = repository_for(crud_window.context, "Songs")
    existing_song = next(
        s for s in songs_repo.all(limit=50) if s["BPM"] is not None
    )
    program_id = programs_repo.insert(
        {"ProgName": "AddScheduleUITest"}, commit=True
    )
    program_service = ProgramService(crud_window.context)

    def fake_exec(dialog: QDialog) -> QDialog.DialogCode:
        list_widget = dialog.findChild(QListWidget)
        assert list_widget is not None
        for i in range(list_widget.count()):
            if list_widget.item(i).text().startswith(
                str(existing_song["SongID"])
            ):
                list_widget.setCurrentRow(i)
                break
        return QDialog.DialogCode.Accepted

    try:
        idx = crud_window.table_combo.findText("Programs")
        crud_window.table_combo.setCurrentIndex(idx)
        row_idx = next(
            r
            for r in range(len(crud_window.table_rows))
            if crud_window.table_rows[r]["ProgramID"] == program_id
        )
        crud_window.table_widget.selectRow(row_idx)

        tab_widget = crud_window.related_tabs.widget(0)
        assert tab_widget is not None
        table_widget = tab_widget.findChild(QTableWidget)
        assert table_widget is not None

        with patch.object(QDialog, "exec", fake_exec):
            crud_window._add_schedule_song(program_id, table_widget)

        scheduled = program_service.schedule_for_program(program_id)
        assert len(scheduled) == 1
        assert scheduled[0]["SongID"] == existing_song["SongID"]
        assert scheduled[0]["BPM"] == existing_song["BPM"]
        assert scheduled[0]["Year"] == existing_song["Year"]
    finally:
        for entry in program_service.schedule_for_program(program_id):
            program_service.remove_song(program_id, entry["Position"])
        programs_repo.delete(program_id, commit=True)


def test_set_schedule_position_handles_repeated_edits(
    crud_window: MainWindow,
) -> None:
    programs_repo = repository_for(crud_window.context, "Programs")
    songs_repo = repository_for(crud_window.context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]
    program_id = programs_repo.insert(
        {"ProgName": "RepositionScheduleUITest"}, commit=True
    )
    program_service = ProgramService(crud_window.context)
    program_service.add_song(
        program_id, 1.0, song_id=existing_song["SongID"]
    )

    try:
        crud_window._set_schedule_position(
            program_id, existing_song["SongID"], 5
        )
        crud_window._set_schedule_position(
            program_id, existing_song["SongID"], 7
        )

        scheduled = program_service.schedule_for_program(program_id)
        assert len(scheduled) == 1
        assert scheduled[0]["Position"] == 7.0
    finally:
        for entry in program_service.schedule_for_program(program_id):
            program_service.remove_song(program_id, entry["Position"])
        programs_repo.delete(program_id, commit=True)


def test_delete_schedule_entry_removes_slot(
    crud_window: MainWindow,
) -> None:
    programs_repo = repository_for(crud_window.context, "Programs")
    songs_repo = repository_for(crud_window.context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]
    program_id = programs_repo.insert(
        {"ProgName": "DeleteScheduleUITest"}, commit=True
    )
    program_service = ProgramService(crud_window.context)
    program_service.add_song(
        program_id, 1.0, song_id=existing_song["SongID"]
    )

    try:
        idx = crud_window.table_combo.findText("Programs")
        crud_window.table_combo.setCurrentIndex(idx)
        row_idx = next(
            r
            for r in range(len(crud_window.table_rows))
            if crud_window.table_rows[r]["ProgramID"] == program_id
        )
        crud_window.table_widget.selectRow(row_idx)

        tab_widget = crud_window.related_tabs.widget(0)
        assert tab_widget is not None
        table_widget = tab_widget.findChild(QTableWidget)
        assert table_widget is not None
        table_widget.selectRow(0)

        crud_window._delete_schedule_entry(program_id, table_widget)

        assert program_service.schedule_for_program(program_id) == []
    finally:
        programs_repo.delete(program_id, commit=True)


def test_scheduled_programs_subform_shows_this_program(
    crud_window: MainWindow,
) -> None:
    programs_repo = repository_for(crud_window.context, "Programs")
    songs_repo = repository_for(crud_window.context, "Songs")
    existing_song = songs_repo.all(limit=1)[0]
    program_id = programs_repo.insert(
        {"ProgName": "ReverseLookupUITest"}, commit=True
    )
    program_service = ProgramService(crud_window.context)
    program_service.add_song(
        program_id, 3.0, song_id=existing_song["SongID"]
    )

    try:
        idx = crud_window.table_combo.findText("Songs")
        crud_window.table_combo.setCurrentIndex(idx)
        row_idx = next(
            r
            for r in range(len(crud_window.table_rows))
            if crud_window.table_rows[r]["SongID"]
            == existing_song["SongID"]
        )
        crud_window.table_widget.selectRow(row_idx)

        # The "Programs scheduling this Song" tab is always last.
        last_tab_index = crud_window.related_tabs.count() - 1
        tab_widget = crud_window.related_tabs.widget(last_tab_index)
        assert tab_widget is not None
        table_widget = tab_widget.findChild(QTableWidget)
        assert table_widget is not None

        program_ids_shown = set()
        for r in range(table_widget.rowCount()):
            item = table_widget.item(r, 1)
            if item is not None:
                program_ids_shown.add(int(item.text()))
        assert program_id in program_ids_shown
    finally:
        for entry in program_service.schedule_for_program(program_id):
            program_service.remove_song(program_id, entry["Position"])
        programs_repo.delete(program_id, commit=True)


# ============================================================
# Dashboard and Reports tabs (Milestone 5A (3/N))
# ============================================================
#
# Read-only against the real database, like the other window-level
# tests above - these verify the UI layer correctly reflects what
# ReportService computes, not the computations themselves (already
# covered by tests/test_report_service.py).


def test_main_tabs_has_five_tabs(window: MainWindow) -> None:
    assert window.main_tabs.count() == 5
    assert [
        window.main_tabs.tabText(i) for i in range(window.main_tabs.count())
    ] == ["Browse", "Dashboard", "Reports", "Search", "Discogs"]


def test_dashboard_matches_report_service(window: MainWindow) -> None:
    window.main_tabs.setCurrentIndex(1)

    reports = ReportService(window.context)
    stats = reports.dashboard_stats()

    assert str(stats.artist_count) in window._dashboard_labels["counts"].text()
    assert str(stats.song_count) in window._dashboard_labels["counts"].text()
    assert (
        window._dashboard_recent_table.rowCount()
        == len(stats.recently_added_programs)
    )


def test_dashboard_refreshes_on_tab_switch(window: MainWindow) -> None:
    assert window._dashboard_recent_table.rowCount() == 0

    window.main_tabs.setCurrentIndex(1)

    assert window._dashboard_recent_table.rowCount() > 0


@pytest.mark.parametrize(
    "definition_index", range(len(REPORT_DEFINITIONS))
)
def test_report_row_count_matches_report_service(
    window: MainWindow, definition_index: int
) -> None:
    definition = REPORT_DEFINITIONS[definition_index]
    reports = ReportService(window.context)

    window.main_tabs.setCurrentIndex(2)
    window._report_combo.setCurrentIndex(definition_index)

    raw = getattr(reports, definition.method_name)()
    if definition.method_name == "duplicate_artists":
        expected_rows = sum(len(group) for group in raw)
    else:
        expected_rows = len(raw)

    assert window._report_table.rowCount() == expected_rows


def test_reports_refreshes_on_tab_switch(crud_window: MainWindow) -> None:
    songs = repository_for(crud_window.context, "Songs")
    song_id = songs.insert(
        {"Title": "ZzzReportsRefreshUITest"}, commit=True
    )

    try:
        assert crud_window._report_table.rowCount() == 0

        crud_window.main_tabs.setCurrentIndex(2)

        assert crud_window._report_table.rowCount() > 0
    finally:
        songs.delete(song_id, commit=True)


def test_report_double_click_navigates_to_browse_tab(
    crud_window: MainWindow,
) -> None:
    songs = repository_for(crud_window.context, "Songs")
    song_id = songs.insert(
        {"Title": "ZzzReportNavigateUITest"}, commit=True
    )

    try:
        crud_window.load_table_data("Songs")

        crud_window.main_tabs.setCurrentIndex(2)
        crud_window._report_combo.setCurrentIndex(0)  # Songs without an Artist

        matching_row = None
        for r in range(crud_window._report_table.rowCount()):
            cell = crud_window._report_table.item(r, 0)
            if cell is not None and cell.text() == str(song_id):
                matching_row = r
                break
        assert matching_row is not None

        crud_window._on_report_row_double_clicked(matching_row, 0)

        assert crud_window.main_tabs.currentIndex() == 0
        assert crud_window.current_table == "Songs"
        assert crud_window.current_row is not None
        assert crud_window.current_row["SongID"] == song_id
    finally:
        songs.delete(song_id, commit=True)


# ============================================================
# Search tab (Milestone 5B (2/N))
# ============================================================
#
# These run against the dedicated CRUD test database and clean up
# whatever they create, exactly like the other crud_window tests.


def test_global_search_finds_matches_across_tables(
    crud_window: MainWindow,
) -> None:
    artists = repository_for(crud_window.context, "Artists")
    songs = repository_for(crud_window.context, "Songs")
    records = repository_for(crud_window.context, "Records")
    programs = repository_for(crud_window.context, "Programs")
    styles = repository_for(crud_window.context, "Styles")

    needle = "ZzzGlobalSearchUITest"
    artist_id = artists.insert({"Surname": needle}, commit=True)
    song_id = songs.insert({"Title": needle}, commit=True)
    record_id = records.insert({"Title": needle}, commit=True)
    program_id = programs.insert({"ProgName": needle}, commit=True)
    style_id = styles.insert({"Label": needle}, commit=True)

    try:
        crud_window.main_tabs.setCurrentIndex(3)  # Search
        crud_window._global_search_box.setText(needle)
        crud_window._run_global_search()

        assert crud_window._search_table.rowCount() == 5

        found: dict[str, str] = {}
        for r in range(crud_window._search_table.rowCount()):
            table_item = crud_window._search_table.item(r, 0)
            id_item = crud_window._search_table.item(r, 2)
            assert table_item is not None
            assert id_item is not None
            found[table_item.text()] = id_item.text()
        assert found["Artists"] == str(artist_id)
        assert found["Songs"] == str(song_id)
        assert found["Records"] == str(record_id)
        assert found["Programs"] == str(program_id)
        assert found["Styles"] == str(style_id)
        assert f"5 result(s)" in crud_window._search_summary_label.text()
    finally:
        artists.delete(artist_id, commit=True)
        songs.delete(song_id, commit=True)
        records.delete(record_id, commit=True)
        programs.delete(program_id, commit=True)
        styles.delete(style_id, commit=True)


def test_global_search_blank_query_shows_no_results(
    crud_window: MainWindow,
) -> None:
    crud_window.main_tabs.setCurrentIndex(3)
    crud_window._global_search_box.setText("")
    crud_window._run_global_search()

    assert crud_window._search_table.rowCount() == 0
    assert "Type something" in crud_window._search_summary_label.text()


def test_search_row_double_click_navigates_to_browse_tab(
    crud_window: MainWindow,
) -> None:
    artists = repository_for(crud_window.context, "Artists")
    needle = "ZzzSearchNavigateUITest"
    artist_id = artists.insert({"Surname": needle}, commit=True)

    try:
        # crud_window redirects to the CRUD test database after
        # MainWindow() already loaded Artists from the production
        # one, and table_combo is still sitting on "Artists" from
        # that initial load - so _navigate_to_related_value's own
        # setCurrentIndex() call later is a no-op (Qt doesn't re-fire
        # on an unchanged value) and won't refresh table_rows itself.
        # Force a fresh load now, after inserting, so the Browse grid
        # already contains the new artist before navigation runs.
        crud_window.load_table_data("Artists")

        crud_window.main_tabs.setCurrentIndex(3)
        crud_window._global_search_box.setText(needle)
        crud_window._run_global_search()

        assert crud_window._search_table.rowCount() == 1

        crud_window._on_search_row_double_clicked(0, 0)

        assert crud_window.main_tabs.currentIndex() == 0
        assert crud_window.current_table == "Artists"
        assert crud_window.current_row is not None
        assert crud_window.current_row["ArtistID"] == artist_id
    finally:
        artists.delete(artist_id, commit=True)


# ============================================================
# Export (Milestone 5C (2/N)): Browse, Reports, Search
# ============================================================
#
# These patch QFileDialog.getSaveFileName so no real dialog ever
# opens, and (where relevant) patch QMessageBox so a blocking modal
# never waits for a click that can't come in an automated test.


def test_browse_export_writes_all_loaded_rows(
    window: MainWindow, tmp_path: Path
) -> None:
    window.load_table_data("Styles")
    export_path = tmp_path / "styles.csv"

    with patch(
        "main.QFileDialog.getSaveFileName",
        return_value=(str(export_path), ""),
    ):
        window._export_table_widget(window.table_widget, "styles.csv", "Styles")

    with open(export_path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == len(window.table_rows)
    assert rows[0]["Label"] == window.table_rows[0]["Label"]


def test_browse_export_respects_active_filter(
    window: MainWindow, tmp_path: Path
) -> None:
    """
    filter_rows() hides rows with setRowHidden() without touching
    table_rows - export must follow what's visible, not the full
    underlying dataset, or a deliberately filtered export would
    silently include everything anyway.
    """

    window.load_table_data("Styles")
    sample_label = window.table_rows[0]["Label"]
    window.search_box.setText(sample_label)
    window.filter_rows()

    visible_count = sum(
        1
        for row in range(window.table_widget.rowCount())
        if not window.table_widget.isRowHidden(row)
    )
    assert visible_count < len(window.table_rows)

    export_path = tmp_path / "filtered.csv"
    with patch(
        "main.QFileDialog.getSaveFileName",
        return_value=(str(export_path), ""),
    ):
        window._export_table_widget(window.table_widget, "styles.csv", "Styles")

    with open(export_path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == visible_count


def test_reports_export_to_excel(
    crud_window: MainWindow, tmp_path: Path
) -> None:
    songs = repository_for(crud_window.context, "Songs")
    song_id = songs.insert(
        {"Title": "ZzzReportsExportUITest"}, commit=True
    )

    try:
        crud_window.main_tabs.setCurrentIndex(2)
        crud_window._report_combo.setCurrentIndex(0)  # Songs without an Artist
        report_rows = crud_window._report_table.rowCount()
        assert report_rows > 0

        export_path = tmp_path / "report.xlsx"
        with patch(
            "main.QFileDialog.getSaveFileName",
            return_value=(str(export_path), ""),
        ):
            crud_window._export_table_widget(
                crud_window._report_table,
                "report.csv",
                crud_window._report_combo.currentText(),
            )

        workbook = load_workbook(export_path)
        worksheet = workbook.active
        assert worksheet is not None
        assert worksheet.max_row - 1 == report_rows
        assert worksheet.title == "Songs without an Artist"
    finally:
        songs.delete(song_id, commit=True)


def test_search_export_to_pdf(
    crud_window: MainWindow, tmp_path: Path
) -> None:
    artists = repository_for(crud_window.context, "Artists")
    needle = "ZzzSearchExportUITest"
    artist_id = artists.insert({"Surname": needle}, commit=True)

    try:
        crud_window.main_tabs.setCurrentIndex(3)
        crud_window._global_search_box.setText(needle)
        crud_window._run_global_search()
        assert crud_window._search_table.rowCount() == 1

        export_path = tmp_path / "search.pdf"
        with patch(
            "main.QFileDialog.getSaveFileName",
            return_value=(str(export_path), ""),
        ):
            crud_window._export_table_widget(
                crud_window._search_table, "search_results.csv", "Search Results"
            )

        text = PdfReader(export_path).pages[0].extract_text()
        assert "Search Results" in text
        assert needle in text
    finally:
        artists.delete(artist_id, commit=True)


def test_export_shows_message_when_nothing_to_export(
    window: MainWindow,
) -> None:
    window.main_tabs.setCurrentIndex(3)
    window._global_search_box.setText("")
    window._run_global_search()
    assert window._search_table.rowCount() == 0

    with patch("main.QMessageBox.information") as mock_information:
        window._export_table_widget(window._search_table, "x.csv", "X")
        mock_information.assert_called_once()


def test_export_cancelled_dialog_does_nothing(
    window: MainWindow, tmp_path: Path
) -> None:
    window.load_table_data("Styles")

    with patch(
        "main.QFileDialog.getSaveFileName", return_value=("", "")
    ):
        # Should return cleanly without attempting to write anything.
        window._export_table_widget(window.table_widget, "styles.csv", "Styles")

    assert list(tmp_path.iterdir()) == []


def test_export_unsupported_extension_warns_and_writes_nothing(
    window: MainWindow, tmp_path: Path
) -> None:
    window.load_table_data("Styles")
    export_path = tmp_path / "styles.txt"

    with patch(
        "main.QFileDialog.getSaveFileName",
        return_value=(str(export_path), ""),
    ):
        with patch("main.QMessageBox.warning") as mock_warning:
            window._export_table_widget(
                window.table_widget, "styles.csv", "Styles"
            )
            mock_warning.assert_called_once()

    assert not export_path.exists()


# ============================================================
# Discogs tab (Milestone 6A (2/N))
# ============================================================
#
# Synthetic release ids start with "99" and have six digits, e.g.
# "990101". Rows are created in the CRUD test database and removed
# again; QMessageBox is never reached (the tab reports problems in
# its status label), so nothing here can block on a dialog.

DISCOGS_TAB_INDEX = 4


def _make_discogs_fixture(
    context: Any, release_id: str, tag: str, *, linked: bool
) -> tuple[int, int, int | None]:
    """Create artist + record + release (+ one track and the link)."""

    artists = repository_for(context, "Artists")
    songs = repository_for(context, "Songs")
    records = RecordService(context)

    artist_id = artists.insert({"Surname": f"Zzz{tag}"}, commit=True)
    record_id = records.create(title=f"Zzz{tag} Title", artist_id=artist_id)
    repository_for(context, "Discogs").insert(
        {
            "ID": 990000 + int(release_id[2:]),
            "release_id": release_id,
            "Artist": f"Zzz{tag}",
            "Title": f"Zzz{tag} Title",
        },
        commit=True,
    )

    song_id = None
    if linked:
        song_id = songs.insert({"Title": f"Zzz{tag} Song"}, commit=True)
        records.add_track(record_id, song_id, position="A1")
        records.link_discogs(record_id, release_id)

    return artist_id, record_id, song_id


def _drop_discogs_fixture(
    context: Any,
    release_id: str,
    artist_id: int,
    record_id: int,
    song_id: int | None,
) -> None:
    records = RecordService(context)
    records.unlink_discogs(record_id)
    if song_id is not None:
        records.remove_track(record_id, song_id)
        repository_for(context, "Songs").delete(song_id, commit=True)
    records.delete(record_id)
    repository_for(context, "Artists").delete(artist_id, commit=True)
    repository_for(context, "Discogs").delete(release_id, commit=True)


def test_discogs_tab_loads_releases_when_opened(window: MainWindow) -> None:
    assert window._discogs_table.rowCount() == 0

    window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)

    expected = len(DiscogsService(window.context).list_releases())
    assert expected > 0
    assert window._discogs_table.rowCount() == expected


def test_discogs_filter_splits_linked_and_unlinked(window: MainWindow) -> None:
    window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
    service = DiscogsService(window.context)

    window._discogs_filter.setCurrentIndex(1)
    assert window._discogs_table.rowCount() == len(
        service.list_releases(linked=True)
    )

    window._discogs_filter.setCurrentIndex(2)
    assert window._discogs_table.rowCount() == len(
        service.list_releases(linked=False)
    )


def test_discogs_lookup_unknown_id_is_reported(window: MainWindow) -> None:
    window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
    window._discogs_id_box.setText("999999999")
    window._run_discogs_lookup()

    assert "No release found" in window._discogs_status.text()


def test_discogs_lookup_blank_input_asks_for_an_id(window: MainWindow) -> None:
    window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
    window._discogs_id_box.setText("   ")
    window._run_discogs_lookup()

    assert "Type a Discogs ID" in window._discogs_status.text()


def test_discogs_lookup_shows_record_and_tracks(
    crud_window: MainWindow,
) -> None:
    context = crud_window.context
    artist_id, record_id, song_id = _make_discogs_fixture(
        context, "990101", "DiscogsTabLinked", linked=True
    )

    try:
        crud_window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
        crud_window._discogs_id_box.setText(
            "https://www.discogs.com/release/990101-Anything"
        )
        crud_window._run_discogs_lookup()

        assert crud_window._selected_discogs_release_id() == "990101"
        assert not crud_window._discogs_tracks_group.isHidden()
        assert crud_window._discogs_suggest_group.isHidden()
        assert f"record #{record_id}" in crud_window._discogs_detail_label.text()
        assert crud_window._discogs_tracks_table.rowCount() == 1
        position_item = crud_window._discogs_tracks_table.item(0, 0)
        assert position_item is not None
        assert position_item.text() == "A1"
    finally:
        _drop_discogs_fixture(context, "990101", artist_id, record_id, song_id)


def test_discogs_lookup_resets_a_filter_that_would_hide_the_release(
    crud_window: MainWindow,
) -> None:
    context = crud_window.context
    artist_id, record_id, song_id = _make_discogs_fixture(
        context, "990102", "DiscogsTabFilter", linked=True
    )

    try:
        crud_window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
        crud_window._discogs_filter.setCurrentIndex(2)  # not linked yet
        assert "990102" not in crud_window._discogs_releases

        crud_window._discogs_id_box.setText("990102")
        crud_window._run_discogs_lookup()

        assert crud_window._discogs_filter.currentIndex() == 0
        assert crud_window._selected_discogs_release_id() == "990102"
    finally:
        _drop_discogs_fixture(context, "990102", artist_id, record_id, song_id)


def test_discogs_unlinked_release_offers_suggestions_and_links(
    crud_window: MainWindow,
) -> None:
    context = crud_window.context
    artist_id, record_id, song_id = _make_discogs_fixture(
        context, "990103", "DiscogsTabMatch", linked=False
    )

    try:
        crud_window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
        crud_window._discogs_filter.setCurrentIndex(2)  # not linked yet
        assert crud_window._select_discogs_release("990103")

        assert crud_window._discogs_tracks_group.isHidden()
        assert not crud_window._discogs_suggest_group.isHidden()
        record_item = crud_window._discogs_suggest_table.item(0, 1)
        assert record_item is not None
        assert record_item.text() == str(record_id)

        crud_window._discogs_suggest_table.selectRow(0)
        crud_window._link_selected_discogs_suggestion()

        assert "Linked release 990103" in crud_window._discogs_status.text()
        lookup = DiscogsService(context).lookup("990103")
        assert lookup is not None
        assert lookup.record is not None
        assert lookup.record["RecordID"] == record_id
        # The release left the "not linked yet" list.
        assert "990103" not in crud_window._discogs_releases
    finally:
        _drop_discogs_fixture(context, "990103", artist_id, record_id, song_id)


def test_discogs_link_without_a_selection_asks_for_one(
    window: MainWindow,
) -> None:
    window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
    window._link_selected_discogs_suggestion()

    assert "Select a suggested record" in window._discogs_status.text()


def test_discogs_double_click_opens_the_linked_record(
    crud_window: MainWindow,
) -> None:
    context = crud_window.context
    artist_id, record_id, song_id = _make_discogs_fixture(
        context, "990104", "DiscogsTabOpen", linked=True
    )

    try:
        crud_window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
        assert crud_window._select_discogs_release("990104")
        row = crud_window._discogs_table.selectionModel().selectedRows()[0].row()

        crud_window._on_discogs_release_double_clicked(row, 0)

        assert crud_window.main_tabs.currentIndex() == 0
        assert crud_window.current_table == "Records"
        assert crud_window.current_row is not None
        assert crud_window.current_row["RecordID"] == record_id
    finally:
        _drop_discogs_fixture(context, "990104", artist_id, record_id, song_id)


def test_discogs_double_click_on_unlinked_release_stays_put(
    crud_window: MainWindow,
) -> None:
    context = crud_window.context
    artist_id, record_id, song_id = _make_discogs_fixture(
        context, "990105", "DiscogsTabStay", linked=False
    )

    try:
        crud_window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
        assert crud_window._select_discogs_release("990105")
        row = crud_window._discogs_table.selectionModel().selectedRows()[0].row()

        crud_window._on_discogs_release_double_clicked(row, 0)

        assert crud_window.main_tabs.currentIndex() == DISCOGS_TAB_INDEX
        assert "no record yet" in crud_window._discogs_status.text()
    finally:
        _drop_discogs_fixture(context, "990105", artist_id, record_id, song_id)


def test_discogs_export_writes_the_visible_releases(
    window: MainWindow, tmp_path: Path
) -> None:
    window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
    window._discogs_filter.setCurrentIndex(1)  # linked only
    export_path = tmp_path / "discogs.csv"

    with patch(
        "main.QFileDialog.getSaveFileName",
        return_value=(str(export_path), ""),
    ):
        window._export_table_widget(
            window._discogs_table, "discogs_releases.csv", "Discogs Releases"
        )

    with open(export_path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == window._discogs_table.rowCount()
    assert "Release ID" in rows[0]


# ============================================================
# Discogs import (Milestone 6B (2/N))
# ============================================================
#
# Both the file dialog and the Yes/No confirmation are patched, so
# nothing can wait for a click. Rows are created in the CRUD test
# database with release ids 9904xx and removed again.

IMPORT_HEADER = ["Artist", "Title", "release_id"]


def _write_discogs_csv(path: Path, rows: list[dict[str, str]]) -> Path:
    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=IMPORT_HEADER)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _add_plain_release(
    context: Any, release_id: str, artist: str, title: str
) -> None:
    repository_for(context, "Discogs").insert(
        {
            "ID": 990000 + int(release_id[2:]),
            "release_id": release_id,
            "Artist": artist,
            "Title": title,
        },
        commit=True,
    )


def _drop_plain_releases(context: Any, *release_ids: str) -> None:
    discogs = repository_for(context, "Discogs")
    for release_id in release_ids:
        discogs.delete(release_id, commit=True)


def test_discogs_import_adds_and_updates_after_confirmation(
    crud_window: MainWindow, tmp_path: Path
) -> None:
    context = crud_window.context
    _add_plain_release(context, "990401", "Zzz Import", "Old Title")
    csv_path = _write_discogs_csv(
        tmp_path / "export.csv",
        [
            {"Artist": "Zzz Import", "Title": "New Title", "release_id": "990401"},
            {"Artist": "Zzz Fresh", "Title": "Brand New", "release_id": "990402"},
        ],
    )

    try:
        crud_window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(str(csv_path), ""),
        ), patch(
            "main.QMessageBox.question",
            return_value=QMessageBox.StandardButton.Yes,
        ) as question:
            crud_window._import_discogs_export()

        summary = question.call_args[0][2]
        assert "1 new release(s) will be added" in summary
        assert "1 existing release(s) will be updated" in summary
        assert "Nothing is deleted" in summary

        assert "Imported: 1 new, 1 updated." in crud_window._discogs_status.text()
        discogs = repository_for(context, "Discogs")
        assert discogs.require("990401")["Title"] == "New Title"
        assert discogs.require("990402")["Title"] == "Brand New"
        assert "990402" in crud_window._discogs_releases  # list refreshed
    finally:
        _drop_plain_releases(context, "990401", "990402")


def test_discogs_import_declined_changes_nothing(
    crud_window: MainWindow, tmp_path: Path
) -> None:
    context = crud_window.context
    _add_plain_release(context, "990403", "Zzz Import", "Old Title")
    csv_path = _write_discogs_csv(
        tmp_path / "export.csv",
        [{"Artist": "Zzz Import", "Title": "New Title", "release_id": "990403"}],
    )

    try:
        crud_window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(str(csv_path), ""),
        ), patch(
            "main.QMessageBox.question",
            return_value=QMessageBox.StandardButton.No,
        ):
            crud_window._import_discogs_export()

        assert crud_window._discogs_status.text() == "Import cancelled."
        title = repository_for(context, "Discogs").require("990403")["Title"]
        assert title == "Old Title"
    finally:
        _drop_plain_releases(context, "990403")


def test_discogs_import_cancelled_file_dialog_does_nothing(
    crud_window: MainWindow,
) -> None:
    crud_window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
    status_before = crud_window._discogs_status.text()

    with patch(
        "main.QFileDialog.getOpenFileName", return_value=("", "")
    ), patch("main.QMessageBox.question") as question:
        crud_window._import_discogs_export()

    question.assert_not_called()
    assert crud_window._discogs_status.text() == status_before


def test_discogs_import_rejects_a_file_that_is_not_a_discogs_export(
    crud_window: MainWindow, tmp_path: Path
) -> None:
    bad = tmp_path / "other.csv"
    bad.write_text("Name,Age\nAnna,30\n", encoding="utf-8")

    crud_window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
    with patch(
        "main.QFileDialog.getOpenFileName", return_value=(str(bad), "")
    ), patch("main.QMessageBox.question") as question:
        crud_window._import_discogs_export()

    question.assert_not_called()
    assert "Import failed" in crud_window._discogs_status.text()
    assert "release_id" in crud_window._discogs_status.text()


def test_discogs_import_up_to_date_file_needs_no_confirmation(
    crud_window: MainWindow, tmp_path: Path
) -> None:
    context = crud_window.context
    _add_plain_release(context, "990404", "Zzz Same", "Same Title")
    csv_path = _write_discogs_csv(
        tmp_path / "export.csv",
        [{"Artist": "Zzz Same", "Title": "Same Title", "release_id": "990404"}],
    )

    try:
        crud_window.main_tabs.setCurrentIndex(DISCOGS_TAB_INDEX)
        with patch(
            "main.QFileDialog.getOpenFileName",
            return_value=(str(csv_path), ""),
        ), patch("main.QMessageBox.question") as question:
            crud_window._import_discogs_export()

        question.assert_not_called()
        assert "Nothing to import" in crud_window._discogs_status.text()
    finally:
        _drop_plain_releases(context, "990404")


# ============================================================
# Keyboard shortcuts (Milestone 6D (1/N))
# ============================================================
#
# Two styles of test. Tests using shown_window send REAL key presses
# to a shown, active window, which proves the key combinations
# themselves work. The others call a shortcut's activated signal,
# which is the same code path without needing window focus.

EXPECTED_SHORTCUTS = {
    "Ctrl+1", "Ctrl+2", "Ctrl+3", "Ctrl+4", "Ctrl+5",
    "Ctrl+F", "F5", "Ctrl+E", "Ctrl+N", "Ctrl+S", "Alt+Up", "Alt+Down",
}


@pytest.fixture()
def shown_window(window: MainWindow) -> Iterator[MainWindow]:
    window.show()
    window.activateWindow()
    QApplication.processEvents()
    try:
        yield window
    finally:
        window.hide()


def _press(window: MainWindow, key: str) -> None:
    """Send a real key press such as 'Ctrl+3' or 'F5' to the window."""

    *modifier_names, key_name = key.split("+")
    modifier_flags = {
        "Ctrl": Qt.KeyboardModifier.ControlModifier,
        "Alt": Qt.KeyboardModifier.AltModifier,
        "Shift": Qt.KeyboardModifier.ShiftModifier,
    }

    modifiers = Qt.KeyboardModifier.NoModifier
    for name in modifier_names:
        modifiers |= modifier_flags[name]

    QTest.keyClick(window, getattr(Qt.Key, f"Key_{key_name}"), modifiers)
    QApplication.processEvents()


def _trigger(window: MainWindow, key: str) -> None:
    window._shortcuts[key].activated.emit()


def test_all_expected_shortcuts_are_registered(window: MainWindow) -> None:
    assert set(window._shortcuts) == EXPECTED_SHORTCUTS

    for key, shortcut in window._shortcuts.items():
        assert isinstance(shortcut, QShortcut)
        assert shortcut.key() == QKeySequence(key)


def test_tabs_show_their_shortcut_as_a_tooltip(window: MainWindow) -> None:
    assert [
        window.main_tabs.tabToolTip(i) for i in range(window.main_tabs.count())
    ] == ["Ctrl+1", "Ctrl+2", "Ctrl+3", "Ctrl+4", "Ctrl+5"]


@pytest.mark.parametrize("number", [1, 2, 3, 4, 5])
def test_ctrl_number_switches_tab_with_a_real_key_press(
    shown_window: MainWindow, number: int
) -> None:
    other = 0 if number != 1 else 1
    shown_window.main_tabs.setCurrentIndex(other)

    _press(shown_window, f"Ctrl+{number}")

    assert shown_window.main_tabs.currentIndex() == number - 1


def test_ctrl_f_focuses_the_search_box_of_the_current_tab(
    shown_window: MainWindow,
) -> None:
    for tab_index, box_name in [
        (0, "search_box"),
        (3, "_global_search_box"),
        (4, "_discogs_id_box"),
    ]:
        shown_window.main_tabs.setCurrentIndex(tab_index)
        _press(shown_window, "Ctrl+F")

        assert getattr(shown_window, box_name).hasFocus(), box_name


def test_ctrl_f_on_the_dashboard_does_nothing(window: MainWindow) -> None:
    window.main_tabs.setCurrentIndex(1)

    with patch.object(window.search_box, "setFocus") as browse_focus:
        _trigger(window, "Ctrl+F")

    browse_focus.assert_not_called()


@pytest.mark.parametrize(
    ("tab_index", "method_name"),
    [
        (0, "refresh_database"),
        (1, "_refresh_dashboard"),
        (2, "_run_selected_report"),
        (3, "_run_global_search"),
        (4, "_refresh_discogs"),
    ],
)
def test_f5_refreshes_whatever_the_current_tab_shows(
    window: MainWindow, tab_index: int, method_name: str
) -> None:
    window.main_tabs.setCurrentIndex(tab_index)

    with patch.object(window, method_name) as refresh:
        _trigger(window, "F5")

    refresh.assert_called_once()


def test_ctrl_e_exports_the_rows_of_the_current_tab(
    window: MainWindow, tmp_path: Path
) -> None:
    window.load_table_data("Styles")
    export_path = tmp_path / "styles.csv"

    with patch(
        "main.QFileDialog.getSaveFileName",
        return_value=(str(export_path), ""),
    ):
        _trigger(window, "Ctrl+E")

    with open(export_path, newline="", encoding="utf-8") as handle:
        assert len(list(csv.DictReader(handle))) == len(window.table_rows)


def test_ctrl_e_on_the_dashboard_has_nothing_to_export(
    window: MainWindow,
) -> None:
    window.main_tabs.setCurrentIndex(1)

    with patch("main.QFileDialog.getSaveFileName") as dialog:
        _trigger(window, "Ctrl+E")

    dialog.assert_not_called()


def test_ctrl_n_starts_a_new_record(window: MainWindow) -> None:
    window.load_table_data("Artists")
    window.table_widget.selectRow(0)
    assert window.current_row is not None

    _trigger(window, "Ctrl+N")

    assert window.current_row is None
    assert "New row ready" in window.message_label.text()


def test_ctrl_s_saves_the_record_being_edited(
    crud_window: MainWindow,
) -> None:
    artists = repository_for(crud_window.context, "Artists")
    artist_id = artists.insert({"Surname": "ZzzShortcutSave"}, commit=True)

    try:
        crud_window.load_table_data("Artists")
        row_idx = next(
            r
            for r in range(len(crud_window.table_rows))
            if crud_window.table_rows[r]["ArtistID"] == artist_id
        )
        crud_window.table_widget.selectRow(row_idx)
        _set_form_field_text(crud_window, "Surname", "ZzzShortcutSaved")

        _trigger(crud_window, "Ctrl+S")

        assert artists.require(artist_id)["Surname"] == "ZzzShortcutSaved"
    finally:
        artists.delete(artist_id, commit=True)


@pytest.mark.parametrize("key", ["Ctrl+S", "Ctrl+N"])
def test_save_and_new_do_nothing_outside_the_browse_tab(
    window: MainWindow, key: str
) -> None:
    window.main_tabs.setCurrentIndex(2)  # Reports

    with patch.object(window.save_button, "click") as save, patch.object(
        window.new_button, "click"
    ) as new:
        _trigger(window, key)

    save.assert_not_called()
    new.assert_not_called()


def test_alt_down_and_alt_up_move_the_selected_schedule_row(
    crud_window: MainWindow,
) -> None:
    programs_repo = repository_for(crud_window.context, "Programs")
    songs = repository_for(crud_window.context, "Songs")
    song_a, song_b = songs.all(limit=2)
    program_id = programs_repo.insert(
        {"ProgName": "ShortcutMoveUITest"}, commit=True
    )
    program_service = ProgramService(crud_window.context)
    program_service.add_song(program_id, 1.0, song_id=song_a["SongID"])
    program_service.add_song(program_id, 2.0, song_id=song_b["SongID"])

    def positions() -> dict[int, float]:
        return {
            entry["SongID"]: entry["Position"]
            for entry in program_service.schedule_for_program(program_id)
        }

    try:
        table_widget = _schedule_table_widget(crud_window, program_id)
        table_widget.selectRow(0)  # song_a at position 1

        _trigger(crud_window, "Alt+Down")

        assert positions() == {song_a["SongID"]: 2.0, song_b["SongID"]: 1.0}

        # The selection followed the moved row, so Alt+Up undoes it
        # without selecting anything again.
        _trigger(crud_window, "Alt+Up")

        assert positions() == {song_a["SongID"]: 1.0, song_b["SongID"]: 2.0}
    finally:
        for entry in program_service.schedule_for_program(program_id):
            program_service.remove_song(program_id, entry["Position"])
        programs_repo.delete(program_id, commit=True)


def test_alt_arrows_do_nothing_when_the_tab_has_no_move_buttons(
    window: MainWindow,
) -> None:
    window.load_table_data("Artists")
    window.table_widget.selectRow(0)

    _trigger(window, "Alt+Up")  # must simply do nothing
    _trigger(window, "Alt+Down")

    assert window.main_tabs.currentIndex() == 0
