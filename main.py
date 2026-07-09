from __future__ import annotations

import logging
import sys
from typing import Any, TypedDict

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

import config
from core.database import ConnectionError, DatabaseManager, QueryError


logger = logging.getLogger(__name__)

MAIN_TABLES = ["Artists", "Songs", "Records", "Programs"]


class DatabaseInfo(TypedDict):
    connected: bool
    database: str
    tables: list[str]
    message: str


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
        self.form_fields: dict[str, QLineEdit] = {}
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

        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)

        self.table_widget = QTableWidget()
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.SingleSelection)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_widget.itemSelectionChanged.connect(self.on_row_selected)

        self.form_group = QGroupBox("Record details")
        self.form_layout = QFormLayout(self.form_group)
        self.form_group.setMinimumWidth(320)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Table"))
        controls_layout.addWidget(self.table_combo, 1)
        controls_layout.addWidget(self.refresh_button)
        controls_layout.addWidget(self.new_button)
        controls_layout.addWidget(self.save_button)
        controls_layout.addWidget(self.delete_button)
        controls_layout.addWidget(self.clear_button)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.table_widget)
        splitter.addWidget(self.form_group)
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

        if self.current_table not in self.table_combo.allItems() if hasattr(self.table_combo, "allItems") else False:
            self.current_table = ""

        if self.current_table:
            self.load_table_data(self.current_table)
        elif self.table_combo.count() > 0:
            self.table_combo.setCurrentIndex(0)

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
                self.table_widget.setItem(row_index, column_index, QTableWidgetItem(text))

        self.table_widget.resizeColumnsToContents()
        self.table_widget.clearSelection()
        self.clear_form()

    def _build_form_fields(self) -> None:
        while self.form_layout.rowCount() > 0:
            self.form_layout.removeRow(0)

        self.form_fields = {}
        for column_name in self.column_names:
            field = QLineEdit()
            self.form_fields[column_name] = field
            self.form_layout.addRow(column_name, field)

    def on_row_selected(self) -> None:
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            return

        row_index = selected_rows[0].row()
        if row_index >= len(self.table_rows):
            return

        self.current_row = self.table_rows[row_index]
        self._populate_form_from_row(self.current_row)

    def _populate_form_from_row(self, row: dict[str, Any]) -> None:
        for column_name, field in self.form_fields.items():
            value = row.get(column_name)
            field.setText("" if value is None else str(value))

    def start_new_record(self) -> None:
        self.current_row = None
        self.clear_form()

    def clear_form(self) -> None:
        self.current_row = None
        for field in self.form_fields.values():
            field.clear()

    def save_record(self) -> None:
        if not self.current_table:
            return

        try:
            primary_key = self.db.primary_key(self.current_table)
            values = self._collect_form_values()

            if self.current_row is None or primary_key is None or self.current_row.get(primary_key) in (None, ""):
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
            raw_value = field.text().strip()
            if not raw_value:
                values[column_name] = None
                continue

            column_type = self.column_types.get(column_name, "")
            normalized = column_type.lower()
            if "int" in normalized:
                values[column_name] = int(raw_value)
            elif "real" in normalized or "float" in normalized or "double" in normalized:
                values[column_name] = float(raw_value)
            else:
                values[column_name] = raw_value

        return values

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
