from unittest import TestCase

import rx
import rx.operators as op

from metal import Pin


class PinTest(TestCase):

    def setUp(self):
        self.pin = Pin()
        self.results = []

    def probe(self, element):
        self.results.append(element)

    def test_pin_connects_to_one_source_at_a_time(self):
        from time import sleep

        source1 = rx.interval(0.01).pipe(op.map(lambda _: 1))
        source2 = rx.interval(0.01).pipe(op.map(lambda _: 'a'))

        self.pin.subscribe(self.probe)
        self.pin.connect(source1)

        sleep(0.1)

        self.assertEqual({1}, set(self.results))

        self.pin.connect(source2)
        current_position = len(self.results)

        sleep(0.1)

        self.assertEqual({'a'}, set(self.results[current_position:]))
        self.pin.disconnect()

    def test_pin_emits_only_on_source_changes(self):

        source = rx.of(1, 1, 1, 2, 2, 2, 1, 3)

        self.pin.subscribe(self.probe)
        self.pin.connect(source)

        self.assertEqual([1, 2, 1, 3], self.results)
