import rx.operators as op
from rx.subject import Subject, ReplaySubject

from physical.signals import L


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
