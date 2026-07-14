
    def ButtonRemoveRecord_Click(self) -> None:

        RelationsMgt.RemoveFromButton "Contain", self.RecordID, Forms!Songs![SongID], "BPM"

    def RecordCombo_AfterUpdate(self) -> None:

        RelationsMgt.AddFromCombo Forms!Songs![SongID], "BPM", self.RecordCombo, "SongID", "RecordID", "Songs", "Contain"

    def RecordCombo_NotInList(self, NewData: str, Response: int) -> None:

        ActiveID: int = None
        Prompt: str = None
        MyQuery: str = None
        Const MB_ICONQUESTION = 32
        Const YES = 6
        Const YES_NO = 4
        CRLF = Chr$(13)
        Prompt = "Create Record?"
        GetText = RecordCombo.Text
        # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  == YES:

            # like ButtonAddRecord_Click

            MyQuery = "FreeRecordIDs"
            MyForm = "Records"
            MyID = "RecordID"
            MyFirstControl = "Title"

            # DoCmd.OpenQuery MyQuery
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            # DoCmd.Close A_QUERY, MyQuery
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToRecord A_FORM, MyForm, A_NEWREC
            # DoCmd.GoToControl MyID
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            Forms!Artists!Name = GetText
            # DoCmd.GoToControl MyFirstControl
        Forms!Songs!ArtistCombo = ""
        Forms!Songs.Refresh

    def RecordID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyKey: str = None

        if Screen.ActiveControl != "":
            MyForm = "Records"
            MyKey = "RecordID"
            MyFirstControl = "Title"

            GotoCriteria = Screen.ActiveControl
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl