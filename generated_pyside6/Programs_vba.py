
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