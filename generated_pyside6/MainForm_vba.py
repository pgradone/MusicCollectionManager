
def Button_OpenQuery_Rec_Click(self) -> None:
    # VBA: On Error GoTo Err_Button_OpenQuery_Rec_Click

    QueryName: str = ""
    LinkCriteria: str = ""

    QueryName = "Records_Songs_Artists"
    # TODO: DoCmd.OpenQuery QueryName

    # label: Exit_Button_OpenQuery_Rec_Click
    return

    # label: Err_Button_OpenQuery_Rec_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_Button_OpenQuery_Rec_Click

def ButtonOpenArtists_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonOpenArtists_Click

    DocName: str = ""
    LinkCriteria: str = ""

    DocName = "Artists"
    # TODO: DoCmd.OpenForm DocName, , , LinkCriteria

    # label: Exit_ButtonOpenArtists_Click
    return

    # label: Err_ButtonOpenArtists_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonOpenArtists_Click

def ButtonOpenPrograms_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonOpenPrograms_Click

    DocName: str = ""
    LinkCriteria: str = ""

    DocName = "Programs"
    # TODO: DoCmd.OpenForm DocName, , , LinkCriteria
    # TODO: DoCmd.GoToRecord , "", acLast
    # TODO: DoCmd.MoveSize 0, 0

    # label: Exit_ButtonOpenPrograms_Click
    return

    # label: Err_ButtonOpenPrograms_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonOpenPrograms_Click

def ButtonOpenRecords_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonOpenRecords_Click

    DocName: str = ""
    LinkCriteria: str = ""

    DocName = "Records"
    # TODO: DoCmd.OpenForm DocName, , , LinkCriteria

    # label: Exit_ButtonOpenRecords_Click
    return

    # label: Err_ButtonOpenRecords_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonOpenRecords_Click

def ButtonOpenSongs_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonOpenSongs_Click

    DocName: str = ""
    LinkCriteria: str = ""

    DocName = "Songs"
    # TODO: DoCmd.OpenForm DocName, , , LinkCriteria

    # label: Exit_ButtonOpenSongs_Click
    return

    # label: Err_ButtonOpenSongs_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonOpenSongs_Click

def ButtonOpenStyles_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonOpenStyles_Click

    DocName: str = ""
    LinkCriteria: str = ""

    DocName = "Styles"
    # TODO: DoCmd.OpenForm DocName, , , LinkCriteria

    # label: Exit_ButtonOpenStyles_Click
    return

    # label: Err_ButtonOpenStyles_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonOpenStyles_Click

def ButtonQuitApplicatio_Click(self) -> None:
    # VBA: On Error GoTo Err_ButtonQuitApplicatio_Click

    # TODO: DoCmd.Close

    # label: Exit_ButtonQuitApplicatio_Click
    return

    # label: Err_ButtonQuitApplicatio_Click
    QMessageBox.information(self, '', str("Unknown error"))
    # VBA: Resume Exit_ButtonQuitApplicatio_Click