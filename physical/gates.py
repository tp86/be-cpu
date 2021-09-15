from rx.operators import map as rxmap

from .elements import Pin


class _Gate:
    def combine(self, combiner, *sources):
        return Pin.combine_latest(*sources).pipe(combiner)


class And(_Gate):
    def __init__(self):
        self.A = Pin()
        self.B = Pin()
        self.C = Pin()

        self.C.connect(
            self.combine(rxmap(lambda t: t[0] and t[1]), self.A, self.B)
        )


class Or(_Gate):
    def __init__(self):
        self.A = Pin()
        self.B = Pin()
        self.C = Pin()

        self.C.connect(
            self.combine(rxmap(lambda t: t[0] or t[1]), self.A, self.B)
        )


class Not(_Gate):
    def __init__(self):
        self.A = Pin()
        self.B = Pin()

        self.B.connect(
            self.A.pipe(rxmap(lambda s: s.flip))
        )
