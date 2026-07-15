"""
Auto-generated PySide6 form: Programs
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


class Programs(QMainWindow):
    """Migrated from Access form: Programs.

    Coordinates converted from twips (Access) to pixels.
    """

    def __init__(self) -> None:
        super().__init__()
        self._dbl_click_widgets: set[QObject] = set()
        self.setWindowTitle("Programs")
        self.setObjectName("Programs")
        self.resize(651, 559)

        # Central widget (no layout = absolute positioning like Access)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0;")

        # --- Controls (absolute positions, twips converted to px) ---

        self.text12 = QLabel(self.central_widget)
        self.text12.setObjectName("Text12")
        self.text12.setText("Programs")
        self.text12.setGeometry(22, 3, 95, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text12.setFont(_fnt)


        self.text13 = QLabel(self.central_widget)
        self.text13.setObjectName("Text13")
        self.text13.setText("Programs")
        self.text13.setGeometry(19, 1, 95, 27)
        _fnt = QFont()
        _fnt.setPointSize(14)
        self.text13.setFont(_fnt)


        self.button_add_program = QPushButton(self.central_widget)
        self.button_add_program.setObjectName("ButtonAddProgram")
        self.button_add_program.setText("Add Program")
        self.button_add_program.setToolTip("Create A new Program")
        self.button_add_program.setGeometry(136, 6, 7, 2)

        self.button_add_program.clicked.connect(self.ButtonAddProgram_Click)

        self.button_print_record = QPushButton(self.central_widget)
        self.button_print_record.setObjectName("ButtonPrintRecord")
        self.button_print_record.setText("Button35")
        self.button_print_record.setToolTip("Print This Schedule")
        self.button_print_record.setGeometry(422, 1, 38, 32)

        self.button_print_record.clicked.connect(self.ButtonPrintRecord_Click)

        self.button_delete_schedule = QPushButton(self.central_widget)
        self.button_delete_schedule.setObjectName("ButtonDeleteSchedule")
        self.button_delete_schedule.setText("Button36")
        self.button_delete_schedule.setGeometry(470, 1, 38, 32)

        self.button_delete_schedule.clicked.connect(self.ButtonDeleteSchedule_Click)

        self.text_sched_songs = QLabel(self.central_widget)
        self.text_sched_songs.setObjectName("TextSchedSongs")
        self.text_sched_songs.setText("Scheduled Songs")
        self.text_sched_songs.setGeometry(250, 8, 163, 24)
        _fnt = QFont("Book Antiqua", 14)
        self.text_sched_songs.setFont(_fnt)


        self.program_i_d = QLineEdit(self.central_widget)
        self.program_i_d.setObjectName("ProgramID")
        self.program_i_d.setText("ProgramID")
        self.program_i_d.setToolTip("Auto Number generated with \\\"ADD PROGRAM\\")
        self.program_i_d.setGeometry(86, 8, 67, 2)


        self.prog_name = QLineEdit(self.central_widget)
        self.prog_name.setObjectName("ProgName")
        self.prog_name.setText("ProgName")
        self.prog_name.setToolTip("Label of Program")
        self.prog_name.setGeometry(240, 8, 221, 2)
        self.prog_name.setPlaceholderText("\\\"AstraDyne\\\" & Year(Date()) & Month(Date()) & Day(Date())")


        self.date_sched = QLineEdit(self.central_widget)
        self.date_sched.setObjectName("DateSched")
        self.date_sched.setText("DateSched")
        self.date_sched.setGeometry(125, 32, 125, 2)
        self.date_sched.setPlaceholderText("=Date() & \\\" 19:00:00\\")


        self.date_create = QLineEdit(self.central_widget)
        self.date_create.setObjectName("DateCreate")
        self.date_create.setText("DateCreate")
        self.date_create.setGeometry(336, 32, 124, 2)
        self.date_create.setPlaceholderText("=Now()")


        self.description = QLineEdit(self.central_widget)
        self.description.setObjectName("Description")
        self.description.setText("Description")
        self.description.setGeometry(96, 56, 442, 2)


        self.text28 = QLabel(self.central_widget)
        self.text28.setObjectName("Text28")
        self.text28.setText("Song to Schedule")
        self.text28.setGeometry(10, 80, 105, 16)
        self.text28.setStyleSheet("background-color: #80FF80")


        self.position_schedule = QLineEdit(self.central_widget)
        self.position_schedule.setObjectName("PositionSchedule")
        self.position_schedule.setGeometry(547, 80, 29, 16)
        self.position_schedule.setPlaceholderText("1")


        self.text31 = QLabel(self.central_widget)
        self.text31.setObjectName("Text31")
        self.text31.setText("position:")
        self.text31.setGeometry(490, 80, 54, 16)
        self.text31.setStyleSheet("background-color: #80FF80")


        self.song_combo = QComboBox(self.central_widget)
        self.song_combo.setObjectName("SongCombo")
        self.song_combo.addItems(["SongInProgramSelect"])
        self.song_combo.setGeometry(113, 82, 225, 16)
        self.song_combo.setEditable(True)


        # SubForm: ProgramsSched
        self.programs_sched = QWidget(self.central_widget)
        self.programs_sched.setObjectName("ProgramsSched")
        self.programs_sched.setProperty("sourceObject", "Form.ProgramsSched")
        self.programs_sched.setGeometry(1, 104, 651, 425)


        self.support_choose_combo = QComboBox(self.central_widget)
        self.support_choose_combo.setObjectName("SupportChooseCombo")
        self.support_choose_combo.addItems(["SupportsOfRecord"])
        self.support_choose_combo.setGeometry(401, 82, 79, 16)
        self.support_choose_combo.setEditable(True)


        self.tot_time_avg = QLineEdit(self.central_widget)
        self.tot_time_avg.setObjectName("TotTimeAvg")
        self.tot_time_avg.setText("=CalcTTime()")
        self.tot_time_avg.setGeometry(537, 31, 106, 16)


        self.label72 = QLabel(self.central_widget)
        self.label72.setObjectName("Label72")
        self.label72.setText("TotTime")
        self.label72.setGeometry(480, 31, 52, 16)
        self.label72.setStyleSheet("background-color: #80FF80")


        self.label73 = QLabel(self.central_widget)
        self.label73.setObjectName("Label73")
        self.label73.setText("real - extrapolated")
        self.label73.setGeometry(535, 13, 109, 16)
        self.label73.setStyleSheet("background-color: #80FF80")



    # --- VBA Event Handlers ---


    def ButtonAddProgram_Click(self) -> None:
        # TODO: DoCmd.GoToRecord , , A_NEWREC
        self.description.setFocus()

    def ButtonDeleteProgram_Click(self) -> None:
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20
        pass

    def ButtonDeleteSchedule_Click(self) -> None:
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20
        pass

    def ButtonPrintRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonPrintRecord_Click

        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
        # TODO: DoCmd.PrintOut A_SELECTION

        # label: Exit_ButtonPrintRecord_Click
        return

        # label: Err_ButtonPrintRecord_Click
        QMessageBox.information(self, '', str("Unknown error"))
        # VBA: Resume Exit_ButtonPrintRecord_Click

    def Form_BeforeInsert(self, Cancel: int) -> None:
        # TODO: BuildNewID Me.Name, "ProgramID"
        pass

    def Form_Open(self, Cancel: int) -> None:
        # TODO: DoCmd.MoveSize , 0, , 9500
        pass

    def ProgramID_AfterUpdate(self) -> None:
        self.Refresh()

    def SongCombo_AfterUpdate(self) -> None:
        # VBA: On Error GoTo Err_SongCombo_AfterUpdate

        Criteria: str = ""
        ArtistsOfSong: str = ""
        ArtistCriteria: str = ""
        RecordCriteria: str = ""
        MyRecords: Any = None
          # dim MyContain As Recordset,
        MyDb: Any = None
        MySchedule: Any = None
        RecordsOfSong: str = ""
        MySongs: Any = None
        MyArtists: Any = None
        MySing: Any = None
        MyWS: Any = None
        Myfile: str = ""
          # Myfile = Right(CurrentDb.TableDefs(1).Connect, Len(CurrentDb.TableDefs(1).Connect) - 10)
          # Myfile = "MusiDB.mdb"
        # TODO: Set MyWS = DBEngine.Workspaces(0)
          # Set MyDB = MyWS.OpenDatabase(Myfile)
        # TODO: Set MyDb = CurrentDb
        Criteria = "[SongID] = " + self.song_combo.currentText()
        MySchedule = MyDb.OpenRecordset("Schedule", 1)
        MySongs = MyDb.OpenRecordset("Songs", 2)
        MyArtists = MyDb.OpenRecordset("Artists", 2)
        MySing = MyDb.OpenRecordset("Sing", 2)
        MyContain = MyDb.OpenRecordset("Contain", 2)
        MyRecords = MyDb.OpenRecordset("Records", 2)

        MySongs.FindFirst(Criteria)
        MySchedule.Index = "PrimaryKey"
        MySchedule.AddNew()
        MySchedule["ProgramID"] = self.program_i_d  # **** Fill Schedule IDs
        MySchedule["Position"] = self.position_schedule
        MySing.FindFirst(Criteria)
        while not (MySing.NoMatch):
            ArtistCriteria = "[ArtistID] = " + MySing["ArtistID"]
            MyArtists.FindFirst(ArtistCriteria)
            if MyArtists["Name"] != "":
                ArtistsOfSong = ArtistsOfSong + " " + MyArtists["Name"]
            if MyArtists["Surname"] != "":
                ArtistsOfSong = ArtistsOfSong + " " + MyArtists["Surname"]
            MySing.FindNext(Criteria)
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
        # TODO: RecordsOfSong = Me.SongCombo.Column(3)
          # ********* Fill Fields with calculated contents
        MySchedule["SongID"] = self.song_combo.currentText()
        ArtistsOfSong = ArtistsOfSong.strip()
        MySchedule["Song_Artist"] = MySongs["Title"] + " * " + ArtistsOfSong[:int(79)]
        MySchedule["Record"] = RecordsOfSong.strip()[:int(79)]
        MySchedule["BPM"] = MySongs["BPM"]
        MySchedule["Year"] = MySongs["Year"]
        MySchedule.Update()
        MyRecords.Close()
        MyContain.Close()
        MySchedule.Close()
        MySongs.Close()
        MySing.Close()
        MyArtists.Close()
        self.position_schedule.setText(str(int(self.position_schedule.text() or "0") + 1))

        self.Refresh()

        # label: Exit_SongCombo_AfterUpdate
        return

        # label: Err_SongCombo_AfterUpdate
        QMessageBox.information(self, '', str("Unknown error"))
          # MsgBox Error$ & " enter program ID!"
        # VBA: Resume Exit_SongCombo_AfterUpdate

    def SupportChooseCombo_AfterUpdate(self) -> None:
        # TODO: self.song_combo.currentText().Requery()
        pass

    def CalcTTime(self) -> str:
        TotTime: datetime.datetime | None = None
        totRec: Any = None
        TotRecNull: int = 0
        sqlTxT: str = ""
        rst: Any = None
        CTT: str = ""
        CTT = ""
        if self.program_i_d is None:
            return ""

        sqlTxT = "SELECT Schedule.ProgramID, datetime.datetime.strptime(Sum(datetime.datetime.now().time() Is None if None else CDate('00:' + str(datetime.datetime.now(.time()[:int(""hh:nn"")],5))))) AS Tim, datetime.datetime.strptime(CDate(Sum(datetime.datetime.now().time() Is None if None else CDate('00:' + str(datetime.datetime.now(.time()[:int(""hh:nn"")],5)))))*(Count(TIme Is None if None else 'FulTim')+Count(TIme Is None if 'NulTim' else None))/Count(TIme Is None if None else 'FulTim')) AS AvgTim, Count(TIme Is None if None else 'FulTim') AS FullTim, Count(TIme Is None if 'NulTim' else None) AS NullTim FROM Songs INNER JOIN Schedule ON Songs.SongID = Schedule.SongID GROUP BY Schedule.ProgramID " + "HAVING ProgramID = " + self.program_i_d.text()
          # sqltxt = "SELECT IIF(Time is null,NULL,'00:' & left(format(time,""hh:nn""),5)) AS Tim " &         "FROM Songs INNER JOIN Schedule on Songs.SongID = Schedule.SongID " &         "WHERE ProgramID = " & Me.ProgramID
        # TODO: Set rst = CurrentDb.OpenRecordset(sqlTxT)
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
        CTT = rst["Tim"] + " - " + rst["AvgTim"]
        # VBA: On Error GoTo 0
        rst.Close()
          # If totRec = 0 Then Exit Function
          # CTT = TotTime & " - " & CDate(TotTime * (totRec + TotRecNull) / totRec)
        return CTT

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
    window = Programs()
    window.show()
    sys.exit(app.exec())
