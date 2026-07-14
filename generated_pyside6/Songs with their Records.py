"""
Auto-generated PySide6 form: Songs with their Records
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


class Songs_with_their_Records(QMainWindow):
    """Migrated from Access form: Songs with their Records"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Songs with their Records")
        self.setObjectName("Songs with their Records")
        self.resize(27408, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text7 = QLabel()
        self.text7.setObjectName("Text7")
        self.text7.setText("Songs with their Records")
        self.text7.setGeometry(180, 40, 3585, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text7.setFont(_fnt)

        self.text8 = QLabel()
        self.text8.setObjectName("Text8")
        self.text8.setText("Songs with their Records")
        self.text8.setGeometry(144, 10, 3585, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text8.setFont(_fnt)

        self.text10 = QLabel()
        self.text10.setObjectName("Text10")
        self.text10.setText("ID")
        self.text10.setGeometry(144, 360, 285, 240)

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("Songs.Title")
        self.text12.setGeometry(720, 360, 1110, 240)

        self.text14 = QLabel()
        self.text14.setObjectName("Text14")
        self.text14.setText("BPM")
        self.text14.setGeometry(4464, 360, 540, 240)

        self.text16 = QLabel()
        self.text16.setObjectName("Text16")
        self.text16.setText("Year")
        self.text16.setGeometry(4896, 120, 540, 240)

        self.text18 = QLabel()
        self.text18.setObjectName("Text18")
        self.text18.setText("Position")
        self.text18.setGeometry(5472, 360, 825, 240)

        self.text20 = QLabel()
        self.text20.setObjectName("Text20")
        self.text20.setText("RecordID")
        self.text20.setGeometry(6048, 120, 960, 240)

        self.text22 = QLabel()
        self.text22.setObjectName("Text22")
        self.text22.setText("Records.Title")
        self.text22.setGeometry(6768, 360, 1290, 240)

        self.text24 = QLabel()
        self.text24.setObjectName("Text24")
        self.text24.setText("Record House")
        self.text24.setGeometry(10224, 360, 1365, 240)

        self.text28 = QLabel()
        self.text28.setObjectName("Text28")
        self.text28.setText("M")
        self.text28.setGeometry(12384, 360, 285, 240)

        self.text30 = QLabel()
        self.text30.setObjectName("Text30")
        self.text30.setText("T")
        self.text30.setGeometry(12672, 360, 285, 240)

        self.song_i_d = QLineEdit()
        self.song_i_d.setObjectName("SongID")
        self.song_i_d.setText("SongID")
        self.song_i_d.setGeometry(144, 10, 420, 25)

        self.songs__title = QLineEdit()
        self.songs__title.setObjectName("Songs.Title")
        self.songs__title.setText("Songs.Title")
        self.songs__title.setGeometry(720, 10, 3600, 25)

        self.b_p_m = QLineEdit()
        self.b_p_m.setObjectName("BPM")
        self.b_p_m.setText("BPM")
        self.b_p_m.setGeometry(4464, 10, 420, 25)

        self.year = QLineEdit()
        self.year.setObjectName("Year")
        self.year.setText("Year")
        self.year.setGeometry(5040, 10, 285, 25)

        self.position = QLineEdit()
        self.position.setObjectName("Position")
        self.position.setText("Position")
        self.position.setGeometry(5472, 10, 435, 25)

        self.record_i_d = QLineEdit()
        self.record_i_d.setObjectName("RecordID")
        self.record_i_d.setText("RecordID")
        self.record_i_d.setGeometry(5904, 10, 570, 25)

        self.records__title = QLineEdit()
        self.records__title.setObjectName("Records.Title")
        self.records__title.setText("Records.Title")
        self.records__title.setGeometry(6624, 10, 3450, 25)

        self.record__house = QLineEdit()
        self.record__house.setObjectName("Record House")
        self.record__house.setText("Record House")
        self.record__house.setGeometry(10224, 10, 2010, 25)

        self.mike = QCheckBox()
        self.mike.setObjectName("Mike")
        self.mike.setText("Mike")
        self.mike.setGeometry(12384, 10, 100, 25)

        self.tito = QCheckBox()
        self.tito.setObjectName("Tito")
        self.tito.setText("Tito")
        self.tito.setGeometry(12672, 10, 100, 25)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Songs_with_their_Records()
    window.show()
    sys.exit(app.exec())
