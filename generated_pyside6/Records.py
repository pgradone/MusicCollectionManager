"""
Auto-generated PySide6 form: Records
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


class Records(QMainWindow):
    """Migrated from Access form: Records.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("RecordsByTitle")
        self.setObjectName("Records")
        self.resize(595, 479)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.button_add_record = QPushButton(self.central_widget)
        self.button_add_record.setObjectName("ButtonAddRecord")
        self.button_add_record.setText("Add Record")
        self.button_add_record.setToolTip("Create new record and its ID")
        self.button_add_record.setGeometry(450, 1, 107, 32)
        _fnt = QFont("Terminal", 6)
        self.button_add_record.setFont(_fnt)

        self.button_add_record.clicked.connect(self.ButtonAddRecord_Click)

        self.button_del_record = QPushButton(self.central_widget)
        self.button_del_record.setObjectName("ButtonDelRecord")
        self.button_del_record.setText("Button36")
        self.button_del_record.setGeometry(556, 1, 39, 32)

        self.button_del_record.clicked.connect(self.ButtonDelRecord_Click)

        self.record_i_d = QComboBox(self.central_widget)
        self.record_i_d.setObjectName("RecordID")
        self.record_i_d.addItems(["FreeRecordIDs"])
        self.record_i_d.setCurrentText("RecordID")
        self.record_i_d.setGeometry(58, 6, 67, 16)
        self.record_i_d.setEditable(True)


        self.text39 = QLabel(self.central_widget)
        self.text39.setObjectName("Text39")
        self.text39.setText("RecordID:")
        self.text39.setGeometry(1, 6, 57, 16)


        self.record_combo = QComboBox(self.central_widget)
        self.record_combo.setObjectName("RecordCombo")
        self.record_combo.addItems(["RecordCombo_Query"])
        self.record_combo.setToolTip("enter record to go to")
        self.record_combo.setGeometry(363, 6, 79, 16)
        self.record_combo.setStyleSheet("background-color: #FFFF80")
        self.record_combo.setEditable(True)


        self.list51 = QListWidget(self.central_widget)
        self.list51.setObjectName("List51")
        self.list51.addItems(["Main_Artist_of Record"])
        self.list51.setToolTip("Main Artist of this record")
        self.list51.setGeometry(205, 6, 113, 16)
        self.list51.setStyleSheet("background-color: #C0C0C0")

        self.list51.doubleClicked.connect(self.List51_DblClick)

        self.artist_i_d = QComboBox(self.central_widget)
        self.artist_i_d.setObjectName("ArtistID")
        self.artist_i_d.addItems(["ArtistsQuery"])
        self.artist_i_d.setCurrentText("ArtistID")
        self.artist_i_d.setToolTip("Artist of this record. Double Click to go to Artist")
        self.artist_i_d.setGeometry(61, 31, 127, 2)
        self.artist_i_d.setEditable(True)

        self.artist_i_d.doubleClicked.connect(self.ArtistID_DblClick)

        self.text59 = QLineEdit(self.central_widget)
        self.text59.setObjectName("Text59")
        self.text59.setText("Anno")
        self.text59.setGeometry(251, 31, 40, 2)


        self.text61 = QLineEdit(self.central_widget)
        self.text61.setObjectName("Text61")
        self.text61.setText("Val2026")
        self.text61.setGeometry(348, 31, 49, 2)


        self.discogs_release = QComboBox(self.central_widget)
        self.discogs_release.setObjectName("Discogs_release")
        self.discogs_release.addItems(["SELECT Title, release_ID from Discogs order by Title",""])
        self.discogs_release.setCurrentText("Discogs_release")
        self.discogs_release.setGeometry(60, 54, 167, 2)
        self.discogs_release.setEditable(True)


        self.title = QLineEdit(self.central_widget)
        self.title.setObjectName("Title")
        self.title.setText("Title")
        self.title.setGeometry(38, 1, 482, 2)
        _fnt = QFont()
        _fnt.setPointSize(10)
        self.title.setFont(_fnt)

        self.title.doubleClicked.connect(self.Title_DblClick)

        self.mike = QCheckBox(self.central_widget)
        self.mike.setObjectName("Mike")
        self.mike.setText("Mike")
        self.mike.setGeometry(48, 46, 10, 16)


        self.tito = QCheckBox(self.central_widget)
        self.tito.setObjectName("Tito")
        self.tito.setText("Tito")
        self.tito.setGeometry(86, 46, 9, 16)


        # SubForm: SongsInRecord
        self.songs_in_record = QWidget(self.central_widget)
        self.songs_in_record.setObjectName("SongsInRecord")
        self.songs_in_record.setProperty("sourceObject", "Form.SongsOfRecord")
        self.songs_in_record.setGeometry(1, 70, 540, 379)


        self.support = QComboBox(self.central_widget)
        self.support.setObjectName("Support")
        self.support.addItems(["SupportsOfRecord"])
        self.support.setCurrentText("Support")
        self.support.setGeometry(249, 46, 106, 16)
        self.support.setEditable(True)


        self.record_house = QComboBox(self.central_widget)
        self.record_house.setObjectName("RecordHouse")
        self.record_house.addItems(["HousesOfRecords"])
        self.record_house.setCurrentText("Record House")
        self.record_house.setToolTip("record house")
        self.record_house.setGeometry(48, 22, 179, 16)
        self.record_house.setEditable(True)


        self.button_print_record = QPushButton(self.central_widget)
        self.button_print_record.setObjectName("ButtonPrintRecord")
        self.button_print_record.setText("Button50")
        self.button_print_record.setToolTip("Print this record")
        self.button_print_record.setGeometry(442, 31, 48, 30)

        self.button_print_record.clicked.connect(self.ButtonPrintRecord_Click)


    # --- VBA Event Handlers ---


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

    def ButtonAddRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonAddRecord_Click

        NewIDMgt.AddNewID("RecordID", "FreeRecordIDs")

        MyFirstControl: str = None
        MyFirstControl = "Title"

        # DoCmd.GoToControl MyFirstControl

        # label: Exit_ButtonAddRecord_Click
        return

        # label: Err_ButtonAddRecord_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonAddRecord_Click

    def ButtonDelRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDelRecord_Click


        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

        # label: Exit_ButtonDelRecord_Click
        return

        # label: Err_ButtonDelRecord_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonDelRecord_Click

    def ButtonFindRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonFindRecord_Click

        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

        # label: Exit_ButtonFindRecord_Click
        return

        # label: Err_ButtonFindRecord_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonFindRecord_Click

    def ButtonPrintRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonPrintRecord_Click


        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # DoCmd.PrintOut A_SELECTION

        # label: Exit_ButtonPrintRecord_Click
        return

        # label: Err_ButtonPrintRecord_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonPrintRecord_Click

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID(self.Name, "RecordID")

    def Form_Current(self) -> None:
        self.Refresh()

    def List51_DblClick(self, Cancel: int) -> None:

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

    def RecordCombo_AfterUpdate(self) -> None:

        Criteria: str = None
        MyRS: Any = None
        ActiveName: int = None

        MyRS = self.RecordsetClone

          # Build the criteria.
        ActiveName = self.focusWidget() if self.focusWidget() else ""
        Criteria = "[RecordID]=" + ActiveName

          # Perform the search.
        MyRS.FindFirst(Criteria)

        if MyRS.NoMatch:
            QMessageBox.information(self, '', str("Not Found, Creating new record: " + ActiveName))
            # DoCmd.GoToRecord , , A_NEWREC
            self.RecordID = self.RecordCombo
            self.Refresh()
        else:
              # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark

        self.RecordCombo = ""

    def RecordID_AfterUpdate(self) -> None:
        self.Refresh()

    def SongView_AfterUpdate(self) -> None:

        ActiveValue: str = None

        ActiveValue = self.focusWidget() if self.focusWidget() else ""
        if ActiveValue  ==  "Form":
            self.SongsInRecord.SourceObject = "Songs"
        if ActiveValue  ==  "Tabular":
            self.SongsInRecord.SourceObject = "SongsOfRecord"

    def Title_DblClick(self, Cancel: int) -> None:

        # VBA: On Error GoTo Err_title_dblClick

        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

        # label: Exit_Button48_Click
        return

        # label: Err_title_dblClick
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_Button48_Click


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Records()
    window.show()
    sys.exit(app.exec())
