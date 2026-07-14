
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