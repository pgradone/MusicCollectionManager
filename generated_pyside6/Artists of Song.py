"""
Auto-generated PySide6 form: Artists of Song
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


class Artists_of_Song(QMainWindow):
    """Migrated from Access form: Artists of Song"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Artists of Song")
        self.setObjectName("Artists of Song")
        self.resize(6195, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text7 = QLabel()
        self.text7.setObjectName("Text7")
        self.text7.setText("Artists of Song")
        self.text7.setGeometry(180, 40, 2100, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)

        self.text8 = QLabel()
        self.text8.setObjectName("Text8")
        self.text8.setText("Artists of Song")
        self.text8.setGeometry(144, 10, 2100, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)

        self.text10 = QLabel()
        self.text10.setObjectName("Text10")
        self.text10.setText("ArtistID")
        self.text10.setGeometry(10, 480, 780, 240)

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("Name")
        self.text12.setGeometry(864, 480, 585, 240)

        self.text15 = QLabel()
        self.text15.setObjectName("Text15")
        self.text15.setText("Surname")
        self.text15.setGeometry(2448, 480, 825, 240)

        self.text16 = QLabel()
        self.text16.setObjectName("Text16")
        self.text16.setText("remove")
        self.text16.setGeometry(5472, 480, 714, 240)

        self.artist_combo = QComboBox()
        self.artist_combo.setObjectName("ArtistCombo")
        self.artist_combo.addItems(["ArtistsQuery"])
        self.artist_combo.setGeometry(3004, 94, 2868, 240)
        self.artist_combo.setEditable(True)

        self.text17 = QLabel()
        self.text17.setObjectName("Text17")
        self.text17.setText("add:")
        self.text17.setGeometry(2494, 94, 480, 240)

        self.artist_i_d = QLineEdit()
        self.artist_i_d.setObjectName("ArtistID")
        self.artist_i_d.setText("ArtistID")
        self.artist_i_d.setToolTip("ID of artist")
        self.artist_i_d.setGeometry(10, 10, 720, 25)
        self.artist_i_d.doubleClicked.connect(self.ArtistID_DblClick)

        self.artist_name = QLineEdit()
        self.artist_name.setObjectName("ArtistName")
        self.artist_name.setText("Name")
        self.artist_name.setGeometry(720, 10, 1725, 25)

        self.artist_surname = QLineEdit()
        self.artist_surname.setObjectName("ArtistSurname")
        self.artist_surname.setText("Surname")
        self.artist_surname.setGeometry(2442, 10, 3027, 240)

        self.button_remove_singer = QPushButton()
        self.button_remove_singer.setObjectName("ButtonRemoveSinger")
        self.button_remove_singer.setText("del")
        self.button_remove_singer.setToolTip("dissociate")
        self.button_remove_singer.setGeometry(5472, 10, 723, 240)
        _fnt = QFont("Terminal", 6)
        self.button_remove_singer.setFont(_fnt)
        self.button_remove_singer.clicked.connect(self.ButtonRemoveSinger_Click)


    # --- VBA Event Handlers ---


    def ArtistCombo_AfterUpdate(self) -> None:

        RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.ArtistCombo, "SongID", "ArtistID", "Songs", "Sing"

    def ArtistCombo_NotInList(self, NewData: str, Response: int) -> None:

        ActiveID: int = None
        Prompt: str = None
        MyQuery: str = None
        Const MB_ICONQUESTION = 32
        Const YES = 6
        Const YES_NO = 4
        CRLF = Chr$(13)
        Prompt = "Create Artist?"
        GetText = ArtistCombo.Text
        # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  == YES:

            # like ButtonAddArtist_Click

            MyQuery = "FreeArtistsID"
            MyID = "ArtistID"
            MyFirstControl = "Name"

            # DoCmd.OpenQuery MyQuery
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            # DoCmd.Close A_QUERY, MyQuery
            # DoCmd.OpenForm "Artists"
            # DoCmd.GoToRecord A_FORM, "Artists", A_NEWREC
            # DoCmd.GoToControl MyID
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            Forms!Artists!Name = GetText
            # DoCmd.GoToControl MyFirstControl
        Forms!Songs!ArtistCombo = ""
        Forms!Songs.Refresh

    def ArtistID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyKey: str = None

        if Screen.ActiveControl != "":
            MyForm = "Artists"
            MyKey = "ArtistID"
            MyFirstControl = "Name"

            GotoCriteria = Screen.ActiveControl
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl

    def Button13_Click(self) -> None:
        pass

    def ButtonRemoveSinger_Click(self) -> None:

        RelationsMgt.RemoveFromButton "Sing", self.ArtistID, Forms!Songs![SongID], "Title"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Artists_of_Song()
    window.show()
    sys.exit(app.exec())
