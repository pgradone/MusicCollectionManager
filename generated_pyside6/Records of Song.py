"""
Auto-generated PySide6 form: Records of Song
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


class Records_of_Song(QMainWindow):
    """Migrated from Access form: Records of Song"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Records of Song")
        self.setObjectName("Records of Song")
        self.resize(8496, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text7 = QLabel()
        self.text7.setObjectName("Text7")
        self.text7.setText("Records of Song")
        self.text7.setGeometry(36, 40, 2430, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)

        self.text8 = QLabel()
        self.text8.setObjectName("Text8")
        self.text8.setText("Records of Song")
        self.text8.setGeometry(10, 10, 2430, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("recID")
        self.text12.setGeometry(10, 480, 570, 240)

        self.text14 = QLabel()
        self.text14.setObjectName("Text14")
        self.text14.setText("Title")
        self.text14.setGeometry(1296, 480, 525, 240)

        self.text16 = QLabel()
        self.text16.setObjectName("Text16")
        self.text16.setText("House")
        self.text16.setGeometry(5904, 480, 645, 240)

        self.text18 = QLabel()
        self.text18.setObjectName("Text18")
        self.text18.setText("Mike")
        self.text18.setGeometry(6768, 480, 405, 240)

        self.text20 = QLabel()
        self.text20.setObjectName("Text20")
        self.text20.setText("Tito")
        self.text20.setGeometry(7200, 480, 480, 240)

        self.text21 = QLabel()
        self.text21.setObjectName("Text21")
        self.text21.setText("pos")
        self.text21.setGeometry(576, 480, 585, 210)

        self.text25 = QLabel()
        self.text25.setObjectName("Text25")
        self.text25.setText("support")
        self.text25.setGeometry(4464, 480, 720, 210)

        self.text29 = QLabel()
        self.text29.setObjectName("Text29")
        self.text29.setText("remove")
        self.text29.setGeometry(7776, 480, 720, 240)

        self.record_combo = QComboBox()
        self.record_combo.setObjectName("RecordCombo")
        self.record_combo.addItems(["RecordComboInSongs"])
        self.record_combo.setToolTip("enter record containing song")
        self.record_combo.setGeometry(4176, 120, 3588, 240)
        self.record_combo.setEditable(True)

        self.text30 = QLabel()
        self.text30.setObjectName("Text30")
        self.text30.setText("Add to record:")
        self.text30.setGeometry(2664, 141, 1365, 240)

        self.title = QLineEdit()
        self.title.setObjectName("Title")
        self.title.setText("Records.Title")
        self.title.setGeometry(1305, 10, 3165, 25)

        self.mike = QCheckBox()
        self.mike.setObjectName("Mike")
        self.mike.setText("Mike")
        self.mike.setGeometry(7056, 10, 100, 25)

        self.tito = QCheckBox()
        self.tito.setObjectName("Tito")
        self.tito.setText("Tito")
        self.tito.setGeometry(7344, 10, 100, 25)

        self.record_i_d = QLineEdit()
        self.record_i_d.setObjectName("RecordID")
        self.record_i_d.setText("RecordID")
        self.record_i_d.setGeometry(10, 10, 570, 25)
        self.record_i_d.doubleClicked.connect(self.RecordID_DblClick)

        self.support = QComboBox()
        self.support.setObjectName("Support")
        self.support.addItems(["SupportsOfRecord"])
        self.support.setCurrentText("Records.Support")
        self.support.setGeometry(4464, 10, 100, 240)
        self.support.setEditable(True)

        self.field27 = QComboBox()
        self.field27.setObjectName("Field27")
        self.field27.addItems(["HousesOfRecords"])
        self.field27.setCurrentText("Record House")
        self.field27.setGeometry(5904, 10, 1152, 240)
        self.field27.setEditable(True)

        self.position = QComboBox()
        self.position.setObjectName("Position")
        self.position.addItems(["PositionsOfContain"])
        self.position.setCurrentText("Position")
        self.position.setGeometry(576, 10, 726, 240)
        self.position.setEditable(True)

        self.button_remove_record = QPushButton()
        self.button_remove_record.setObjectName("ButtonRemoveRecord")
        self.button_remove_record.setText("del")
        self.button_remove_record.setToolTip("dissociate")
        self.button_remove_record.setGeometry(7632, 10, 852, 240)
        _fnt = QFont("Terminal", 6)
        self.button_remove_record.setFont(_fnt)
        self.button_remove_record.clicked.connect(self.ButtonRemoveRecord_Click)


    # --- VBA Event Handlers ---


    def ButtonRemoveRecord_Click(self) -> None:

        RelationsMgt.RemoveFromButton "Contain", self.RecordID, Forms!Songs![SongID], "BPM"

    def RecordCombo_AfterUpdate(self) -> None:

        RelationsMgt.AddFromCombo Forms!Songs![SongID], "BPM", self.RecordCombo, "SongID", "RecordID", "Songs", "Contain"

    def RecordCombo_NotInList(self, NewData: str, Response: int) -> None:

        ActiveID: int = None
        Prompt: str = None
        MyQuery: str = None
        Const MB_ICONQUESTION = 32
        Const YES = 6
        Const YES_NO = 4
        CRLF = Chr$(13)
        Prompt = "Create Record?"
        GetText = RecordCombo.Text
        # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  == YES:

            # like ButtonAddRecord_Click

            MyQuery = "FreeRecordIDs"
            MyForm = "Records"
            MyID = "RecordID"
            MyFirstControl = "Title"

            # DoCmd.OpenQuery MyQuery
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            # DoCmd.Close A_QUERY, MyQuery
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToRecord A_FORM, MyForm, A_NEWREC
            # DoCmd.GoToControl MyID
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            Forms!Artists!Name = GetText
            # DoCmd.GoToControl MyFirstControl
        Forms!Songs!ArtistCombo = ""
        Forms!Songs.Refresh

    def RecordID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyKey: str = None

        if Screen.ActiveControl != "":
            MyForm = "Records"
            MyKey = "RecordID"
            MyFirstControl = "Title"

            GotoCriteria = Screen.ActiveControl
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Records_of_Song()
    window.show()
    sys.exit(app.exec())
