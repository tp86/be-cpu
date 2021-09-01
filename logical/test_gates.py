from unittest import TestCase

from physical.elements import Pin
from physical.signals import H, L
from test_utils import Probe

from logical.gates import And, Nand, Nor, Not, Or


class AndGateTest(TestCase):

    def setUp(self):
        self.probe = Probe()
        self.and_gate = And()

    def test_and_gate_is_initialized_low(self):
        self.and_gate.C.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_and_gate_propagates_partial_inputs(self):
        self.and_gate.A.on_next(H)

        self.and_gate.C.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_and_gate_ands_inputs(self):
        self.and_gate.A.on_next(H)
        self.and_gate.B.on_next(H)

        self.and_gate.C.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_and_gate_propagates_inputs_from_pins(self):
        a_pin = Pin(H)

        self.and_gate.A.connect(a_pin)
        self.and_gate.B.on_next(H)

        self.and_gate.C.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_and_gate_logic(self):
        self.and_gate.C.subscribe(self.probe)
        self.assertEqual([L], self.probe.results)

        self.and_gate.A.on_next(H)
        self.assertEqual([L], self.probe.results)

        self.and_gate.B.on_next(H)
        self.assertEqual([L, H], self.probe.results)

        self.and_gate.A.on_next(L)
        self.assertEqual([L, H, L], self.probe.results)

    def test_and_gate_outputs_last_signal_to_new_connection(self):
        self.and_gate.A.on_next(H)
        self.and_gate.B.on_next(H)
        self.and_gate.C.subscribe(self.probe)
        self.assertEqual([H], self.probe.results)

        probe = Probe()
        self.and_gate.C.subscribe(probe)
        self.assertEqual([H], probe.results)


class OrGateTest(TestCase):

    def setUp(self):
        self.probe = Probe()
        self.or_gate = Or()

    def test_or_gate_is_initialized_low(self):
        self.or_gate.C.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_or_gate_propagates_partial_inputs(self):
        self.or_gate.A.on_next(H)

        self.or_gate.C.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_or_gate_ors_inputs(self):
        self.or_gate.A.on_next(H)
        self.or_gate.B.on_next(L)

        self.or_gate.C.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_or_gate_propagates_inputs_from_pins(self):
        a_pin = Pin(H)

        self.or_gate.A.connect(a_pin)

        self.or_gate.C.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_or_gate_logic(self):
        self.or_gate.C.subscribe(self.probe)
        self.assertEqual([L], self.probe.results)

        self.or_gate.A.on_next(H)
        self.assertEqual([L, H], self.probe.results)

        self.or_gate.B.on_next(H)
        self.assertEqual([L, H], self.probe.results)

        self.or_gate.A.on_next(L)
        self.assertEqual([L, H], self.probe.results)

        self.or_gate.B.on_next(L)
        self.assertEqual([L, H, L], self.probe.results)

    def test_or_gate_outputs_last_signal_to_new_connection(self):
        self.or_gate.A.on_next(H)
        self.or_gate.C.subscribe(self.probe)
        self.assertEqual([H], self.probe.results)

        probe = Probe()
        self.or_gate.C.subscribe(probe)
        self.assertEqual([H], probe.results)


class NotGateTest(TestCase):

    def setUp(self):
        self.probe = Probe()
        self.not_gate = Not()

    def test_not_gate_is_initialized_high(self):
        self.not_gate.B.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_not_gate_flips_input(self):
        self.not_gate.A.on_next(H)
        self.not_gate.B.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_not_gate_propagates_inputs_from_pin(self):
        a_pin = Pin(H)

        self.not_gate.A.connect(a_pin)
        self.not_gate.B.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_not_gate_logic(self):
        self.not_gate.B.subscribe(self.probe)
        self.assertEqual([H], self.probe.results)

        self.not_gate.A.on_next(H)
        self.assertEqual([H, L], self.probe.results)

        self.not_gate.A.on_next(H)
        self.assertEqual([H, L], self.probe.results)

        self.not_gate.A.on_next(L)
        self.assertEqual([H, L, H], self.probe.results)

    def test_not_gate_outputs_last_signal_to_new_connection(self):
        self.not_gate.B.subscribe(self.probe)
        self.not_gate.A.on_next(H)
        self.assertEqual([H, L], self.probe.results)

        probe = Probe()
        self.not_gate.B.subscribe(probe)
        self.assertEqual([L], probe.results)


class NandGateTest(TestCase):

    def setUp(self):
        self.probe = Probe()
        self.nand_gate = Nand()

    def test_nand_gate_is_initialized_high(self):
        self.nand_gate.C.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_nand_gate_propagates_partial_inputs(self):
        self.nand_gate.A.on_next(H)

        self.nand_gate.C.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_nand_gate_nands_inputs(self):
        self.nand_gate.A.on_next(H)
        self.nand_gate.B.on_next(H)
        self.nand_gate.C.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_nand_gate_propagates_inputs_from_pins(self):
        a_pin = Pin(H)

        self.nand_gate.A.connect(a_pin)
        self.nand_gate.B.on_next(H)

        self.nand_gate.C.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_nand_gate_logic(self):
        self.nand_gate.C.subscribe(self.probe)
        self.assertEqual([H], self.probe.results)

        self.nand_gate.A.on_next(H)
        self.assertEqual([H], self.probe.results)

        self.nand_gate.B.on_next(H)
        self.assertEqual([H, L], self.probe.results)

        self.nand_gate.A.on_next(L)
        self.assertEqual([H, L, H], self.probe.results)

        self.nand_gate.B.on_next(L)
        self.assertEqual([H, L, H], self.probe.results)

    def test_nand_gate_outputs_last_signal_to_new_connection(self):
        self.nand_gate.A.on_next(H)
        self.nand_gate.B.on_next(H)
        self.nand_gate.C.subscribe(self.probe)
        self.assertEqual([L], self.probe.results)

        probe = Probe()
        self.nand_gate.C.subscribe(probe)
        self.assertEqual([L], probe.results)


class NorGateTest(TestCase):

    def setUp(self):
        self.probe = Probe()
        self.nor_gate = Nor()

    def test_nor_gate_is_initialized_high(self):
        self.nor_gate.C.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

    def test_nor_gate_propagates_partial_inputs(self):
        self.nor_gate.A.on_next(H)

        self.nor_gate.C.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_nor_gate_nors_inputs(self):
        self.nor_gate.A.on_next(H)
        self.nor_gate.B.on_next(H)
        self.nor_gate.C.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_nor_gate_propagates_inputs_from_pins(self):
        a_pin = Pin(H)

        self.nor_gate.A.connect(a_pin)

        self.nor_gate.C.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

    def test_nor_gate_logic(self):
        self.nor_gate.C.subscribe(self.probe)
        self.assertEqual([H], self.probe.results)

        self.nor_gate.A.on_next(H)
        self.assertEqual([H, L], self.probe.results)

        self.nor_gate.B.on_next(H)
        self.assertEqual([H, L], self.probe.results)

        self.nor_gate.A.on_next(L)
        self.assertEqual([H, L], self.probe.results)

        self.nor_gate.B.on_next(L)
        self.assertEqual([H, L, H], self.probe.results)

    def test_nor_gate_outputs_last_signal_to_new_connection(self):
        self.nor_gate.A.on_next(H)
        self.nor_gate.C.subscribe(self.probe)
        self.assertEqual([L], self.probe.results)

        probe = Probe()
        self.nor_gate.C.subscribe(probe)
        self.assertEqual([L], probe.results)
