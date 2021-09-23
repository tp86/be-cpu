from math import inf
from time import sleep, time
from typing import Union

from physical.elements import Pin
from physical.signals import H, L
from rx import cold, concat, interval, of, zip as rxzip
from rx.operators import delay as rxdelay
from rx.operators import filter as rxfilter
from rx.operators import flat_map
from rx.operators import map as rxmap


class AdjustableInterval:
    def __init__(self, interval=1.0) -> None:
        self._interval = interval
        self.OUTPUT = Pin()
        self._last_timestamp = None
        self.OUTPUT.connect(self._new_interval)

    def _set_last_timestamp(self, _):
        self._last_timestamp = time()
        return self._last_timestamp

    @property
    def _new_interval(self):
        # concatenate with single element at the beginning to avoid
        # waiting for first element at interval end
        return concat(of(-1), interval(self.interval)).pipe(
            # ensure value is unique in order to always pass through Pin
            # even for quick changes of interval, when -1 is emitted
            # at the start
            rxmap(self._set_last_timestamp)
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
                rxdelay(interval - passed)
            ))


class Clock:
    def __init__(self, frequency=1) -> None:
        self.CLOCK = Pin()

        self._interval = AdjustableInterval(self._freq2period(frequency))
        previous_signal_flipped = self.CLOCK.pipe(rxmap(lambda s: s.flip))
        self.CLOCK.connect(
            rxzip(self._interval.OUTPUT, previous_signal_flipped).pipe(
                rxmap(lambda t: t[1])
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
    def __init__(self, edge: Union[H, L] = H, duration=0.001) -> None:
        self.CLOCK = Pin()
        self.PULSE = Pin()

        self.PULSE.connect(
            self.CLOCK.pipe(
                rxfilter(lambda s: s == edge),
                flat_map(lambda _: cold("e-f", timespan=duration,
                                        lookup={'e': edge, 'f': edge.flip}))
            )
        )

        def delay():
            sleep(duration+0.005)
        delay()

        def next_clock(signal):
            super(Pin, self.CLOCK).on_next(signal)
            delay()

        self.CLOCK.on_next = next_clock
