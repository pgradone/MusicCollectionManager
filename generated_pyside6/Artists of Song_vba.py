
    def ArtistCombo_AfterUpdate(self) -> None:

        RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.ArtistCombo, "SongID", "ArtistID", "Songs", "Sing"

    def ArtistCombo_NotInList(self, NewData: str, Response: int) -> None:

        ActiveID: int = None
        Prompt: str = None
        MyQuery: str = None
        Const MB_ICONQUESTION = 32
        Const YES = 6
        Const YES_NO = 4
        CRLF = Chr$(13)
        Prompt = "Create Artist?"
        GetText = ArtistCombo.Text
        # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  == YES:

            # like ButtonAddArtist_Click

            MyQuery = "FreeArtistsID"
            MyID = "ArtistID"
            MyFirstControl = "Name"

            # DoCmd.OpenQuery MyQuery
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            # DoCmd.Close A_QUERY, MyQuery
            # DoCmd.OpenForm "Artists"
            # DoCmd.GoToRecord A_FORM, "Artists", A_NEWREC
            # DoCmd.GoToControl MyID
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            Forms!Artists!Name = GetText
            # DoCmd.GoToControl MyFirstControl
        Forms!Songs!ArtistCombo = ""
        Forms!Songs.Refresh

    def ArtistID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyKey: str = None

        if Screen.ActiveControl != "":
            MyForm = "Artists"
            MyKey = "ArtistID"
            MyFirstControl = "Name"

            GotoCriteria = Screen.ActiveControl
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl

    def Button13_Click(self) -> None:
        pass

    def ButtonRemoveSinger_Click(self) -> None:

        RelationsMgt.RemoveFromButton "Sing", self.ArtistID, Forms!Songs![SongID], "Title"