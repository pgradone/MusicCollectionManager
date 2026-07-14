
def BPM_DblClick(self, Cancel: int) -> None:

    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
    pass

def ButtonAddSong_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonAddSong_Click

      # NewIDMgt.AddNewID "SongID", "FreeSongIDs"

    MyFirstControl: str = ""
    # TODO: DoCmd.GoToRecord , , acNewRec
    MyFirstControl = "Title"

    # TODO: DoCmd.GoToControl MyFirstControl

    # label: Exit_ButtonAddSong_Click
    return

    # label: Err_ButtonAddSong_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonAddSong_Click

def ButtonDeleteSong_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonDeleteSong_Click

    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

    # label: Exit_ButtonDeleteSong_Click
    return

    # label: Err_ButtonDeleteSong_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonDeleteSong_Click

def Field37_AfterUpdate(self) -> None:

    MyDb: Any = None
    MyTable: Any = None
    # TODO: Set MyDb = DBEngine.Workspaces(0).Databases(0)
    MyTable = MyDb.OpenRecordset("Contain", 1)
    MyTable.Index = "PrimaryKey"
    MyTable.AddNew()
    MyTable["SongID"] = self.song_combo
    MyTable["RecordID"] = self.record_i_d
    MyTable.Update()
    MyTable.Close()
    self.Refresh()
    self.song_combo = ""

def Form_BeforeInsert(self, Cancel: int) -> None:
    # TODO: BuildNewID Me.Name, "SongID"
    pass

def SongCombo_AfterUpdate(self) -> None:

    Criteria: str = ""
    MyRS: Any = None
    ActiveName: str = ""
    Prompt: str = ""
    Message: str = ""
    CRLF: str = ""
    # VBA Const: MB_ICONQUESTION = 32
    # VBA Const: YES = 6
    # VBA Const: YES_NO = 4
    CRLF = chr(13)

    Prompt = "Create new one?"
    MyRS = self.RecordsetClone

      # Build the criteria.
    ActiveName = str(self.focusWidget()) if self.focusWidget() else ""
    Criteria = "[SongID] = " + ActiveName
      # Perform the search.
    MyRS.FindFirst(Criteria)

    if MyRS.NoMatch:
        Message = ActiveName + " not found" + CRLF
        if QMessageBox.question(self, "", str(Message + Prompt), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)  ==  QMessageBox.StandardButton.Yes:
            # TODO: DoCmd.GoToRecord , , A_NEWREC
            self.song_i_d = self.song_combo
            self.Refresh()
    else:
          # Synchronize the form's record to the dynaset's record.
        self.Bookmark = MyRS.Bookmark

    self.song_combo = ""

def SongID_AfterUpdate(self) -> None:
    self.Refresh()

def SongID_DblClick(self, Cancel: int) -> None:
    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
    pass

def Time_DblClick(self, Cancel: int) -> None:
    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
    pass

def Title_DblClick(self, Cancel: int) -> None:
    # VBA: On Error GoTo Err_title_dblClick

    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20

    # label: Exit_Button48_Click
    return

    # label: Err_title_dblClick
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_Button48_Click

def Year_DblClick(self, Cancel: int) -> None:
    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, 10, , A_MENU_VER20
    pass