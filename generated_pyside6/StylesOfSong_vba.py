
    def ButtonRemoveBelong_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonRemoveBelong_Click
        # try:

            RelationsMgt.RemoveFromButton "Belong", Forms!Songs![SongID], self.StyleID, "Title"

            # label: Exit_ButtonRemoveBelong_Click

        # label: Err_ButtonRemoveBelong_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonRemoveBelong_Click

    def StyleCombo_AfterUpdate(self) -> None:

        RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.StyleCombo, "SongID", "StyleID", "Songs", "Belong"

    def StyleCombo_NotInList(self, NewData: str, Response: int) -> None:
        ActiveID: int = None
        Prompt: str = None
        MyQuery: str = None
        Const MB_ICONQUESTION = 32
        Const YES = 6
        Const YES_NO = 4
        CRLF = Chr$(13)
        Prompt = "Create New Style?"
        GetText = StyleCombo.Text
        # Debug.Print GetText

        Message = GetText + " not found" + CRLF
        if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  == YES:
            # DoCmd.OpenForm "Styles"

            # like ButtonAddStyle_Click

            MyQuery = "FreeStyleIDs"
            MyID = "StyleID"
            MyFirstControl = "Label"

            # DoCmd.OpenQuery MyQuery
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
            # DoCmd.Close A_QUERY, MyQuery
            # DoCmd.GoToRecord A_FORM, "Styles", A_NEWREC
            # DoCmd.GoToControl MyID
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
            # DoCmd.GoToControl MyFirstControl
            Forms!Styles!Label = GetText
        # DoCmd.Close A_FORM, "Styles"
        self.StyleCombo = ""
        self.Refresh

    def StyleID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyKey: str = None

        if Screen.ActiveControl != "":
            MyForm = "Styles"
            MyKey = "StyleID"
            MyFirstControl = "Label"

            GotoCriteria = Screen.ActiveControl
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl