from random import choice
from unittest import TestCase

from test_utils import Probe
from physical.signals import H, L

from .registers import _D_1bit, DType_4bit


class D1RegisterTest(TestCase):

    def setUp(self):
        self.probe = Probe()
        self.register = _D_1bit()

    def test_d1reg_initializes_in_reset_state(self):
        self.register.Q.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_d1reg_stores_value_when_enabled_on_clock_high(self):
        self.register.Q.subscribe(self.probe)

        self.register.DI.on_next(H)
        self.assertEqual([L], self.probe.results)
        self.register.IE.on_next(H)
        self.assertEqual([L], self.probe.results)
        self.register.CLK.on_next(H)
        self.assertEqual([L, H], self.probe.results)


class DType_4bitTest(TestCase):

    def setUp(self) -> None:
        self.probe1 = Probe()
        self.probe2 = Probe()
        self.probe3 = Probe()
        self.probe4 = Probe()
        self.register = DType_4bit()

        self.register.Q1.subscribe(self.probe1)
        self.register.Q2.subscribe(self.probe2)
        self.register.Q3.subscribe(self.probe3)
        self.register.Q4.subscribe(self.probe4)

    def test_dreg_initializes_in_LLLL_state(self):
        self.assertEqual([L], self.probe1.results)
        self.assertEqual([L], self.probe2.results)
        self.assertEqual([L], self.probe3.results)
        self.assertEqual([L], self.probe4.results)

    def test_dreg_initializes_in_input_and_output_enabled_state(self):
        self.register.D1.on_next(H)
        self.register.D2.on_next(H)
        self.register.D3.on_next(H)
        self.register.D4.on_next(H)

        self.register.CLK.on_next(H)

        self.assertEqual([L, H], self.probe1.results)
        self.assertEqual([L, H], self.probe2.results)
        self.assertEqual([L, H], self.probe3.results)
        self.assertEqual([L, H], self.probe4.results)

    def test_dreg_output_can_be_disabled(self):
        output_enabler = choice([self.register.M, self.register.N])
        output_enabler.on_next(H)

        self.register.D1.on_next(H)
        self.register.D2.on_next(H)
        self.register.D3.on_next(H)
        self.register.D4.on_next(H)

        self.register.CLK.on_next(H)
        self.register.CLK.on_next(L)

        self.register.D1.on_next(L)
        self.register.D2.on_next(L)
        self.register.D3.on_next(L)
        self.register.D4.on_next(L)

        self.assertEqual([L], self.probe1.results)
        self.assertEqual([L], self.probe2.results)
        self.assertEqual([L], self.probe3.results)
        self.assertEqual([L], self.probe4.results)

        output_enabler.on_next(L)

        self.assertEqual([L, H], self.probe1.results)
        self.assertEqual([L, H], self.probe2.results)
        self.assertEqual([L, H], self.probe3.results)
        self.assertEqual([L, H], self.probe4.results)

    def test_dreg_input_can_be_disabled(self):
        input_enabler = choice([self.register.G1, self.register.G2])
        input_enabler.on_next(H)

        self.register.D1.on_next(H)
        self.register.D2.on_next(H)
        self.register.D3.on_next(H)
        self.register.D4.on_next(H)

        self.register.CLK.on_next(H)
        self.register.CLK.on_next(L)

        self.assertEqual([L], self.probe1.results)
        self.assertEqual([L], self.probe2.results)
        self.assertEqual([L], self.probe3.results)
        self.assertEqual([L], self.probe4.results)
