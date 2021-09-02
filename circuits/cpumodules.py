import rx
from logical.clock import Clock
from logical.gates import And, Not
from physical.elements import Pin, Switch
from physical.signals import H, L


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
