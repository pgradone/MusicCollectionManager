# VBA Dim: Timin As Date, Counter, Secs As Double

    def BPMVal_AfterUpdate(self) -> None:
        # TODO: ResetAll
        pass

    def Form_Load(self) -> None:
        # TODO: ResetAll
        pass

    def CommandReset_Click(self) -> None:
        # TODO: ResetAll
        pass

    def Form_Timer(self) -> None:
        # TODO: Secs = Format(Time - Timin, "s")
        self.timing = Secs
        Counter = Secs * self.b_p_m_val / 60
        self.count = Counter
        # TODO: Me.BR.Left = 500 + 2000 * (Counter - Int(Counter))

    def MinusOne_Click(self) -> None:
        self.b_p_m_val = self.b_p_m_val - 1
        # TODO: DoCmd.RunCommand acCmdSave
        # TODO: ResetAll

    def PlusOne_Click(self) -> None:
        self.b_p_m_val = self.b_p_m_val + 1
        # TODO: DoCmd.RunCommand acCmdSave
        # TODO: ResetAll

    def ResetAll(self) -> None:
        # TODO: Me.BR.Left = 500
        Counter = 0
        # TODO: Timin = Time