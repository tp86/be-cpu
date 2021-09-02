from physical.signals import H, L
from time import sleep
from unittest import TestCase

import pytest
from test_utils import Probe

from logical.clock import AdjustableInterval, Clock


class AdjustableIntervalTest(TestCase):

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

        self.assertEqual(3, len(self.probe.results))

    @pytest.mark.slow
    def test_adjustable_interval_can_be_changed(self):
        self.ai.interval = 0.2
        self.ai.OUTPUT.subscribe(self.probe)

        sleep(0.9)

        self.assertEqual(5, len(self.probe.results))

        self.ai.interval = 0.5
        sleep(1.0)
        self.assertEqual(7, len(self.probe.results))

    @pytest.mark.slow
    def test_adjustable_interval_can_be_set_on_creation(self):
        ai = AdjustableInterval(0.5)
        ai.OUTPUT.subscribe(self.probe)

        sleep(0.7)

        self.assertEqual(2, len(self.probe.results))


class ClockTest(TestCase):

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

        self.assertEqual([L, H], self.probe.results)

        sleep(0.5)

        self.assertEqual([L, H, L], self.probe.results)

    @pytest.mark.skip('not implemented yet')
    def test_clock_frequency_can_be_set_on_creation(self):
        pass

    @pytest.mark.skip('not implemented yet')
    def test_clock_frequency_can_be_changed(self):
        pass
