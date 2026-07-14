
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
    Criteria = "[SongID] = " + self.song_combo
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
    MySchedule["SongID"] = self.song_combo
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
    self.position_schedule = self.position_schedule + 1
    self.Refresh()

    # label: Exit_SongCombo_AfterUpdate
    return

    # label: Err_SongCombo_AfterUpdate
    QMessageBox.information(self, '', str("Unknown error"))
      # MsgBox Error$ & " enter program ID!"
    # VBA: Resume Exit_SongCombo_AfterUpdate

def SupportChooseCombo_AfterUpdate(self) -> None:
    # TODO: self.song_combo.Requery()
    pass

def CalcTTime(self) -> str:
    TotTime: datetime.datetime = None
    totRec: Any = None
    TotRecNull: int = 0
    sqlTxT: str = ""
    rst: Any = None
    CTT: str = ""
    CTT = ""
    if self.program_i_d is None:
        return
    sqlTxT = "SELECT Schedule.ProgramID, datetime.datetime.strptime(Sum(datetime.datetime.now().time() Is None if None else CDate('00:' + str(datetime.datetime.now(.time()[:int(""hh:nn"")],5))))) AS Tim, datetime.datetime.strptime(CDate(Sum(datetime.datetime.now().time() Is None if None else CDate('00:' + str(datetime.datetime.now(.time()[:int(""hh:nn"")],5)))))*(Count(TIme Is None if None else 'FulTim')+Count(TIme Is None if 'NulTim' else None))/Count(TIme Is None if None else 'FulTim')) AS AvgTim, Count(TIme Is None if None else 'FulTim') AS FullTim, Count(TIme Is None if 'NulTim' else None) AS NullTim FROM Songs INNER JOIN Schedule ON Songs.SongID = Schedule.SongID GROUP BY Schedule.ProgramID " + "HAVING ProgramID = " + self.program_i_d
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
    CalcTTime = CTT