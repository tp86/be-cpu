from time import time
from typing import Union

import rx
import rx.operators as op
from metal import H, L, Pin


class AdjustableInterval:
    def __init__(self, interval=1.0) -> None:
        self._interval = interval
        self.OUTPUT = Pin()
        self.OUTPUT.connect(self._new_interval)
        self._last_timestamp = None

    def _set_last_timestamp(self, _):
        self._last_timestamp = time()
        return self._last_timestamp

    @property
    def _new_interval(self):
        # concatenate with single element at the beginning to avoid
        # waiting for first element at interval end
        return rx.concat(rx.of(-1), rx.interval(self.interval)).pipe(
            # ensure value is unique in order to always pass through Pin
            # even for quick changes of interval, when -1 is emitted
            # at the start
            op.map(self._set_last_timestamp),
        )

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval):
        self._interval = interval
        passed = time() - self._last_timestamp
        if passed > interval:
            self.OUTPUT.connect(self._new_interval)
        else:
            self.OUTPUT.connect(self._new_interval.pipe(
                op.delay(interval - passed)
            ))


class Clock:
    def __init__(self) -> None:
        self.CLOCK = Pin()

        self._interval = AdjustableInterval()
        previous_signal_flipped = self.CLOCK.pipe(op.map(lambda s: s.flip))
        previous_signal_with_starter = rx.concat(
            rx.of(H), previous_signal_flipped)
        self.CLOCK.connect(
            rx.zip(self._interval.OUTPUT, previous_signal_with_starter).pipe(
                op.map(lambda t: t[1])
            )
        )

    @property
    def frequency(self):
        return 1 / (2 * self._interval.interval)

    @frequency.setter
    def frequency(self, frequency):
        self._interval.interval = 1 / (2 * frequency)


class Pulse:
    def __init__(self, edge: Union[H, L]) -> None:
        self.CLOCK = Pin()
        self.PULSE = Pin()

        self.PULSE.connect(
            self.CLOCK.pipe(
                op.filter(lambda s: s == edge),
                op.flat_map(lambda _: rx.of(edge, edge.flip))
            )
        )
