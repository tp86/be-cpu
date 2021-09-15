from rx.operators import filter as rxfilter, starmap

from physical.elements import Pin


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
