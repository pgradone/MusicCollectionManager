"""
Auto-generated PySide6 form: StylesOfSong
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


class StylesOfSong(QMainWindow):
    """Migrated from Access form: StylesOfSong.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("StylesOfSong")
        self.setObjectName("StylesOfSong")
        self.resize(199, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text7 = QLabel(self.central_widget)
        self.text7.setObjectName("Text7")
        self.text7.setText("StylesOfSong")
        self.text7.setGeometry(2, 3, 131, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)


        self.text8 = QLabel(self.central_widget)
        self.text8.setObjectName("Text8")
        self.text8.setText("StylesOfSong")
        self.text8.setGeometry(1, 1, 131, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)


        self.text10 = QLabel(self.central_widget)
        self.text10.setObjectName("Text10")
        self.text10.setText("ID")
        self.text10.setGeometry(1, 32, 19, 16)


        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Label")
        self.text12.setGeometry(29, 32, 41, 16)


        self.text14 = QLabel(self.central_widget)
        self.text14.setObjectName("Text14")
        self.text14.setText("remove")
        self.text14.setGeometry(144, 32, 48, 16)


        self.style_combo = QComboBox(self.central_widget)
        self.style_combo.setObjectName("StyleCombo")
        self.style_combo.addItems(["Styles_of_song"])
        self.style_combo.setToolTip("style to add to song")
        self.style_combo.setGeometry(134, 16, 65, 16)
        self.style_combo.setEditable(True)


        self.text15 = QLabel(self.central_widget)
        self.text15.setObjectName("Text15")
        self.text15.setText("add:")
        self.text15.setGeometry(134, 1, 31, 14)


        self.style_i_d = QLineEdit(self.central_widget)
        self.style_i_d.setObjectName("StyleID")
        self.style_i_d.setText("StyleID")
        self.style_i_d.setToolTip("id of style")
        self.style_i_d.setGeometry(1, 1, 29, 2)

        self.style_i_d.doubleClicked.connect(self.StyleID_DblClick)

        self.label = QLineEdit(self.central_widget)
        self.label.setObjectName("Label")
        self.label.setText("Label")
        self.label.setToolTip("Style name")
        self.label.setGeometry(29, 1, 115, 2)


        self.button_remove_belong = QPushButton(self.central_widget)
        self.button_remove_belong.setObjectName("ButtonRemoveBelong")
        self.button_remove_belong.setText("del")
        self.button_remove_belong.setToolTip("dissociate")
        self.button_remove_belong.setGeometry(144, 1, 48, 16)
        _fnt = QFont("Terminal", 6)
        self.button_remove_belong.setFont(_fnt)

        self.button_remove_belong.clicked.connect(self.ButtonRemoveBelong_Click)


    # --- VBA Event Handlers ---


    def ButtonRemoveBelong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonRemoveBelong_Click

        # Forms! reference: RelationsMgt.RemoveFromButton "Belong", Forms!Songs![SongID], self.StyleID, "Title"

        # label: Exit_ButtonRemoveBelong_Click
        return

        # label: Err_ButtonRemoveBelong_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonRemoveBelong_Click

    def StyleCombo_AfterUpdate(self) -> None:

        # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.StyleCombo, "SongID", "StyleID", "Songs", "Belong"
        pass

    def StyleCombo_NotInList(self, NewData: str, Response: int) -> None:
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
        Prompt = "Create New Style?"
        GetText = StyleCombo.text()
          # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  ==  YES:
            import Styles
            self.sub_form = Styles.Styles()
            self.sub_form.show()

              # like ButtonAddStyle_Click

            MyQuery = "FreeStyleIDs"
            MyID = "StyleID"
            MyFirstControl = "Label"

            # DoCmd.OpenQuery MyQuery
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            self.close()
            # DoCmd.GoToRecord A_FORM, "Styles", A_NEWREC
            # DoCmd.GoToControl MyID
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            # DoCmd.GoToControl MyFirstControl
            # Forms! reference: Forms!Styles!Label = GetText
        self.close()
        self.StyleCombo = ""
        self.Refresh()

    def StyleID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyForm: str = None
        MyKey: str = None
        MyFirstControl: str = None

        if self.focusWidget() if self.focusWidget() else "" != "":
            MyForm = "Styles"
            MyKey = "StyleID"
            MyFirstControl = "Label"

            GotoCriteria = self.focusWidget() if self.focusWidget() else ""
            # TODO: DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StylesOfSong()
    window.show()
    sys.exit(app.exec())
