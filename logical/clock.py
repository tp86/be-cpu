from time import time
from typing import Union
from math import inf

import rx
import rx.operators as op
from physical.elements import Pin
from physical.signals import H, L


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
        passed = time() - self._last_timestamp if self._last_timestamp else inf
        if passed > interval:
            self.OUTPUT.connect(self._new_interval)
        else:
            self.OUTPUT.connect(self._new_interval.pipe(
                op.delay(interval - passed)
            ))


class Clock:
    def __init__(self, frequency=1) -> None:
        self.CLOCK = Pin()

        self._interval = AdjustableInterval(self._freq2period(frequency))
        previous_signal_flipped = self.CLOCK.pipe(op.map(lambda s: s.flip))
        self.CLOCK.connect(
            rx.zip(self._interval.OUTPUT, previous_signal_flipped).pipe(
                op.map(lambda t: t[1])
            )
        )

    def _freq2period(self, frequency):
        return 1 / (2 * frequency)

    @property
    def frequency(self):
        return self._freq2period(self._interval.interval)

    @frequency.setter
    def frequency(self, frequency):
        self._interval.interval = self._freq2period(frequency)


class Pulse:
    def __init__(self, edge: Union[H, L] = H) -> None:
        self.CLOCK = Pin()
        self.PULSE = Pin()

        self.PULSE.connect(
            self.CLOCK.pipe(
                op.filter(lambda s: s == edge),
                op.flat_map(lambda _: rx.of(edge, edge.flip))
            )
        )
