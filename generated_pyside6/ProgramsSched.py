"""
Auto-generated PySide6 form: ProgramsSched
Generated: 2026-07-14 15:06:58
"""

import sys
from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QTextEdit, QPushButton, QCheckBox,
    QRadioButton, QComboBox, QListWidget, QTabWidget,
    QFrame, QMessageBox, QDateEdit, QSpinBox,
)
from PySide6.QtGui import QFont, QPixmap, QAction


class ProgramsSched(QMainWindow):
    """Migrated from Access form: ProgramsSched"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ProgramsSchedule")
        self.setObjectName("ProgramsSched")
        self.resize(9242, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("ProgramsSchedule")
        self.text12.setGeometry(324, 40, 2760, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text12.setFont(_fnt)

        self.text13 = QLabel()
        self.text13.setObjectName("Text13")
        self.text13.setText("ProgramsSchedule")
        self.text13.setGeometry(288, 10, 2760, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text13.setFont(_fnt)

        self.text40 = QLabel()
        self.text40.setObjectName("Text40")
        self.text40.setText("Song")
        self.text40.setGeometry(432, 480, 564, 240)
        self.text40.setStyleSheet("background-color: #E8FFFF")

        self.text42 = QLabel()
        self.text42.setObjectName("Text42")
        self.text42.setText("SongTitle * Artist(s)")
        self.text42.setGeometry(1008, 480, 1890, 240)
        self.text42.setStyleSheet("background-color: #8080FF")

        self.text43 = QLabel()
        self.text43.setObjectName("Text43")
        self.text43.setText("Record(s) of Song")
        self.text43.setGeometry(4608, 480, 2025, 240)
        self.text43.setStyleSheet("background-color: #8080FF")

        self.text44 = QLabel()
        self.text44.setObjectName("Text44")
        self.text44.setText("BPM")
        self.text44.setGeometry(8333, 480, 441, 240)
        self.text44.setStyleSheet("background-color: #8080FF")

        self.text45 = QLabel()
        self.text45.setObjectName("Text45")
        self.text45.setText("yr")
        self.text45.setGeometry(8765, 480, 426, 240)
        self.text45.setStyleSheet("background-color: #8080FF")

        self.text46 = QLabel()
        self.text46.setObjectName("Text46")
        self.text46.setText("pos.")
        self.text46.setGeometry(10, 480, 450, 240)
        self.text46.setStyleSheet("background-color: #E8FFFF")

        self.song_i_d = QLineEdit()
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(288, 10, 435, 25)
        self.song_i_d.doubleClicked.connect(self.SongID_DblClick)

        self.song__artist = QLineEdit()
        self.song__artist.setObjectName("Song_Artist")
        self.song__artist.setText("Song_Artist")
        self.song__artist.setGeometry(720, 10, 3750, 25)

        self.b_p_m = QLineEdit()
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setToolTip("beats per minute")
        self.b_p_m.setGeometry(8339, 10, 435, 25)

        self.year = QLineEdit()
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(8777, 10, 465, 25)

        self.record = QLineEdit()
        self.record.setObjectName("Record")
        self.record.setText("Record")
        self.record.setGeometry(4464, 10, 3855, 25)

        self.position = QLineEdit()
        self.position.setObjectName("Position")
        self.position.setText("Position")
        self.position.setGeometry(10, 10, 282, 240)


    # --- VBA Event Handlers ---


    def SongID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyKey: str = None

        if Screen.ActiveControl != "":
            MyForm = "Songs"
            MyKey = "SongID"
            MyFirstControl = "Title"

            GotoCriteria = Screen.ActiveControl
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProgramsSched()
    window.show()
    sys.exit(app.exec())
