"""
Auto-generated PySide6 form: Songs
Generated: 2026-07-15 08:57:01
"""

import sys
import datetime
from typing import Any
from PySide6.QtCore import Qt, Slot, QTimer, QEvent, QObject
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
        self._dbl_click_widgets: set[QObject] = set()
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

        self.song_i_d.installEventFilter(self)
        self._dbl_click_widgets.add(self.song_i_d)
        # DblClick -> self.SongID_DblClick (via eventFilter)

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

        self.title.installEventFilter(self)
        self._dbl_click_widgets.add(self.title)
        # DblClick -> self.Title_DblClick (via eventFilter)

        self.b_p_m = QLineEdit(self.central_widget)
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setToolTip("Beats Per Minute")
        self.b_p_m.setGeometry(474, 6, 39, 2)
        _fnt = QFont()
        _fnt.setPointSize(9)
        self.b_p_m.setFont(_fnt)

        self.b_p_m.installEventFilter(self)
        self._dbl_click_widgets.add(self.b_p_m)
        # DblClick -> self.BPM_DblClick (via eventFilter)

        self.year = QLineEdit(self.central_widget)
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setToolTip("Year of Song")
        self.year.setGeometry(550, 6, 39, 2)
        _fnt = QFont()
        _fnt.setPointSize(9)
        self.year.setFont(_fnt)

        self.year.installEventFilter(self)
        self._dbl_click_widgets.add(self.year)
        # DblClick -> self.Year_DblClick (via eventFilter)

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

        self.time.installEventFilter(self)
        self._dbl_click_widgets.add(self.time)
        # DblClick -> self.Time_DblClick (via eventFilter)

        # SubForm: StylesOfSong
        self.styles_of_song = QWidget(self.central_widget)
        self.styles_of_song.setObjectName("StylesOfSong")
        self.styles_of_song.setProperty("sourceObject", "Form.StylesOfSong")
        self.styles_of_song.setGeometry(451, 32, 233, 110)



    # --- VBA Event Handlers ---


    def BPM_DblClick(self, Cancel: int) -> None:

        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
        pass

    def ButtonAddSong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonAddSong_Click

          # NewIDMgt.AddNewID "SongID", "FreeSongIDs"

        MyFirstControl: str = ""
        # TODO: DoCmd.GoToRecord , , acNewRec
        MyFirstControl = "Title"

        # TODO: DoCmd.GoToControl MyFirstControl

        # label: Exit_ButtonAddSong_Click
        return

        # label: Err_ButtonAddSong_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonAddSong_Click

    def ButtonDeleteSong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDeleteSong_Click

        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

        # label: Exit_ButtonDeleteSong_Click
        return

        # label: Err_ButtonDeleteSong_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonDeleteSong_Click

    def Field37_AfterUpdate(self) -> None:

        MyDb: Any = None
        MyTable: Any = None
        # TODO: Set MyDb = DBEngine.Workspaces(0).Databases(0)
        MyTable = MyDb.OpenRecordset("Contain", 1)
        MyTable.Index = "PrimaryKey"
        MyTable.AddNew()
        MyTable["SongID"] = self.song_combo.currentText()
        MyTable["RecordID"] = ""  # TODO: self.record_i_d.currentText()
        MyTable.Update()
        MyTable.Close()
        self.Refresh()
        self.song_combo.setCurrentText("")


    def Form_BeforeInsert(self, Cancel: int) -> None:
        # TODO: BuildNewID Me.Name, "SongID"
        pass

    def SongCombo_AfterUpdate(self) -> None:

        Criteria: str = ""
        MyRS: Any = None
        ActiveName: str = ""
        Prompt: str = ""
        Message: str = ""
        CRLF: str = ""
        # VBA Const: MB_ICONQUESTION = 32
        # VBA Const: YES = 6
        # VBA Const: YES_NO = 4
        CRLF = chr(13)

        Prompt = "Create new one?"
        MyRS = self.RecordsetClone

          # Build the criteria.
        ActiveName = str(self.focusWidget()) if self.focusWidget() else ""
        Criteria = "[SongID] = " + str(str(ActiveName))
          # Perform the search.
        MyRS.FindFirst(Criteria)

        if MyRS.NoMatch:
            Message = ActiveName + " not found" + CRLF
            if QMessageBox.question(self, "", str(Message + Prompt), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)  ==  QMessageBox.StandardButton.Yes:
                # TODO: DoCmd.GoToRecord , , A_NEWREC
                # TODO: self.song_i_d = self.song_combo.currentText()
                self.Refresh()
        else:
              # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark

        self.song_combo.setCurrentText("")


    def SongID_AfterUpdate(self) -> None:
        self.Refresh()

    def SongID_DblClick(self, Cancel: int) -> None:
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
        pass

    def Time_DblClick(self, Cancel: int) -> None:
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
        pass

    def Title_DblClick(self, Cancel: int) -> None:
        # VBA: On Error GoTo Err_title_dblClick

        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

        # label: Exit_Button48_Click
        return

        # label: Err_title_dblClick
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_Button48_Click

    def Year_DblClick(self, Cancel: int) -> None:
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
        pass

    # Access form compatibility stubs
    @property
    def RecordsetClone(self) -> Any:
        return None

    @property
    def Bookmark(self) -> Any:
        return None

    @Bookmark.setter
    def Bookmark(self, value: Any) -> None:
        pass

    def Refresh(self) -> None:
        pass

    def Requery(self) -> None:
        pass

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.MouseButtonDblClick:
            if obj in self._dbl_click_widgets:
                handler_name = f"{obj.objectName()}_DblClick"
                handler = getattr(self, handler_name, None)
                if handler:
                    handler()
                    return True
        return super().eventFilter(obj, event)


        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Songs()
    window.show()
    sys.exit(app.exec())
