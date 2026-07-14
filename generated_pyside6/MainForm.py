"""
Auto-generated PySide6 form: MainForm
Generated: 2026-07-14 15:06:58
"""

import sys
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QWidget,
)
from PySide6.QtGui import QFont


class MainForm(QMainWindow):
    """Migrated from Access form: MainForm."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MainForm")
        self.setObjectName("MainForm")
        self.resize(6606, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(5)

        self.button_open_songs = QPushButton("Songs", self)
        self.button_open_songs.setObjectName("ButtonOpenSongs")
        self.button_open_songs.setGeometry(2304, 1440, 870, 465)
        self.button_open_songs.clicked.connect(self.ButtonOpenSongs_Click)

        self.button_open_records = QPushButton("Records", self)
        self.button_open_records.setObjectName("ButtonOpenRecords")
        self.button_open_records.setGeometry(144, 1440, 1005, 465)
        self.button_open_records.clicked.connect(self.ButtonOpenRecords_Click)

        self.button_open_artists = QPushButton("Artists", self)
        self.button_open_artists.setObjectName("ButtonOpenArtists")
        self.button_open_artists.setGeometry(4464, 1440, 870, 465)
        self.button_open_artists.clicked.connect(self.ButtonOpenArtists_Click)

        self.button_open_programs = QPushButton("Programs", self)
        self.button_open_programs.setObjectName("ButtonOpenPrograms")
        self.button_open_programs.setGeometry(2160, 3240, 1140, 465)
        self.button_open_programs.clicked.connect(self.ButtonOpenPrograms_Click)

        self.text4 = QLabel("schedule", self)
        self.text4.setObjectName("Text4")
        self.text4.setGeometry(2304, 2640, 870, 240)

        self.text5 = QLabel("sing", self)
        self.text5.setObjectName("Text5")
        self.text5.setGeometry(3600, 1560, 435, 240)

        self.text6 = QLabel("contain", self)
        self.text6.setObjectName("Text6")
        self.text6.setGeometry(1440, 1560, 579, 240)

        self.line7 = QFrame(self)
        self.line7.setFrameShape(QFrame.Shape.HLine)
        self.line7.setObjectName("Line7")

        self.line8 = QFrame(self)
        self.line8.setFrameShape(QFrame.Shape.HLine)
        self.line8.setObjectName("Line8")

        self.line9 = QFrame(self)
        self.line9.setFrameShape(QFrame.Shape.HLine)
        self.line9.setObjectName("Line9")

        self.line10 = QFrame(self)
        self.line10.setFrameShape(QFrame.Shape.HLine)
        self.line10.setObjectName("Line10")

        self.line11 = QFrame(self)
        self.line11.setFrameShape(QFrame.Shape.HLine)
        self.line11.setObjectName("Line11")

        self.line12 = QFrame(self)
        self.line12.setFrameShape(QFrame.Shape.HLine)
        self.line12.setObjectName("Line12")

        self.button_quit_application = QPushButton("Quit", self)
        self.button_quit_application.setObjectName("ButtonQuitApplication")
        self.button_quit_application.setGeometry(144, 3000, 576, 576)
        self.button_quit_application.clicked.connect(self.ButtonQuitApplicatio_Click)

        self.line14 = QFrame(self)
        self.line14.setFrameShape(QFrame.Shape.HLine)
        self.line14.setObjectName("Line14")

        self.line15 = QFrame(self)
        self.line15.setFrameShape(QFrame.Shape.HLine)
        self.line15.setObjectName("Line15")

        self.line16 = QFrame(self)
        self.line16.setFrameShape(QFrame.Shape.HLine)
        self.line16.setObjectName("Line16")

        self.line17 = QFrame(self)
        self.line17.setFrameShape(QFrame.Shape.HLine)
        self.line17.setObjectName("Line17")

        self.button_open_styles = QPushButton("Styles", self)
        self.button_open_styles.setObjectName("ButtonOpenStyles")
        self.button_open_styles.setGeometry(2304, 120, 840, 465)
        self.button_open_styles.clicked.connect(self.ButtonOpenStyles_Click)

        self.text20 = QLabel("belong", self)
        self.text20.setObjectName("Text20")
        self.text20.setGeometry(2448, 840, 576, 240)

        self.line21 = QFrame(self)
        self.line21.setFrameShape(QFrame.Shape.HLine)
        self.line21.setObjectName("Line21")

        self.line22 = QFrame(self)
        self.line22.setFrameShape(QFrame.Shape.HLine)
        self.line22.setObjectName("Line22")

        self.button__open_query__records__songs__artists = QPushButton("Records_Songs_Artists", self)
        self.button__open_query__records__songs__artists.setObjectName("Button_OpenQuery_Records_Songs_Artists")
        self.button__open_query__records__songs__artists.setGeometry(3753, 600, 2295, 345)
        self.button__open_query__records__songs__artists.setFont(QFont("r_ansi", 8))
        self.button__open_query__records__songs__artists.clicked.connect(self.Button_OpenQuery_Rec_Click)

        self.label24 = QLabel("v5  25-Mar-2003", self)
        self.label24.setObjectName("Label24")
        self.label24.setGeometry(285, 285, 1290, 240)

    def _show_message(self, message: str) -> None:
        QMessageBox.information(self, "", message)

    def Button_OpenQuery_Rec_Click(self) -> None:
        try:
            query_name = "Records_Songs_Artists"
            self._show_message(f"Open query: {query_name}")
        except Exception as exc:  # noqa: BLE001
            self._show_message(str(exc))

    def ButtonOpenArtists_Click(self) -> None:
        try:
            self._show_message("Open Artists")
        except Exception as exc:  # noqa: BLE001
            self._show_message(str(exc))

    def ButtonOpenPrograms_Click(self) -> None:
        try:
            self._show_message("Open Programs")
        except Exception as exc:  # noqa: BLE001
            self._show_message(str(exc))

    def ButtonOpenRecords_Click(self) -> None:
        try:
            self._show_message("Open Records")
        except Exception as exc:  # noqa: BLE001
            self._show_message(str(exc))

    def ButtonOpenSongs_Click(self) -> None:
        try:
            self._show_message("Open Songs")
        except Exception as exc:  # noqa: BLE001
            self._show_message(str(exc))

    def ButtonOpenStyles_Click(self) -> None:
        try:
            self._show_message("Open Styles")
        except Exception as exc:  # noqa: BLE001
            self._show_message(str(exc))

    def ButtonQuitApplicatio_Click(self) -> None:
        try:
            self.close()
        except Exception as exc:  # noqa: BLE001
            self._show_message(str(exc))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec())
