from circuits.clock import Pulse
from metal import H, L, Pin
from gates import And, Nor, Not


class SR:
    def __init__(self) -> None:
        s_nor = Nor()
        r_nor = Nor()

        self.S = s_nor.A
        self.R = r_nor.A
        self.Q = r_nor.C
        self.Q_ = s_nor.C

        s_nor.B.connect(r_nor.C)
        r_nor.B.connect(s_nor.C)

        # initialize in reset state
        self.Q.on_next(L)
        self.Q_.on_next(H)


class SREnable:
    def __init__(self):
        sr = SR()
        s_and = And()
        r_and = And()

        self.R = Pin()
        self.EN = Pin()
        self.S = Pin()

        self.Q = sr.Q
        self.Q_ = sr.Q_

        sr.R.connect(r_and.C)
        sr.S.connect(s_and.C)
        r_and.A.connect(self.R)
        s_and.A.connect(self.S)
        r_and.B.connect(self.EN)
        s_and.B.connect(self.EN)


class D:
    def __init__(self) -> None:
        sre = SREnable()
        notGate = Not()

        self.D = sre.S
        self.EN = sre.EN
        self.Q = sre.Q
        self.Q_ = sre.Q_

        sre.R.connect(notGate.B)
        notGate.A.connect(sre.S)
