"""
Auto-generated PySide6 form: Artists of Song
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


class Artists_of_Song(QMainWindow):
    """Migrated from Access form: Artists of Song.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self._dbl_click_widgets: set[QObject] = set()
        self.setWindowTitle("Artists of Song")
        self.setObjectName("Artists of Song")
        self.resize(413, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text7 = QLabel(self.central_widget)
        self.text7.setObjectName("Text7")
        self.text7.setText("Artists of Song")
        self.text7.setGeometry(12, 3, 140, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)


        self.text8 = QLabel(self.central_widget)
        self.text8.setObjectName("Text8")
        self.text8.setText("Artists of Song")
        self.text8.setGeometry(10, 1, 140, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)


        self.text10 = QLabel(self.central_widget)
        self.text10.setObjectName("Text10")
        self.text10.setText("ArtistID")
        self.text10.setGeometry(1, 32, 52, 16)


        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Name")
        self.text12.setGeometry(58, 32, 39, 16)


        self.text15 = QLabel(self.central_widget)
        self.text15.setObjectName("Text15")
        self.text15.setText("Surname")
        self.text15.setGeometry(163, 32, 55, 16)


        self.text16 = QLabel(self.central_widget)
        self.text16.setObjectName("Text16")
        self.text16.setText("remove")
        self.text16.setGeometry(365, 32, 48, 16)


        self.artist_combo = QComboBox(self.central_widget)
        self.artist_combo.setObjectName("ArtistCombo")
        self.artist_combo.addItems(["ArtistsQuery"])
        self.artist_combo.setGeometry(200, 6, 191, 16)
        self.artist_combo.setEditable(True)


        self.text17 = QLabel(self.central_widget)
        self.text17.setObjectName("Text17")
        self.text17.setText("add:")
        self.text17.setGeometry(166, 6, 32, 16)


        self.artist_i_d = QLineEdit(self.central_widget)
        self.artist_i_d.setObjectName("ArtistID")
        self.artist_i_d.setText("ArtistID")
        self.artist_i_d.setToolTip("ID of artist")
        self.artist_i_d.setGeometry(1, 1, 48, 2)

        self.artist_i_d.installEventFilter(self)
        self._dbl_click_widgets.add(self.artist_i_d)
        # DblClick -> self.ArtistID_DblClick (via eventFilter)

        self.artist_name = QLineEdit(self.central_widget)
        self.artist_name.setObjectName("ArtistName")
        self.artist_name.setText("Name")
        self.artist_name.setGeometry(48, 1, 115, 2)


        self.artist_surname = QLineEdit(self.central_widget)
        self.artist_surname.setObjectName("ArtistSurname")
        self.artist_surname.setText("Surname")
        self.artist_surname.setGeometry(163, 1, 202, 16)


        self.button_remove_singer = QPushButton(self.central_widget)
        self.button_remove_singer.setObjectName("ButtonRemoveSinger")
        self.button_remove_singer.setText("del")
        self.button_remove_singer.setToolTip("dissociate")
        self.button_remove_singer.setGeometry(365, 1, 48, 16)
        _fnt = QFont("Terminal", 6)
        self.button_remove_singer.setFont(_fnt)

        self.button_remove_singer.clicked.connect(self.ButtonRemoveSinger_Click)


    # --- VBA Event Handlers ---


    def ArtistCombo_AfterUpdate(self) -> None:

        # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.artist_combo, "SongID", "ArtistID", "Songs", "Sing"
        pass

    def ArtistCombo_NotInList(self, NewData: str, Response: int) -> None:

        ActiveID: int = 0
        NewID: int = 0
        GetText: Any = None
        Prompt: str = ""
        Message: str = ""
        CRLF: str = ""
        ActiveName: str = ""
        MyQuery: str = ""
        MyID: str = ""
        MyFirstControl: str = ""
        # VBA Const: MB_ICONQUESTION = 32
        # VBA Const: YES = 6
        # VBA Const: YES_NO = 4
        CRLF = chr(13)
        Prompt = "Create Artist?"
        GetText = self.artist_combo.currentText()
          # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if QMessageBox.question(self, "", str(Message + Prompt), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)  ==  QMessageBox.StandardButton.Yes:

              # like ButtonAddArtist_Click

            MyQuery = "FreeArtistsID"
            MyID = "ArtistID"
            MyFirstControl = "Name"

            # TODO: DoCmd.OpenQuery MyQuery
            # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            # TODO: DoCmd.Close A_QUERY, MyQuery
            # TODO: DoCmd.OpenForm "Artists"
            # TODO: DoCmd.GoToRecord A_FORM, "Artists", A_NEWREC
            # TODO: DoCmd.GoToControl MyID
            # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            # Forms! reference: Forms!Artists!Name = GetText
            # TODO: DoCmd.GoToControl MyFirstControl
        # Forms! reference: Forms!Songs!ArtistCombo = ""
        # Forms! reference: Forms!Songs.Refresh

    def ArtistID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = ""
        MyForm: str = ""
        MyKey: str = ""
        MyFirstControl: str = ""

        if str(self.focusWidget()) if self.focusWidget() else "" != "":
            MyForm = "Artists"
            MyKey = "ArtistID"
            MyFirstControl = "Name"

            GotoCriteria = str(self.focusWidget()) if self.focusWidget() else ""
            # TODO: DoCmd.OpenForm MyForm
            # TODO: DoCmd.GoToControl MyKey
            # TODO: DoCmd.FindRecord GotoCriteria
            # TODO: DoCmd.GoToControl MyFirstControl

    def Button13_Click(self) -> None:
        pass

    def ButtonRemoveSinger_Click(self) -> None:

        # Forms! reference: RelationsMgt.RemoveFromButton "Sing", self.artist_i_d, Forms!Songs![SongID], "Title"
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
    window = Artists_of_Song()
    window.show()
    sys.exit(app.exec())
