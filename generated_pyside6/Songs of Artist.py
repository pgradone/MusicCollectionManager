"""
Auto-generated PySide6 form: Songs of Artist
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


class Songs_of_Artist(QMainWindow):
    """Migrated from Access form: Songs of Artist.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Songs of Artist")
        self.setObjectName("Songs of Artist")
        self.resize(423, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text7 = QLabel(self.central_widget)
        self.text7.setObjectName("Text7")
        self.text7.setText("Songs of Artist")
        self.text7.setGeometry(2, 3, 140, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)


        self.text8 = QLabel(self.central_widget)
        self.text8.setObjectName("Text8")
        self.text8.setText("Songs of Artist")
        self.text8.setGeometry(1, 1, 140, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)


        self.text10 = QLabel(self.central_widget)
        self.text10.setObjectName("Text10")
        self.text10.setText("SongID")
        self.text10.setGeometry(1, 32, 52, 16)


        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Title")
        self.text12.setGeometry(58, 32, 37, 16)


        self.text18 = QLabel(self.central_widget)
        self.text18.setObjectName("Text18")
        self.text18.setText("BPM")
        self.text18.setGeometry(278, 32, 29, 16)


        self.text20 = QLabel(self.central_widget)
        self.text20.setObjectName("Text20")
        self.text20.setText("year")
        self.text20.setGeometry(307, 32, 30, 16)


        self.text24 = QLabel(self.central_widget)
        self.text24.setObjectName("Text24")
        self.text24.setText("time")
        self.text24.setGeometry(336, 32, 29, 16)


        self.text26 = QLabel(self.central_widget)
        self.text26.setObjectName("Text26")
        self.text26.setText("remove")
        self.text26.setGeometry(374, 32, 46, 16)


        self.song_combo = QComboBox(self.central_widget)
        self.song_combo.setObjectName("SongCombo")
        self.song_combo.addItems(["SongofArtistsCombo_Query"])
        self.song_combo.setGeometry(181, 8, 236, 16)
        self.song_combo.setEditable(True)


        self.text27 = QLabel(self.central_widget)
        self.text27.setObjectName("Text27")
        self.text27.setText("Add:")
        self.text27.setGeometry(144, 8, 32, 16)


        self.song_i_d = QLineEdit(self.central_widget)
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(1, 1, 38, 2)

        self.song_i_d.doubleClicked.connect(self.SongID_DblClick)

        self.songs__title = QLineEdit(self.central_widget)
        self.songs__title.setObjectName("Songs.Title")
        self.songs__title.setText("Songs.Title")
        self.songs__title.setGeometry(38, 1, 240, 2)


        self.b_p_m = QLineEdit(self.central_widget)
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setGeometry(278, 1, 29, 2)


        self.year = QLineEdit(self.central_widget)
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(307, 1, 29, 2)


        self.time = QLineEdit(self.central_widget)
        self.time.setObjectName("Time")
        self.time.setText("Time")
        self.time.setGeometry(336, 1, 38, 16)


        self.button_remove_song = QPushButton(self.central_widget)
        self.button_remove_song.setObjectName("ButtonRemoveSong")
        self.button_remove_song.setText("del")
        self.button_remove_song.setGeometry(374, 1, 49, 16)
        _fnt = QFont("Terminal", 6)
        self.button_remove_song.setFont(_fnt)

        self.button_remove_song.clicked.connect(self.ButtonRemoveSong_Click)


    # --- VBA Event Handlers ---


    def Button23_Click(self) -> None:

        MyDb: Any = None
        MyTable: Any = None
        MyQuery: Any = None
        MyDb = DBEngine.Workspaces(0).Databases(0)
        MyTable = MyDb.OpenRecordset("Sing", DB_OPEN_TABLE)

        MyTable.Index = "PrimaryKey"
        # Forms! reference: MyTable.Seek "=", Forms!Employees![EmployeeID], self.CompanyID

        if not MyTable.NoMatch:
            MyTable.Delete()
        MyTable.Close()
        Forms.Artistss.Refresh()

    def ButtonRemoveSong_Click(self) -> None:

        # Forms! reference: RelationsMgt.RemoveFromButton "Sing", Forms!Artists![ArtistID], self.SongID, "Surname"
        pass

    def RecordID_DblClick(self, Cancel: int) -> None:

        FormName: str = None
        LinkCriteria: str = None

        FormName = "Records"
        if self.RecordID != "":
            LinkCriteria = "[RecordID]=" + self.focusWidget() if self.focusWidget() else ""
            # TODO: DoCmd.OpenForm FormName, , , LinkCriteria

    def SongCombo_AfterUpdate(self) -> None:

        # Forms! reference: RelationsMgt.AddFromCombo Forms!Artists![ArtistID], "Surname", self.SongCombo, "ArtistID", "SongID", "Artists", "Sing"
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
    window = Songs_of_Artist()
    window.show()
    sys.exit(app.exec())
