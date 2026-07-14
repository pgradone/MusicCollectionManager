"""
Auto-generated PySide6 form: Programs
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


class Programs(QMainWindow):
    """Migrated from Access form: Programs"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programs")
        self.setObjectName("Programs")
        self.resize(9765, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # --- Controls ---

        self.text12 = QLabel()
        self.text12.setObjectName("Text12")
        self.text12.setText("Programs")
        self.text12.setGeometry(324, 40, 1425, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text12.setFont(_fnt)

        self.text13 = QLabel()
        self.text13.setObjectName("Text13")
        self.text13.setText("Programs")
        self.text13.setGeometry(288, 10, 1425, 405)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text13.setFont(_fnt)

        self.button_add_program = QPushButton()
        self.button_add_program.setObjectName("ButtonAddProgram")
        self.button_add_program.setText("Add Program")
        self.button_add_program.setToolTip("Create A new Program")
        self.button_add_program.setGeometry(2040, 94, 100, 25)
        self.button_add_program.clicked.connect(self.ButtonAddProgram_Click)

        self.button_print_record = QPushButton()
        self.button_print_record.setObjectName("ButtonPrintRecord")
        self.button_print_record.setText("Button35")
        self.button_print_record.setToolTip("Print This Schedule")
        self.button_print_record.setGeometry(6336, 10, 576, 486)
        self.button_print_record.clicked.connect(self.ButtonPrintRecord_Click)

        self.button_delete_schedule = QPushButton()
        self.button_delete_schedule.setObjectName("ButtonDeleteSchedule")
        self.button_delete_schedule.setText("Button36")
        self.button_delete_schedule.setGeometry(7056, 10, 576, 486)
        self.button_delete_schedule.clicked.connect(self.ButtonDeleteSchedule_Click)

        self.text_sched_songs = QLabel()
        self.text_sched_songs.setObjectName("TextSchedSongs")
        self.text_sched_songs.setText("Scheduled Songs")
        self.text_sched_songs.setGeometry(3744, 120, 2445, 360)
        _fnt = QFont("Book Antiqua", 14)
        self.text_sched_songs.setFont(_fnt)

        self.program_i_d = QLineEdit()
        self.program_i_d.setObjectName("ProgramID")
        self.program_i_d.setText("ProgramID")
        self.program_i_d.setToolTip("Auto Number generated with \"ADD PROGRAM\")
        self.program_i_d.setGeometry(1296, 120, 1005, 25)

        self.prog_name = QLineEdit()
        self.prog_name.setObjectName("ProgName")
        self.prog_name.setText("ProgName")
        self.prog_name.setToolTip("Label of Program")
        self.prog_name.setGeometry(3600, 120, 3315, 25)
        self.prog_name.setPlaceholderText("\"AstraDyne\" & Year(Date()) & Month(Date()) & Day(Date())")

        self.date_sched = QLineEdit()
        self.date_sched.setObjectName("DateSched")
        self.date_sched.setText("DateSched")
        self.date_sched.setGeometry(1869, 480, 1875, 25)
        self.date_sched.setPlaceholderText("=Date() & \" 19:00:00\")

        self.date_create = QLineEdit()
        self.date_create.setObjectName("DateCreate")
        self.date_create.setText("DateCreate")
        self.date_create.setGeometry(5034, 480, 1860, 25)
        self.date_create.setPlaceholderText("=Now()")

        self.description = QLineEdit()
        self.description.setObjectName("Description")
        self.description.setText("Description")
        self.description.setGeometry(1440, 840, 6630, 25)

        self.text28 = QLabel()
        self.text28.setObjectName("Text28")
        self.text28.setText("Song to Schedule")
        self.text28.setGeometry(144, 1200, 1578, 240)
        self.text28.setStyleSheet("background-color: #80FF80")

        self.position_schedule = QLineEdit()
        self.position_schedule.setObjectName("PositionSchedule")
        self.position_schedule.setGeometry(8208, 1200, 429, 240)
        self.position_schedule.setPlaceholderText("1")

        self.text31 = QLabel()
        self.text31.setObjectName("Text31")
        self.text31.setText("position:")
        self.text31.setGeometry(7344, 1200, 810, 240)
        self.text31.setStyleSheet("background-color: #80FF80")

        self.song_combo = QComboBox()
        self.song_combo.setObjectName("SongCombo")
        self.song_combo.addItems(["SongInProgramSelect"])
        self.song_combo.setGeometry(1700, 1228, 3369, 240)
        self.song_combo.setEditable(True)

        # SubForm: ProgramsSched
        self.programs_sched = QWidget()
        self.programs_sched.setObjectName("ProgramsSched")
        self.programs_sched.setProperty("sourceObject", "Form.ProgramsSched")
        self.programs_sched.setGeometry(10, 1560, 9765, 6375)

        self.support_choose_combo = QComboBox()
        self.support_choose_combo.setObjectName("SupportChooseCombo")
        self.support_choose_combo.addItems(["SupportsOfRecord"])
        self.support_choose_combo.setGeometry(6009, 1228, 1191, 236)
        self.support_choose_combo.setEditable(True)

        self.tot_time_avg = QLineEdit()
        self.tot_time_avg.setObjectName("TotTimeAvg")
        self.tot_time_avg.setText("=CalcTTime()")
        self.tot_time_avg.setGeometry(8050, 472, 1584, 240)

        self.label72 = QLabel()
        self.label72.setObjectName("Label72")
        self.label72.setText("TotTime")
        self.label72.setGeometry(7200, 472, 780, 240)
        self.label72.setStyleSheet("background-color: #80FF80")

        self.label73 = QLabel()
        self.label73.setObjectName("Label73")
        self.label73.setText("real - extrapolated")
        self.label73.setGeometry(8025, 195, 1635, 240)
        self.label73.setStyleSheet("background-color: #80FF80")


    # --- VBA Event Handlers ---


    def ButtonAddProgram_Click(self) -> None:
        # DoCmd.GoToRecord , , A_NEWREC
        self.Description.SetFocus

    def ButtonDeleteProgram_Click(self) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

    def ButtonDeleteSchedule_Click(self) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

    def ButtonPrintRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonPrintRecord_Click
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
            # DoCmd.PrintOut A_SELECTION

            # label: Exit_ButtonPrintRecord_Click

        # label: Err_ButtonPrintRecord_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonPrintRecord_Click

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID self.Name, "ProgramID"

    def Form_Open(self, Cancel: int) -> None:
        # DoCmd.MoveSize , 0, , 9500

    def ProgramID_AfterUpdate(self) -> None:
        self.Refresh

    def SongCombo_AfterUpdate(self) -> None:
        # VBA: On Error GoTo Err_SongCombo_AfterUpdate
        # try:

            Criteria: str = None
            RecordCriteria: str = None
            # dim MyContain As Recordset,
            MyDb: Any = None
            MySongs: Any = None
            MyWS: Any = None
            # Myfile = Right(CurrentDb.TableDefs(1).Connect, Len(CurrentDb.TableDefs(1).Connect) - 10)
            # Myfile = "MusiDB.mdb"
            MyWS = DBEngine.Workspaces(0)
            # Set MyDB = MyWS.OpenDatabase(Myfile)
            MyDb = CurrentDb
            Criteria = "[SongID] = " + self.SongCombo
            MySchedule = MyDb.OpenRecordset("Schedule", DB_OPEN_TABLE)
            MySongs = MyDb.OpenRecordset("Songs", DB_OPEN_DYNASET)
            MyArtists = MyDb.OpenRecordset("Artists", DB_OPEN_DYNASET)
            MySing = MyDb.OpenRecordset("Sing", DB_OPEN_DYNASET)
            MyContain = MyDb.OpenRecordset("Contain", DB_OPEN_DYNASET)
            MyRecords = MyDb.OpenRecordset("Records", DB_OPEN_DYNASET)

            MySongs.FindFirst Criteria
            MySchedule.Index = "PrimaryKey"
            MySchedule.AddNew
            MySchedule("ProgramID") = self.ProgramID   ' **** Fill Schedule IDs
            MySchedule("Position") = self.PositionSchedule
            MySing.FindFirst Criteria
            while not (MySing.NoMatch  ' ********* Get all Artists singing song):
                ArtistCriteria = "[ArtistID] = " + MySing("ArtistID")
                MyArtists.FindFirst ArtistCriteria
                if MyArtists("Name") != "":
                    ArtistsOfSong = ArtistsOfSong + " " + MyArtists("Name")
                if MyArtists("Surname") != "":
                    ArtistsOfSong = ArtistsOfSong + " " + MyArtists("Surname")
                MySing.FindNext Criteria
            # MyContain.FindFirst Criteria
            # Do Until MyContain.NoMatch  '  ******** Get all Records containing
            # RecordCriteria = "[RecordID] = " & MyContain("RecordID")
            # MyRecords.FindFirst RecordCriteria
            # If MyRecords("Title") <> "" Then
            # RecordsOfSong = RecordsOfSong + "  " + MyRecords("Title")
            # End If
            # If MyRecords("Support") <> "" Then
            # RecordsOfSong = RecordsOfSong + " " + MyRecords("Support")
            # End If
            # If MyContain("Position") <> "" Then
            # RecordsOfSong = RecordsOfSong + " :" + MyContain("Position")
            # End If
            # MyContain.FindNext Criteria
            # Loop
            RecordsOfSong = self.SongCombo.Column(3)
            # ********* Fill Fields with calculated contents
            MySchedule("SongID") = self.SongCombo
            ArtistsOfSong = Trim$(ArtistsOfSong)
            MySchedule("Song_Artist") = Left$(MySongs("Title") + " * " + ArtistsOfSong, 79)
            MySchedule("Record") = Left$(Trim$(RecordsOfSong), 79)
            MySchedule("BPM") = MySongs("BPM")
            MySchedule("Year") = MySongs("Year")
            MySchedule.Update
            MyRecords.Close
            MyContain.Close
            MySchedule.Close
            MySongs.Close
            MySing.Close
            MyArtists.Close
            self.PositionSchedule = self.PositionSchedule + 1
            self.Refresh

            # label: Exit_SongCombo_AfterUpdate

        # label: Err_SongCombo_AfterUpdate
        QMessageBox.information(self, '', str(E))
        # MsgBox Error$ & " enter program ID!"
        # VBA: Resume Exit_SongCombo_AfterUpdate

    def SupportChooseCombo_AfterUpdate(self) -> None:
        self.SongCombo.Requery

    def CalcTTime(self) -> str:
        TotTime: datetime.datetime = None
        Dim totRec, TotRecNull As Integer
        sqlTxT: str = None
        rst: Any = None
        CTT: str = None
        CTT = ""
        if self.ProgramID is None:
        sqlTxT = "SELECT Schedule.ProgramID, datetime.datetime.strptime(Sum(datetime.datetime.now().time() Is None if None else CDate('00:' + str(datetime.datetime.now(.time()[:int(""hh:nn"")],5))))) AS Tim, datetime.datetime.strptime(CDate(Sum(datetime.datetime.now().time() Is None if None else CDate('00:' + str(datetime.datetime.now(.time()[:int(""hh:nn"")],5)))))*(Count(TIme Is None if None else 'FulTim')+Count(TIme Is None if 'NulTim' else None))/Count(TIme Is None if None else 'FulTim')) AS AvgTim, Count(TIme Is None if None else 'FulTim') AS FullTim, Count(TIme Is None if 'NulTim' else None) AS NullTim FROM Songs INNER JOIN Schedule ON Songs.SongID = Schedule.SongID GROUP BY Schedule.ProgramID " + "HAVING ProgramID = " + self.ProgramID
        # sqltxt = "SELECT IIF(Time is null,NULL,'00:' & left(format(time,""hh:nn""),5)) AS Tim " &         "FROM Songs INNER JOIN Schedule on Songs.SongID = Schedule.SongID " &         "WHERE ProgramID = " & Me.ProgramID
        rst = CurrentDb.OpenRecordset(sqlTxT)
        # Do While Not rst.EOF
        # If IsNull(rst!Tim) Then
        # TotTime = TotTime + CDate(rst!Tim)
        # totRec = totRec + 1
        # Else
        # TotRecNull = TotRecNull + 1
        # End If
        # rst.MoveNext
        # Loop
        # VBA: On Error Resume Next
        # try:
            CTT = rst!Tim + " - " + rst!AvgTim
            # VBA: On Error GoTo 0
            # try:
                rst.Close
                # If totRec = 0 Then Exit Function
                # CTT = TotTime & " - " & CDate(TotTime * (totRec + TotRecNull) / totRec)
                CalcTTime = CTT


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Programs()
    window.show()
    sys.exit(app.exec())
