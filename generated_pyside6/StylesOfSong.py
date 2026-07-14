"""
Auto-generated PySide6 form: StylesOfSong
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


class StylesOfSong(QMainWindow):
    """Migrated from Access form: StylesOfSong"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("StylesOfSong")
        self.setObjectName("StylesOfSong")
        self.resize(2980, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text7 = QLabel()
        self.text7.setObjectName("Text7")
        self.text7.setText("StylesOfSong")
        self.text7.setGeometry(36, 40, 1965, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)

        self.text8 = QLabel()
        self.text8.setObjectName("Text8")
        self.text8.setText("StylesOfSong")
        self.text8.setGeometry(10, 10, 1965, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)

        self.text10 = QLabel()
        self.text10.setObjectName("Text10")
        self.text10.setText("ID")
        self.text10.setGeometry(10, 480, 285, 240)

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("Label")
        self.text12.setGeometry(432, 480, 615, 240)

        self.text14 = QLabel()
        self.text14.setObjectName("Text14")
        self.text14.setText("remove")
        self.text14.setGeometry(2160, 480, 714, 240)

        self.style_combo = QComboBox()
        self.style_combo.setObjectName("StyleCombo")
        self.style_combo.addItems(["Styles_of_song"])
        self.style_combo.setToolTip("style to add to song")
        self.style_combo.setGeometry(2010, 240, 970, 240)
        self.style_combo.setEditable(True)

        self.text15 = QLabel()
        self.text15.setObjectName("Text15")
        self.text15.setText("add:")
        self.text15.setGeometry(2016, 10, 465, 210)

        self.style_i_d = QLineEdit()
        self.style_i_d.setObjectName("StyleID")
        self.style_i_d.setText("StyleID")
        self.style_i_d.setToolTip("id of style")
        self.style_i_d.setGeometry(10, 10, 435, 25)
        self.style_i_d.doubleClicked.connect(self.StyleID_DblClick)

        self.label = QLineEdit()
        self.label.setObjectName("Label")
        self.label.setText("Label")
        self.label.setToolTip("Style name")
        self.label.setGeometry(441, 10, 1725, 25)

        self.button_remove_belong = QPushButton()
        self.button_remove_belong.setObjectName("ButtonRemoveBelong")
        self.button_remove_belong.setText("del")
        self.button_remove_belong.setToolTip("dissociate")
        self.button_remove_belong.setGeometry(2160, 10, 720, 240)
        _fnt = QFont("Terminal", 6)
        self.button_remove_belong.setFont(_fnt)
        self.button_remove_belong.clicked.connect(self.ButtonRemoveBelong_Click)


    # --- VBA Event Handlers ---


    def ButtonRemoveBelong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonRemoveBelong_Click
        # try:

            RelationsMgt.RemoveFromButton "Belong", Forms!Songs![SongID], self.StyleID, "Title"

            # label: Exit_ButtonRemoveBelong_Click

        # label: Err_ButtonRemoveBelong_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonRemoveBelong_Click

    def StyleCombo_AfterUpdate(self) -> None:

        RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.StyleCombo, "SongID", "StyleID", "Songs", "Belong"

    def StyleCombo_NotInList(self, NewData: str, Response: int) -> None:
        ActiveID: int = None
        Prompt: str = None
        MyQuery: str = None
        Const MB_ICONQUESTION = 32
        Const YES = 6
        Const YES_NO = 4
        CRLF = Chr$(13)
        Prompt = "Create New Style?"
        GetText = StyleCombo.Text
        # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  == YES:
            # DoCmd.OpenForm "Styles"

            # like ButtonAddStyle_Click

            MyQuery = "FreeStyleIDs"
            MyID = "StyleID"
            MyFirstControl = "Label"

            # DoCmd.OpenQuery MyQuery
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            # DoCmd.Close A_QUERY, MyQuery
            # DoCmd.GoToRecord A_FORM, "Styles", A_NEWREC
            # DoCmd.GoToControl MyID
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            # DoCmd.GoToControl MyFirstControl
            Forms!Styles!Label = GetText
        # DoCmd.Close A_FORM, "Styles"
        self.StyleCombo = ""
        self.Refresh

    def StyleID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyKey: str = None

        if Screen.ActiveControl != "":
            MyForm = "Styles"
            MyKey = "StyleID"
            MyFirstControl = "Label"

            GotoCriteria = Screen.ActiveControl
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StylesOfSong()
    window.show()
    sys.exit(app.exec())
