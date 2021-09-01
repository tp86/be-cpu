from unittest import TestCase

from test_utils import Probe

from logical.switches import Buffer
from physical.signals import H, L


class BufferTest(TestCase):

    def setUp(self):
        self.probe = Probe()
        self.buffer = Buffer()

    def test_buffer_is_initialized_in_disabled_state(self):
        self.buffer.OUT.subscribe(self.probe)

        self.assertEqual([L], self.probe.results)

        self.buffer.IN.on_next(H)
        self.assertEqual([L], self.probe.results)

    def test_buffer_passes_input_when_enabled(self):
        self.buffer.ENABLE.on_next(H)
        self.buffer.OUT.subscribe(self.probe)
        self.assertEqual([L], self.probe.results)

        self.buffer.IN.on_next(H)
        self.buffer.IN.on_next(L)
        self.assertEqual([L, H, L], self.probe.results)

    def test_buffer_passes_last_input_on_new_connection_when_disabled(self):
        self.buffer.ENABLE.on_next(H)
        self.buffer.IN.on_next(H)
        self.buffer.ENABLE.on_next(L)
        self.buffer.OUT.subscribe(self.probe)

        self.assertEqual([H], self.probe.results)

        probe = Probe()
        self.buffer.OUT.subscribe(probe)
        self.assertEqual([H], probe.results)
