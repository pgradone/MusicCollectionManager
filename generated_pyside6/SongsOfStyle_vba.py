
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

    # Forms! reference: RelationsMgt.RemoveFromButton "Belong", self.song_i_d, Forms!Styles![StyleID], "Label"

      # Dim MyDB As DATABASE, MyTable As Recordset, MyQuery As QueryDef
      # Set MyDB = DBEngine.Workspaces(0).Databases(0)
      # Set MyTable = MyDB.OpenRecordset("Sing", DB_OPEN_TABLE)

      # MyTable.Index = "PrimaryKey"
      # MyTable.Seek "=", Forms!Artists![ArtistID], Me![SongID]

      # If Not MyTable.NoMatch Then
      # MyTable.Delete
      # End If
      # MyTable.Close
      # Forms.Artists.Refresh
    pass

def RecordID_DblClick(self, Cancel: int) -> None:

    FormName: str = ""
    LinkCriteria: str = ""

    FormName = "Records"
    if self.record_i_d != "":
        LinkCriteria = "[RecordID]=" + str(self.focusWidget()) if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm FormName, , , LinkCriteria

def SongCombo_AfterUpdate(self) -> None:

    # Forms! reference: RelationsMgt.AddFromCombo Forms!Styles![StyleID], "Label", self.song_combo, "StyleID", "SongID", "Styles", "Belong"
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