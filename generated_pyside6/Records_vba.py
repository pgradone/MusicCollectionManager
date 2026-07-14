
def ArtistID_DblClick(self, Cancel: int) -> None:
    GotoCriteria: str = ""
    MyForm: str = ""
    MyKey: str = ""
    MyFirstControl: str = ""

    if str(self.focusWidget()) if self.focusWidget() else "" != "":
        MyForm = "Artists"
        MyKey = "ArtistID"
        MyFirstControl = "Name"

        GotoCriteria = str(self.focusWidget()) if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm MyForm
        # TODO: DoCmd.GoToControl MyKey
        # TODO: DoCmd.FindRecord GotoCriteria
        # TODO: DoCmd.GoToControl MyFirstControl

def ButtonAddRecord_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonAddRecord_Click

    # TODO: NewIDMgt.AddNewID "RecordID", "FreeRecordIDs"

    MyFirstControl: str = ""
    MyFirstControl = "Title"

    # TODO: DoCmd.GoToControl MyFirstControl

    # label: Exit_ButtonAddRecord_Click
    return

    # label: Err_ButtonAddRecord_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonAddRecord_Click

def ButtonDelRecord_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonDelRecord_Click


    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

    # label: Exit_ButtonDelRecord_Click
    return

    # label: Err_ButtonDelRecord_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonDelRecord_Click

def ButtonFindRecord_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonFindRecord_Click

    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    # label: Exit_ButtonFindRecord_Click
    return

    # label: Err_ButtonFindRecord_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonFindRecord_Click

def ButtonPrintRecord_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonPrintRecord_Click


    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
    # TODO: DoCmd.PrintOut A_SELECTION

    # label: Exit_ButtonPrintRecord_Click
    return

    # label: Err_ButtonPrintRecord_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonPrintRecord_Click

def Form_BeforeInsert(self, Cancel: int) -> None:
    # TODO: BuildNewID Me.Name, "RecordID"
    pass

def Form_Current(self) -> None:
    self.Refresh()

def List51_DblClick(self, Cancel: int) -> None:

    GotoCriteria: str = ""
    MyForm: str = ""
    MyKey: str = ""
    MyFirstControl: str = ""

    if str(self.focusWidget()) if self.focusWidget() else "" != "":
        MyForm = "Artists"
        MyKey = "ArtistID"
        MyFirstControl = "Name"

        GotoCriteria = str(self.focusWidget()) if self.focusWidget() else ""
        # TODO: DoCmd.OpenForm MyForm
        # TODO: DoCmd.GoToControl MyKey
        # TODO: DoCmd.FindRecord GotoCriteria
        # TODO: DoCmd.GoToControl MyFirstControl

def RecordCombo_AfterUpdate(self) -> None:

    Criteria: str = ""
    MyRS: Any = None
    ActiveName: int = 0

    MyRS = self.RecordsetClone

      # Build the criteria.
    ActiveName = str(self.focusWidget()) if self.focusWidget() else ""
    Criteria = "[RecordID]=" + ActiveName

      # Perform the search.
    MyRS.FindFirst(Criteria)

    if MyRS.NoMatch:
        QMessageBox.information(self, '', str("Not Found, Creating new record: " + ActiveName))
        # TODO: DoCmd.GoToRecord , , A_NEWREC
        self.record_i_d = self.record_combo
        self.Refresh()
    else:
          # Synchronize the form's record to the dynaset's record.
        self.Bookmark = MyRS.Bookmark

    self.record_combo = ""

def RecordID_AfterUpdate(self) -> None:
    self.Refresh()

def SongView_AfterUpdate(self) -> None:

    ActiveValue: str = ""

    ActiveValue = str(self.focusWidget()) if self.focusWidget() else ""
    if ActiveValue  ==  "Form":
        pass
        # TODO: Me![SongsInRecord].SourceObject = "Songs"
    if ActiveValue  ==  "Tabular":
        pass
        # TODO: Me![SongsInRecord].SourceObject = "SongsOfRecord"

def Title_DblClick(self, Cancel: int) -> None:

    # VBA: On Error GoTo Err_title_dblClick

    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    # label: Exit_Button48_Click
    return

    # label: Err_title_dblClick
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_Button48_Click