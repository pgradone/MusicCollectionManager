
    def Button23_Click(self) -> None:

        MyDb: Any = None
        MyDb = DBEngine.Workspaces(0).Databases(0)
        MyTable = MyDb.OpenRecordset("Sing", DB_OPEN_TABLE)

        MyTable.Index = "PrimaryKey"
        MyTable.Seek "=", Forms!Employees![EmployeeID], self.CompanyID

        if Not MyTable.NoMatch:
            MyTable.Delete
        MyTable.Close
        Forms.Artistss.Refresh

    def ButtonRemoveSong_Click(self) -> None:

        RelationsMgt.RemoveFromButton "Belong", self.SongID, Forms!Styles![StyleID], "Label"

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

    def RecordID_DblClick(self, Cancel: int) -> None:

        FormName: str = None
        LinkCriteria: str = None

        FormName = "Records"
        if self.RecordID != "":
            LinkCriteria = "[RecordID]=" + Screen.ActiveControl
            # DoCmd.OpenForm FormName, , , LinkCriteria

    def SongCombo_AfterUpdate(self) -> None:

        RelationsMgt.AddFromCombo Forms!Styles![StyleID], "Label", self.SongCombo, "StyleID", "SongID", "Styles", "Belong"

    def SongID_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyKey: str = None

        if Screen.ActiveControl != "":
            MyForm = "Songs"
            MyKey = "SongID"
            MyFirstControl = "Title"

            GotoCriteria = Screen.ActiveControl
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl