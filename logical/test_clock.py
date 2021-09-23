from time import sleep

import pytest
from physical.signals import H, L
from test_utils import CPUTestCase, Probe

from .clock import AdjustableInterval, Clock, Pulse


class AdjustableIntervalTest(CPUTestCase):

    def setUp(self):
        self.probe = Probe()
        self.ai = AdjustableInterval()

    def test_adjustable_interval_produces_first_value_immediately(self):
        self.ai.OUTPUT.subscribe(self.probe)
        self.assertEqual(1, len(self.probe.results))

    @pytest.mark.slow
    def test_adjustable_interval_produces_values_each_second_initially(self):
        self.ai.OUTPUT.subscribe(self.probe)

        sleep(2.5)

        self.assertEqual(4, len(self.probe.results))

    @pytest.mark.slow
    def test_adjustable_interval_can_be_changed(self):
        self.ai.interval = 0.2
        self.ai.OUTPUT.subscribe(self.probe)

        sleep(0.9)

        self.assertEqual(6, len(self.probe.results))

        self.ai.interval = 0.5
        sleep(1.0)
        self.assertEqual(8, len(self.probe.results))

    @pytest.mark.slow
    def test_adjustable_interval_can_be_set_on_creation(self):
        ai = AdjustableInterval(0.5)
        ai.OUTPUT.subscribe(self.probe)

        sleep(0.7)

        self.assertEqual(3, len(self.probe.results))


class ClockTest(CPUTestCase):

    def setUp(self):
        self.probe = Probe()
        self.clock = Clock()

    def test_clock_starts_with_low_state(self):
        self.clock.CLOCK.subscribe(self.probe)
        self.assertEqual([L], self.probe.results)

    @pytest.mark.slow
    def test_clock_starts_with_default_1Hz_frequency(self):
        self.assertEqual(1, self.clock.frequency)
        self.clock.CLOCK.subscribe(self.probe)

        sleep(0.6)

        self.assertEqual([L, H, L], self.probe.results)

        sleep(0.5)

        self.assertEqual([L, H, L, H], self.probe.results)

    @pytest.mark.slow
    def test_clock_frequency_can_be_set_on_creation(self):
        clock = Clock(2.5)
        clock.CLOCK.subscribe(self.probe)

        sleep(0.5)

        self.assertEqual([L, H, L, H], self.probe.results)

    @pytest.mark.slow
    def test_clock_frequency_can_be_changed(self):
        self.assertEqual(1, self.clock.frequency)
        self.clock.CLOCK.subscribe(self.probe)

        sleep(0.6)

        self.assertEqual([L, H], self.probe.results)

        self.clock.frequency = 2.5

        sleep(0.4)

        self.assertEqual([L, H, L, H], self.probe.results)


class PulseTest(CPUTestCase):

    def setUp(self):
        self.probe = Probe()
        self.pulse = Pulse()

    def test_pulse_initializes_with_low_state(self):
        self.pulse.PULSE.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_pulse_emits_two_changes_on_high_input_only(self):
        self.pulse.PULSE.subscribe(self.probe)

        self.pulse.CLOCK.on_next(H)

        self.assertEqual([L, H, L], self.probe.results)

        self.pulse.CLOCK.on_next(L)

        self.assertEqual([L, H, L], self.probe.results)

    def test_pulse_detected_edge_may_be_changed_on_creation(self):
        pulse = Pulse(L)
        pulse.PULSE.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

        pulse.CLOCK.on_next(H)

        self.assertEqual([H], self.probe.results)

        pulse.CLOCK.on_next(L)

        self.assertEqual([H, L, H], self.probe.results)
