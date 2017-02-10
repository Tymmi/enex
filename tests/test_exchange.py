import unittest

from exchange import Exchange


class MatchingTest(unittest.TestCase):
    def test(self):

        ex = Exchange()

        ex.add_order({
            "amount": 10,
            "price": 25.00
        }, "sell")

        ex.add_order({
            "amount": 5,
            "price": 25.01
        }, "buy")

        res = ex.sells[0]["rem_amount"]

        self.assertEqual(res, 5)


class AddOrderTest(unittest.TestCase):
    def test(self):

        ex = Exchange()

        order = {
            "amount": 15,
            "price": 20
        }

        ex.add_order(order, "sell")

        self.assertEqual(ex.sells[0]["amount"], 15)
        self.assertEqual(len(ex.sells), 1)
