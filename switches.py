import rx
import rx.operators as op

from metal import H, L, Pin


class Buffer:
    def __init__(self):
        self.ENABLE = Pin()
        self.IN = Pin()
        self.OUT = Pin()

        self.OUT.connect(
            rx.combine_latest(self.ENABLE, self.IN).pipe(
                op.filter(lambda t: t[0]),
                op.starmap(lambda _, s: s)
            )
        )

        # initialize in disabled state
        self.ENABLE.on_next(L)
