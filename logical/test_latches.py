from unittest import TestCase
from test_utils import Probe

from logical.latches import D, SR, SREnable
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


class SREnableTest(TestCase):

    def setUp(self):
        self.probe_q = Probe()
        self.probe_q_ = Probe()
        self.sre = SREnable()

    def test_srenable_initializes_in_reset_state(self):
        self.sre.Q.subscribe(self.probe_q)
        self.sre.Q_.subscribe(self.probe_q_)

        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)

    def test_srenable_does_not_react_without_enable_high(self):
        self.sre.Q.subscribe(self.probe_q)
        self.sre.Q_.subscribe(self.probe_q_)

        self.sre.S.on_next(H)
        self.sre.S.on_next(L)
        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)

        self.sre.R.on_next(L)
        self.sre.R.on_next(H)
        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)

    def test_srenable_sets_and_resets_on_enable_high(self):
        self.sre.Q.subscribe(self.probe_q)
        self.sre.Q_.subscribe(self.probe_q_)

        self.sre.S.on_next(H)
        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)
        self.sre.EN.on_next(H)
        self.assertEqual([L, H], self.probe_q.results)
        self.assertEqual([H, L], self.probe_q_.results)
        self.sre.EN.on_next(L)
        self.sre.S.on_next(L)

        self.sre.R.on_next(H)
        self.assertEqual([L, H], self.probe_q.results)
        self.assertEqual([H, L], self.probe_q_.results)
        self.sre.EN.on_next(H)
        self.assertEqual([L, H, L], self.probe_q.results)
        self.assertEqual([H, L, H], self.probe_q_.results)
        self.sre.EN.on_next(L)
        self.sre.R.on_next(L)

        self.sre.EN.on_next(H)
        self.sre.S.on_next(H)
        self.assertEqual([L, H, L, H], self.probe_q.results)
        self.assertEqual([H, L, H, L], self.probe_q_.results)
        self.sre.S.on_next(L)
        self.sre.R.on_next(H)
        self.assertEqual([L, H, L, H, L], self.probe_q.results)
        self.assertEqual([H, L, H, L, H], self.probe_q_.results)


class DTest(TestCase):

    def setUp(self):
        self.probe_q = Probe()
        self.probe_q_ = Probe()
        self.d = D()

    def test_d_initializes_in_reset_state(self):
        self.d.Q.subscribe(self.probe_q)
        self.d.Q_.subscribe(self.probe_q_)

        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)

    def test_d_does_not_react_when_enabled_is_low(self):
        self.d.Q.subscribe(self.probe_q)
        self.d.Q_.subscribe(self.probe_q_)
        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)

        self.d.D.on_next(H)
        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)

        self.d.D.on_next(L)
        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)

    def test_d_sets_and_resets_when_enabled_is_high(self):
        self.d.Q.subscribe(self.probe_q)
        self.d.Q_.subscribe(self.probe_q_)
        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)

        self.d.EN.on_next(H)
        self.assertEqual([L], self.probe_q.results)
        self.assertEqual([H], self.probe_q_.results)
        self.d.D.on_next(H)
        self.assertEqual([L, H], self.probe_q.results)
        self.assertEqual([H, L], self.probe_q_.results)

        self.d.EN.on_next(L)
        self.d.D.on_next(L)
        self.assertEqual([L, H], self.probe_q.results)
        self.assertEqual([H, L], self.probe_q_.results)
        self.d.EN.on_next(H)
        self.assertEqual([L, H, L], self.probe_q.results)
        self.assertEqual([H, L, H], self.probe_q_.results)
