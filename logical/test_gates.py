from physical.elements import Pin
from unittest import TestCase

from physical.signals import H, L
from test_utils import Probe

from logical.gates import And


class AndGateTest(TestCase):

    def setUp(self):
        self.probe = Probe()
        self.andGate = And()

    def test_and_gate_is_initialized_low(self):
        self.andGate.C.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_and_gate_ands_inputs(self):
        self.andGate.A.on_next(H)
        self.andGate.B.on_next(H)

        self.andGate.C.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_and_gate_propagates_inputs_from_pins(self):
        a_pin = Pin(H)

        self.andGate.A.connect(a_pin)
        self.andGate.B.on_next(H)

        self.andGate.C.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_and_gate_logic(self):
        self.andGate.C.subscribe(self.probe)
        self.assertEqual([L], self.probe.results)

        self.andGate.A.on_next(H)
        self.assertEqual([L], self.probe.results)

        self.andGate.B.on_next(H)
        self.assertEqual([L, H], self.probe.results)

        self.andGate.A.on_next(L)
        self.assertEqual([L, H, L], self.probe.results)

    def test_and_gate_outputs_last_signal_to_new_connection(self):
        self.andGate.A.on_next(H)
        self.andGate.B.on_next(H)
        self.andGate.C.subscribe(self.probe)
        self.assertEqual([H], self.probe.results)

        probe = Probe()
        self.andGate.C.subscribe(probe)
        self.assertEqual([H], probe.results)
