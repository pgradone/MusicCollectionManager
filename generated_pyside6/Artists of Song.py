"""
Auto-generated PySide6 form: Artists of Song
Generated: 2026-07-14 15:57:48
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


class Artists_of_Song(QMainWindow):
    """Migrated from Access form: Artists of Song.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
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

        self.artist_i_d.doubleClicked.connect(self.ArtistID_DblClick)

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

        # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.ArtistCombo, "SongID", "ArtistID", "Songs", "Sing"
        pass

    def ArtistCombo_NotInList(self, NewData: str, Response: int) -> None:

        ActiveID: int = None
        NewID: int = None
        GetText: Any = None
        Prompt: str = None
        Message: str = None
        CRLF: str = None
        ActiveName: str = None
        MyQuery: str = None
        MyID: str = None
        MyFirstControl: str = None
        # VBA Const: MB_ICONQUESTION = 32
        # VBA Const: YES = 6
        # VBA Const: YES_NO = 4
        CRLF = chr(13)
        Prompt = "Create Artist?"
        GetText = ArtistCombo.text()
          # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  ==  YES:

              # like ButtonAddArtist_Click

            MyQuery = "FreeArtistsID"
            MyID = "ArtistID"
            MyFirstControl = "Name"

            # DoCmd.OpenQuery MyQuery
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            self.close()
            import Artists
            self.sub_form = Artists.Artists()
            self.sub_form.show()
            # DoCmd.GoToRecord A_FORM, "Artists", A_NEWREC
            # DoCmd.GoToControl MyID
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            # Forms! reference: Forms!Artists!Name = GetText
            # DoCmd.GoToControl MyFirstControl
        # Forms! reference: Forms!Songs!ArtistCombo = ""
        # Forms! reference: Forms!Songs.Refresh

    def ArtistID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyForm: str = None
        MyKey: str = None
        MyFirstControl: str = None

        if self.focusWidget() if self.focusWidget() else "" != "":
            MyForm = "Artists"
            MyKey = "ArtistID"
            MyFirstControl = "Name"

            GotoCriteria = self.focusWidget() if self.focusWidget() else ""
            # TODO: DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl

    def Button13_Click(self) -> None:
        pass

    def ButtonRemoveSinger_Click(self) -> None:

        # Forms! reference: RelationsMgt.RemoveFromButton "Sing", self.ArtistID, Forms!Songs![SongID], "Title"
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Artists_of_Song()
    window.show()
    sys.exit(app.exec())
