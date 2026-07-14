"""
Auto-generated PySide6 form: SongsOfRecord
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


class SongsOfRecord(QMainWindow):
    """Migrated from Access form: SongsOfRecord"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Songs Of Record")
        self.setObjectName("SongsOfRecord")
        self.resize(7540, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text7 = QLabel()
        self.text7.setObjectName("Text7")
        self.text7.setText("Songs Of Record")
        self.text7.setGeometry(36, 40, 2490, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)

        self.text8 = QLabel()
        self.text8.setObjectName("Text8")
        self.text8.setText("Songs Of Record")
        self.text8.setGeometry(10, 10, 2490, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)

        self.text10 = QLabel()
        self.text10.setObjectName("Text10")
        self.text10.setText("SongID")
        self.text10.setGeometry(10, 360, 720, 240)

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("Pos")
        self.text12.setGeometry(720, 360, 435, 240)

        self.text14 = QLabel()
        self.text14.setObjectName("Text14")
        self.text14.setText("Title")
        self.text14.setGeometry(1296, 360, 525, 240)

        self.text16 = QLabel()
        self.text16.setObjectName("Text16")
        self.text16.setText("BPM")
        self.text16.setGeometry(4932, 360, 540, 240)

        self.text18 = QLabel()
        self.text18.setObjectName("Text18")
        self.text18.setText("yr")
        self.text18.setGeometry(5493, 360, 510, 240)

        self.text20 = QLabel()
        self.text20.setObjectName("Text20")
        self.text20.setText("Time")
        self.text20.setGeometry(6009, 360, 555, 240)

        self.text25 = QLabel()
        self.text25.setObjectName("Text25")
        self.text25.setText("remove")
        self.text25.setGeometry(6585, 360, 864, 240)

        self.song_combo = QComboBox()
        self.song_combo.setObjectName("SongCombo")
        self.song_combo.addItems(["SongOfRecordCombo_Query"])
        self.song_combo.setGeometry(4026, 10, 2883, 240)
        self.song_combo.setEditable(True)

        self.song_i_d = QLineEdit()
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(10, 10, 570, 25)
        self.song_i_d.doubleClicked.connect(self.SongID_DblClick)

        self.title = QLineEdit()
        self.title.setObjectName("Title")
        self.title.setText("Title")
        self.title.setGeometry(1152, 10, 3765, 25)

        self.b_p_m = QLineEdit()
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setGeometry(4932, 10, 570, 25)

        self.year = QLineEdit()
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(5493, 10, 510, 25)

        self.time = QLineEdit()
        self.time.setObjectName("Time")
        self.time.setText("Time")
        self.time.setGeometry(6009, 10, 570, 25)

        self.position = QComboBox()
        self.position.setObjectName("Position")
        self.position.addItems(["PositionsOfContain"])
        self.position.setCurrentText("Position")
        self.position.setGeometry(576, 10, 576, 240)
        self.position.setEditable(True)

        self.button_remove_song = QPushButton()
        self.button_remove_song.setObjectName("ButtonRemoveSong")
        self.button_remove_song.setText("del")
        self.button_remove_song.setGeometry(6585, 10, 873, 240)
        _fnt = QFont("Terminal", 6)
        self.button_remove_song.setFont(_fnt)
        self.button_remove_song.clicked.connect(self.ButtonRemoveSong_Click)


    # --- VBA Event Handlers ---


    def ButtonOpenAllSongs_Click(self) -> None:
        pass

    def ButtonRemoveSong_Click(self) -> None:

        RelationsMgt.RemoveFromButton "Contain", Forms!Records![RecordID], self.SongID, "RecordHouse"

    def SongCombo_AfterUpdate(self) -> None:

        RelationsMgt.AddFromCombo Forms!Records![RecordID], "RecordHouse", self.SongCombo, "RecordID", "SongID", "Records", "Contain"

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
    window = SongsOfRecord()
    window.show()
    sys.exit(app.exec())
