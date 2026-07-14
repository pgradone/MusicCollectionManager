"""
Auto-generated PySide6 form: Songs
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


class Songs(QMainWindow):
    """Migrated from Access form: Songs.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Songs")
        self.setObjectName("Songs")
        self.resize(684, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Songs")
        self.text12.setGeometry(2, 3, 74, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text12.setFont(_fnt)


        self.text13 = QLabel(self.central_widget)
        self.text13.setObjectName("Text13")
        self.text13.setText("Songs")
        self.text13.setGeometry(1, 1, 68, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text13.setFont(_fnt)


        self.button_delete_song = QPushButton(self.central_widget)
        self.button_delete_song.setObjectName("ButtonDeleteSong")
        self.button_delete_song.setText("Button42")
        self.button_delete_song.setGeometry(567, 1, 38, 32)

        self.button_delete_song.clicked.connect(self.ButtonDeleteSong_Click)

        self.button_add_song = QPushButton(self.central_widget)
        self.button_add_song.setObjectName("ButtonAddSong")
        self.button_add_song.setText("Add New Song")
        self.button_add_song.setToolTip("Create new song with ID")
        self.button_add_song.setGeometry(461, 1, 102, 32)
        _fnt = QFont("Terminal", 8)
        self.button_add_song.setFont(_fnt)

        self.button_add_song.clicked.connect(self.ButtonAddSong_Click)

        self.song_i_d = QComboBox(self.central_widget)
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.addItems(["FreeSongIDs"])
        self.song_i_d.setCurrentText("SongID")
        self.song_i_d.setToolTip("ID or Code of record")
        self.song_i_d.setGeometry(114, 8, 58, 16)
        self.song_i_d.setEditable(True)

        self.song_i_d.doubleClicked.connect(self.SongID_DblClick)

        self.song_combo = QComboBox(self.central_widget)
        self.song_combo.setObjectName("SongCombo")
        self.song_combo.addItems(["SongCombo_Query"])
        self.song_combo.setToolTip("Song to go to")
        self.song_combo.setGeometry(244, 8, 208, 16)
        self.song_combo.setStyleSheet("background-color: #FFFF80")
        self.song_combo.setEditable(True)


        self.title = QLineEdit(self.central_widget)
        self.title.setObjectName("Title")
        self.title.setText("Title")
        self.title.setToolTip("Song Title")
        self.title.setGeometry(48, 6, 379, 17)
        _fnt = QFont()
        _fnt.setPointSize(9)
        self.title.setFont(_fnt)

        self.title.doubleClicked.connect(self.Title_DblClick)

        self.b_p_m = QLineEdit(self.central_widget)
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setToolTip("Beats Per Minute")
        self.b_p_m.setGeometry(474, 6, 39, 2)
        _fnt = QFont()
        _fnt.setPointSize(9)
        self.b_p_m.setFont(_fnt)

        self.b_p_m.doubleClicked.connect(self.BPM_DblClick)

        self.year = QLineEdit(self.central_widget)
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setToolTip("Year of Song")
        self.year.setGeometry(550, 6, 39, 2)
        _fnt = QFont()
        _fnt.setPointSize(9)
        self.year.setFont(_fnt)

        self.year.doubleClicked.connect(self.Year_DblClick)

        # SubForm: Embedded33
        self.embedded33 = QWidget(self.central_widget)
        self.embedded33.setObjectName("Embedded33")
        self.embedded33.setProperty("sourceObject", "Form.Artists of Song")
        self.embedded33.setGeometry(1, 32, 442, 112)


        # SubForm: Embedded35
        self.embedded35 = QWidget(self.central_widget)
        self.embedded35.setObjectName("Embedded35")
        self.embedded35.setProperty("sourceObject", "Form.Records of Song")
        self.embedded35.setGeometry(1, 152, 605, 119)


        self.time = QLineEdit(self.central_widget)
        self.time.setObjectName("Time")
        self.time.setText("Time")
        self.time.setToolTip("duration")
        self.time.setGeometry(636, 6, 39, 16)
        _fnt = QFont()
        _fnt.setPointSize(9)
        self.time.setFont(_fnt)

        self.time.doubleClicked.connect(self.Time_DblClick)

        # SubForm: StylesOfSong
        self.styles_of_song = QWidget(self.central_widget)
        self.styles_of_song.setObjectName("StylesOfSong")
        self.styles_of_song.setProperty("sourceObject", "Form.StylesOfSong")
        self.styles_of_song.setGeometry(451, 32, 233, 110)



    # --- VBA Event Handlers ---


    def BPM_DblClick(self, Cancel: int) -> None:

        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
        pass

    def ButtonAddSong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonAddSong_Click

          # NewIDMgt.AddNewID "SongID", "FreeSongIDs"

        MyFirstControl: str = None
        # DoCmd.GoToRecord , , acNewRec
        MyFirstControl = "Title"

        # DoCmd.GoToControl MyFirstControl

        # label: Exit_ButtonAddSong_Click
        return

        # label: Err_ButtonAddSong_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonAddSong_Click

    def ButtonDeleteSong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDeleteSong_Click

        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

        # label: Exit_ButtonDeleteSong_Click
        return

        # label: Err_ButtonDeleteSong_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonDeleteSong_Click

    def Field37_AfterUpdate(self) -> None:

        MyDb: Any = None
        MyTable: Any = None
        MyDb = DBEngine.Workspaces(0).Databases(0)
        MyTable = MyDb.OpenRecordset("Contain", DB_OPEN_TABLE)
        MyTable.Index = "PrimaryKey"
        MyTable.AddNew()
        MyTable["SongID"] = self.SongCombo
        MyTable["RecordID"] = self.RecordID
        MyTable.Update()
        MyTable.Close()
        self.Refresh()
        self.SongCombo = ""

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID(self.Name, "SongID")

    def SongCombo_AfterUpdate(self) -> None:

        Criteria: str = None
        MyRS: Any = None
        ActiveName: str = None
        Prompt: str = None
        Message: str = None
        CRLF: str = None
        # VBA Const: MB_ICONQUESTION = 32
        # VBA Const: YES = 6
        # VBA Const: YES_NO = 4
        CRLF = chr(13)

        Prompt = "Create new one?"
        MyRS = self.RecordsetClone

          # Build the criteria.
        ActiveName = self.focusWidget() if self.focusWidget() else ""
        Criteria = "[SongID] = " + ActiveName
          # Perform the search.
        MyRS.FindFirst(Criteria)

        if MyRS.NoMatch:
            Message = ActiveName + " not found" + CRLF
            if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new Song")  ==  YES:
                # DoCmd.GoToRecord , , A_NEWREC
                self.SongID = self.SongCombo
                self.Refresh()
        else:
              # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark

        self.SongCombo = ""

    def SongID_AfterUpdate(self) -> None:
        self.Refresh()

    def SongID_DblClick(self, Cancel: int) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
        pass

    def Time_DblClick(self, Cancel: int) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
        pass

    def Title_DblClick(self, Cancel: int) -> None:
        # VBA: On Error GoTo Err_title_dblClick

        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

        # label: Exit_Button48_Click
        return

        # label: Err_title_dblClick
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_Button48_Click

    def Year_DblClick(self, Cancel: int) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Songs()
    window.show()
    sys.exit(app.exec())
