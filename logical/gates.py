from physical.gates import And, Not, Or


class Nand:
    def __init__(self):
        andGate = And()
        notGate = Not()

        self.A = andGate.A
        self.B = andGate.B
        self.C = notGate.B

        notGate.A.connect(andGate.C)


class Nor:
    def __init__(self):
        orGate = Or()
        notGate = Not()

        self.A = orGate.A
        self.B = orGate.B
        self.C = notGate.B

        notGate.A.connect(orGate.C)
