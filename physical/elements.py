import rx
import rx.operators as op
from rx.subject import ReplaySubject, Subject

from physical.signals import H, L


class Pin(Subject):
    """Pin is element that has one incoming connection at a time.

    Emits element only on change of incoming value
    or on new connection to pin (replay).
    """

    def __init__(self, init=L):
        super().__init__()
        self._output = ReplaySubject(1)
        super().pipe(op.distinct_until_changed()).subscribe(self._output)
        self._connection = None
        self.subscribe = self._output.subscribe
        self.pipe = self._output.pipe
        self.on_next(init)

    @property
    def is_connected(self):
        return self._connection and not self._connection.is_disposed

    def disconnect(self):
        if self.is_connected:
            self._connection.dispose()

    def connect(self, source):
        self.disconnect()
        self._connection = source.subscribe(self)

    @staticmethod
    def combine_latest(*pins):
        subjects = [ReplaySubject() for _ in pins]
        for index, pin in enumerate(pins):
            pin.subscribe(subjects[index])
        return rx.combine_latest(*subjects)


class Switch:
    def __init__(self):

        self.IN1 = Pin()
        self.IN2 = Pin()
        self.OUT = Pin()

        self._sw = Subject()

        self.OUT.connect(
            Pin.combine_latest(self._sw, self.IN1, self.IN2).pipe(
                op.starmap(lambda sw, in1, in2: in2 if sw else in1)
            )
        )

        # initialize in turned off state
        self.off()

    def on(self):
        self._sw.on_next(H)

    def off(self):
        self._sw.on_next(L)
