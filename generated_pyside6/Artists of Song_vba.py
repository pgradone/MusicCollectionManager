
def ArtistCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.artist_combo, "SongID", "ArtistID", "Songs", "Sing"
    pass

def ArtistCombo_NotInList(self, NewData: str, Response: int) -> None:

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
    Prompt = "Create Artist?"
    GetText = ArtistCombo.text()
      # Debug.Print GetText

    Message = GetText + " not found" + CRLF
    if QMessageBox.question(self, "", str(Message + Prompt), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)  ==  QMessageBox.StandardButton.Yes:

          # like ButtonAddArtist_Click

        MyQuery = "FreeArtistsID"
        MyID = "ArtistID"
        MyFirstControl = "Name"

        # TODO: DoCmd.OpenQuery MyQuery
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
        # TODO: DoCmd.Close A_QUERY, MyQuery
        # TODO: DoCmd.OpenForm "Artists"
        # TODO: DoCmd.GoToRecord A_FORM, "Artists", A_NEWREC
        # TODO: DoCmd.GoToControl MyID
        # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
        # Forms! reference: Forms!Artists!Name = GetText
        # TODO: DoCmd.GoToControl MyFirstControl
    # Forms! reference: Forms!Songs!ArtistCombo = ""
    # Forms! reference: Forms!Songs.Refresh

def ArtistID_DblClick(self, Cancel: int) -> None:

    GotoCriteria: str = ""
    MyForm: str = ""
    MyKey: str = ""
    MyFirstControl: str = ""

    if str(self.focusWidget()) if self.focusWidget() else "" != "":
        MyForm = "Artists"
        MyKey = "ArtistID"
        MyFirstControl = "Name"

        GotoCriteria = str(self.focusWidget()) if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm MyForm
        # TODO: DoCmd.GoToControl MyKey
        # TODO: DoCmd.FindRecord GotoCriteria
        # TODO: DoCmd.GoToControl MyFirstControl

def Button13_Click(self) -> None:
    pass

def ButtonRemoveSinger_Click(self) -> None:

    # Forms! reference: RelationsMgt.RemoveFromButton "Sing", self.artist_i_d, Forms!Songs![SongID], "Title"
    pass