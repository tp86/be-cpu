from unittest import TestCase

import rx
import rx.operators as op
from rx.subject import Subject
from test_utils import Probe

from physical.elements import Pin, Switch
from physical.signals import H, L


class PinTest(TestCase):

    def setUp(self):
        self.pin = Pin()
        self.probe = Probe()

    def test_pin_has_initial_state(self):
        self.pin.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_pin_initial_state_can_be_set(self):
        pin = Pin(H)
        pin.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_pin_propagates_only_changes(self):
        self.pin.subscribe(self.probe)
        rx.of(H, L, H, H, H, L).subscribe(self.pin)

        self.assertEqual([L, H, L, H, L], self.probe.results)

    def test_pin_sends_last_value_on_new_connection(self):
        self.pin.subscribe(self.probe)
        self.pin.on_next(H)

        probe2 = Probe()
        self.pin.pipe(
            op.map(lambda x: x)
        ).subscribe(probe2)

        self.assertEqual([L, H], self.probe.results)
        self.assertEqual([H], probe2.results)

    def test_pin_can_be_connected_to_one_source_at_the_time(self):
        src1 = Subject()
        src2 = Subject()
        self.pin.connect(src1)
        self.pin.subscribe(self.probe)
        src1.on_next(H)
        src2.on_next(L)

        self.assertEqual([L, H], self.probe.results)

        self.pin.connect(src2)
        src1.on_next(L)

        self.assertEqual([L, H], self.probe.results)

        src2.on_next(L)
        src1.on_next(H)

        self.assertEqual([L, H, L], self.probe.results)

    def test_downstream_pins_get_values_from_upstream_pins_on_connection(self):
        upstream_pin = Pin(H)
        downstream_pin = Pin(L)

        downstream_pin.connect(upstream_pin)
        downstream_pin.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_pin_states_propagate_through_combine_latest(self):
        pin1 = Pin()
        pin2 = Pin(H)

        Pin.combine_latest(pin1, pin2).subscribe(self.probe)
        self.assertEqual([(L, H)], self.probe.results)

        pin1.on_next(H)
        self.assertEqual([(L, H), (H, H)], self.probe.results)

        probe = Probe()
        Pin.combine_latest(pin1, pin2).subscribe(probe)
        self.assertEqual([(H, H)], probe.results)


class SwitchTest(TestCase):

    def setUp(self):
        self.probe = Probe()
        self.switch = Switch()

    def test_switch_is_initialized_in_turned_off_state(self):
        self.switch.OUT.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

        self.switch.IN1.on_next(H)

        self.assertEqual([L, H], self.probe.results)

        self.switch.IN1.on_next(L)
        self.switch.IN2.on_next(H)

        self.assertEqual([L, H, L], self.probe.results)

    def test_switching_between_pins(self):
        self.switch.IN2.on_next(H)
        self.switch.on()

        self.switch.OUT.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

        self.switch.IN1.on_next(H)
        self.switch.off()

        self.assertEqual([H], self.probe.results)
