import unittest
import datetime

from exchange.exchange import Exchange


class MatchingTest(unittest.TestCase):
    def test(self):

        ex = Exchange(onchain=False)

        start = datetime.datetime.now()
        end = datetime.datetime.now()
        count = 0

        while end - start < datetime.timedelta(seconds=10):

            ex.add_order({
                "amount": 10,
                "price": 25.00
            }, "sell", None)

            ex.add_order({
                "amount": 5,
                "price": 25.01
            }, "buy", None)

            count += 1
            end = datetime.datetime.now()

            res = ex.sells[0]["rem_amount"]

        print(count/10)

        #self.assertEqual(res, 5)


class AddOrderTest(unittest.TestCase):
    def test(self):

        ex = Exchange()

        order = {
            "amount": 15,
            "price": 20
        }

        ex.add_order(order, "sell", None)

        self.assertEqual(ex.sells[0]["amount"], 15)
        self.assertEqual(len(ex.sells), 1)


if __name__ == "__main__":
    unittest.main()