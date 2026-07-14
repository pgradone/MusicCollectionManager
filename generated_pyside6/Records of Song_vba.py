
def ButtonRemoveRecord_Click(self) -> None:

    # Forms! reference: RelationsMgt.RemoveFromButton "Contain", self.record_i_d, Forms!Songs![SongID], "BPM"
    pass

def RecordCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "BPM", self.record_combo, "SongID", "RecordID", "Songs", "Contain"
    pass

def RecordCombo_NotInList(self, NewData: str, Response: int) -> None:

    ActiveID: int = 0
    NewID: int = 0
    GetText: Any = None
    Prompt: str = ""
    Message: str = ""
    CRLF: str = ""
    ActiveName: str = ""
    MyQuery: str = ""
    MyForm: str = ""
    MyID: str = ""
    MyFirstControl: str = ""
    # VBA Const: MB_ICONQUESTION = 32
    # VBA Const: YES = 6
    # VBA Const: YES_NO = 4
    CRLF = chr(13)
    Prompt = "Create Record?"
    GetText = RecordCombo.text()
      # Debug.Print GetText

    Message = GetText + " not found" + CRLF
    if QMessageBox.question(self, "", str(Message + Prompt), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)  ==  QMessageBox.StandardButton.Yes:

          # like ButtonAddRecord_Click

        MyQuery = "FreeRecordIDs"
        MyForm = "Records"
        MyID = "RecordID"
        MyFirstControl = "Title"

        # TODO: DoCmd.OpenQuery MyQuery
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
        # TODO: DoCmd.Close A_QUERY, MyQuery
        # TODO: DoCmd.OpenForm MyForm
        # TODO: DoCmd.GoToRecord A_FORM, MyForm, A_NEWREC
        # TODO: DoCmd.GoToControl MyID
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
        # Forms! reference: Forms!Artists!Name = GetText
        # TODO: DoCmd.GoToControl MyFirstControl
    # Forms! reference: Forms!Songs!ArtistCombo = ""
    # Forms! reference: Forms!Songs.Refresh

def RecordID_DblClick(self, Cancel: int) -> None:

    GotoCriteria: str = ""
    MyForm: str = ""
    MyKey: str = ""
    MyFirstControl: str = ""

    if str(self.focusWidget()) if self.focusWidget() else "" != "":
        MyForm = "Records"
        MyKey = "RecordID"
        MyFirstControl = "Title"

        GotoCriteria = str(self.focusWidget()) if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm MyForm
        # TODO: DoCmd.GoToControl MyKey
        # TODO: DoCmd.FindRecord GotoCriteria
        # TODO: DoCmd.GoToControl MyFirstControl