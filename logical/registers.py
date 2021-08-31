from gates import And, Not, Or
from metal import H, L
from switches import Buffer

from circuits.latches import DFlipFlopWithClear as D


class _D_1bit:
    def __init__(self):
        d = D()
        loop_and = And()
        input_and = And()
        data_or = Or()
        input_not = Not()

        self.IE = input_and.B
        self.DI = input_and.A
        self.CLK = d.CLK
        self.CLR = d.CLR
        self.Q = d.Q

        input_not.A.connect(self.IE)
        loop_and.A.connect(self.Q)
        loop_and.B.connect(input_not.B)
        data_or.A.connect(loop_and.C)
        data_or.B.connect(input_and.C)
        d.D.connect(data_or.C)

        # initialize with low state
        # need to trigger CHANGES to be propagated through pins
        self.Q.on_next(H)
        self.Q.on_next(L)


class DType_4bit:
    def __init__(self):
        d1 = _D_1bit()
        d2 = _D_1bit()
        d3 = _D_1bit()
        d4 = _D_1bit()

        b1 = Buffer()
        b2 = Buffer()
        b3 = Buffer()
        b4 = Buffer()

        g1_not = Not()
        g2_not = Not()
        m_not = Not()
        n_not = Not()
        g_and = And()
        mn_and = And()

        self.M = m_not.A
        self.N = n_not.A
        self.G1 = g1_not.A
        self.G2 = g2_not.A
        self.D1 = d1.DI
        self.D2 = d2.DI
        self.D3 = d3.DI
        self.D4 = d4.DI
        self.CLK = d1.CLK
        self.CLR = d1.CLR
        self.Q1 = b1.OUT
        self.Q2 = b2.OUT
        self.Q3 = b3.OUT
        self.Q4 = b4.OUT

        d2.CLK.connect(self.CLK)
        d3.CLK.connect(self.CLK)
        d4.CLK.connect(self.CLK)
        d2.CLR.connect(self.CLR)
        d3.CLR.connect(self.CLR)
        d4.CLR.connect(self.CLR)
        mn_and.A.connect(m_not.B)
        mn_and.B.connect(n_not.B)
        b1.ENABLE.connect(mn_and.C)
        b2.ENABLE.connect(mn_and.C)
        b3.ENABLE.connect(mn_and.C)
        b4.ENABLE.connect(mn_and.C)
        g_and.A.connect(g1_not.B)
        g_and.B.connect(g2_not.B)
        d1.IE.connect(g_and.C)
        d2.IE.connect(g_and.C)
        d3.IE.connect(g_and.C)
        d4.IE.connect(g_and.C)
        b1.IN.connect(d1.Q)
        b2.IN.connect(d2.Q)
        b3.IN.connect(d3.Q)
        b4.IN.connect(d4.Q)
