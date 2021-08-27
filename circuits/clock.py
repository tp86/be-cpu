from time import time

import rx
import rx.operators as op
from metal import Pin


class AdjustableInterval:
    def __init__(self, interval=1.0) -> None:
        self._interval = interval
        self.output = Pin()
        self.output.connect(self._new_interval)
        self._last_timestamp = None

    def _set_last_timestamp(self, time):
        self._last_timestamp = time

    @property
    def _new_interval(self):
        # concatenate with single element at the beginning to avoid
        # waiting for first element at interval end
        return rx.concat(rx.of(-1), rx.interval(self.interval)).pipe(
            # ensure value is unique in order to always pass through Pin
            # even for quick changes of interval, when -1 is emitted
            # at the start
            op.map(lambda _: time()),
            op.do_action(self._set_last_timestamp),
        )

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval):
        passed = time() - self._last_timestamp
        if interval < self.interval and passed > interval:
            new_interval = self._new_interval
        else:
            new_interval = self._new_interval.pipe(
                op.delay(interval - passed)
            )
        self.output.connect(new_interval)
        self._interval = interval
