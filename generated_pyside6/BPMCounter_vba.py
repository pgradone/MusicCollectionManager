
    def BPMVal_AfterUpdate(self) -> None:
        ResetAll

    def Form_Load(self) -> None:
        ResetAll

    def CommandReset_Click(self) -> None:
        ResetAll

    def Form_Timer(self) -> None:
        Secs = str(datetime.datetime.now().time() - Timin)
        self.Timing = Secs
        Counter = Secs * self.BPMVal / 60
        self.Count = Counter
        self.BR.Left = 500 + 2000 * (Counter - Int(Counter))

    def MinusOne_Click(self) -> None:
        self.BPMVal = self.BPMVal - 1
        # DoCmd.RunCommand acCmdSave
        ResetAll

    def PlusOne_Click(self) -> None:
        self.BPMVal = self.BPMVal + 1
        # DoCmd.RunCommand acCmdSave
        ResetAll

    def ResetAll(self) -> None:
        self.BR.Left = 500
        Counter = 0
        Timin = datetime.datetime.now().time()