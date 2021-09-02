from unittest import TestCase
from test_utils import Probe

from logical.latches import SR
from physical.signals import H, L


class SRTest(TestCase):

    def setUp(self):
        self.probe_q = Probe()
        self.probe_q_ = Probe()
        self.sr = SR()

    def test_sr_initializes_in_reset_state(self):
        self.sr.Q.subscribe(self.probe_q)
        self.sr.Q_.subscribe(self.probe_q_)

        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)

    def test_sr_sets_resets_and_latches(self):
        self.sr.Q.subscribe(self.probe_q)
        self.sr.Q_.subscribe(self.probe_q_)

        self.sr.S.on_next(H)

        self.assertEqual([L, H], self.probe_q.results)
        self.assertEqual([H, L], self.probe_q_.results)

        self.sr.S.on_next(L)

        probe = Probe()
        self.sr.Q.subscribe(probe)

        self.assertEqual([L, H], self.probe_q.results)
        self.assertEqual([H, L], self.probe_q_.results)
        self.assertEqual([H], probe.results)

        self.sr.R.on_next(H)

        self.assertEqual([L, H, L], self.probe_q.results)
        self.assertEqual([H, L, H], self.probe_q_.results)
        self.assertEqual([H, L], probe.results)

        self.sr.R.on_next(L)

        self.assertEqual([L, H, L], self.probe_q.results)
        self.assertEqual([H, L, H], self.probe_q_.results)
        self.assertEqual([H, L], probe.results)
