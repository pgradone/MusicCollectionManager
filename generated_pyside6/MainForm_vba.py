
    def Button_OpenQuery_Rec_Click(self) -> None:
        # VBA: On Error GoTo Err_Button_OpenQuery_Rec_Click
        # try:

            QueryName: str = None
            LinkCriteria: str = None

            QueryName = "Records_Songs_Artists"
            # DoCmd.OpenQuery QueryName

            # label: Exit_Button_OpenQuery_Rec_Click

        # label: Err_Button_OpenQuery_Rec_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_Button_OpenQuery_Rec_Click

    def ButtonOpenArtists_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonOpenArtists_Click
        # try:

            DocName: str = None
            LinkCriteria: str = None

            DocName = "Artists"
            # DoCmd.OpenForm DocName, , , LinkCriteria

            # label: Exit_ButtonOpenArtists_Click

        # label: Err_ButtonOpenArtists_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonOpenArtists_Click

    def ButtonOpenPrograms_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonOpenPrograms_Click
        # try:

            DocName: str = None
            LinkCriteria: str = None

            DocName = "Programs"
            # DoCmd.OpenForm DocName, , , LinkCriteria
            # DoCmd.GoToRecord , "", acLast
            # DoCmd.MoveSize 0, 0

            # label: Exit_ButtonOpenPrograms_Click

        # label: Err_ButtonOpenPrograms_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonOpenPrograms_Click

    def ButtonOpenRecords_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonOpenRecords_Click
        # try:

            DocName: str = None
            LinkCriteria: str = None

            DocName = "Records"
            # DoCmd.OpenForm DocName, , , LinkCriteria

            # label: Exit_ButtonOpenRecords_Click

        # label: Err_ButtonOpenRecords_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonOpenRecords_Click

    def ButtonOpenSongs_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonOpenSongs_Click
        # try:

            DocName: str = None
            LinkCriteria: str = None

            DocName = "Songs"
            # DoCmd.OpenForm DocName, , , LinkCriteria

            # label: Exit_ButtonOpenSongs_Click

        # label: Err_ButtonOpenSongs_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonOpenSongs_Click

    def ButtonOpenStyles_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonOpenStyles_Click
        # try:

            DocName: str = None
            LinkCriteria: str = None

            DocName = "Styles"
            # DoCmd.OpenForm DocName, , , LinkCriteria

            # label: Exit_ButtonOpenStyles_Click

        # label: Err_ButtonOpenStyles_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonOpenStyles_Click

    def ButtonQuitApplicatio_Click(self) -> None:
        # VBA: On Error GoTo Err_ButtonQuitApplicatio_Click
        # try:

            # DoCmd.Close 

            # label: Exit_ButtonQuitApplicatio_Click

        # label: Err_ButtonQuitApplicatio_Click
        QMessageBox.information(self, '', str(E))
        # VBA: Resume Exit_ButtonQuitApplicatio_Click