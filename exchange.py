from sortedcontainers import SortedListWithKey


class Exchange(object):

    def __init__(self):
        # Setup orderbook
        self.sells = SortedListWithKey(key=(lambda x: (x['price'])))
        self.buys = SortedListWithKey(key=(lambda x: (x['price'])))

    def add_order(self, order, gender):
        
        order["rem_amount"] = order["amount"]
        
        if gender.upper() == "BUY":
            self.buys.add(order)
        elif gender.upper() == "SELL":
            self.sells.add(order)
        else:
            raise Exception

        # invoke match
        if self.delegate_match():
            self.execute_match()

    def delegate_match(self):

        try:
            low_sell = self.sells[0]
            high_buy = self.buys[-1]
        except:
            return False

        if low_sell["price"] <= high_buy["price"]:
            return True
        return False
        
    def execute_match(self):

        buys = reversed(self.buys)
        sells = self.sells
        consumed_orders = list()
        
        for buy in buys:
            if buy["rem_amount"] == 0:
                continue
            for sell in sells:
                if sell["rem_amount"] == 0:
                    continue
                if buy["price"] >= sell["price"]:
                    res = self._determine(buy, sell)
                    consumed_orders.extend(res)
                else:
                    break

        self._cleanup_orderbook(consumed_orders)

    @staticmethod
    def _determine(buy, sell):

        curr_consumed_orders = list()
        same_amount = False
        buy_is_zero = False

        if buy["rem_amount"] > sell["rem_amount"]:
            master = buy
            slave = sell
        elif buy["rem_amount"] < sell["rem_amount"]:
            master = sell
            slave = buy
            buy_is_zero = True
        elif buy["rem_amount"] == sell["rem_amount"]:
            same_amount = True

        if not same_amount:
            master["rem_amount"] -= slave["rem_amount"]
            slave["rem_amount"] = 0
            curr_consumed_orders.append(slave)
            if buy_is_zero:
                return []
        else:
            buy["rem_amount"] = 0
            sell["rem_amount"] = 0
            return [buy, sell]

    def _cleanup_orderbook(self, orders):

        for order in orders:
            try:
                self.sells.remove(order)
            except:
                try:
                    self.buys.remove(order)
                except:
                    pass


def main():
    pass


if __name__ == "__main__":
    main()