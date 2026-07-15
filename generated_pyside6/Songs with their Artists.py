"""
Auto-generated PySide6 form: Songs with their Artists
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


class Songs_with_their_Artists(QMainWindow):
    """Migrated from Access form: Songs with their Artists.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self._dbl_click_widgets: set[QObject] = set()
        self.setWindowTitle("Songs with their Artists")
        self.setObjectName("Songs with their Artists")
        self.resize(1275, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text7 = QLabel(self.central_widget)
        self.text7.setObjectName("Text7")
        self.text7.setText("Songs with their Artists")
        self.text7.setGeometry(12, 3, 217, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)


        self.text8 = QLabel(self.central_widget)
        self.text8.setObjectName("Text8")
        self.text8.setText("Songs with their Artists")
        self.text8.setGeometry(10, 1, 217, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)


        self.text10 = QLabel(self.central_widget)
        self.text10.setObjectName("Text10")
        self.text10.setText("ID")
        self.text10.setGeometry(1, 32, 19, 16)


        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Title")
        self.text12.setGeometry(48, 32, 35, 16)


        self.text14 = QLabel(self.central_widget)
        self.text14.setObjectName("Text14")
        self.text14.setText("BPM")
        self.text14.setGeometry(230, 32, 36, 16)


        self.text16 = QLabel(self.central_widget)
        self.text16.setObjectName("Text16")
        self.text16.setText("Year")
        self.text16.setGeometry(259, 16, 38, 16)


        self.text18 = QLabel(self.central_widget)
        self.text18.setObjectName("Text18")
        self.text18.setText("ArtistID")
        self.text18.setGeometry(288, 32, 52, 16)


        self.text20 = QLabel(self.central_widget)
        self.text20.setObjectName("Text20")
        self.text20.setText("Name")
        self.text20.setGeometry(355, 32, 42, 16)


        self.text22 = QLabel(self.central_widget)
        self.text22.setObjectName("Text22")
        self.text22.setText("Surname")
        self.text22.setGeometry(422, 32, 59, 16)


        self.song_i_d = QLineEdit(self.central_widget)
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(1, 1, 29, 2)


        self.title = QLineEdit(self.central_widget)
        self.title.setObjectName("Title")
        self.title.setText("Title")
        self.title.setGeometry(38, 1, 192, 2)


        self.b_p_m = QLineEdit(self.central_widget)
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setGeometry(230, 1, 38, 2)


        self.year = QLineEdit(self.central_widget)
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(269, 1, 29, 2)


        self.artist_i_d = QLineEdit(self.central_widget)
        self.artist_i_d.setObjectName("ArtistID")
        self.artist_i_d.setText("ArtistID")
        self.artist_i_d.setGeometry(298, 1, 38, 2)


        self.name = QLineEdit(self.central_widget)
        self.name.setObjectName("Name")
        self.name.setText("Name")
        self.name.setGeometry(346, 1, 76, 2)


        self.surname = QLineEdit(self.central_widget)
        self.surname.setObjectName("Surname")
        self.surname.setText("Surname")
        self.surname.setGeometry(422, 1, 135, 2)



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
    window = Songs_with_their_Artists()
    window.show()
    sys.exit(app.exec())
