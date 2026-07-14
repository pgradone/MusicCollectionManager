"""
Auto-generated PySide6 form: Artists
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


class Artists(QMainWindow):
    """Migrated from Access form: Artists.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Artists")
        self.setObjectName("Artists")
        self.resize(461, 417)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Artists")
        self.text12.setGeometry(12, 3, 62, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text12.setFont(_fnt)


        self.text13 = QLabel(self.central_widget)
        self.text13.setObjectName("Text13")
        self.text13.setText("Artists")
        self.text13.setGeometry(10, 1, 62, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text13.setFont(_fnt)


        self.name = QLineEdit(self.central_widget)
        self.name.setObjectName("Name")
        self.name.setText("Name")
        self.name.setGeometry(67, 32, 106, 2)

        self.name.doubleClicked.connect(self.Name_DblClick)

        self.surname = QLineEdit(self.central_widget)
        self.surname.setObjectName("Surname")
        self.surname.setText("Surname")
        self.surname.setGeometry(240, 32, 182, 2)

        self.surname.doubleClicked.connect(self.Surname_DblClick)

        self.artist_combo = QComboBox(self.central_widget)
        self.artist_combo.setObjectName("ArtistCombo")
        self.artist_combo.addItems(["ArtistsQuery"])
        self.artist_combo.setGeometry(242, 8, 128, 16)
        self.artist_combo.setStyleSheet("background-color: #FFFF80")
        self.artist_combo.setEditable(True)


        self.button_delete_artist = QPushButton(self.central_widget)
        self.button_delete_artist.setObjectName("ButtonDeleteArtist")
        self.button_delete_artist.setText("Button25")
        self.button_delete_artist.setGeometry(422, 24, 29, 24)

        self.button_delete_artist.clicked.connect(self.ButtonDeleteArtist_Click)

        self.text26 = QLabel(self.central_widget)
        self.text26.setObjectName("Text26")
        self.text26.setText("ArtistID:")
        self.text26.setGeometry(77, 8, 52, 16)


        self.artist_i_d = QComboBox(self.central_widget)
        self.artist_i_d.setObjectName("ArtistID")
        self.artist_i_d.addItems(["FreeArtistIDs"])
        self.artist_i_d.setCurrentText("ArtistID")
        self.artist_i_d.setGeometry(134, 8, 58, 16)
        self.artist_i_d.setEditable(True)


        self.add_artist_button = QPushButton(self.central_widget)
        self.add_artist_button.setObjectName("AddArtistButton")
        self.add_artist_button.setText("New Artist")
        self.add_artist_button.setGeometry(374, 1, 87, 2)
        _fnt = QFont("Arial", 8)
        self.add_artist_button.setFont(_fnt)

        self.add_artist_button.clicked.connect(self.AddArtistButton_Click)

        # SubForm: SongsOfArtist
        self.songs_of_artist = QWidget(self.central_widget)
        self.songs_of_artist.setObjectName("SongsOfArtist")
        self.songs_of_artist.setProperty("sourceObject", "Form.Songs of Artist")
        self.songs_of_artist.setGeometry(0, 1, 458, 387)



    # --- VBA Event Handlers ---


    def AddArtistButton_Click(self) -> None:
        # VBA: On Error GoTo Err_AddArtistButton_Click

          # NewIDMgt.AddNewID "ArtistID", "FreeArtistIDs"

        MyFirstControl: str = None

        # DoCmd.GoToRecord , , acNewRec

        MyFirstControl = "Name"

        # DoCmd.GoToControl MyFirstControl

        # label: Exit_AddArtistButton_Click
        return

        # label: Err_AddArtistButton_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_AddArtistButton_Click

    def ArtistCombo_AfterUpdate(self) -> None:

        Criteria: str = None
        MyRS: Any = None
        ActiveName: int = None

        MyRS = self.RecordsetClone

          # Build the criteria.
        ActiveName = self.focusWidget() if self.focusWidget() else ""
        Criteria = "[ArtistID]=" + ActiveName

          # Perform the search.
        MyRS.FindFirst(Criteria)

        if MyRS.NoMatch:
            QMessageBox.information(self, '', str("Not Found, Creating new record: " + ActiveName))
            # DoCmd.GoToRecord , , A_NEWREC
            self.ArtistID = self.ArtistCombo
            self.Refresh()
        else:
              # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark

        self.ArtistCombo = ""

    def ArtistID_AfterUpdate(self) -> None:
        self.Refresh()

    def ButtonDeleteArtist_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDeleteArtist_Click


        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

        # label: Exit_ButtonDeleteArtist_Click
        return

        # label: Err_ButtonDeleteArtist_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonDeleteArtist_Click

    def ButtonPreviousArtist_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonPreviousArtist_Click

        # DoCmd.GoToRecord , , A_PREVIOUS

        # label: Exit_ButtonPreviousArtist_Click
        return

        # label: Err_ButtonPreviousArtist_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonPreviousArtist_Click

    def Form_AfterUpdate(self) -> None:
        self.ArtistCombo.Requery()
        ArtistDuplicates()

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID(self.Name, "ArtistID")

    def Name_DblClick(self, Cancel: int) -> None:
        # VBA: On Error GoTo Err_Name_DblClick

        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

        # label: Exit_Name_DblClick
        return

        # label: Err_Name_DblClick
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_Name_DblClick

    def Surname_DblClick(self, Cancel: int) -> None:
        # VBA: On Error GoTo Err_title_dblClick

        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

        # label: Exit_Button48_Click
        return

        # label: Err_title_dblClick
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_Button48_Click

    def ArtistDuplicates(self) -> bool:
        qdf: Any = None
        rst: Any = None
        sqlTxT: str = None
        # VBA: On Error Resume Next
        sqlTxT = "SELECT Count([Artists].[Name] + [Artists].[Surname]) AS Duplications, " + "[Artists].[Name] + ' ' + [Artists].[Surname] AS DuplicatedArtist " + "FROM Artists WHERE ([Artists].[Name] + [Artists].[Surname])= '" + self.Name.strip() + self.Surname.strip() + "' " + "GROUP BY Artists.Name + ' ' + Artists.Surname " + "HAVING (((Count([Artists].[Name] + [Artists].[Surname]))>1)) "
        rst = CurrentDb.OpenRecordset(sqlTxT)
        # With rst:
        if rst.RecordCount >=  1:
            QMessageBox.information(self, '', str("the artist " + "" + "already exists"))
            ArtistDuplicates = True
        rst.Close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Artists()
    window.show()
    sys.exit(app.exec())
