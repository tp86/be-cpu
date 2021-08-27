"""Basic physical components of CPU."""

import rx.operators as op
from rx.subject import Subject


class Pin(Subject):
    """Pin is element that has one incoming connection at a time.

    Emits element only on change.
    """

    def __init__(self):
        super().__init__()
        self._output = Subject()
        super().pipe(op.distinct_until_changed()).subscribe(self._output)
        self._connection = None
        self.subscribe = self._output.subscribe
        self.pipe = self._output.pipe

    @property
    def is_connected(self):
        return self._connection and not self._connection.is_disposed

    def disconnect(self):
        if self.is_connected:
            self._connection.dispose()

    def connect(self, source):
        self.disconnect()
        self._connection = source.subscribe(self)
