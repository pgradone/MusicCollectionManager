"""
Auto-generated PySide6 form: Records of Song
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


class Records_of_Song(QMainWindow):
    """Migrated from Access form: Records of Song.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self._dbl_click_widgets: set[QObject] = set()
        self.setWindowTitle("Records of Song")
        self.setObjectName("Records of Song")
        self.resize(566, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text7 = QLabel(self.central_widget)
        self.text7.setObjectName("Text7")
        self.text7.setText("Records of Song")
        self.text7.setGeometry(2, 3, 162, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)


        self.text8 = QLabel(self.central_widget)
        self.text8.setObjectName("Text8")
        self.text8.setText("Records of Song")
        self.text8.setGeometry(1, 1, 162, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)


        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("recID")
        self.text12.setGeometry(1, 32, 38, 16)


        self.text14 = QLabel(self.central_widget)
        self.text14.setObjectName("Text14")
        self.text14.setText("Title")
        self.text14.setGeometry(86, 32, 35, 16)


        self.text16 = QLabel(self.central_widget)
        self.text16.setObjectName("Text16")
        self.text16.setText("House")
        self.text16.setGeometry(394, 32, 43, 16)


        self.text18 = QLabel(self.central_widget)
        self.text18.setObjectName("Text18")
        self.text18.setText("Mike")
        self.text18.setGeometry(451, 32, 27, 16)


        self.text20 = QLabel(self.central_widget)
        self.text20.setObjectName("Text20")
        self.text20.setText("Tito")
        self.text20.setGeometry(480, 32, 32, 16)


        self.text21 = QLabel(self.central_widget)
        self.text21.setObjectName("Text21")
        self.text21.setText("pos")
        self.text21.setGeometry(38, 32, 39, 14)


        self.text25 = QLabel(self.central_widget)
        self.text25.setObjectName("Text25")
        self.text25.setText("support")
        self.text25.setGeometry(298, 32, 48, 14)


        self.text29 = QLabel(self.central_widget)
        self.text29.setObjectName("Text29")
        self.text29.setText("remove")
        self.text29.setGeometry(518, 32, 48, 16)


        self.record_combo = QComboBox(self.central_widget)
        self.record_combo.setObjectName("RecordCombo")
        self.record_combo.addItems(["RecordComboInSongs"])
        self.record_combo.setToolTip("enter record containing song")
        self.record_combo.setGeometry(278, 8, 239, 16)
        self.record_combo.setEditable(True)


        self.text30 = QLabel(self.central_widget)
        self.text30.setObjectName("Text30")
        self.text30.setText("Add to record:")
        self.text30.setGeometry(178, 9, 91, 16)


        self.title = QLineEdit(self.central_widget)
        self.title.setObjectName("Title")
        self.title.setText("Records.Title")
        self.title.setGeometry(87, 1, 211, 2)


        self.mike = QCheckBox(self.central_widget)
        self.mike.setObjectName("Mike")
        self.mike.setText("Mike")
        self.mike.setGeometry(470, 1, 7, 2)


        self.tito = QCheckBox(self.central_widget)
        self.tito.setObjectName("Tito")
        self.tito.setText("Tito")
        self.tito.setGeometry(490, 1, 7, 2)


        self.record_i_d = QLineEdit(self.central_widget)
        self.record_i_d.setObjectName("RecordID")
        self.record_i_d.setText("RecordID")
        self.record_i_d.setGeometry(1, 1, 38, 2)

        self.record_i_d.installEventFilter(self)
        self._dbl_click_widgets.add(self.record_i_d)
        # DblClick -> self.RecordID_DblClick (via eventFilter)

        self.support = QComboBox(self.central_widget)
        self.support.setObjectName("Support")
        self.support.addItems(["SupportsOfRecord"])
        self.support.setCurrentText("Records.Support")
        self.support.setGeometry(298, 1, 7, 16)
        self.support.setEditable(True)


        self.field27 = QComboBox(self.central_widget)
        self.field27.setObjectName("Field27")
        self.field27.addItems(["HousesOfRecords"])
        self.field27.setCurrentText("Record House")
        self.field27.setGeometry(394, 1, 77, 16)
        self.field27.setEditable(True)


        self.position = QComboBox(self.central_widget)
        self.position.setObjectName("Position")
        self.position.addItems(["PositionsOfContain"])
        self.position.setCurrentText("Position")
        self.position.setGeometry(38, 1, 48, 16)
        self.position.setEditable(True)


        self.button_remove_record = QPushButton(self.central_widget)
        self.button_remove_record.setObjectName("ButtonRemoveRecord")
        self.button_remove_record.setText("del")
        self.button_remove_record.setToolTip("dissociate")
        self.button_remove_record.setGeometry(509, 1, 57, 16)
        _fnt = QFont("Terminal", 6)
        self.button_remove_record.setFont(_fnt)

        self.button_remove_record.clicked.connect(self.ButtonRemoveRecord_Click)


    # --- VBA Event Handlers ---


    def ButtonRemoveRecord_Click(self) -> None:

        # Forms! reference: RelationsMgt.RemoveFromButton "Contain", self.record_i_d.currentText(), Forms!Songs![SongID], "BPM"
        pass

    def RecordCombo_AfterUpdate(self) -> None:

        # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "BPM", self.record_combo, "SongID", "RecordID", "Songs", "Contain"
        pass

    def RecordCombo_NotInList(self, NewData: str, Response: int) -> None:

        ActiveID: int = 0
        NewID: int = 0
        GetText: Any = None
        Prompt: str = ""
        Message: str = ""
        CRLF: str = ""
        ActiveName: str = ""
        MyQuery: str = ""
        MyForm: str = ""
        MyID: str = ""
        MyFirstControl: str = ""
        # VBA Const: MB_ICONQUESTION = 32
        # VBA Const: YES = 6
        # VBA Const: YES_NO = 4
        CRLF = chr(13)
        Prompt = "Create Record?"
        GetText = self.record_combo.currentText()
          # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if QMessageBox.question(self, "", str(Message + Prompt), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)  ==  QMessageBox.StandardButton.Yes:

              # like ButtonAddRecord_Click

            MyQuery = "FreeRecordIDs"
            MyForm = "Records"
            MyID = "RecordID"
            MyFirstControl = "Title"

            # TODO: DoCmd.OpenQuery MyQuery
            # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            # TODO: DoCmd.Close A_QUERY, MyQuery
            # TODO: DoCmd.OpenForm MyForm
            # TODO: DoCmd.GoToRecord A_FORM, MyForm, A_NEWREC
            # TODO: DoCmd.GoToControl MyID
            # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            # Forms! reference: Forms!Artists!Name = GetText
            # TODO: DoCmd.GoToControl MyFirstControl
        # Forms! reference: Forms!Songs!ArtistCombo = ""
        # Forms! reference: Forms!Songs.Refresh

    def RecordID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = ""
        MyForm: str = ""
        MyKey: str = ""
        MyFirstControl: str = ""

        if str(self.focusWidget()) if self.focusWidget() else "" != "":
            MyForm = "Records"
            MyKey = "RecordID"
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


        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Records_of_Song()
    window.show()
    sys.exit(app.exec())
