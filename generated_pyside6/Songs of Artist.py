"""
Auto-generated PySide6 form: Songs of Artist
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


class Songs_of_Artist(QMainWindow):
    """Migrated from Access form: Songs of Artist"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Songs of Artist")
        self.setObjectName("Songs of Artist")
        self.resize(6348, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text7 = QLabel()
        self.text7.setObjectName("Text7")
        self.text7.setText("Songs of Artist")
        self.text7.setGeometry(36, 40, 2100, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)

        self.text8 = QLabel()
        self.text8.setObjectName("Text8")
        self.text8.setText("Songs of Artist")
        self.text8.setGeometry(10, 10, 2100, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)

        self.text10 = QLabel()
        self.text10.setObjectName("Text10")
        self.text10.setText("SongID")
        self.text10.setGeometry(10, 480, 780, 240)

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("Title")
        self.text12.setGeometry(864, 480, 555, 240)

        self.text18 = QLabel()
        self.text18.setObjectName("Text18")
        self.text18.setText("BPM")
        self.text18.setGeometry(4176, 480, 435, 240)

        self.text20 = QLabel()
        self.text20.setObjectName("Text20")
        self.text20.setText("year")
        self.text20.setGeometry(4608, 480, 450, 240)

        self.text24 = QLabel()
        self.text24.setObjectName("Text24")
        self.text24.setText("time")
        self.text24.setGeometry(5040, 480, 432, 240)

        self.text26 = QLabel()
        self.text26.setObjectName("Text26")
        self.text26.setText("remove")
        self.text26.setGeometry(5616, 480, 690, 240)

        self.song_combo = QComboBox()
        self.song_combo.setObjectName("SongCombo")
        self.song_combo.addItems(["SongofArtistsCombo_Query"])
        self.song_combo.setGeometry(2712, 120, 3534, 240)
        self.song_combo.setEditable(True)

        self.text27 = QLabel()
        self.text27.setObjectName("Text27")
        self.text27.setText("Add:")
        self.text27.setGeometry(2160, 120, 480, 240)

        self.song_i_d = QLineEdit()
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(10, 10, 570, 25)
        self.song_i_d.doubleClicked.connect(self.SongID_DblClick)

        self.songs__title = QLineEdit()
        self.songs__title.setObjectName("Songs.Title")
        self.songs__title.setText("Songs.Title")
        self.songs__title.setGeometry(576, 10, 3600, 25)

        self.b_p_m = QLineEdit()
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setGeometry(4176, 10, 435, 25)

        self.year = QLineEdit()
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(4608, 10, 435, 25)

        self.time = QLineEdit()
        self.time.setObjectName("Time")
        self.time.setText("Time")
        self.time.setGeometry(5040, 10, 576, 240)

        self.button_remove_song = QPushButton()
        self.button_remove_song.setObjectName("ButtonRemoveSong")
        self.button_remove_song.setText("del")
        self.button_remove_song.setGeometry(5616, 10, 732, 240)
        _fnt = QFont("Terminal", 6)
        self.button_remove_song.setFont(_fnt)
        self.button_remove_song.clicked.connect(self.ButtonRemoveSong_Click)


    # --- VBA Event Handlers ---


    def Button23_Click(self) -> None:

        MyDb: Any = None
        MyDb = DBEngine.Workspaces(0).Databases(0)
        MyTable = MyDb.OpenRecordset("Sing", DB_OPEN_TABLE)

        MyTable.Index = "PrimaryKey"
        MyTable.Seek "=", Forms!Employees![EmployeeID], self.CompanyID

        if Not MyTable.NoMatch:
            MyTable.Delete
        MyTable.Close
        Forms.Artistss.Refresh

    def ButtonRemoveSong_Click(self) -> None:

        RelationsMgt.RemoveFromButton "Sing", Forms!Artists![ArtistID], self.SongID, "Surname"

    def RecordID_DblClick(self, Cancel: int) -> None:

        FormName: str = None
        LinkCriteria: str = None

        FormName = "Records"
        if self.RecordID != "":
            LinkCriteria = "[RecordID]=" + Screen.ActiveControl
            # DoCmd.OpenForm FormName, , , LinkCriteria

    def SongCombo_AfterUpdate(self) -> None:

        RelationsMgt.AddFromCombo Forms!Artists![ArtistID], "Surname", self.SongCombo, "ArtistID", "SongID", "Artists", "Sing"

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
    window = Songs_of_Artist()
    window.show()
    sys.exit(app.exec())
