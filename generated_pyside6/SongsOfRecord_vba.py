
def ButtonOpenAllSongs_Click(self) -> None:
    pass

def ButtonRemoveSong_Click(self) -> None:

    # Forms! reference: RelationsMgt.RemoveFromButton "Contain", Forms!Records![RecordID], self.SongID, "RecordHouse"
    pass

def SongCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Records![RecordID], "RecordHouse", self.SongCombo, "RecordID", "SongID", "Records", "Contain"
    pass

def SongID_DblClick(self, Cancel: int) -> None:

    GotoCriteria: str = None
    MyForm: str = None
    MyKey: str = None
    MyFirstControl: str = None

    if self.focusWidget() if self.focusWidget() else "" != "":
        MyForm = "Songs"
        MyKey = "SongID"
        MyFirstControl = "Title"

        GotoCriteria = self.focusWidget() if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm MyForm
        # DoCmd.GoToControl MyKey
        # DoCmd.FindRecord GotoCriteria
        # DoCmd.GoToControl MyFirstControl