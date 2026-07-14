"""
Auto-generated PySide6 form: BPMCounter
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


class BPMCounter(QMainWindow):
    """Migrated from Access form: BPMCounter.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("BPMCounter")
        self.setObjectName("BPMCounter")
        self.resize(404, 400)
        self.timer_interval = 5
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.Form_Timer)
        self._timer.start(5)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.b_p_m_val = QLineEdit(self.central_widget)
        self.b_p_m_val.setObjectName("BPMVal")
        self.b_p_m_val.setText("BPMVal")
        self.b_p_m_val.setGeometry(113, 23, 38, 26)
        _fnt = QFont("Times New Roman", 14)
        self.b_p_m_val.setFont(_fnt)


        self.b_r = QPushButton(self.central_widget)
        self.b_r.setObjectName("BR")
        self.b_r.setText("---->")
        self.b_r.setToolTip("BPMArrow")
        self.b_r.setGeometry(38, 76, 38, 38)


        self.command_reset = QPushButton(self.central_widget)
        self.command_reset.setObjectName("CommandReset")
        self.command_reset.setText("Reset")
        self.command_reset.setGeometry(189, 23, 63, 26)

        self.command_reset.clicked.connect(self.CommandReset_Click)

        self.plus_one = QPushButton(self.central_widget)
        self.plus_one.setObjectName("PlusOne")
        self.plus_one.setText("+")
        self.plus_one.setGeometry(155, 23, 15, 26)

        self.plus_one.clicked.connect(self.PlusOne_Click)

        self.minus_one = QPushButton(self.central_widget)
        self.minus_one.setObjectName("MinusOne")
        self.minus_one.setText("-")
        self.minus_one.setGeometry(94, 23, 15, 26)

        self.minus_one.clicked.connect(self.MinusOne_Click)

        self.count = QLineEdit(self.central_widget)
        self.count.setObjectName("Count")
        self.count.setGeometry(265, 23, 38, 26)
        _fnt = QFont("Times New Roman", 14)
        self.count.setFont(_fnt)


        self.timing = QLineEdit(self.central_widget)
        self.timing.setObjectName("Timing")
        self.timing.setGeometry(265, 57, 86, 26)
        _fnt = QFont("Times New Roman", 14)
        self.timing.setFont(_fnt)



    # --- VBA Event Handlers ---


    def BPMVal_AfterUpdate(self) -> None:
        ResetAll()

    def Form_Load(self) -> None:
        ResetAll()

    def CommandReset_Click(self) -> None:
        ResetAll()

    def Form_Timer(self) -> None:
        Secs = str(datetime.datetime.now().time() - Timin)
        self.Timing = Secs
        Counter = Secs * self.BPMVal / 60
        self.Count = Counter
        self.BR.Left = 500 + 2000 * (Counter - Int(Counter))

    def MinusOne_Click(self) -> None:
        self.BPMVal = self.BPMVal - 1
        # DoCmd.RunCommand acCmdSave
        ResetAll()

    def PlusOne_Click(self) -> None:
        self.BPMVal = self.BPMVal + 1
        # DoCmd.RunCommand acCmdSave
        ResetAll()

    def ResetAll(self) -> None:
        self.BR.Left = 500
        Counter = 0
        Timin = datetime.datetime.now().time()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BPMCounter()
    window.show()
    sys.exit(app.exec())
