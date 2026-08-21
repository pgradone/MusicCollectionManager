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
from typing import Any
from unittest.mock import patch

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLineEdit,
    QListWidget,
    QPushButton,
    QTableWidget,
)

from core.relationship_operations import link, list_related, unlink
from core.relationships import JUNCTION, discover_relationships
from main import REPORT_DEFINITIONS, SOFT_FOREIGN_KEYS, MainWindow
from services.program_service import ProgramService
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


def test_main_tabs_has_three_tabs(window: MainWindow) -> None:
    assert window.main_tabs.count() == 3
    assert [
        window.main_tabs.tabText(i) for i in range(window.main_tabs.count())
    ] == ["Browse", "Dashboard", "Reports"]


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


def test_reports_refreshes_on_tab_switch(window: MainWindow) -> None:
    assert window._report_table.rowCount() == 0

    window.main_tabs.setCurrentIndex(2)

    assert window._report_table.rowCount() > 0


def test_report_double_click_navigates_to_browse_tab(
    window: MainWindow,
) -> None:
    window.main_tabs.setCurrentIndex(2)
    window._report_combo.setCurrentIndex(0)  # Songs without an Artist

    assert window._report_table.rowCount() > 0
    item = window._report_table.item(0, 0)
    assert item is not None
    song_id = int(item.text())

    window._on_report_row_double_clicked(0, 0)

    assert window.main_tabs.currentIndex() == 0
    assert window.current_table == "Songs"
    assert window.current_row is not None
    assert window.current_row["SongID"] == song_id
