
def AddArtistButton_Click(self) -> None:
    # VBA: On Error GoTo Err_AddArtistButton_Click

      # NewIDMgt.AddNewID "ArtistID", "FreeArtistIDs"

    MyFirstControl: str = ""

    # TODO: DoCmd.GoToRecord , , acNewRec

    MyFirstControl = "Name"

    # TODO: DoCmd.GoToControl MyFirstControl

    # label: Exit_AddArtistButton_Click
    return

    # label: Err_AddArtistButton_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_AddArtistButton_Click

def ArtistCombo_AfterUpdate(self) -> None:

    Criteria: str = ""
    MyRS: Any = None
    ActiveName: int = 0

    MyRS = self.RecordsetClone

      # Build the criteria.
    ActiveName = str(self.focusWidget()) if self.focusWidget() else ""
    Criteria = "[ArtistID]=" + ActiveName

      # Perform the search.
    MyRS.FindFirst(Criteria)

    if MyRS.NoMatch:
        QMessageBox.information(self, '', str("Not Found, Creating new record: " + ActiveName))
        # TODO: DoCmd.GoToRecord , , A_NEWREC
        self.artist_i_d = self.artist_combo
        self.Refresh()
    else:
          # Synchronize the form's record to the dynaset's record.
        self.Bookmark = MyRS.Bookmark

    self.artist_combo = ""

def ArtistID_AfterUpdate(self) -> None:
    self.Refresh()

def ButtonDeleteArtist_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonDeleteArtist_Click


    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

    # label: Exit_ButtonDeleteArtist_Click
    return

    # label: Err_ButtonDeleteArtist_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonDeleteArtist_Click

def ButtonPreviousArtist_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonPreviousArtist_Click

    # TODO: DoCmd.GoToRecord , , A_PREVIOUS

    # label: Exit_ButtonPreviousArtist_Click
    return

    # label: Err_ButtonPreviousArtist_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonPreviousArtist_Click

def Form_AfterUpdate(self) -> None:
    # TODO: self.artist_combo.Requery()
    ArtistDuplicates()

def Form_BeforeInsert(self, Cancel: int) -> None:
    # TODO: BuildNewID Me.Name, "ArtistID"
    pass

def Name_DblClick(self, Cancel: int) -> None:
    # VBA: On Error GoTo Err_Name_DblClick

    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    # label: Exit_Name_DblClick
    return

    # label: Err_Name_DblClick
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_Name_DblClick

def Surname_DblClick(self, Cancel: int) -> None:
    # VBA: On Error GoTo Err_title_dblClick

    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    # label: Exit_Button48_Click
    return

    # label: Err_title_dblClick
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_Button48_Click

def ArtistDuplicates(self) -> bool:
    qdf: Any = None
    rst: Any = None
    sqlTxT: str = ""
    # VBA: On Error Resume Next
    sqlTxT = "SELECT Count([Artists].[Name] + [Artists].[Surname]) AS Duplications, " + "[Artists].[Name] + ' ' + [Artists].[Surname] AS DuplicatedArtist " + "FROM Artists WHERE ([Artists].[Name] + [Artists].[Surname])= '" + self.name.text().strip() + self.surname.text().strip() + "' " + "GROUP BY Artists.Name + ' ' + Artists.Surname " + "HAVING (((Count([Artists].[Name] + [Artists].[Surname]))>1)) "
    # TODO: Set rst = CurrentDb.OpenRecordset(sqlTxT)
    # With rst:
    if rst.RecordCount >=  1:
        QMessageBox.information(self, '', str("the artist " + "" + "already exists"))
        ArtistDuplicates = True
    rst.Close()