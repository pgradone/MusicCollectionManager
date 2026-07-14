"""
Auto-generated PySide6 form: Songs with their Records
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


class Songs_with_their_Records(QMainWindow):
    """Migrated from Access form: Songs with their Records.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Songs with their Records")
        self.setObjectName("Songs with their Records")
        self.resize(1827, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text7 = QLabel(self.central_widget)
        self.text7.setObjectName("Text7")
        self.text7.setText("Songs with their Records")
        self.text7.setGeometry(12, 3, 239, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)


        self.text8 = QLabel(self.central_widget)
        self.text8.setObjectName("Text8")
        self.text8.setText("Songs with their Records")
        self.text8.setGeometry(10, 1, 239, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)


        self.text10 = QLabel(self.central_widget)
        self.text10.setObjectName("Text10")
        self.text10.setText("ID")
        self.text10.setGeometry(10, 24, 19, 16)


        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Songs.Title")
        self.text12.setGeometry(48, 24, 74, 16)


        self.text14 = QLabel(self.central_widget)
        self.text14.setObjectName("Text14")
        self.text14.setText("BPM")
        self.text14.setGeometry(298, 24, 36, 16)


        self.text16 = QLabel(self.central_widget)
        self.text16.setObjectName("Text16")
        self.text16.setText("Year")
        self.text16.setGeometry(326, 8, 36, 16)


        self.text18 = QLabel(self.central_widget)
        self.text18.setObjectName("Text18")
        self.text18.setText("Position")
        self.text18.setGeometry(365, 24, 55, 16)


        self.text20 = QLabel(self.central_widget)
        self.text20.setObjectName("Text20")
        self.text20.setText("RecordID")
        self.text20.setGeometry(403, 8, 64, 16)


        self.text22 = QLabel(self.central_widget)
        self.text22.setObjectName("Text22")
        self.text22.setText("Records.Title")
        self.text22.setGeometry(451, 24, 86, 16)


        self.text24 = QLabel(self.central_widget)
        self.text24.setObjectName("Text24")
        self.text24.setText("Record House")
        self.text24.setGeometry(682, 24, 91, 16)


        self.text28 = QLabel(self.central_widget)
        self.text28.setObjectName("Text28")
        self.text28.setText("M")
        self.text28.setGeometry(826, 24, 19, 16)


        self.text30 = QLabel(self.central_widget)
        self.text30.setObjectName("Text30")
        self.text30.setText("T")
        self.text30.setGeometry(845, 24, 19, 16)


        self.song_i_d = QLineEdit(self.central_widget)
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(10, 1, 28, 2)


        self.songs__title = QLineEdit(self.central_widget)
        self.songs__title.setObjectName("Songs.Title")
        self.songs__title.setText("Songs.Title")
        self.songs__title.setGeometry(48, 1, 240, 2)


        self.b_p_m = QLineEdit(self.central_widget)
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setGeometry(298, 1, 28, 2)


        self.year = QLineEdit(self.central_widget)
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(336, 1, 19, 2)


        self.position = QLineEdit(self.central_widget)
        self.position.setObjectName("Position")
        self.position.setText("Position")
        self.position.setGeometry(365, 1, 29, 2)


        self.record_i_d = QLineEdit(self.central_widget)
        self.record_i_d.setObjectName("RecordID")
        self.record_i_d.setText("RecordID")
        self.record_i_d.setGeometry(394, 1, 38, 2)


        self.records__title = QLineEdit(self.central_widget)
        self.records__title.setObjectName("Records.Title")
        self.records__title.setText("Records.Title")
        self.records__title.setGeometry(442, 1, 230, 2)


        self.record__house = QLineEdit(self.central_widget)
        self.record__house.setObjectName("Record House")
        self.record__house.setText("Record House")
        self.record__house.setGeometry(682, 1, 134, 2)


        self.mike = QCheckBox(self.central_widget)
        self.mike.setObjectName("Mike")
        self.mike.setText("Mike")
        self.mike.setGeometry(826, 1, 7, 2)


        self.tito = QCheckBox(self.central_widget)
        self.tito.setObjectName("Tito")
        self.tito.setText("Tito")
        self.tito.setGeometry(845, 1, 7, 2)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Songs_with_their_Records()
    window.show()
    sys.exit(app.exec())
