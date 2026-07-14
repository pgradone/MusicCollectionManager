
def Button23_Click(self) -> None:

    MyDb: Any = None
    MyTable: Any = None
    MyQuery: Any = None
    MyDb = DBEngine.Workspaces(0).Databases(0)
    MyTable = MyDb.OpenRecordset("Sing", DB_OPEN_TABLE)

    MyTable.Index = "PrimaryKey"
    # Forms! reference: MyTable.Seek "=", Forms!Employees![EmployeeID], self.CompanyID

    if not MyTable.NoMatch:
        MyTable.Delete()
    MyTable.Close()
    Forms.Artistss.Refresh()

def ButtonRemoveSong_Click(self) -> None:

    # Forms! reference: RelationsMgt.RemoveFromButton "Sing", Forms!Artists![ArtistID], self.SongID, "Surname"
    pass

def RecordID_DblClick(self, Cancel: int) -> None:

    FormName: str = None
    LinkCriteria: str = None

    FormName = "Records"
    if self.RecordID != "":
        LinkCriteria = "[RecordID]=" + self.focusWidget() if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm FormName, , , LinkCriteria

def SongCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Artists![ArtistID], "Surname", self.SongCombo, "ArtistID", "SongID", "Artists", "Sing"
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