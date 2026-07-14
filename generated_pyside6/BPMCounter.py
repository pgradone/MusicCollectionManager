"""
Auto-generated PySide6 form: BPMCounter
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


class BPMCounter(QMainWindow):
    """Migrated from Access form: BPMCounter"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BPMCounter")
        self.setObjectName("BPMCounter")
        self.resize(6066, 600)
        self.timer_interval = 5
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.Form_Timer)
        self._timer.start(5)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.b_p_m_val = QLineEdit()
        self.b_p_m_val.setObjectName("BPMVal")
        self.b_p_m_val.setText("BPMVal")
        self.b_p_m_val.setGeometry(1699, 340, 573, 397)
        _fnt = QFont("Times New Roman", 14)
        self.b_p_m_val.setFont(_fnt)

        self.b_r = QPushButton()
        self.b_r.setObjectName("BR")
        self.b_r.setText("---->")
        self.b_r.setToolTip("BPMArrow")
        self.b_r.setGeometry(567, 1134, 567, 567)

        self.command_reset = QPushButton()
        self.command_reset.setObjectName("CommandReset")
        self.command_reset.setText("Reset")
        self.command_reset.setGeometry(2833, 340, 945, 397)
        self.command_reset.clicked.connect(self.CommandReset_Click)

        self.plus_one = QPushButton()
        self.plus_one.setObjectName("PlusOne")
        self.plus_one.setText("+")
        self.plus_one.setGeometry(2324, 340, 222, 397)
        self.plus_one.clicked.connect(self.PlusOne_Click)

        self.minus_one = QPushButton()
        self.minus_one.setObjectName("MinusOne")
        self.minus_one.setText("-")
        self.minus_one.setGeometry(1417, 340, 222, 397)
        self.minus_one.clicked.connect(self.MinusOne_Click)

        self.count = QLineEdit()
        self.count.setObjectName("Count")
        self.count.setGeometry(3968, 340, 573, 397)
        _fnt = QFont("Times New Roman", 14)
        self.count.setFont(_fnt)

        self.timing = QLineEdit()
        self.timing.setObjectName("Timing")
        self.timing.setGeometry(3968, 857, 1293, 397)
        _fnt = QFont("Times New Roman", 14)
        self.timing.setFont(_fnt)


    # --- VBA Event Handlers ---


    def BPMVal_AfterUpdate(self) -> None:
        ResetAll

    def Form_Load(self) -> None:
        ResetAll

    def CommandReset_Click(self) -> None:
        ResetAll

    def Form_Timer(self) -> None:
        Secs = str(datetime.datetime.now().time() - Timin)
        self.Timing = Secs
        Counter = Secs * self.BPMVal / 60
        self.Count = Counter
        self.BR.Left = 500 + 2000 * (Counter - Int(Counter))

    def MinusOne_Click(self) -> None:
        self.BPMVal = self.BPMVal - 1
        # DoCmd.RunCommand acCmdSave
        ResetAll

    def PlusOne_Click(self) -> None:
        self.BPMVal = self.BPMVal + 1
        # DoCmd.RunCommand acCmdSave
        ResetAll

    def ResetAll(self) -> None:
        self.BR.Left = 500
        Counter = 0
        Timin = datetime.datetime.now().time()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BPMCounter()
    window.show()
    sys.exit(app.exec())
