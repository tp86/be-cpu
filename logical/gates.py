import rx
import rx.operators as op

from physical.elements import Pin


class _Gate:
    def combine(self, combiner, *sources):
        return rx.combine_latest(*sources).pipe(combiner)


class And(_Gate):
    def __init__(self):
        self.A = Pin()
        self.B = Pin()
        self.C = Pin()

        self.C.connect(
            self.combine(op.map(lambda t: t[0] and t[1]), self.A, self.B)
        )


class Or(_Gate):
    def __init__(self):
        self.A = Pin()
        self.B = Pin()
        self.C = Pin()

        self.C.connect(
            self.combine(op.map(lambda t: t[0] or t[1]), self.A, self.B)
        )


class Not(_Gate):
    def __init__(self):
        self.A = Pin()
        self.B = Pin()

        self.B.connect(
            self.A.pipe(op.map(lambda s: s.flip))
        )


class Nand(_Gate):
    def __init__(self):
        andGate = And()
        notGate = Not()

        self.A = andGate.A
        self.B = andGate.B
        self.C = notGate.B

        notGate.A.connect(andGate.C)


class Nor(_Gate):
    def __init__(self):
        orGate = Or()
        notGate = Not()

        self.A = orGate.A
        self.B = orGate.B
        self.C = notGate.B

        notGate.A.connect(orGate.C)
