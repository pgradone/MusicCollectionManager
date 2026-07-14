"""
Auto-generated PySide6 form: SongsOfStyle
Generated: 2026-07-14 17:13:42
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


class SongsOfStyle(QMainWindow):
    """Migrated from Access form: SongsOfStyle.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self._dbl_click_widgets: set[QObject] = set()
        self.setWindowTitle("Songs of Style")
        self.setObjectName("SongsOfStyle")
        self.resize(461, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text7 = QLabel(self.central_widget)
        self.text7.setObjectName("Text7")
        self.text7.setText("Songs of Style")
        self.text7.setGeometry(98, 3, 140, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)


        self.text8 = QLabel(self.central_widget)
        self.text8.setObjectName("Text8")
        self.text8.setText("Songs of Style")
        self.text8.setGeometry(96, 1, 140, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)


        self.text10 = QLabel(self.central_widget)
        self.text10.setObjectName("Text10")
        self.text10.setText("SongID")
        self.text10.setGeometry(1, 16, 52, 16)


        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Title")
        self.text12.setGeometry(58, 16, 37, 16)


        self.text18 = QLabel(self.central_widget)
        self.text18.setObjectName("Text18")
        self.text18.setText("BPM")
        self.text18.setGeometry(307, 16, 36, 16)


        self.text20 = QLabel(self.central_widget)
        self.text20.setObjectName("Text20")
        self.text20.setText("year")
        self.text20.setGeometry(345, 16, 30, 16)


        self.text24 = QLabel(self.central_widget)
        self.text24.setObjectName("Text24")
        self.text24.setText("time")
        self.text24.setGeometry(374, 16, 29, 16)


        self.label26 = QLabel(self.central_widget)
        self.label26.setObjectName("Label26")
        self.label26.setText("Add:")
        self.label26.setGeometry(250, 1, 38, 16)


        self.label27 = QLabel(self.central_widget)
        self.label27.setObjectName("Label27")
        self.label27.setText("remove")
        self.label27.setGeometry(413, 16, 48, 16)


        self.song_combo = QComboBox(self.central_widget)
        self.song_combo.setObjectName("SongCombo")
        self.song_combo.addItems(["SongOfStyleCombo_Query"])
        self.song_combo.setGeometry(288, 1, 173, 16)
        self.song_combo.setEditable(True)


        self.song_i_d = QLineEdit(self.central_widget)
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(1, 1, 48, 2)

        self.song_i_d.installEventFilter(self)
        self._dbl_click_widgets.add(self.song_i_d)
        # DblClick -> self.SongID_DblClick (via eventFilter)

        self.songs__title = QLineEdit(self.central_widget)
        self.songs__title.setObjectName("Songs.Title")
        self.songs__title.setText("Songs.Title")
        self.songs__title.setGeometry(58, 1, 249, 2)


        self.b_p_m = QLineEdit(self.central_widget)
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setGeometry(307, 1, 39, 2)


        self.year = QLineEdit(self.central_widget)
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(346, 1, 29, 2)


        self.time = QLineEdit(self.central_widget)
        self.time.setObjectName("Time")
        self.time.setText("Time")
        self.time.setGeometry(374, 1, 39, 16)


        self.button_remove_song = QPushButton(self.central_widget)
        self.button_remove_song.setObjectName("ButtonRemoveSong")
        self.button_remove_song.setText("del")
        self.button_remove_song.setGeometry(413, 1, 48, 16)
        _fnt = QFont("Terminal", 9)
        self.button_remove_song.setFont(_fnt)

        self.button_remove_song.clicked.connect(self.ButtonRemoveSong_Click)


    # --- VBA Event Handlers ---


    def Button23_Click(self) -> None:

        MyDb: Any = None
        MyTable: Any = None
        MyQuery: Any = None
        # TODO: Set MyDb = DBEngine.Workspaces(0).Databases(0)
        MyTable = MyDb.OpenRecordset("Sing", 1)

        MyTable.Index = "PrimaryKey"
        # Forms! reference: MyTable.Seek "=", Forms!Employees![EmployeeID], self.company_i_d

        if not MyTable.NoMatch:
            MyTable.Delete()
        MyTable.Close()
        # TODO: Forms.Artistss.Refresh()

    def ButtonRemoveSong_Click(self) -> None:

        # Forms! reference: RelationsMgt.RemoveFromButton "Belong", self.song_i_d, Forms!Styles![StyleID], "Label"

          # Dim MyDB As DATABASE, MyTable As Recordset, MyQuery As QueryDef
          # Set MyDB = DBEngine.Workspaces(0).Databases(0)
          # Set MyTable = MyDB.OpenRecordset("Sing", DB_OPEN_TABLE)

          # MyTable.Index = "PrimaryKey"
          # MyTable.Seek "=", Forms!Artists![ArtistID], Me![SongID]

          # If Not MyTable.NoMatch Then
          # MyTable.Delete
          # End If
          # MyTable.Close
          # Forms.Artists.Refresh
        pass

    def RecordID_DblClick(self, Cancel: int) -> None:

        FormName: str = ""
        LinkCriteria: str = ""

        FormName = "Records"
        if self.record_i_d != "":
            LinkCriteria = "[RecordID]=" + str(self.focusWidget()) if self.focusWidget() else ""
            # TODO: DoCmd.OpenForm FormName, , , LinkCriteria

    def SongCombo_AfterUpdate(self) -> None:

        # Forms! reference: RelationsMgt.AddFromCombo Forms!Styles![StyleID], "Label", self.song_combo, "StyleID", "SongID", "Styles", "Belong"
        pass

    def SongID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = ""
        MyForm: str = ""
        MyKey: str = ""
        MyFirstControl: str = ""

        if str(self.focusWidget()) if self.focusWidget() else "" != "":
            MyForm = "Songs"
            MyKey = "SongID"
            MyFirstControl = "Title"

            GotoCriteria = str(self.focusWidget()) if self.focusWidget() else ""
            # TODO: DoCmd.OpenForm MyForm
            # TODO: DoCmd.GoToControl MyKey
            # TODO: DoCmd.FindRecord GotoCriteria
            # TODO: DoCmd.GoToControl MyFirstControl

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SongsOfStyle()
    window.show()
    sys.exit(app.exec())
