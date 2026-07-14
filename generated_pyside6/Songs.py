"""
Auto-generated PySide6 form: Songs
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


class Songs(QMainWindow):
    """Migrated from Access form: Songs"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Songs")
        self.setObjectName("Songs")
        self.resize(10261, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("Songs")
        self.text12.setGeometry(36, 40, 1110, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text12.setFont(_fnt)

        self.text13 = QLabel()
        self.text13.setObjectName("Text13")
        self.text13.setText("Songs")
        self.text13.setGeometry(10, 10, 1020, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text13.setFont(_fnt)

        self.button_delete_song = QPushButton()
        self.button_delete_song.setObjectName("ButtonDeleteSong")
        self.button_delete_song.setText("Button42")
        self.button_delete_song.setGeometry(8503, 10, 576, 486)
        self.button_delete_song.clicked.connect(self.ButtonDeleteSong_Click)

        self.button_add_song = QPushButton()
        self.button_add_song.setObjectName("ButtonAddSong")
        self.button_add_song.setText("Add New Song")
        self.button_add_song.setToolTip("Create new song with ID")
        self.button_add_song.setGeometry(6915, 10, 1530, 480)
        _fnt = QFont("Terminal", 8)
        self.button_add_song.setFont(_fnt)
        self.button_add_song.clicked.connect(self.ButtonAddSong_Click)

        self.song_i_d = QComboBox()
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.addItems(["FreeSongIDs"])
        self.song_i_d.setCurrentText("SongID")
        self.song_i_d.setToolTip("ID or Code of record")
        self.song_i_d.setGeometry(1710, 120, 864, 240)
        self.song_i_d.setEditable(True)
        self.song_i_d.doubleClicked.connect(self.SongID_DblClick)

        self.song_combo = QComboBox()
        self.song_combo.setObjectName("SongCombo")
        self.song_combo.addItems(["SongCombo_Query"])
        self.song_combo.setToolTip("Song to go to")
        self.song_combo.setGeometry(3655, 120, 3114, 240)
        self.song_combo.setStyleSheet("background-color: #FFFF80")
        self.song_combo.setEditable(True)

        self.title = QLineEdit()
        self.title.setObjectName("Title")
        self.title.setText("Title")
        self.title.setToolTip("Song Title")
        self.title.setGeometry(720, 94, 5685, 261)
        _fnt = QFont()
        _fnt.setPointSize(9)
        self.title.setFont(_fnt)
        self.title.doubleClicked.connect(self.Title_DblClick)

        self.b_p_m = QLineEdit()
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setToolTip("Beats Per Minute")
        self.b_p_m.setGeometry(7104, 94, 585, 25)
        _fnt = QFont()
        _fnt.setPointSize(9)
        self.b_p_m.setFont(_fnt)
        self.b_p_m.doubleClicked.connect(self.BPM_DblClick)

        self.year = QLineEdit()
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setToolTip("Year of Song")
        self.year.setGeometry(8256, 94, 585, 25)
        _fnt = QFont()
        _fnt.setPointSize(9)
        self.year.setFont(_fnt)
        self.year.doubleClicked.connect(self.Year_DblClick)

        # SubForm: Embedded33
        self.embedded33 = QWidget()
        self.embedded33.setObjectName("Embedded33")
        self.embedded33.setProperty("sourceObject", "Form.Artists of Song")
        self.embedded33.setGeometry(10, 480, 6627, 1680)

        # SubForm: Embedded35
        self.embedded35 = QWidget()
        self.embedded35.setObjectName("Embedded35")
        self.embedded35.setProperty("sourceObject", "Form.Records of Song")
        self.embedded35.setGeometry(10, 2280, 9075, 1785)

        self.time = QLineEdit()
        self.time.setObjectName("Time")
        self.time.setText("Time")
        self.time.setToolTip("duration")
        self.time.setGeometry(9544, 94, 582, 240)
        _fnt = QFont()
        _fnt.setPointSize(9)
        self.time.setFont(_fnt)
        self.time.doubleClicked.connect(self.Time_DblClick)

        # SubForm: StylesOfSong
        self.styles_of_song = QWidget()
        self.styles_of_song.setObjectName("StylesOfSong")
        self.styles_of_song.setProperty("sourceObject", "Form.StylesOfSong")
        self.styles_of_song.setGeometry(6768, 480, 3492, 1650)


    # --- VBA Event Handlers ---


    def BPM_DblClick(self, Cancel: int) -> None:

        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    def ButtonAddSong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonAddSong_Click
        # try:

            # NewIDMgt.AddNewID "SongID", "FreeSongIDs"

            MyFirstControl: str = None
            # DoCmd.GoToRecord , , acNewRec
            MyFirstControl = "Title"

            # DoCmd.GoToControl MyFirstControl

            # label: Exit_ButtonAddSong_Click

        # label: Err_ButtonAddSong_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonAddSong_Click

    def ButtonDeleteSong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDeleteSong_Click
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

            # label: Exit_ButtonDeleteSong_Click

        # label: Err_ButtonDeleteSong_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonDeleteSong_Click

    def Field37_AfterUpdate(self) -> None:

        MyDb: Any = None
        MyDb = DBEngine.Workspaces(0).Databases(0)
        MyTable = MyDb.OpenRecordset("Contain", DB_OPEN_TABLE)
        MyTable.Index = "PrimaryKey"
        MyTable.AddNew
        MyTable("SongID") = self.SongCombo
        MyTable("RecordID") = self.RecordID
        MyTable.Update
        MyTable.Close
        self.Refresh
        self.SongCombo = ""

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID self.Name, "SongID"

    def SongCombo_AfterUpdate(self) -> None:

        Criteria: str = None
        MyRS: Any = None
        ActiveName: str = None
        Prompt: str = None
        Const MB_ICONQUESTION = 32
        Const YES = 6
        Const YES_NO = 4
        CRLF = Chr$(13)

        Prompt = "Create new one?"
        MyRS = self.RecordsetClone

        # Build the criteria.
        ActiveName = Screen.ActiveControl
        Criteria = "[SongID] = " + ActiveName
        # Perform the search.
        MyRS.FindFirst Criteria

        if MyRS.NoMatch:
            Message = ActiveName + " not found" + CRLF
            if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new Song")  == YES:
                # DoCmd.GoToRecord , , A_NEWREC
                self.SongID = self.SongCombo
                self.Refresh
        else:
            # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark

        self.SongCombo = ""

    def SongID_AfterUpdate(self) -> None:
        self.Refresh

    def SongID_DblClick(self, Cancel: int) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    def Time_DblClick(self, Cancel: int) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    def Title_DblClick(self, Cancel: int) -> None:
        # VBA: On Error GoTo Err_title_dblClick
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

            # label: Exit_Button48_Click

        # label: Err_title_dblClick
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_Button48_Click

    def Year_DblClick(self, Cancel: int) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Songs()
    window.show()
    sys.exit(app.exec())
