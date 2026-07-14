"""
Auto-generated PySide6 form: SongsOfRecord
Generated: 2026-07-14 15:57:49
"""

import sys
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QGroupBox, QLabel, QLineEdit, QTextEdit, QPushButton,
    QCheckBox, QRadioButton, QComboBox, QListWidget,
    QTabWidget, QFrame, QMessageBox, QDateEdit, QSpinBox,
)
from PySide6.QtGui import QFont, QPixmap, QAction


class SongsOfRecord(QMainWindow):
    """Migrated from Access form: SongsOfRecord.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Songs Of Record")
        self.setObjectName("SongsOfRecord")
        self.resize(503, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text7 = QLabel(self.central_widget)
        self.text7.setObjectName("Text7")
        self.text7.setText("Songs Of Record")
        self.text7.setGeometry(2, 3, 166, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)


        self.text8 = QLabel(self.central_widget)
        self.text8.setObjectName("Text8")
        self.text8.setText("Songs Of Record")
        self.text8.setGeometry(1, 1, 166, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)


        self.text10 = QLabel(self.central_widget)
        self.text10.setObjectName("Text10")
        self.text10.setText("SongID")
        self.text10.setGeometry(1, 24, 48, 16)


        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Pos")
        self.text12.setGeometry(48, 24, 29, 16)


        self.text14 = QLabel(self.central_widget)
        self.text14.setObjectName("Text14")
        self.text14.setText("Title")
        self.text14.setGeometry(86, 24, 35, 16)


        self.text16 = QLabel(self.central_widget)
        self.text16.setObjectName("Text16")
        self.text16.setText("BPM")
        self.text16.setGeometry(329, 24, 36, 16)


        self.text18 = QLabel(self.central_widget)
        self.text18.setObjectName("Text18")
        self.text18.setText("yr")
        self.text18.setGeometry(366, 24, 34, 16)


        self.text20 = QLabel(self.central_widget)
        self.text20.setObjectName("Text20")
        self.text20.setText("Time")
        self.text20.setGeometry(401, 24, 37, 16)


        self.text25 = QLabel(self.central_widget)
        self.text25.setObjectName("Text25")
        self.text25.setText("remove")
        self.text25.setGeometry(439, 24, 58, 16)


        self.song_combo = QComboBox(self.central_widget)
        self.song_combo.setObjectName("SongCombo")
        self.song_combo.addItems(["SongOfRecordCombo_Query"])
        self.song_combo.setGeometry(268, 1, 192, 16)
        self.song_combo.setEditable(True)


        self.song_i_d = QLineEdit(self.central_widget)
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(1, 1, 38, 2)

        self.song_i_d.doubleClicked.connect(self.SongID_DblClick)

        self.title = QLineEdit(self.central_widget)
        self.title.setObjectName("Title")
        self.title.setText("Title")
        self.title.setGeometry(77, 1, 251, 2)


        self.b_p_m = QLineEdit(self.central_widget)
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setGeometry(329, 1, 38, 2)


        self.year = QLineEdit(self.central_widget)
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(366, 1, 34, 2)


        self.time = QLineEdit(self.central_widget)
        self.time.setObjectName("Time")
        self.time.setText("Time")
        self.time.setGeometry(401, 1, 38, 2)


        self.position = QComboBox(self.central_widget)
        self.position.setObjectName("Position")
        self.position.addItems(["PositionsOfContain"])
        self.position.setCurrentText("Position")
        self.position.setGeometry(38, 1, 38, 16)
        self.position.setEditable(True)


        self.button_remove_song = QPushButton(self.central_widget)
        self.button_remove_song.setObjectName("ButtonRemoveSong")
        self.button_remove_song.setText("del")
        self.button_remove_song.setGeometry(439, 1, 58, 16)
        _fnt = QFont("Terminal", 6)
        self.button_remove_song.setFont(_fnt)

        self.button_remove_song.clicked.connect(self.ButtonRemoveSong_Click)


    # --- VBA Event Handlers ---


    def ButtonOpenAllSongs_Click(self) -> None:
        pass

    def ButtonRemoveSong_Click(self) -> None:

        # Forms! reference: RelationsMgt.RemoveFromButton "Contain", Forms!Records![RecordID], self.SongID, "RecordHouse"
        pass

    def SongCombo_AfterUpdate(self) -> None:

        # Forms! reference: RelationsMgt.AddFromCombo Forms!Records![RecordID], "RecordHouse", self.SongCombo, "RecordID", "SongID", "Records", "Contain"
        pass

    def SongID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyForm: str = None
        MyKey: str = None
        MyFirstControl: str = None

        if self.focusWidget() if self.focusWidget() else "" != "":
            MyForm = "Songs"
            MyKey = "SongID"
            MyFirstControl = "Title"

            GotoCriteria = self.focusWidget() if self.focusWidget() else ""
            # TODO: DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SongsOfRecord()
    window.show()
    sys.exit(app.exec())
