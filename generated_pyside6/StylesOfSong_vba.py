
def ButtonRemoveBelong_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonRemoveBelong_Click

    # Forms! reference: RelationsMgt.RemoveFromButton "Belong", Forms!Songs![SongID], self.StyleID, "Title"

    # label: Exit_ButtonRemoveBelong_Click
    return

    # label: Err_ButtonRemoveBelong_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonRemoveBelong_Click

def StyleCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.StyleCombo, "SongID", "StyleID", "Songs", "Belong"
    pass

def StyleCombo_NotInList(self, NewData: str, Response: int) -> None:
    ActiveID: int = None
    NewID: int = None
    GetText: Any = None
    Prompt: str = None
    Message: str = None
    CRLF: str = None
    ActiveName: str = None
    MyQuery: str = None
    MyID: str = None
    MyFirstControl: str = None
    # VBA Const: MB_ICONQUESTION = 32
    # VBA Const: YES = 6
    # VBA Const: YES_NO = 4
    CRLF = chr(13)
    Prompt = "Create New Style?"
    GetText = StyleCombo.text()
      # Debug.Print GetText

    Message = GetText + " not found" + CRLF
    if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  ==  YES:
        import Styles
        self.sub_form = Styles.Styles()
        self.sub_form.show()

          # like ButtonAddStyle_Click

        MyQuery = "FreeStyleIDs"
        MyID = "StyleID"
        MyFirstControl = "Label"

        # DoCmd.OpenQuery MyQuery
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
        self.close()
        # DoCmd.GoToRecord A_FORM, "Styles", A_NEWREC
        # DoCmd.GoToControl MyID
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
        # DoCmd.GoToControl MyFirstControl
        # Forms! reference: Forms!Styles!Label = GetText
    self.close()
    self.StyleCombo = ""
    self.Refresh()

def StyleID_DblClick(self, Cancel: int) -> None:

    GotoCriteria: str = None
    MyForm: str = None
    MyKey: str = None
    MyFirstControl: str = None

    if self.focusWidget() if self.focusWidget() else "" != "":
        MyForm = "Styles"
        MyKey = "StyleID"
        MyFirstControl = "Label"

        GotoCriteria = self.focusWidget() if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm MyForm
        # DoCmd.GoToControl MyKey
        # DoCmd.FindRecord GotoCriteria
        # DoCmd.GoToControl MyFirstControl