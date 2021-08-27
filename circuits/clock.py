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

    def _set_last_timestamp(self, _):
        self._last_timestamp = time()

    @property
    def _new_interval(self):
        # concatenate with single element at the beginning to avoid
        # waiting for first element at interval end
        return rx.concat(rx.of(-1), rx.interval(self.interval)).pipe(
            op.do_action(self._set_last_timestamp),
            # ensure value is unique in order to always pass through Pin
            # even for quick changes of interval, when -1 is emitted
            # at the start
            op.map(lambda _: time()),
        )

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval):
        passed = time() - self._last_timestamp
        if interval < self.interval and passed > interval:
            delay = 0.0
        else:
            delay = interval - passed
        self._interval = interval
        self.output.connect(
            self._new_interval.pipe(
                op.delay(delay)
            )
        )
