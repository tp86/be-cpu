import rx
import rx.operators as op
from rx.subject import Subject

from metal import H, L, Pin


class Switch:
    def __init__(self):

        self.IN1 = Pin()
        self.IN2 = Pin()
        self.OUT = Pin()

        self._sw = Subject()

        self.OUT.connect(
            rx.combine_latest(self._sw, self.IN1, self.IN2).pipe(
                op.starmap(lambda sw, in1, in2: in1 if sw else in2)
            )
        )

        # initialize in turned off state
        self.off()

    def on(self):
        self._sw.on_next(H)

    def off(self):
        self._sw.on_next(L)
