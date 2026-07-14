"""
Auto-generated PySide6 form: Records of Song
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


class Records_of_Song(QMainWindow):
    """Migrated from Access form: Records of Song.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
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

        self.record_i_d.doubleClicked.connect(self.RecordID_DblClick)

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

        # Forms! reference: RelationsMgt.RemoveFromButton "Contain", self.RecordID, Forms!Songs![SongID], "BPM"
        pass

    def RecordCombo_AfterUpdate(self) -> None:

        # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "BPM", self.RecordCombo, "SongID", "RecordID", "Songs", "Contain"
        pass

    def RecordCombo_NotInList(self, NewData: str, Response: int) -> None:

        ActiveID: int = None
        NewID: int = None
        GetText: Any = None
        Prompt: str = None
        Message: str = None
        CRLF: str = None
        ActiveName: str = None
        MyQuery: str = None
        MyForm: str = None
        MyID: str = None
        MyFirstControl: str = None
        # VBA Const: MB_ICONQUESTION = 32
        # VBA Const: YES = 6
        # VBA Const: YES_NO = 4
        CRLF = chr(13)
        Prompt = "Create Record?"
        GetText = RecordCombo.text()
          # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  ==  YES:

              # like ButtonAddRecord_Click

            MyQuery = "FreeRecordIDs"
            MyForm = "Records"
            MyID = "RecordID"
            MyFirstControl = "Title"

            # DoCmd.OpenQuery MyQuery
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            self.close()
            # TODO: DoCmd.OpenForm MyForm
            # DoCmd.GoToRecord A_FORM, MyForm, A_NEWREC
            # DoCmd.GoToControl MyID
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            # Forms! reference: Forms!Artists!Name = GetText
            # DoCmd.GoToControl MyFirstControl
        # Forms! reference: Forms!Songs!ArtistCombo = ""
        # Forms! reference: Forms!Songs.Refresh

    def RecordID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyForm: str = None
        MyKey: str = None
        MyFirstControl: str = None

        if self.focusWidget() if self.focusWidget() else "" != "":
            MyForm = "Records"
            MyKey = "RecordID"
            MyFirstControl = "Title"

            GotoCriteria = self.focusWidget() if self.focusWidget() else ""
            # TODO: DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Records_of_Song()
    window.show()
    sys.exit(app.exec())
