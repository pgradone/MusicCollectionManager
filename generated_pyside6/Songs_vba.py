
    def BPM_DblClick(self, Cancel: int) -> None:

        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    def ButtonAddSong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonAddSong_Click
        # try:

            # NewIDMgt.AddNewID "SongID", "FreeSongIDs"

            MyFirstControl: str = None
            # DoCmd.GoToRecord , , acNewRec
            MyFirstControl = "Title"

            # DoCmd.GoToControl MyFirstControl

            # label: Exit_ButtonAddSong_Click

        # label: Err_ButtonAddSong_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonAddSong_Click

    def ButtonDeleteSong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDeleteSong_Click
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

            # label: Exit_ButtonDeleteSong_Click

        # label: Err_ButtonDeleteSong_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonDeleteSong_Click

    def Field37_AfterUpdate(self) -> None:

        MyDb: Any = None
        MyDb = DBEngine.Workspaces(0).Databases(0)
        MyTable = MyDb.OpenRecordset("Contain", DB_OPEN_TABLE)
        MyTable.Index = "PrimaryKey"
        MyTable.AddNew
        MyTable("SongID") = self.SongCombo
        MyTable("RecordID") = self.RecordID
        MyTable.Update
        MyTable.Close
        self.Refresh
        self.SongCombo = ""

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID self.Name, "SongID"

    def SongCombo_AfterUpdate(self) -> None:

        Criteria: str = None
        MyRS: Any = None
        ActiveName: str = None
        Prompt: str = None
        Const MB_ICONQUESTION = 32
        Const YES = 6
        Const YES_NO = 4
        CRLF = Chr$(13)

        Prompt = "Create new one?"
        MyRS = self.RecordsetClone

        # Build the criteria.
        ActiveName = Screen.ActiveControl
        Criteria = "[SongID] = " + ActiveName
        # Perform the search.
        MyRS.FindFirst Criteria

        if MyRS.NoMatch:
            Message = ActiveName + " not found" + CRLF
            if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new Song")  == YES:
                # DoCmd.GoToRecord , , A_NEWREC
                self.SongID = self.SongCombo
                self.Refresh
        else:
            # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark

        self.SongCombo = ""

    def SongID_AfterUpdate(self) -> None:
        self.Refresh

    def SongID_DblClick(self, Cancel: int) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    def Time_DblClick(self, Cancel: int) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    def Title_DblClick(self, Cancel: int) -> None:
        # VBA: On Error GoTo Err_title_dblClick
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

            # label: Exit_Button48_Click

        # label: Err_title_dblClick
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_Button48_Click

    def Year_DblClick(self, Cancel: int) -> None:
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20