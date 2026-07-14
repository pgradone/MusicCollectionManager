
    def ArtistID_DblClick(self, Cancel: int) -> None:
        GotoCriteria: str = None
        MyKey: str = None

        if Screen.ActiveControl != "":
            MyForm = "Artists"
            MyKey = "ArtistID"
            MyFirstControl = "Name"

            GotoCriteria = Screen.ActiveControl
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl

    def ButtonAddRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonAddRecord_Click
        # try:

            NewIDMgt.AddNewID "RecordID", "FreeRecordIDs"

            MyFirstControl: str = None
            MyFirstControl = "Title"

            # DoCmd.GoToControl MyFirstControl

            # label: Exit_ButtonAddRecord_Click

        # label: Err_ButtonAddRecord_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonAddRecord_Click

    def ButtonDelRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDelRecord_Click
        # try:


            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

            # label: Exit_ButtonDelRecord_Click

        # label: Err_ButtonDelRecord_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonDelRecord_Click

    def ButtonFindRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonFindRecord_Click
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

            # label: Exit_ButtonFindRecord_Click

        # label: Err_ButtonFindRecord_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonFindRecord_Click

    def ButtonPrintRecord_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonPrintRecord_Click
        # try:


            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
            # DoCmd.PrintOut A_SELECTION

            # label: Exit_ButtonPrintRecord_Click

        # label: Err_ButtonPrintRecord_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonPrintRecord_Click

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID self.Name, "RecordID"

    def Form_Current(self) -> None:
        self.Refresh

    def List51_DblClick(self, Cancel: int) -> None:

        GotoCriteria: str = None
        MyKey: str = None

        if Screen.ActiveControl != "":
            MyForm = "Artists"
            MyKey = "ArtistID"
            MyFirstControl = "Name"

            GotoCriteria = Screen.ActiveControl
            # DoCmd.OpenForm MyForm
            # DoCmd.GoToControl MyKey
            # DoCmd.FindRecord GotoCriteria
            # DoCmd.GoToControl MyFirstControl

    def RecordCombo_AfterUpdate(self) -> None:

        Criteria: str = None
        MyRS: Any = None
        ActiveName: int = None

        MyRS = self.RecordsetClone

        # Build the criteria.
        ActiveName = Screen.ActiveControl
        Criteria = "[RecordID]=" + ActiveName

        # Perform the search.
        MyRS.FindFirst Criteria

        if MyRS.NoMatch:
            QMessageBox.information(self, '', str("))
            # DoCmd.GoToRecord , , A_NEWREC
            self.RecordID = self.RecordCombo
            self.Refresh
        else:
            # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark

        self.RecordCombo = ""

    def RecordID_AfterUpdate(self) -> None:
        self.Refresh

    def SongView_AfterUpdate(self) -> None:

        ActiveValue: str = None

        ActiveValue = Screen.ActiveControl
        if ActiveValue = "Form":
            self.SongsInRecord.SourceObject = "Songs"
        if ActiveValue = "Tabular":
            self.SongsInRecord.SourceObject = "SongsOfRecord"

    def Title_DblClick(self, Cancel: int) -> None:

        # VBA: On Error GoTo Err_title_dblClick
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

            # label: Exit_Button48_Click

        # label: Err_title_dblClick
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_Button48_Click