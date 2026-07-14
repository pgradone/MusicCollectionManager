
def ArtistCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Songs![SongID], "Title", self.ArtistCombo, "SongID", "ArtistID", "Songs", "Sing"
    pass

def ArtistCombo_NotInList(self, NewData: str, Response: int) -> None:

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
    Prompt = "Create Artist?"
    GetText = ArtistCombo.text()
      # Debug.Print GetText

    Message = GetText + " not found" + CRLF
    if MsgBox(Message + Prompt, MB_ICONQUESTION + YES_NO, "Create new?")  ==  YES:

          # like ButtonAddArtist_Click

        MyQuery = "FreeArtistsID"
        MyID = "ArtistID"
        MyFirstControl = "Name"

        # DoCmd.OpenQuery MyQuery
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_COPY
        self.close()
        import Artists
        self.sub_form = Artists.Artists()
        self.sub_form.show()
        # DoCmd.GoToRecord A_FORM, "Artists", A_NEWREC
        # DoCmd.GoToControl MyID
        # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_PASTE
        # Forms! reference: Forms!Artists!Name = GetText
        # DoCmd.GoToControl MyFirstControl
    # Forms! reference: Forms!Songs!ArtistCombo = ""
    # Forms! reference: Forms!Songs.Refresh

def ArtistID_DblClick(self, Cancel: int) -> None:

    GotoCriteria: str = None
    MyForm: str = None
    MyKey: str = None
    MyFirstControl: str = None

    if self.focusWidget() if self.focusWidget() else "" != "":
        MyForm = "Artists"
        MyKey = "ArtistID"
        MyFirstControl = "Name"

        GotoCriteria = self.focusWidget() if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm MyForm
        # DoCmd.GoToControl MyKey
        # DoCmd.FindRecord GotoCriteria
        # DoCmd.GoToControl MyFirstControl

def Button13_Click(self) -> None:
    pass

def ButtonRemoveSinger_Click(self) -> None:

    # Forms! reference: RelationsMgt.RemoveFromButton "Sing", self.ArtistID, Forms!Songs![SongID], "Title"
    pass