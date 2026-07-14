"""
Auto-generated PySide6 form: Songs with their Artists
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


class Songs_with_their_Artists(QMainWindow):
    """Migrated from Access form: Songs with their Artists"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Songs with their Artists")
        self.setObjectName("Songs with their Artists")
        self.resize(19128, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text7 = QLabel()
        self.text7.setObjectName("Text7")
        self.text7.setText("Songs with their Artists")
        self.text7.setGeometry(180, 40, 3255, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)

        self.text8 = QLabel()
        self.text8.setObjectName("Text8")
        self.text8.setText("Songs with their Artists")
        self.text8.setGeometry(144, 10, 3255, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)

        self.text10 = QLabel()
        self.text10.setObjectName("Text10")
        self.text10.setText("ID")
        self.text10.setGeometry(10, 480, 285, 240)

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("Title")
        self.text12.setGeometry(720, 480, 525, 240)

        self.text14 = QLabel()
        self.text14.setObjectName("Text14")
        self.text14.setText("BPM")
        self.text14.setGeometry(3456, 480, 540, 240)

        self.text16 = QLabel()
        self.text16.setObjectName("Text16")
        self.text16.setText("Year")
        self.text16.setGeometry(3888, 240, 570, 240)

        self.text18 = QLabel()
        self.text18.setObjectName("Text18")
        self.text18.setText("ArtistID")
        self.text18.setGeometry(4320, 480, 780, 240)

        self.text20 = QLabel()
        self.text20.setObjectName("Text20")
        self.text20.setText("Name")
        self.text20.setGeometry(5328, 480, 630, 240)

        self.text22 = QLabel()
        self.text22.setObjectName("Text22")
        self.text22.setText("Surname")
        self.text22.setGeometry(6336, 480, 885, 240)

        self.song_i_d = QLineEdit()
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(10, 10, 435, 25)

        self.title = QLineEdit()
        self.title.setObjectName("Title")
        self.title.setText("Title")
        self.title.setGeometry(576, 10, 2880, 25)

        self.b_p_m = QLineEdit()
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setGeometry(3456, 10, 570, 25)

        self.year = QLineEdit()
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(4032, 10, 435, 25)

        self.artist_i_d = QLineEdit()
        self.artist_i_d.setObjectName("ArtistID")
        self.artist_i_d.setText("ArtistID")
        self.artist_i_d.setGeometry(4464, 10, 570, 25)

        self.name = QLineEdit()
        self.name.setObjectName("Name")
        self.name.setText("Name")
        self.name.setGeometry(5184, 10, 1140, 25)

        self.surname = QLineEdit()
        self.surname.setObjectName("Surname")
        self.surname.setText("Surname")
        self.surname.setGeometry(6336, 10, 2025, 25)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Songs_with_their_Artists()
    window.show()
    sys.exit(app.exec())
