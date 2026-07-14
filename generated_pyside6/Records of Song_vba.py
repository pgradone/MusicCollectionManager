
def ButtonRemoveRecord_Click(self) -> None:

    # Forms! reference: RelationsMgt.RemoveFromButton "Contain", self.RecordID, Forms!Songs![SongID], "BPM"
    pass

def RecordCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "BPM", self.RecordCombo, "SongID", "RecordID", "Songs", "Contain"
    pass

def RecordCombo_NotInList(self, NewData: str, Response: int) -> None:

    ActiveID: int = None
    NewID: int = None
    GetText: Any = None
    Prompt: str = None
    Message: str = None
    CRLF: str = None
    ActiveName: str = None
    MyQuery: str = None
    MyForm: str = None
    MyID: str = None
    MyFirstControl: str = None
    # VBA Const: MB_ICONQUESTION = 32
    # VBA Const: YES = 6
    # VBA Const: YES_NO = 4
    CRLF = chr(13)
    Prompt = "Create Record?"
    GetText = RecordCombo.text()
      # Debug.Print GetText

    Message = GetText + " not found" + CRLF
    if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  ==  YES:

          # like ButtonAddRecord_Click

        MyQuery = "FreeRecordIDs"
        MyForm = "Records"
        MyID = "RecordID"
        MyFirstControl = "Title"

        # DoCmd.OpenQuery MyQuery
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
        self.close()
        # TODO: DoCmd.OpenForm MyForm
        # DoCmd.GoToRecord A_FORM, MyForm, A_NEWREC
        # DoCmd.GoToControl MyID
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
        # Forms! reference: Forms!Artists!Name = GetText
        # DoCmd.GoToControl MyFirstControl
    # Forms! reference: Forms!Songs!ArtistCombo = ""
    # Forms! reference: Forms!Songs.Refresh

def RecordID_DblClick(self, Cancel: int) -> None:

    GotoCriteria: str = None
    MyForm: str = None
    MyKey: str = None
    MyFirstControl: str = None

    if self.focusWidget() if self.focusWidget() else "" != "":
        MyForm = "Records"
        MyKey = "RecordID"
        MyFirstControl = "Title"

        GotoCriteria = self.focusWidget() if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm MyForm
        # DoCmd.GoToControl MyKey
        # DoCmd.FindRecord GotoCriteria
        # DoCmd.GoToControl MyFirstControl