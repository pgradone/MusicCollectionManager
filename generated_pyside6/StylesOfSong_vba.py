
def ButtonRemoveBelong_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonRemoveBelong_Click

    # Forms! reference: RelationsMgt.RemoveFromButton "Belong", Forms!Songs![SongID], self.style_i_d, "Title"

    # label: Exit_ButtonRemoveBelong_Click
    return

    # label: Err_ButtonRemoveBelong_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonRemoveBelong_Click

def StyleCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.style_combo, "SongID", "StyleID", "Songs", "Belong"
    pass

def StyleCombo_NotInList(self, NewData: str, Response: int) -> None:
    ActiveID: int = 0
    NewID: int = 0
    GetText: Any = None
    Prompt: str = ""
    Message: str = ""
    CRLF: str = ""
    ActiveName: str = ""
    MyQuery: str = ""
    MyID: str = ""
    MyFirstControl: str = ""
    # VBA Const: MB_ICONQUESTION = 32
    # VBA Const: YES = 6
    # VBA Const: YES_NO = 4
    CRLF = chr(13)
    Prompt = "Create New Style?"
    GetText = StyleCombo.text()
      # Debug.Print GetText

    Message = GetText + " not found" + CRLF
    if QMessageBox.question(self, "", str(Message + Prompt), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)  ==  QMessageBox.StandardButton.Yes:
        # TODO: DoCmd.OpenForm "Styles"

          # like ButtonAddStyle_Click

        MyQuery = "FreeStyleIDs"
        MyID = "StyleID"
        MyFirstControl = "Label"

        # TODO: DoCmd.OpenQuery MyQuery
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
        # TODO: DoCmd.Close A_QUERY, MyQuery
        # TODO: DoCmd.GoToRecord A_FORM, "Styles", A_NEWREC
        # TODO: DoCmd.GoToControl MyID
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
        # TODO: DoCmd.GoToControl MyFirstControl
        # Forms! reference: Forms!Styles!Label = GetText
    # TODO: DoCmd.Close A_FORM, "Styles"
    self.style_combo = ""
    self.Refresh()

def StyleID_DblClick(self, Cancel: int) -> None:

    GotoCriteria: str = ""
    MyForm: str = ""
    MyKey: str = ""
    MyFirstControl: str = ""

    if str(self.focusWidget()) if self.focusWidget() else "" != "":
        MyForm = "Styles"
        MyKey = "StyleID"
        MyFirstControl = "Label"

        GotoCriteria = str(self.focusWidget()) if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm MyForm
        # TODO: DoCmd.GoToControl MyKey
        # TODO: DoCmd.FindRecord GotoCriteria
        # TODO: DoCmd.GoToControl MyFirstControl