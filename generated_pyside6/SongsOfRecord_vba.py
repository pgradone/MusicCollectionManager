
def ButtonOpenAllSongs_Click(self) -> None:
    pass

def ButtonRemoveSong_Click(self) -> None:

    # Forms! reference: RelationsMgt.RemoveFromButton "Contain", Forms!Records![RecordID], self.song_i_d, "RecordHouse"
    pass

def SongCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Records![RecordID], "RecordHouse", self.song_combo, "RecordID", "SongID", "Records", "Contain"
    pass

def SongID_DblClick(self, Cancel: int) -> None:

    GotoCriteria: str = ""
    MyForm: str = ""
    MyKey: str = ""
    MyFirstControl: str = ""

    if str(self.focusWidget()) if self.focusWidget() else "" != "":
        MyForm = "Songs"
        MyKey = "SongID"
        MyFirstControl = "Title"

        GotoCriteria = str(self.focusWidget()) if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm MyForm
        # TODO: DoCmd.GoToControl MyKey
        # TODO: DoCmd.FindRecord GotoCriteria
        # TODO: DoCmd.GoToControl MyFirstControl