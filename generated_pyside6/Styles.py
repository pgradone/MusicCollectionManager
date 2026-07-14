"""
Auto-generated PySide6 form: Styles
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


class Styles(QMainWindow):
    """Migrated from Access form: Styles.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Styles")
        self.setObjectName("Styles")
        self.resize(509, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Music Styles")
        self.text12.setGeometry(12, 3, 122, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text12.setFont(_fnt)


        self.text13 = QLabel(self.central_widget)
        self.text13.setObjectName("Text13")
        self.text13.setText("Music Styles")
        self.text13.setGeometry(10, 1, 124, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text13.setFont(_fnt)


        self.button_delete_style = QPushButton(self.central_widget)
        self.button_delete_style.setObjectName("ButtonDeleteStyle")
        self.button_delete_style.setText("Button18")
        self.button_delete_style.setGeometry(461, 1, 47, 32)

        self.button_delete_style.clicked.connect(self.ButtonDeleteStyle_Click)

        self.button_add_style = QPushButton(self.central_widget)
        self.button_add_style.setObjectName("ButtonAddStyle")
        self.button_add_style.setText("Add New Style")
        self.button_add_style.setGeometry(346, 1, 106, 2)
        _fnt = QFont("Arial", 9)
        self.button_add_style.setFont(_fnt)

        self.button_add_style.clicked.connect(self.ButtonAddStyle_Click)

        self.style_i_d = QComboBox(self.central_widget)
        self.style_i_d.setObjectName("StyleID")
        self.style_i_d.addItems(["FreeStyleIDs"])
        self.style_i_d.setCurrentText("StyleID")
        self.style_i_d.setGeometry(163, 8, 58, 16)
        self.style_i_d.setEditable(True)


        self.music_style_combo = QComboBox(self.central_widget)
        self.music_style_combo.setObjectName("MusicStyleCombo")
        self.music_style_combo.addItems(["MusicStyleCombo_Query"])
        self.music_style_combo.setGeometry(279, 8, 67, 16)
        self.music_style_combo.setEditable(True)


        self.label = QLineEdit(self.central_widget)
        self.label.setObjectName("Label")
        self.label.setText("Label")
        self.label.setGeometry(58, 8, 152, 2)


        # SubForm: SongsOfStyle
        self.songs_of_style = QWidget(self.central_widget)
        self.songs_of_style.setObjectName("SongsOfStyle")
        self.songs_of_style.setProperty("sourceObject", "Form.SongsOfStyle")
        self.songs_of_style.setGeometry(0, 32, 509, 308)



    # --- VBA Event Handlers ---


    def ButtonAddStyle_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonAddStyle_Click

        NewIDMgt.AddNewID("StyleID", "FreeStyleIDs")

        MyFirstControl: str = None
        MyFirstControl = "Label"

        # DoCmd.GoToControl MyFirstControl

        # label: Exit_ButtonAddStyle_Click
        return

        # label: Err_ButtonAddStyle_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonAddStyle_Click

    def ButtonDeleteStyle_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDeleteStyle_Click


        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

        # label: Exit_ButtonDeleteStyle_Click
        return

        # label: Err_ButtonDeleteStyle_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonDeleteStyle_Click

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID(self.Name, "StyleID")

    def MusicStyleCombo_AfterUpdate(self) -> None:
        Criteria: str = None
        MyRS: Any = None
        ActiveName: str = None
        Prompt: str = None
        Message: str = None
        CRLF: str = None
        # VBA Const: MB_ICONQUESTION = 32
        # VBA Const: YES = 6
        # VBA Const: YES_NO = 4
        CRLF = chr(13)

        Prompt = "Create new one?"
        MyRS = self.RecordsetClone

          # Build the criteria.
        ActiveName = self.focusWidget() if self.focusWidget() else ""
        Criteria = "[StyleID] = " + ActiveName
          # Perform the search.
        MyRS.FindFirst(Criteria)

        if MyRS.NoMatch:
            Message = ActiveName + " not found" + CRLF
            if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new Style")  ==  YES:
                # DoCmd.GoToRecord , , A_NEWREC
                self.SongID = self.SongCombo
                self.Refresh()
        else:
              # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Styles()
    window.show()
    sys.exit(app.exec())
