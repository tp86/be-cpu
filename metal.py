"""Basic physical components of CPU."""

from rx.subject import Subject


class Pin(Subject):
    """Pin is element that has one incoming connection at a time."""

    def __init__(self):
        super().__init__()
        self._connection = None

    @property
    def is_connected(self):
        return self._connection and not self._connection.is_disposed

    def disconnect(self):
        if self.is_connected:
            self._connection.dispose()

    def connect(self, source):
        self.disconnect()
        self._connection = source.subscribe(self)
