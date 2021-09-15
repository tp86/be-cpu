from rx.operators import filter as rxfilter, starmap

from physical.elements import Pin
from .gates import And, Not


class Buffer:
    def __init__(self):
        self.ENABLE = Pin()
        self.IN = Pin()
        self.OUT = Pin()

        self.OUT.connect(
            Pin.combine_latest(self.ENABLE, self.IN).pipe(
                rxfilter(lambda t: t[0]),
                starmap(lambda _, s: s)
            )
        )


class _BusTranceiver_1bit:
    def __init__(self) -> None:
        a_buf = Buffer()
        b_buf = Buffer()

        self.A = b_buf.OUT
        self.B = a_buf.OUT
        a_buf.IN.connect(b_buf.OUT)
        b_buf.IN.connect(a_buf.OUT)

        a_and = And()
        b_and = And()
        a_buf.ENABLE.connect(a_and.C)
        b_buf.ENABLE.connect(b_and.C)
        self.DIR = a_and.B
        en_a_not = Not()
        en_b_not = Not()
        dir_b_not = Not()
        b_and.B.connect(dir_b_not.B)
        b_and.A.connect(en_b_not.B)
        a_and.A.connect(en_a_not.B)
        dir_b_not.A.connect(self.DIR)
        self.EN_ = en_a_not.A
        en_b_not.A.connect(self.EN_)
