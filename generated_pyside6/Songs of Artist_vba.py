
def Button23_Click(self) -> None:

    MyDb: Any = None
    MyTable: Any = None
    MyQuery: Any = None
    # TODO: Set MyDb = DBEngine.Workspaces(0).Databases(0)
    MyTable = MyDb.OpenRecordset("Sing", 1)

    MyTable.Index = "PrimaryKey"
    # Forms! reference: MyTable.Seek "=", Forms!Employees![EmployeeID], self.company_i_d

    if not MyTable.NoMatch:
        MyTable.Delete()
    MyTable.Close()
    # TODO: Forms.Artistss.Refresh()

def ButtonRemoveSong_Click(self) -> None:

    # Forms! reference: RelationsMgt.RemoveFromButton "Sing", Forms!Artists![ArtistID], self.song_i_d, "Surname"
    pass

def RecordID_DblClick(self, Cancel: int) -> None:

    FormName: str = ""
    LinkCriteria: str = ""

    FormName = "Records"
    if self.record_i_d != "":
        LinkCriteria = "[RecordID]=" + str(self.focusWidget()) if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm FormName, , , LinkCriteria

def SongCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Artists![ArtistID], "Surname", self.song_combo, "ArtistID", "SongID", "Artists", "Sing"
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