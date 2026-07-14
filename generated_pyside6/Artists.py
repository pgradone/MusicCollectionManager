"""
Auto-generated PySide6 form: Artists
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


class Artists(QMainWindow):
    """Migrated from Access form: Artists"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Artists")
        self.setObjectName("Artists")
        self.resize(6921, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("Artists")
        self.text12.setGeometry(180, 40, 930, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text12.setFont(_fnt)

        self.text13 = QLabel()
        self.text13.setObjectName("Text13")
        self.text13.setText("Artists")
        self.text13.setGeometry(144, 10, 930, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text13.setFont(_fnt)

        self.name = QLineEdit()
        self.name.setObjectName("Name")
        self.name.setText("Name")
        self.name.setGeometry(1008, 480, 1590, 25)
        self.name.doubleClicked.connect(self.Name_DblClick)

        self.surname = QLineEdit()
        self.surname.setObjectName("Surname")
        self.surname.setText("Surname")
        self.surname.setGeometry(3603, 480, 2730, 25)
        self.surname.doubleClicked.connect(self.Surname_DblClick)

        self.artist_combo = QComboBox()
        self.artist_combo.setObjectName("ArtistCombo")
        self.artist_combo.addItems(["ArtistsQuery"])
        self.artist_combo.setGeometry(3628, 120, 1915, 240)
        self.artist_combo.setStyleSheet("background-color: #FFFF80")
        self.artist_combo.setEditable(True)

        self.button_delete_artist = QPushButton()
        self.button_delete_artist.setObjectName("ButtonDeleteArtist")
        self.button_delete_artist.setText("Button25")
        self.button_delete_artist.setGeometry(6336, 360, 441, 366)
        self.button_delete_artist.clicked.connect(self.ButtonDeleteArtist_Click)

        self.text26 = QLabel()
        self.text26.setObjectName("Text26")
        self.text26.setText("ArtistID:")
        self.text26.setGeometry(1152, 120, 780, 240)

        self.artist_i_d = QComboBox()
        self.artist_i_d.setObjectName("ArtistID")
        self.artist_i_d.addItems(["FreeArtistIDs"])
        self.artist_i_d.setCurrentText("ArtistID")
        self.artist_i_d.setGeometry(2016, 120, 865, 240)
        self.artist_i_d.setEditable(True)

        self.add_artist_button = QPushButton()
        self.add_artist_button.setObjectName("AddArtistButton")
        self.add_artist_button.setText("New Artist")
        self.add_artist_button.setGeometry(5616, 10, 1305, 25)
        _fnt = QFont("Arial", 8)
        self.add_artist_button.setFont(_fnt)
        self.add_artist_button.clicked.connect(self.AddArtistButton_Click)

        # SubForm: SongsOfArtist
        self.songs_of_artist = QWidget()
        self.songs_of_artist.setObjectName("SongsOfArtist")
        self.songs_of_artist.setProperty("sourceObject", "Form.Songs of Artist")
        self.songs_of_artist.setGeometry(-6, 10, 6870, 5805)


    # --- VBA Event Handlers ---


    def AddArtistButton_Click(self) -> None:
        # VBA: On Error GoTo Err_AddArtistButton_Click
        # try:

            # NewIDMgt.AddNewID "ArtistID", "FreeArtistIDs"

            MyFirstControl: str = None

            # DoCmd.GoToRecord , , acNewRec

            MyFirstControl = "Name"

            # DoCmd.GoToControl MyFirstControl

            # label: Exit_AddArtistButton_Click

        # label: Err_AddArtistButton_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_AddArtistButton_Click

    def ArtistCombo_AfterUpdate(self) -> None:

        Criteria: str = None
        MyRS: Any = None
        ActiveName: int = None

        MyRS = self.RecordsetClone

        # Build the criteria.
        ActiveName = Screen.ActiveControl
        Criteria = "[ArtistID]=" + ActiveName

        # Perform the search.
        MyRS.FindFirst Criteria

        if MyRS.NoMatch:
            QMessageBox.information(self, '', str("))
            # DoCmd.GoToRecord , , A_NEWREC
            self.ArtistID = self.ArtistCombo
            self.Refresh
        else:
            # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark

        self.ArtistCombo = ""

    def ArtistID_AfterUpdate(self) -> None:
        self.Refresh

    def ButtonDeleteArtist_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDeleteArtist_Click
        # try:


            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

            # label: Exit_ButtonDeleteArtist_Click

        # label: Err_ButtonDeleteArtist_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonDeleteArtist_Click

    def ButtonPreviousArtist_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonPreviousArtist_Click
        # try:

            # DoCmd.GoToRecord , , A_PREVIOUS

            # label: Exit_ButtonPreviousArtist_Click

        # label: Err_ButtonPreviousArtist_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonPreviousArtist_Click

    def Form_AfterUpdate(self) -> None:
        self.ArtistCombo.Requery
        ArtistDuplicates

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID self.Name, "ArtistID"

    def Name_DblClick(self, Cancel: int) -> None:
        # VBA: On Error GoTo Err_Name_DblClick
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

            # label: Exit_Name_DblClick

        # label: Err_Name_DblClick
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_Name_DblClick

    def Surname_DblClick(self, Cancel: int) -> None:
        # VBA: On Error GoTo Err_title_dblClick
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

            # label: Exit_Button48_Click

        # label: Err_title_dblClick
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_Button48_Click

    def ArtistDuplicates(self) -> bool:
        qdf: Any = None
        # VBA: On Error Resume Next
        # try:
            sqlTxT = "SELECT Count([Artists].[Name] + [Artists].[Surname]) AS Duplications, " + "[Artists].[Name] + ' ' + [Artists].[Surname] AS DuplicatedArtist " + "FROM Artists WHERE ([Artists].[Name] + [Artists].[Surname])= '" + self.Name.strip() + self.Surname.strip() + "' " + "GROUP BY Artists.Name + ' ' + Artists.Surname " + "HAVING (((Count([Artists].[Name] + [Artists].[Surname]))>1)) "
            rst = CurrentDb.OpenRecordset(sqlTxT)
            # With rst:
                if .RecordCount > == 1:
                    QMessageBox.information(self, '', str("))
                    ArtistDuplicates = True
                rst.Close


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Artists()
    window.show()
    sys.exit(app.exec())
