
def ButtonAddStyle_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonAddStyle_Click

    # TODO: NewIDMgt.AddNewID "StyleID", "FreeStyleIDs"

    MyFirstControl: str = ""
    MyFirstControl = "Label"

    # TODO: DoCmd.GoToControl MyFirstControl

    # label: Exit_ButtonAddStyle_Click
    return

    # label: Err_ButtonAddStyle_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonAddStyle_Click

def ButtonDeleteStyle_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonDeleteStyle_Click


    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_SELECTRECORD_V2, , A_MENU_VER20
    # TODO: DoCmd.DoMenuItem A_FORMBAR, A_EDITMENU, A_DELETE_V2, , A_MENU_VER20

    # label: Exit_ButtonDeleteStyle_Click
    return

    # label: Err_ButtonDeleteStyle_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonDeleteStyle_Click

def Form_BeforeInsert(self, Cancel: int) -> None:
    # TODO: BuildNewID Me.Name, "StyleID"
    pass

def MusicStyleCombo_AfterUpdate(self) -> None:
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
    Criteria = "[StyleID] = " + ActiveName
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