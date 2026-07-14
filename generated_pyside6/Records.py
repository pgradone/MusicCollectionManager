"""
Auto-generated PySide6 form: Records
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


class Records(QMainWindow):
    """Migrated from Access form: Records.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self._dbl_click_widgets: set[QObject] = set()
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

        self.artist_i_d.installEventFilter(self)
        self._dbl_click_widgets.add(self.artist_i_d)
        # DblClick -> self.ArtistID_DblClick (via eventFilter)

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

        self.title.installEventFilter(self)
        self._dbl_click_widgets.add(self.title)
        # DblClick -> self.Title_DblClick (via eventFilter)

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

    def ButtonAddRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonAddRecord_Click

        # TODO: NewIDMgt.AddNewID "RecordID", "FreeRecordIDs"

        MyFirstControl: str = ""
        MyFirstControl = "Title"

        # TODO: DoCmd.GoToControl MyFirstControl

        # label: Exit_ButtonAddRecord_Click
        return

        # label: Err_ButtonAddRecord_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonAddRecord_Click

    def ButtonDelRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDelRecord_Click


        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

        # label: Exit_ButtonDelRecord_Click
        return

        # label: Err_ButtonDelRecord_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonDelRecord_Click

    def ButtonFindRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonFindRecord_Click

        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

        # label: Exit_ButtonFindRecord_Click
        return

        # label: Err_ButtonFindRecord_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonFindRecord_Click

    def ButtonPrintRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonPrintRecord_Click


        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # TODO: DoCmd.PrintOut A_SELECTION

        # label: Exit_ButtonPrintRecord_Click
        return

        # label: Err_ButtonPrintRecord_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonPrintRecord_Click

    def Form_BeforeInsert(self, Cancel: int) -> None:
        # TODO: BuildNewID Me.Name, "RecordID"
        pass

    def Form_Current(self) -> None:
        self.Refresh()

    def List51_DblClick(self, Cancel: int) -> None:

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

    def RecordCombo_AfterUpdate(self) -> None:

        Criteria: str = ""
        MyRS: Any = None
        ActiveName: int = 0

        MyRS = self.RecordsetClone

          # Build the criteria.
        ActiveName = str(self.focusWidget()) if self.focusWidget() else ""
        Criteria = "[RecordID]=" + ActiveName

          # Perform the search.
        MyRS.FindFirst(Criteria)

        if MyRS.NoMatch:
            QMessageBox.information(self, '', str("Not Found, Creating new record: " + ActiveName))
            # TODO: DoCmd.GoToRecord , , A_NEWREC
            self.record_i_d = self.record_combo
            self.Refresh()
        else:
              # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark

        self.record_combo = ""

    def RecordID_AfterUpdate(self) -> None:
        self.Refresh()

    def SongView_AfterUpdate(self) -> None:

        ActiveValue: str = ""

        ActiveValue = str(self.focusWidget()) if self.focusWidget() else ""
        if ActiveValue  ==  "Form":
            pass
            # TODO: Me![SongsInRecord].SourceObject = "Songs"
        if ActiveValue  ==  "Tabular":
            pass
            # TODO: Me![SongsInRecord].SourceObject = "SongsOfRecord"

    def Title_DblClick(self, Cancel: int) -> None:

        # VBA: On Error GoTo Err_title_dblClick

        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

        # label: Exit_Button48_Click
        return

        # label: Err_title_dblClick
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_Button48_Click

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
    window = Records()
    window.show()
    sys.exit(app.exec())
