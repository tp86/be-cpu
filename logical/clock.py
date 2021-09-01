from time import time
from typing import Union
from math import inf

import rx
import rx.operators as op
from physical.elements import Pin, Switch
from physical.signals import H, L

from logical.gates import And, Not


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


class ClockModule:
    def __init__(self):
        self._clock = Clock()
        h_src = rx.just(H)
        l_src = rx.just(L)
        self._manual_clk = Switch()
        self._clock_selector = Switch()
        and_halt = And()
        not_halt = Not()
        not_clock = Not()

        self.CLK = and_halt.C
        self.CLK_ = Pin()
        self.HLT = Pin()

        self._clock_selector.IN1.connect(self._manual_clk.OUT)
        self._clock_selector.IN2.connect(self._clock.CLOCK)
        self._manual_clk.IN1.connect(h_src)
        self._manual_clk.IN2.connect(l_src)
        and_halt.A.connect(self._clock_selector.OUT)
        and_halt.B.connect(not_halt.B)
        not_halt.A.connect(self.HLT)
        self.CLK_.connect(not_clock.B)
        not_clock.A.connect(self.CLK)

        # initialize with HTL low
        self.HLT.on_next(L)

    @property
    def frequency(self):
        return self._clock.frequency

    @frequency.setter
    def frequency(self, frequency):
        self._clock.frequency = frequency

    def auto(self):
        self._clock_selector.off()

    def manual(self):
        self._clock_selector.on()

    def high(self):
        self._manual_clk.on()

    def low(self):
        self._manual_clk.off()
