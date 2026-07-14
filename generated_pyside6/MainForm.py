"""
Auto-generated PySide6 form: MainForm
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


class MainForm(QMainWindow):
    """Migrated from Access form: MainForm.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MainForm")
        self.setObjectName("MainForm")
        self.resize(440, 400)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.button_open_songs = QPushButton(self.central_widget)
        self.button_open_songs.setObjectName("ButtonOpenSongs")
        self.button_open_songs.setText("Songs")
        self.button_open_songs.setGeometry(154, 96, 58, 31)

        self.button_open_songs.clicked.connect(self.ButtonOpenSongs_Click)

        self.button_open_records = QPushButton(self.central_widget)
        self.button_open_records.setObjectName("ButtonOpenRecords")
        self.button_open_records.setText("Records")
        self.button_open_records.setGeometry(10, 96, 67, 31)

        self.button_open_records.clicked.connect(self.ButtonOpenRecords_Click)

        self.button_open_artists = QPushButton(self.central_widget)
        self.button_open_artists.setObjectName("ButtonOpenArtists")
        self.button_open_artists.setText("Artists")
        self.button_open_artists.setGeometry(298, 96, 58, 31)

        self.button_open_artists.clicked.connect(self.ButtonOpenArtists_Click)

        self.button_open_programs = QPushButton(self.central_widget)
        self.button_open_programs.setObjectName("ButtonOpenPrograms")
        self.button_open_programs.setText("Programs")
        self.button_open_programs.setGeometry(144, 216, 76, 31)

        self.button_open_programs.clicked.connect(self.ButtonOpenPrograms_Click)

        self.text4 = QLabel(self.central_widget)
        self.text4.setObjectName("Text4")
        self.text4.setText("schedule")
        self.text4.setGeometry(154, 176, 58, 16)


        self.text5 = QLabel(self.central_widget)
        self.text5.setObjectName("Text5")
        self.text5.setText("sing")
        self.text5.setGeometry(240, 104, 29, 16)


        self.text6 = QLabel(self.central_widget)
        self.text6.setObjectName("Text6")
        self.text6.setText("contain")
        self.text6.setGeometry(96, 104, 39, 16)


        # Line: Line7
        self.line7 = QFrame(self.central_widget)
        self.line7.setFrameShape(QFrame.Shape.HLine)
        self.line7.setObjectName("Line7")
        self.line7.setGeometry(38, 136, 115, 2)


        # Line: Line8
        self.line8 = QFrame(self.central_widget)
        self.line8.setFrameShape(QFrame.Shape.VLine)
        self.line8.setObjectName("Line8")
        self.line8.setGeometry(182, 192, 2, 24)


        # Line: Line9
        self.line9 = QFrame(self.central_widget)
        self.line9.setFrameShape(QFrame.Shape.HLine)
        self.line9.setObjectName("Line9")
        self.line9.setGeometry(211, 112, 29, 2)


        # Line: Line10
        self.line10 = QFrame(self.central_widget)
        self.line10.setFrameShape(QFrame.Shape.HLine)
        self.line10.setObjectName("Line10")
        self.line10.setGeometry(269, 112, 29, 2)


        # Line: Line11
        self.line11 = QFrame(self.central_widget)
        self.line11.setFrameShape(QFrame.Shape.HLine)
        self.line11.setObjectName("Line11")
        self.line11.setGeometry(134, 112, 19, 2)


        # Line: Line12
        self.line12 = QFrame(self.central_widget)
        self.line12.setFrameShape(QFrame.Shape.HLine)
        self.line12.setObjectName("Line12")
        self.line12.setGeometry(77, 112, 19, 2)


        self.button_quit_application = QPushButton(self.central_widget)
        self.button_quit_application.setObjectName("ButtonQuitApplication")
        self.button_quit_application.setText("Button13")
        self.button_quit_application.setGeometry(10, 200, 38, 38)

        self.button_quit_application.clicked.connect(self.ButtonQuitApplicatio_Click)

        # Line: Line14
        self.line14 = QFrame(self.central_widget)
        self.line14.setFrameShape(QFrame.Shape.HLine)
        self.line14.setObjectName("Line14")
        self.line14.setGeometry(211, 136, 115, 2)


        # Line: Line15
        self.line15 = QFrame(self.central_widget)
        self.line15.setFrameShape(QFrame.Shape.VLine)
        self.line15.setObjectName("Line15")
        self.line15.setGeometry(182, 136, 2, 40)


        # Line: Line16
        self.line16 = QFrame(self.central_widget)
        self.line16.setFrameShape(QFrame.Shape.HLine)
        self.line16.setObjectName("Line16")
        self.line16.setGeometry(115, 136, 48, 40)


        # Line: Line17
        self.line17 = QFrame(self.central_widget)
        self.line17.setFrameShape(QFrame.Shape.VLine)
        self.line17.setObjectName("Line17")
        self.line17.setGeometry(211, 136, 38, 40)


        self.button_open_styles = QPushButton(self.central_widget)
        self.button_open_styles.setObjectName("ButtonOpenStyles")
        self.button_open_styles.setText("Styles")
        self.button_open_styles.setGeometry(154, 8, 56, 31)

        self.button_open_styles.clicked.connect(self.ButtonOpenStyles_Click)

        self.text20 = QLabel(self.central_widget)
        self.text20.setObjectName("Text20")
        self.text20.setText("belong")
        self.text20.setGeometry(163, 56, 38, 16)


        # Line: Line21
        self.line21 = QFrame(self.central_widget)
        self.line21.setFrameShape(QFrame.Shape.VLine)
        self.line21.setObjectName("Line21")
        self.line21.setGeometry(182, 40, 2, 16)


        # Line: Line22
        self.line22 = QFrame(self.central_widget)
        self.line22.setFrameShape(QFrame.Shape.VLine)
        self.line22.setObjectName("Line22")
        self.line22.setGeometry(182, 72, 2, 24)


        self.button__open_query__records__songs__artists = QPushButton(self.central_widget)
        self.button__open_query__records__songs__artists.setObjectName("Button_OpenQuery_Records_Songs_Artists")
        self.button__open_query__records__songs__artists.setText("Records_Songs_Artists")
        self.button__open_query__records__songs__artists.setGeometry(250, 40, 153, 23)
        _fnt = QFont("r_ansi", 8)
        self.button__open_query__records__songs__artists.setFont(_fnt)

        self.button__open_query__records__songs__artists.clicked.connect(self.Button_OpenQuery_Rec_Click)

        self.label24 = QLabel(self.central_widget)
        self.label24.setObjectName("Label24")
        self.label24.setText("v5  25-Mar-2003")
        self.label24.setGeometry(19, 19, 86, 16)



    # --- VBA Event Handlers ---


    def Button_OpenQuery_Rec_Click(self) -> None:
        # VBA: On Error GoTo Err_Button_OpenQuery_Rec_Click

        QueryName: str = None
        LinkCriteria: str = None

        QueryName = "Records_Songs_Artists"
        # DoCmd.OpenQuery QueryName

        # label: Exit_Button_OpenQuery_Rec_Click
        return

        # label: Err_Button_OpenQuery_Rec_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_Button_OpenQuery_Rec_Click

    def ButtonOpenArtists_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonOpenArtists_Click

        DocName: str = None
        LinkCriteria: str = None

        DocName = "Artists"
        # TODO: DoCmd.OpenForm DocName, , , LinkCriteria

        # label: Exit_ButtonOpenArtists_Click
        return

        # label: Err_ButtonOpenArtists_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonOpenArtists_Click

    def ButtonOpenPrograms_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonOpenPrograms_Click

        DocName: str = None
        LinkCriteria: str = None

        DocName = "Programs"
        # TODO: DoCmd.OpenForm DocName, , , LinkCriteria
        # DoCmd.GoToRecord , "", acLast
        # DoCmd.MoveSize 0, 0

        # label: Exit_ButtonOpenPrograms_Click
        return

        # label: Err_ButtonOpenPrograms_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonOpenPrograms_Click

    def ButtonOpenRecords_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonOpenRecords_Click

        DocName: str = None
        LinkCriteria: str = None

        DocName = "Records"
        # TODO: DoCmd.OpenForm DocName, , , LinkCriteria

        # label: Exit_ButtonOpenRecords_Click
        return

        # label: Err_ButtonOpenRecords_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonOpenRecords_Click

    def ButtonOpenSongs_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonOpenSongs_Click

        DocName: str = None
        LinkCriteria: str = None

        DocName = "Songs"
        # TODO: DoCmd.OpenForm DocName, , , LinkCriteria

        # label: Exit_ButtonOpenSongs_Click
        return

        # label: Err_ButtonOpenSongs_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonOpenSongs_Click

    def ButtonOpenStyles_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonOpenStyles_Click

        DocName: str = None
        LinkCriteria: str = None

        DocName = "Styles"
        # TODO: DoCmd.OpenForm DocName, , , LinkCriteria

        # label: Exit_ButtonOpenStyles_Click
        return

        # label: Err_ButtonOpenStyles_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonOpenStyles_Click

    def ButtonQuitApplicatio_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonQuitApplicatio_Click

        self.close()

        # label: Exit_ButtonQuitApplicatio_Click
        return

        # label: Err_ButtonQuitApplicatio_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonQuitApplicatio_Click


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec())
