from __future__ import annotations

import logging
import sqlite3
import sys
from typing import Any, TypedDict

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDateEdit,
    QDoubleSpinBox,
    QFormLayout,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QSplitter,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

import config
from core.database import ConnectionError, DatabaseManager, QueryError


logger = logging.getLogger(__name__)

MAIN_TABLES = ["Artists", "Songs", "Records", "Programs", "Styles"]


class DatabaseInfo(TypedDict):
    connected: bool
    database: str
    tables: list[str]
    message: str


class TableItem(QTableWidgetItem):
    def __lt__(self, other):
        if isinstance(other, QTableWidgetItem):
            try:
                return float(self.text()) < float(other.text())
            except (ValueError, TypeError):
                pass
        return super().__lt__(other)


def collect_database_info(db: DatabaseManager) -> DatabaseInfo:
    """Connect to the database and return a small summary for the UI."""

    try:
        db.connect()
        tables = db.tables()
        return {
            "connected": True,
            "database": str(db.database),
            "tables": tables,
            "message": "Database connection established.",
        }
    except ConnectionError as exc:
        logger.exception("Could not connect to the database")
        return {
            "connected": False,
            "database": str(db.database),
            "tables": [],
            "message": str(exc),
        }


def build_table_query(table_name: str, db: DatabaseManager | None = None) -> str:
    """Build a simple read query for the selected table."""

    database = db or DatabaseManager()
    columns = [column["name"] for column in database.columns(table_name)]

    if not columns:
        return f"SELECT * FROM [{table_name}]"

    quoted_columns = ", ".join(f"[{column}]" for column in columns)
    primary_key = database.primary_key(table_name)
    order_clause = f" ORDER BY [{primary_key}]" if primary_key else ""

    return f"SELECT {quoted_columns} FROM [{table_name}]{order_clause}"


class MainWindow(QMainWindow):
    """Starter CRUD dashboard for the main database tables."""

    def __init__(self) -> None:
        super().__init__()

        self.db = DatabaseManager()
        self.current_table = ""
        self.current_row: dict[str, Any] | None = None
        self.column_names: list[str] = []
        self.column_types: dict[str, str] = {}
        self.form_fields: dict[str, QWidget] = {}
        self.table_rows: list[dict[str, Any]] = []

        self.setWindowTitle(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        self.status_label = QLabel("Initializing...")
        self.status_label.setWordWrap(True)

        self.table_combo = QComboBox()
        self.table_combo.currentTextChanged.connect(self.load_table_data)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_database)

        self.new_button = QPushButton("New")
        self.new_button.clicked.connect(self.start_new_record)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_record)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_record)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search rows")
        self.search_box.textChanged.connect(self.filter_rows)

        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)

        self.table_widget = QTableWidget()
        self.table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_widget.itemSelectionChanged.connect(self.on_row_selected)

        self.form_group = QGroupBox("Record details")
        self.form_layout = QFormLayout(self.form_group)
        self.form_group.setMinimumWidth(320)

        self.related_tabs = QTabWidget()
        self.related_tabs.setMinimumWidth(400)
        self._subform_sort_state: dict[str, tuple[int, Qt.SortOrder]] = {}

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Table"))
        controls_layout.addWidget(self.table_combo, 1)
        controls_layout.addWidget(QLabel("Search"))
        controls_layout.addWidget(self.search_box, 1)
        controls_layout.addWidget(self.refresh_button)
        controls_layout.addWidget(self.new_button)
        controls_layout.addWidget(self.save_button)
        controls_layout.addWidget(self.delete_button)
        controls_layout.addWidget(self.clear_button)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.table_widget)

        side_panel = QWidget()
        side_layout = QVBoxLayout(side_panel)
        side_layout.addWidget(self.form_group)
        side_layout.addWidget(self.related_tabs, 1)

        splitter.addWidget(side_panel)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(splitter, 1)

        container = QWidget(self)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.refresh_database()

    def refresh_database(self) -> None:
        info = collect_database_info(self.db)

        self.status_label.setText(
            f"Connected: {info['connected']}\nDatabase: {info['database']}"
        )
        self.message_label.setText(str(info["message"]))

        self._populate_table_selector(info["tables"])

        if not info["connected"]:
            QMessageBox.critical(self, "Database error", str(info["message"]))
            return

        if self.current_table and self.table_combo.count() > 0 and self.current_table not in [self.table_combo.itemText(index) for index in range(self.table_combo.count())]:
            self.current_table = ""

        if self.current_table:
            self.load_table_data(self.current_table)
        elif self.table_combo.count() > 0:
            self.table_combo.setCurrentIndex(0)
            self.load_table_data()
        else:
            self._clear_related_tabs()

    def _populate_table_selector(self, available_tables: list[str]) -> None:
        selected_table = self.table_combo.currentText()
        visible_tables = [table for table in MAIN_TABLES if table in available_tables]

        self.table_combo.blockSignals(True)
        self.table_combo.clear()
        self.table_combo.addItems(visible_tables)
        if selected_table in visible_tables:
            self.table_combo.setCurrentText(selected_table)
        elif visible_tables:
            self.table_combo.setCurrentIndex(0)
        self.table_combo.blockSignals(False)

    def load_table_data(self, table_name: str | None = None) -> None:
        if not table_name:
            table_name = self.table_combo.currentText()

        if not table_name:
            return

        previous_pk = None
        previous_pk_col = None
        if self.current_row is not None and self.current_table:
            pk = self.db.primary_key(self.current_table)
            if pk and pk in self.current_row:
                previous_pk = str(self.current_row[pk])
                previous_pk_col = pk
        prev_sort_col = self.table_widget.horizontalHeader().sortIndicatorSection()
        prev_sort_order = self.table_widget.horizontalHeader().sortIndicatorOrder()

        self.current_table = table_name
        self.column_names = [column["name"] for column in self.db.columns(table_name)]
        self.column_types = {column["name"]: str(column["type"]) for column in self.db.columns(table_name)}
        self._build_form_fields()

        query = build_table_query(table_name, self.db)
        rows = self.db.fetchall(query)
        self.table_rows = [dict(row) for row in rows]

        self.table_widget.setColumnCount(len(self.column_names))
        self.table_widget.setRowCount(len(self.table_rows))
        self.table_widget.setHorizontalHeaderLabels(self.column_names)

        for row_index, row in enumerate(self.table_rows):
            for column_index, column_name in enumerate(self.column_names):
                value = row.get(column_name)
                text = "" if value is None else str(value)
                item = TableItem(text)
                if column_index == 0:
                    item.setData(Qt.ItemDataRole.UserRole, row_index)
                self.table_widget.setItem(row_index, column_index, item)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.setSortingEnabled(True)

        if 0 <= prev_sort_col < self.table_widget.columnCount():
            self.table_widget.sortItems(prev_sort_col, prev_sort_order)

        self.table_widget.clearSelection()

        if self.table_rows:
            self.current_row = self.table_rows[0]
            self._populate_form_from_row(self.current_row)
            if previous_pk is not None and previous_pk_col in self.column_names:
                pk_col_idx = self.column_names.index(previous_pk_col)
                for row in range(self.table_widget.rowCount()):
                    item = self.table_widget.item(row, pk_col_idx)
                    if item is not None and item.text() == previous_pk:
                        self.table_widget.selectRow(row)
                        break
                else:
                    self.table_widget.selectRow(0)
            else:
                self.table_widget.selectRow(0)
        else:
            self.current_row = None
            self.clear_form()

        self._update_related_tabs()

    def _build_form_fields(self) -> None:
        while self.form_layout.rowCount() > 0:
            self.form_layout.removeRow(0)

        self.form_fields = {}
        for column_name in self.column_names:
            column_type = self.column_types.get(column_name, "")
            normalized = column_type.lower()
            if "date" in normalized or "datetime" in normalized:
                field = QDateEdit()
                field.setCalendarPopup(True)
            elif "int" in normalized:
                field = QSpinBox()
                field.setMinimum(-10_000_000)
                field.setMaximum(10_000_000)
            elif "real" in normalized or "float" in normalized or "double" in normalized or "numeric" in normalized:
                field = QDoubleSpinBox()
                field.setDecimals(2)
                field.setMinimum(-10_000_000)
                field.setMaximum(10_000_000)
            else:
                field = QLineEdit()

            self.form_fields[column_name] = field
            self.form_layout.addRow(self._field_label(column_name), field)

    def _field_label(self, column_name: str) -> str:
        label = ""
        for i, ch in enumerate(column_name):
            if i > 0 and ch.isupper() and column_name[i - 1].islower():
                label += " " + ch
            else:
                label += ch
        return label

    def _clear_related_tabs(self) -> None:
        while self.related_tabs.count() > 0:
            self.related_tabs.removeTab(0)

    @staticmethod
    def _find_column_index(table: QTableWidget, column_name: str) -> int:
        for col in range(table.columnCount()):
            header = table.horizontalHeaderItem(col)
            if header is not None and header.text() == column_name:
                return col
        return -1

    def _navigate_to_record(self, target_table: str, target_pk: str, table: QTableWidget, row: int) -> None:
        pk_col = self._find_column_index(table, target_pk)
        if pk_col < 0:
            return
        item = table.item(row, pk_col)
        if item is None or not item.text():
            return
        pk_value = item.text()

        idx = self.table_combo.findText(target_table)
        if idx < 0:
            return
        self.table_combo.setCurrentIndex(idx)

        for i, r in enumerate(self.table_rows):
            if str(r.get(target_pk)) == pk_value:
                self.table_widget.selectRow(i)
                self.table_widget.setFocus()
                return

    def _related_relationships(self) -> list[tuple[str, str]]:
        relationships: dict[str, list[tuple[str, str]]] = {
            "Artists": [("Songs", "Sing")],
            "Songs": [("Artists", "Sing"), ("Records", "Contain"), ("Styles", "Belong"), ("Programs scheduling this Song", "ScheduledPrograms")],
            "Records": [("Songs", "Contain")],
            "Styles": [("Songs", "Belong")],
            "Programs": [("Schedule", "Schedule")],
        }
        return relationships.get(self.current_table, [])

    def _update_related_tabs(self) -> None:
        for i in range(self.related_tabs.count()):
            title = self.related_tabs.tabText(i)
            widget = self.related_tabs.widget(i)
            table = widget.findChild(QTableWidget)
            if table is not None:
                col = table.horizontalHeader().sortIndicatorSection()
                order = table.horizontalHeader().sortIndicatorOrder()
                if col >= 0:
                    key = f"{self.current_table}:{title}"
                    self._subform_sort_state[key] = (col, order)

        previous_index = self.related_tabs.currentIndex()
        self._clear_related_tabs()

        if not self.current_row or not self.current_table:
            return

        primary_key = self.db.primary_key(self.current_table)
        if not primary_key:
            return

        for title, relation_table in self._related_relationships():
            if relation_table == "Schedule":
                child_widget = self._build_schedule_subform(
                    self.current_row[primary_key],
                )
                self.related_tabs.addTab(child_widget, title)
                continue

            if relation_table == "ScheduledPrograms":
                child_widget = self._build_scheduled_programs_subform(
                    self.current_row[primary_key],
                )
                self.related_tabs.addTab(child_widget, title)
                continue

            fk = self._find_master_foreign_key(relation_table)
            if fk is None:
                continue

            child_widget = self._build_junction_subform(
                relation_table,
                title,
                fk,
                self.current_row[primary_key],
            )
            self.related_tabs.addTab(child_widget, title)

        for i in range(self.related_tabs.count()):
            title = self.related_tabs.tabText(i)
            key = f"{self.current_table}:{title}"
            widget = self.related_tabs.widget(i)
            table = widget.findChild(QTableWidget)
            if table is not None:
                if key in self._subform_sort_state:
                    col, order = self._subform_sort_state[key]
                    if 0 <= col < table.columnCount():
                        table.sortItems(col, order)
                table.horizontalHeader().sortIndicatorChanged.connect(
                    lambda col, order, k=key: self._subform_sort_state.update({k: (col, order)})
                )

        if 0 <= previous_index < self.related_tabs.count():
            self.related_tabs.setCurrentIndex(previous_index)

    def _find_master_foreign_key(self, relation_table: str) -> sqlite3.Row | None:
        for fk in self.db.foreign_keys(relation_table):
            if fk["table"].upper() == self.current_table.upper():
                return fk
        return None

    def _build_related_table_widget(
        self,
        relation_table: str,
        title: str,
        fk: sqlite3.Row,
        primary_value: Any,
    ) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        other_fk = [candidate for candidate in self.db.foreign_keys(relation_table) if candidate["from"] != fk["from"]][0]
        target_table = other_fk["table"]
        target_pk = self.db.primary_key(target_table)
        columns = [column["name"] for column in self.db.columns(target_table)]

        label = QLabel(f"{title} linked through {relation_table}")
        layout.addWidget(label)

        table = QTableWidget()
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)

        query = (
            f"SELECT {', '.join(f'[{target_table}].[{name}]' for name in columns)} "
            f"FROM [{target_table}] "
            f"INNER JOIN [{relation_table}] ON [{target_table}].[{target_pk}] = [{relation_table}].[{other_fk['from']}] "
            f"WHERE [{relation_table}].[{fk['from']}] = ?"
        )
        rows = self.db.fetchall(query, (primary_value,))

        table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for column_index, column_name in enumerate(columns):
                value = row[column_name]
                text = "" if value is None else str(value)
                table.setItem(row_index, column_index, TableItem(text))

        table.resizeColumnsToContents()
        table.setSortingEnabled(True)
        table.cellDoubleClicked.connect(
            lambda r, c, t=target_table, p=target_pk, tw=table: self._navigate_to_record(t, p, tw, r)
        )
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(table)

        add_button = QPushButton("Add relation")
        delete_button = QPushButton("Delete relation")
        add_button.clicked.connect(lambda _, t=relation_table, fk=fk, pv=primary_value, tw=table: self._open_association_editor(t, fk, pv, tw))
        delete_button.clicked.connect(lambda _, t=relation_table, fk=fk, pv=primary_value, tw=table: self._delete_association_relation(t, fk, pv, tw))
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        return widget

    def _build_junction_subform(
        self,
        junction_table: str,
        title: str,
        fk: sqlite3.Row,
        primary_value: Any,
    ) -> QWidget:
        other_fk = [c for c in self.db.foreign_keys(junction_table) if c["from"] != fk["from"]][0]
        target_table = other_fk["table"]
        target_pk = self.db.primary_key(target_table)

        target_columns = [c["name"] for c in self.db.columns(target_table)]
        junction_fk_cols = {fk["from"], other_fk["from"]}
        junction_extra_cols = [
            c["name"] for c in self.db.columns(junction_table)
            if c["name"] not in junction_fk_cols
        ]
        has_position = "Position" in junction_extra_cols

        display_columns = junction_extra_cols + target_columns

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel(f"{title} linked through {junction_table}"))

        table = QTableWidget()
        table.setColumnCount(len(display_columns))
        table.setHorizontalHeaderLabels(display_columns)

        extra_select = ", ".join(f"[{junction_table}].[{c}]" for c in junction_extra_cols)
        target_select = ", ".join(f"[{target_table}].[{c}]" for c in target_columns)
        select_clause = ", ".join(filter(None, [extra_select, target_select]))

        order_clause = (
            f"ORDER BY CAST([{junction_table}].[Position] AS INTEGER), [{junction_table}].[Position]"
            if has_position else ""
        )
        join_on = f"[{target_table}].[{target_pk}] = [{junction_table}].[{other_fk['from']}]"
        query = (
            f"SELECT {select_clause} "
            f"FROM [{junction_table}] "
            f"INNER JOIN [{target_table}] ON {join_on} "
            f"WHERE [{junction_table}].[{fk['from']}] = ? {order_clause}"
        )
        rows = self.db.fetchall(query, (primary_value,))

        table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            other_fk_value = row[other_fk["from"]]
            for col_idx, col_name in enumerate(display_columns):
                value = row[col_name]
                if col_name == "Position" and value is not None:
                    try:
                        pos_int = int(value)
                    except (ValueError, TypeError):
                        pos_int = None
                    if pos_int is not None:
                        spin = QSpinBox()
                        spin.setRange(1, 99)
                        spin.setValue(pos_int)
                        spin.valueChanged.connect(
                            lambda v, ov=other_fk_value, pv=primary_value:
                            self._set_junction_field(junction_table, fk["from"], pv, other_fk["from"], ov, "Position", v)
                        )
                        table.setCellWidget(row_idx, col_idx, spin)
                    else:
                        item = TableItem(str(value))
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                        table.setItem(row_idx, col_idx, item)
                else:
                    item = TableItem("" if value is None else str(value))
                    if col_name not in junction_extra_cols:
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()
        table.setSortingEnabled(True)
        table.cellDoubleClicked.connect(
            lambda r, c, t=target_table, p=target_pk, tw=table: self._navigate_to_record(t, p, tw, r)
        )
        layout.addWidget(table)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        del_btn = QPushButton("Remove")

        add_btn.clicked.connect(
            lambda: self._add_junction_relation(junction_table, fk, other_fk, primary_value, has_position, table)
        )
        del_btn.clicked.connect(
            lambda: self._delete_junction_relation(junction_table, fk, other_fk, primary_value, display_columns, table)
        )
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)

        if has_position:
            up_btn = QPushButton("Move Up")
            down_btn = QPushButton("Move Down")
            renumber_btn = QPushButton("Renumber")
            up_btn.clicked.connect(
                lambda: self._swap_junction_position(junction_table, fk, other_fk, primary_value, table, -1)
            )
            down_btn.clicked.connect(
                lambda: self._swap_junction_position(junction_table, fk, other_fk, primary_value, table, 1)
            )
            renumber_btn.clicked.connect(
                lambda: self._renumber_junction_positions(junction_table, fk, other_fk, primary_value, table)
            )
            btn_layout.addWidget(up_btn)
            btn_layout.addWidget(down_btn)
            btn_layout.addWidget(renumber_btn)

        layout.addLayout(btn_layout)
        return widget

    def _build_schedule_subform(self, program_id: Any) -> QWidget:
        columns = ["Position", "SongID", "Song_Artist", "Record", "BPM", "Year"]

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Songs scheduled in this Program"))

        table = QTableWidget()
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)

        rows = self.db.fetchall(
            "SELECT s.*, sg.Title FROM [Schedule] s "
            "LEFT JOIN [Songs] sg ON s.[SongID] = sg.[SongID] "
            "WHERE s.[ProgramID] = ? ORDER BY CAST(s.[Position] AS INTEGER), s.[Position]",
            (program_id,),
        )

        table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            pos = row["Position"]
            if pos is not None:
                spin = QSpinBox()
                spin.setRange(1, 999)
                spin.setValue(int(pos))
                spin.valueChanged.connect(
                    lambda v, pid=program_id: self._set_schedule_position(pid, int(row["SongID"]), v)
                )
                table.setCellWidget(row_idx, 0, spin)
            else:
                table.setItem(row_idx, 0, TableItem(""))

            for col_idx, col_name in enumerate(columns):
                if col_idx == 0:
                    continue
                value = row[col_name]
                item = TableItem("" if value is None else str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()
        table.setSortingEnabled(True)
        table.cellDoubleClicked.connect(
            lambda r, c, tw=table: self._navigate_to_record("Songs", "SongID", tw, r)
        )
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(table)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Song")
        del_btn = QPushButton("Remove")

        add_btn.clicked.connect(lambda: self._add_schedule_song(program_id, table))
        del_btn.clicked.connect(lambda: self._delete_schedule_entry(program_id, table))
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        layout.addLayout(btn_layout)

        return widget

    def _add_schedule_song(self, program_id: Any, table_widget: QTableWidget) -> None:
        max_pos = self.db.fetchone(
            "SELECT COALESCE(MAX([Position]), 0) AS max_pos FROM [Schedule] WHERE [ProgramID] = ?",
            (program_id,),
        )
        next_pos = (int(max_pos["max_pos"]) + 1) if max_pos else 1

        rows = self.db.fetchall(
            "SELECT [SongID], [Title], [BPM], [Year] FROM [Songs] ORDER BY [SongID]"
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Add Song to Schedule")
        dlg_layout = QVBoxLayout(dialog)
        dlg_layout.addWidget(QLabel("Choose a song:"))

        list_widget = QListWidget()
        item_ids: list[int] = []
        for row in rows:
            item_ids.append(int(row["SongID"]))
            list_widget.addItem(f"{row['SongID']} - {row['Title']} ({row['Year'] or ''})")
        dlg_layout.addWidget(list_widget)

        pos_spin = QSpinBox()
        pos_spin.setRange(1, 999)
        pos_spin.setValue(next_pos)
        pos_layout = QHBoxLayout()
        pos_layout.addWidget(QLabel("Position:"))
        pos_layout.addWidget(pos_spin)
        dlg_layout.addLayout(pos_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dlg_layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        current_index = list_widget.currentRow()
        if current_index < 0:
            return

        song_id = item_ids[current_index]

        self.db.execute(
            "INSERT INTO [Schedule] ([ProgramID], [SongID], [Position]) VALUES (?, ?, ?)",
            (program_id, song_id, pos_spin.value()),
        )
        self.db.commit()
        self.load_table_data(self.current_table)

    def _delete_schedule_entry(self, program_id: Any, table_widget: QTableWidget) -> None:
        selected_rows = table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Remove", "Select a row first.")
            return

        row_index = selected_rows[0].row()
        pos_widget = table_widget.cellWidget(row_index, 0)
        if not isinstance(pos_widget, QSpinBox):
            return
        position = pos_widget.value()

        self.db.execute(
            "DELETE FROM [Schedule] WHERE [ProgramID] = ? AND [Position] = ?",
            (program_id, position),
        )
        self.db.commit()
        self.load_table_data(self.current_table)

    def _build_scheduled_programs_subform(self, song_id: Any) -> QWidget:
        columns = ["Position", "ProgramID", "ProgName", "DateSched", "DateCreate", "Description"]

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Programs that schedule this Song"))

        table = QTableWidget()
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)

        rows = self.db.fetchall(
            "SELECT s.[Position], s.[SongID], p.* FROM [Schedule] s "
            "INNER JOIN [Programs] p ON s.[ProgramID] = p.[ProgramID] "
            "WHERE s.[SongID] = ? ORDER BY p.[DateSched], p.[ProgName]",
            (song_id,),
        )

        table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, col_name in enumerate(columns):
                value = row[col_name]
                if col_name == "Position" and value is not None:
                    value = int(value)
                item = TableItem("" if value is None else str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                table.setItem(row_idx, col_idx, item)

        table.resizeColumnsToContents()
        table.setSortingEnabled(True)
        table.cellDoubleClicked.connect(
            lambda r, c, tw=table: self._navigate_to_record("Programs", "ProgramID", tw, r)
        )
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(table)

        return widget

    def _set_schedule_position(self, program_id: Any, song_id: Any, new_pos: int) -> None:
        self.db.execute(
            "UPDATE [Schedule] SET [Position] = ? WHERE [ProgramID] = ? AND [SongID] = ?",
            (new_pos, program_id, song_id),
        )
        self.db.commit()

    def _set_junction_field(
        self, junction_table: str, fk_col: str, fk_value: Any,
        other_fk_col: str, other_fk_value: Any,
        field: str, new_value: Any,
    ) -> None:
        self.db.execute(
            f"UPDATE [{junction_table}] SET [{field}] = ? WHERE [{fk_col}] = ? AND [{other_fk_col}] = ?",
            (new_value, fk_value, other_fk_value),
        )
        self.db.commit()

    def _add_junction_relation(
        self, junction_table: str, fk: sqlite3.Row, other_fk: sqlite3.Row,
        primary_value: Any, has_position: bool, table_widget: QTableWidget,
    ) -> None:
        target_table = other_fk["table"]
        target_pk = self.db.primary_key(target_table)
        if not target_pk:
            QMessageBox.warning(self, "Cannot add", f"No primary key found for {target_table}")
            return

        target_cols = [c["name"] for c in self.db.columns(target_table) if c["name"] != target_pk]

        rows = self.db.fetchall(
            f"SELECT [{target_pk}], [{', '.join(target_cols)}] FROM [{target_table}] ORDER BY [{target_pk}]"
        )

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Add {target_table}")
        dlg_layout = QVBoxLayout(dialog)
        dlg_layout.addWidget(QLabel(f"Choose {target_table} to link:"))

        list_widget = QListWidget()
        item_ids: list[int] = []
        for row in rows:
            item_ids.append(int(row[target_pk]))
            label_parts = [str(row[target_pk])]
            for col in target_cols:
                if row[col] is not None:
                    label_parts.append(str(row[col]))
            list_widget.addItem(" - ".join(label_parts))
        dlg_layout.addWidget(list_widget)

        pos_spin = QSpinBox()
        pos_spin.setRange(1, 99)
        pos_spin.setValue(table_widget.rowCount() + 1)
        if has_position:
            pos_layout = QHBoxLayout()
            pos_layout.addWidget(QLabel("Position:"))
            pos_layout.addWidget(pos_spin)
            dlg_layout.addLayout(pos_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dlg_layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        current_index = list_widget.currentRow()
        if current_index < 0:
            return

        other_value = item_ids[current_index]
        extra_cols = [c["name"] for c in self.db.columns(junction_table) if c["name"] not in {fk["from"], other_fk["from"]}]
        col_names = [fk["from"], other_fk["from"]] + extra_cols
        placeholders = ", ".join("?" for _ in col_names)
        params: list[Any] = [primary_value, other_value]

        if has_position:
            params.append(pos_spin.value())

        self.db.execute(
            f"INSERT OR IGNORE INTO [{junction_table}] ({', '.join(f'[{c}]' for c in col_names)}) VALUES ({placeholders})",
            params,
        )
        self.db.commit()
        self.load_table_data(self.current_table)

    def _delete_junction_relation(
        self, junction_table: str, fk: sqlite3.Row, other_fk: sqlite3.Row,
        primary_value: Any, display_columns: list[str], table_widget: QTableWidget,
    ) -> None:
        selected_rows = table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Remove", "Select a row first.")
            return

        row_index = selected_rows[0].row()
        other_fk_col_name = other_fk["from"]
        if other_fk_col_name in display_columns:
            col_idx = display_columns.index(other_fk_col_name)
            item = table_widget.item(row_index, col_idx)
            if item is None or not item.text():
                return
            other_value = int(item.text())
        else:
            target_table = other_fk["table"]
            target_pk = self.db.primary_key(target_table)
            if target_pk in display_columns:
                col_idx = display_columns.index(target_pk)
                item = table_widget.item(row_index, col_idx)
                if item is None or not item.text():
                    return
                other_value = int(item.text())
            else:
                QMessageBox.warning(self, "Cannot remove", "Cannot identify the related record.")
                return

        self.db.execute(
            f"DELETE FROM [{junction_table}] WHERE [{fk['from']}] = ? AND [{other_fk['from']}] = ?",
            (primary_value, other_value),
        )
        self.db.commit()
        self.load_table_data(self.current_table)

    def _swap_junction_position(
        self, junction_table: str, fk: sqlite3.Row, other_fk: sqlite3.Row,
        primary_value: Any, table_widget: QTableWidget, direction: int,
    ) -> None:
        selected_rows = table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return
        row = selected_rows[0].row()
        target_row = row + direction
        if target_row < 0 or target_row >= table_widget.rowCount():
            return

        col_headers: list[str] = []
        for i in range(table_widget.columnCount()):
            h = table_widget.horizontalHeaderItem(i)
            col_headers.append(h.text() if h is not None else "")

        other_fk_name = other_fk["from"]
        pk_col_idx = col_headers.index(other_fk_name) if other_fk_name in col_headers else -1
        if pk_col_idx < 0:
            target_table = other_fk["table"]
            target_pk = self.db.primary_key(target_table)
            pk_col_idx = col_headers.index(target_pk) if target_pk in col_headers else -1
            if pk_col_idx < 0:
                return

        def _get_other_val(r: int) -> int:
            item = table_widget.item(r, pk_col_idx)
            if item is None or not item.text():
                return 0
            return int(item.text())

        val_a = _get_other_val(row)
        val_b = _get_other_val(target_row)
        if not val_a or not val_b:
            return

        pos_a_widget = table_widget.cellWidget(row, 0)
        pos_b_widget = table_widget.cellWidget(target_row, 0)
        pos_a = pos_a_widget.value() if isinstance(pos_a_widget, QSpinBox) else 0
        pos_b = pos_b_widget.value() if isinstance(pos_b_widget, QSpinBox) else 0

        self.db.execute(
            f"UPDATE [{junction_table}] SET [Position] = ? WHERE [{fk['from']}] = ? AND [{other_fk['from']}] = ?",
            (pos_b, primary_value, val_a),
        )
        self.db.execute(
            f"UPDATE [{junction_table}] SET [Position] = ? WHERE [{fk['from']}] = ? AND [{other_fk['from']}] = ?",
            (pos_a, primary_value, val_b),
        )
        self.db.commit()
        self.load_table_data(self.current_table)

    def _renumber_junction_positions(
        self, junction_table: str, fk: sqlite3.Row, other_fk: sqlite3.Row,
        primary_value: Any, table_widget: QTableWidget,
    ) -> None:
        col_headers: list[str] = []
        for i in range(table_widget.columnCount()):
            h = table_widget.horizontalHeaderItem(i)
            col_headers.append(h.text() if h is not None else "")

        other_fk_name = other_fk["from"]
        pk_col_idx = col_headers.index(other_fk_name) if other_fk_name in col_headers else -1
        if pk_col_idx < 0:
            target_pk = self.db.primary_key(other_fk["table"])
            pk_col_idx = col_headers.index(target_pk) if target_pk in col_headers else -1
            if pk_col_idx < 0:
                return

        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, pk_col_idx)
            if item is None:
                continue
            other_value = int(item.text())
            self.db.execute(
                f"UPDATE [{junction_table}] SET [Position] = ? WHERE [{fk['from']}] = ? AND [{other_fk['from']}] = ?",
                (row + 1, primary_value, other_value),
            )
        self.db.commit()
        self.load_table_data(self.current_table)

    def _open_association_editor(
        self,
        association_table: str,
        fk: sqlite3.Row,
        primary_value: Any,
        table_widget: QTableWidget | None = None,
    ) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Link {association_table}")
        dialog_layout = QVBoxLayout(dialog)

        target_column = [candidate for candidate in self.db.foreign_keys(association_table) if candidate['from'] != fk['from']][0]
        target_table = target_column['table']
        target_pk = self.db.primary_key(target_table)
        if not target_pk:
            QMessageBox.warning(self, "Cannot add relation", f"No primary key found for {target_table}")
            return

        list_widget = QListWidget()
        rows = self.db.fetchall(f"SELECT [{target_pk}], [{', '.join([c['name'] for c in self.db.columns(target_table) if c['name'] != target_pk])}] FROM [{target_table}] ORDER BY [{target_pk}]")
        self._association_rows = []
        for row in rows:
            list_widget.addItem(f"{row[target_pk]} - {row[1]}")
            self._association_rows.append(row)

        dialog_layout.addWidget(QLabel(f"Choose {target_table} to link to this {self.current_table}"))
        dialog_layout.addWidget(list_widget)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        current_index = list_widget.currentRow()
        if current_index < 0:
            return

        selected_row = self._association_rows[current_index]
        target_value = selected_row[target_pk]

        self.db.execute(
            f"INSERT OR IGNORE INTO [{association_table}] ([{fk['from']}], [{target_column['from']}]) VALUES (?, ?)",
            (primary_value, target_value),
        )
        self.db.commit()
        self.load_table_data(self.current_table)

    def _delete_association_relation(
        self,
        association_table: str,
        fk: sqlite3.Row,
        primary_value: Any,
        table_widget: QTableWidget,
    ) -> None:
        selected_rows = table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Delete relation", "Select a row first.")
            return

        row_index = selected_rows[0].row()
        columns = [column['name'] for column in self.db.columns(association_table)]
        selected_row: dict[str, str] = {}
        for idx in range(table_widget.columnCount()):
            item = table_widget.item(row_index, idx)
            selected_row[columns[idx]] = "" if item is None else item.text()

        target_column = [candidate for candidate in self.db.foreign_keys(association_table) if candidate['from'] != fk['from']][0]
        self.db.execute(
            f"DELETE FROM [{association_table}] WHERE [{fk['from']}] = ? AND [{target_column['from']}] = ?",
            (primary_value, int(selected_row[target_column['from']])),
        )
        self.db.commit()
        self.load_table_data(self.current_table)

    def on_row_selected(self) -> None:
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return

        visual_row = selected_rows[0].row()
        first_item = self.table_widget.item(visual_row, 0)
        if first_item is None:
            return
        data_index = first_item.data(Qt.ItemDataRole.UserRole)
        if data_index is None or data_index >= len(self.table_rows):
            return

        self.current_row = self.table_rows[data_index]
        self._populate_form_from_row(self.current_row)
        self._update_related_tabs()

    def _populate_form_from_row(self, row: dict[str, Any]) -> None:
        for column_name, field in self.form_fields.items():
            value = row.get(column_name)
            if isinstance(field, QDateEdit):
                if value is None:
                    field.clear()
                else:
                    if isinstance(value, str):
                        parsed = QDate.fromString(value, "yyyy-MM-dd")
                        if parsed.isValid():
                            field.setDate(parsed)
                    else:
                        field.setDate(value)
            elif isinstance(field, (QSpinBox, QDoubleSpinBox)):
                if value in (None, ""):
                    field.setValue(0)
                else:
                    if isinstance(field, QDoubleSpinBox):
                        field.setValue(float(value))
                    else:
                        field.setValue(int(value))
            elif isinstance(field, QLineEdit):
                field.setText("" if value is None else str(value))

    def start_new_record(self) -> None:
        self.current_row = None
        self.clear_form()
        self.message_label.setText("New row ready. Fill the fields and click Save.")

    def clear_form(self) -> None:
        self.current_row = None
        for field in self.form_fields.values():
            if isinstance(field, QDateEdit):
                field.clear()
            elif isinstance(field, (QSpinBox, QDoubleSpinBox)):
                field.setValue(0)
            elif isinstance(field, QLineEdit):
                field.clear()

    def save_record(self) -> None:
        if not self.current_table:
            return

        try:
            primary_key = self.db.primary_key(self.current_table)
            values = self._collect_form_values()

            if self.current_row is None or primary_key is None:
                insert_columns = [name for name in self.column_names if name != primary_key]
                if not insert_columns:
                    self.db.execute(f"INSERT INTO [{self.current_table}] DEFAULT VALUES")
                else:
                    placeholders = ", ".join("?" for _ in insert_columns)
                    columns_sql = ", ".join(f"[{name}]" for name in insert_columns)
                    sql = f"INSERT INTO [{self.current_table}] ({columns_sql}) VALUES ({placeholders})"
                    params = [values.get(name) for name in insert_columns]
                    self.db.execute(sql, params)
            elif self.current_row.get(primary_key) in (None, ""):
                insert_columns = [name for name in self.column_names if name != primary_key]
                if not insert_columns:
                    self.db.execute(f"INSERT INTO [{self.current_table}] DEFAULT VALUES")
                else:
                    placeholders = ", ".join("?" for _ in insert_columns)
                    columns_sql = ", ".join(f"[{name}]" for name in insert_columns)
                    sql = f"INSERT INTO [{self.current_table}] ({columns_sql}) VALUES ({placeholders})"
                    params = [values.get(name) for name in insert_columns]
                    self.db.execute(sql, params)
            else:
                update_columns = [name for name in self.column_names if name != primary_key]
                assignments = ", ".join(f"[{name}] = ?" for name in update_columns)
                sql = f"UPDATE [{self.current_table}] SET {assignments} WHERE [{primary_key}] = ?"
                params = [values.get(name) for name in update_columns]
                params.append(self.current_row[primary_key])
                self.db.execute(sql, params)

            self.db.commit()
            if self.current_row is None or primary_key is None:
                self.message_label.setText("New row added.")
            elif self.current_row.get(primary_key) in (None, ""):
                self.message_label.setText("New row added.")
            else:
                self.message_label.setText("Record saved.")
            self.load_table_data(self.current_table)
        except (QueryError, ValueError, TypeError) as exc:
            self.message_label.setText(f"Save failed: {exc}")
            QMessageBox.critical(self, "Save failed", str(exc))

    def delete_record(self) -> None:
        if not self.current_table or self.current_row is None:
            return

        primary_key = self.db.primary_key(self.current_table)
        if not primary_key:
            return

        try:
            sql = f"DELETE FROM [{self.current_table}] WHERE [{primary_key}] = ?"
            self.db.execute(sql, (self.current_row[primary_key],))
            self.db.commit()
            self.message_label.setText("Record deleted.")
            self.load_table_data(self.current_table)
        except (QueryError, ValueError, TypeError) as exc:
            self.message_label.setText(f"Delete failed: {exc}")
            QMessageBox.critical(self, "Delete failed", str(exc))

    def _collect_form_values(self) -> dict[str, Any]:
        values: dict[str, Any] = {}
        for column_name, field in self.form_fields.items():
            if isinstance(field, QDateEdit):
                value = field.date().toString("yyyy-MM-dd") if field.date().isValid() else None
                values[column_name] = value
            elif isinstance(field, QSpinBox):
                values[column_name] = field.value()
            elif isinstance(field, QDoubleSpinBox):
                values[column_name] = field.value()
            elif isinstance(field, QLineEdit):
                raw_value = field.text().strip()
                if not raw_value:
                    values[column_name] = None
                    continue

                column_type = self.column_types.get(column_name, "")
                normalized = column_type.lower()
                if "int" in normalized:
                    values[column_name] = int(raw_value)
                elif "real" in normalized or "float" in normalized or "double" in normalized or "numeric" in normalized:
                    values[column_name] = float(raw_value)
                else:
                    values[column_name] = raw_value

        return values

    def filter_rows(self) -> None:
        if not self.current_table:
            return

        search_text = self.search_box.text().strip().lower()
        self.table_widget.clearSelection()

        for row_index in range(self.table_widget.rowCount()):
            row_matches = False
            for column_index in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row_index, column_index)
                if item is not None and search_text in item.text().lower():
                    row_matches = True
                    break
            self.table_widget.setRowHidden(row_index, not row_matches if search_text else False)

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        if self.db.connected:
            self.db.disconnect()
        super().closeEvent(event)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
