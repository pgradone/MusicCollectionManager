from __future__ import annotations

import logging
import sys
from typing import TypedDict

from PySide6.QtGui import QCloseEvent

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import config
from core.database import ConnectionError, DatabaseManager


logger = logging.getLogger(__name__)


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


class MainWindow(QMainWindow):
    """Minimal starter window for testing the project."""

    def __init__(self) -> None:
        super().__init__()

        self.db = DatabaseManager()
        self.setWindowTitle(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        self.status_label = QLabel("Initializing...")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.tables_list = QListWidget()
        self.tables_list.setMinimumHeight(250)

        self.refresh_button = QPushButton("Refresh database")
        self.refresh_button.clicked.connect(self.refresh_database)

        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Database status"))
        layout.addWidget(self.status_label)
        layout.addWidget(self.message_label)
        layout.addWidget(self.refresh_button)
        layout.addWidget(QLabel("Tables"))
        layout.addWidget(self.tables_list)

        container = QWidget(self)
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.refresh_database()

    def refresh_database(self) -> None:
        info = collect_database_info(self.db)

        self.status_label.setText(
            f"Connected: {info['connected']}\nDatabase: {info['database']}"
        )
        self.message_label.setText(str(info["message"]))

        self.tables_list.clear()
        for table_name in info["tables"]:
            self.tables_list.addItem(QListWidgetItem(table_name))

        if not info["connected"]:
            QMessageBox.critical(self, "Database error", str(info["message"]))

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
