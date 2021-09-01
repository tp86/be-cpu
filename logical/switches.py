import rx.operators as op

from physical.elements import Pin


class Buffer:
    def __init__(self):
        self.ENABLE = Pin()
        self.IN = Pin()
        self.OUT = Pin()

        self.OUT.connect(
            Pin.combine_latest(self.ENABLE, self.IN).pipe(
                op.filter(lambda t: t[0]),
                op.starmap(lambda _, s: s)
            )
        )
