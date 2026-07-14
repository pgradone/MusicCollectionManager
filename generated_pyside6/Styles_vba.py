
    def ButtonAddStyle_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonAddStyle_Click
        # try:

            NewIDMgt.AddNewID "StyleID", "FreeStyleIDs"

            MyFirstControl: str = None
            MyFirstControl = "Label"

            # DoCmd.GoToControl MyFirstControl

            # label: Exit_ButtonAddStyle_Click

        # label: Err_ButtonAddStyle_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonAddStyle_Click

    def ButtonDeleteStyle_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDeleteStyle_Click
        # try:


            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

            # label: Exit_ButtonDeleteStyle_Click

        # label: Err_ButtonDeleteStyle_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonDeleteStyle_Click

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID self.Name, "StyleID"

    def MusicStyleCombo_AfterUpdate(self) -> None:
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
        Criteria = "[StyleID] = " + ActiveName
        # Perform the search.
        MyRS.FindFirst Criteria

        if MyRS.NoMatch:
            Message = ActiveName + " not found" + CRLF
            if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new Style")  == YES:
                # DoCmd.GoToRecord , , A_NEWREC
                self.SongID = self.SongCombo
                self.Refresh
        else:
            # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark