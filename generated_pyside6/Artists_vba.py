
    def AddArtistButton_Click(self) -> None:
        # VBA: On Error GoTo Err_AddArtistButton_Click
        # try:

            # NewIDMgt.AddNewID "ArtistID", "FreeArtistIDs"

            MyFirstControl: str = None

            # DoCmd.GoToRecord , , acNewRec

            MyFirstControl = "Name"

            # DoCmd.GoToControl MyFirstControl

            # label: Exit_AddArtistButton_Click

        # label: Err_AddArtistButton_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_AddArtistButton_Click

    def ArtistCombo_AfterUpdate(self) -> None:

        Criteria: str = None
        MyRS: Any = None
        ActiveName: int = None

        MyRS = self.RecordsetClone

        # Build the criteria.
        ActiveName = Screen.ActiveControl
        Criteria = "[ArtistID]=" + ActiveName

        # Perform the search.
        MyRS.FindFirst Criteria

        if MyRS.NoMatch:
            QMessageBox.information(self, '', str("))
            # DoCmd.GoToRecord , , A_NEWREC
            self.ArtistID = self.ArtistCombo
            self.Refresh
        else:
            # Synchronize the form's record to the dynaset's record.
            self.Bookmark = MyRS.Bookmark

        self.ArtistCombo = ""

    def ArtistID_AfterUpdate(self) -> None:
        self.Refresh

    def ButtonDeleteArtist_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonDeleteArtist_Click
        # try:


            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

            # label: Exit_ButtonDeleteArtist_Click

        # label: Err_ButtonDeleteArtist_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonDeleteArtist_Click

    def ButtonPreviousArtist_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonPreviousArtist_Click
        # try:

            # DoCmd.GoToRecord , , A_PREVIOUS

            # label: Exit_ButtonPreviousArtist_Click

        # label: Err_ButtonPreviousArtist_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonPreviousArtist_Click

    def Form_AfterUpdate(self) -> None:
        self.ArtistCombo.Requery
        ArtistDuplicates

    def Form_BeforeInsert(self, Cancel: int) -> None:
        BuildNewID self.Name, "ArtistID"

    def Name_DblClick(self, Cancel: int) -> None:
        # VBA: On Error GoTo Err_Name_DblClick
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

            # label: Exit_Name_DblClick

        # label: Err_Name_DblClick
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_Name_DblClick

    def Surname_DblClick(self, Cancel: int) -> None:
        # VBA: On Error GoTo Err_title_dblClick
        # try:

            # DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

            # label: Exit_Button48_Click

        # label: Err_title_dblClick
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_Button48_Click

    def ArtistDuplicates(self) -> bool:
        qdf: Any = None
        # VBA: On Error Resume Next
        # try:
            sqlTxT = "SELECT Count([Artists].[Name] + [Artists].[Surname]) AS Duplications, " + "[Artists].[Name] + ' ' + [Artists].[Surname] AS DuplicatedArtist " + "FROM Artists WHERE ([Artists].[Name] + [Artists].[Surname])= '" + self.Name.strip() + self.Surname.strip() + "' " + "GROUP BY Artists.Name + ' ' + Artists.Surname " + "HAVING (((Count([Artists].[Name] + [Artists].[Surname]))>1)) "
            rst = CurrentDb.OpenRecordset(sqlTxT)
            # With rst:
                if .RecordCount > == 1:
                    QMessageBox.information(self, '', str("))
                    ArtistDuplicates = True
                rst.Close