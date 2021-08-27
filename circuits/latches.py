from gates import Nor


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
        self.Q.on_next(False)
        self.Q_.on_next(True)
