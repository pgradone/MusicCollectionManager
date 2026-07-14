"""
Auto-generated PySide6 form: ProgramsSched
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


class ProgramsSched(QMainWindow):
    """Migrated from Access form: ProgramsSched.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ProgramsSchedule")
        self.setObjectName("ProgramsSched")
        self.resize(616, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("ProgramsSchedule")
        self.text12.setGeometry(22, 3, 184, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text12.setFont(_fnt)


        self.text13 = QLabel(self.central_widget)
        self.text13.setObjectName("Text13")
        self.text13.setText("ProgramsSchedule")
        self.text13.setGeometry(19, 1, 184, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text13.setFont(_fnt)


        self.text40 = QLabel(self.central_widget)
        self.text40.setObjectName("Text40")
        self.text40.setText("Song")
        self.text40.setGeometry(29, 32, 38, 16)
        self.text40.setStyleSheet("background-color: #E8FFFF")


        self.text42 = QLabel(self.central_widget)
        self.text42.setObjectName("Text42")
        self.text42.setText("SongTitle * Artist(s)")
        self.text42.setGeometry(67, 32, 126, 16)
        self.text42.setStyleSheet("background-color: #8080FF")


        self.text43 = QLabel(self.central_widget)
        self.text43.setObjectName("Text43")
        self.text43.setText("Record(s) of Song")
        self.text43.setGeometry(307, 32, 135, 16)
        self.text43.setStyleSheet("background-color: #8080FF")


        self.text44 = QLabel(self.central_widget)
        self.text44.setObjectName("Text44")
        self.text44.setText("BPM")
        self.text44.setGeometry(556, 32, 29, 16)
        self.text44.setStyleSheet("background-color: #8080FF")


        self.text45 = QLabel(self.central_widget)
        self.text45.setObjectName("Text45")
        self.text45.setText("yr")
        self.text45.setGeometry(584, 32, 28, 16)
        self.text45.setStyleSheet("background-color: #8080FF")


        self.text46 = QLabel(self.central_widget)
        self.text46.setObjectName("Text46")
        self.text46.setText("pos.")
        self.text46.setGeometry(1, 32, 30, 16)
        self.text46.setStyleSheet("background-color: #E8FFFF")


        self.song_i_d = QLineEdit(self.central_widget)
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(19, 1, 29, 2)

        self.song_i_d.doubleClicked.connect(self.SongID_DblClick)

        self.song__artist = QLineEdit(self.central_widget)
        self.song__artist.setObjectName("Song_Artist")
        self.song__artist.setText("Song_Artist")
        self.song__artist.setGeometry(48, 1, 250, 2)


        self.b_p_m = QLineEdit(self.central_widget)
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setToolTip("beats per minute")
        self.b_p_m.setGeometry(556, 1, 29, 2)


        self.year = QLineEdit(self.central_widget)
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(585, 1, 31, 2)


        self.record = QLineEdit(self.central_widget)
        self.record.setObjectName("Record")
        self.record.setText("Record")
        self.record.setGeometry(298, 1, 257, 2)


        self.position = QLineEdit(self.central_widget)
        self.position.setObjectName("Position")
        self.position.setText("Position")
        self.position.setGeometry(1, 1, 19, 16)



    # --- VBA Event Handlers ---


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
    window = ProgramsSched()
    window.show()
    sys.exit(app.exec())
