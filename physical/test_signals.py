from physical.signals import H, L
from unittest import TestCase


class SignalTest(TestCase):

    def test_signals_can_be_flipped(self):
        self.assertEqual(H.flip, L)
        self.assertEqual(L.flip, H)

    def test_signals_have_boolean_values(self):
        self.assertTrue(H)
        self.assertFalse(L)
        self.assertTrue(L or H)
        self.assertFalse(H and L)

    def test_signals_have_character_representation(self):
        self.assertEqual(repr(H), str(H))
        self.assertEqual(repr(L), str(L))
        self.assertEqual(len(str(H)), 1)
        self.assertEqual(len(str(L)), 1)
