from sortedcontainers import SortedListWithKey
from wallet.wallet import TokenWallet


class Exchange(object):

    def __init__(self, onchain=True):
        # Setup orderbook
        self.sells = SortedListWithKey(key=(lambda x: (x['price'])))
        self.buys = SortedListWithKey(key=(lambda x: (x['price'])))
        self.onchain = onchain

    def add_order(self, order, gender, wallet):

        order["rem_amount"] = order["amount"]
        order["wallet"] = wallet
        
        if gender.upper() == "BUY":
            self.buys.add(order)
        elif gender.upper() == "SELL":
            self.sells.add(order)
        else:
            raise Exception

        # invoke match
        if self.delegate_match():
            print("match!")
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

        if buy["rem_amount"] > sell["rem_amount"]:
            master = buy
            slave = sell
        elif buy["rem_amount"] < sell["rem_amount"]:
            master = sell
            slave = buy
        elif buy["rem_amount"] == sell["rem_amount"]:
            same_amount = True

        try:
            sell["wallet"].send(slave["rem_amount"], buy["wallet"].identity)
            # buy["wallet"].send(slave["rem_amount"], sell["wallet"].identity)
        except:
            pass

        if not same_amount:
            master["rem_amount"] -= slave["rem_amount"]
            slave["rem_amount"] = 0
            curr_consumed_orders.append(slave)
        else:
            buy["rem_amount"] = 0
            sell["rem_amount"] = 0
            return [buy, sell]
        return curr_consumed_orders

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
