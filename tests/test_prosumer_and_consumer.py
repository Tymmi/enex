from wallet.wallet import TokenWallet
from bigchain_interface.bigchain_interface import BigchainInterface
from asset.asset import EnergyToken
from exchange.exchange import Exchange

from datetime import datetime
import time
import unittest

class ProsumerConsumerTest(unittest.TestCase):
    def test(self):
        #BigchainDB and Exchange instantiated
        bc_db = BigchainInterface("http://kyber.ipdb.foundation", 80)
        exchange = Exchange()


        # Two users exist
        prosumer = TokenWallet(bc_db)
        consumer = TokenWallet(bc_db)


        # Prosumer is producing 5 kWh
        for i in range(0,5):

            data ={
                'manufacturer': "Vattenfall",
                'timestamp': str(datetime.now()),
                'source': "GREEN"
            }

            token = EnergyToken.fetch(data)
            txid = prosumer.issue(token)
            print(bc_db.get_transaction(txid))

        time.sleep(1)

        print("\n\nList of issued token id's:\n" + str(prosumer.get_utxos()))


        # Prosumer is selling some token (1 kWh)
        order = {
            "amount": 3,
            "price": 25.00
        }
        print("\n\nProsumer is selling:\n" + str(order))
        if order["amount"] <= prosumer.get_balance():
            exchange.add_order(order, "sell", prosumer)


        # Consumer is buying 1 token (1 kWh)
        order = {
            "amount": 1,
            "price": 25.10
        }
        print("\n\nConsumer is buying:\n" + str(order))
        exchange.add_order(order, "buy", consumer)
        order = {
            "amount": 1,
            "price": 25.10
        }
        print("\n\nConsumer is buying:\n" + str(order))
        exchange.add_order(order, "buy", consumer)

        print("Leftover sellside:\n" + str(exchange.sells))

        self.assertEqual(exchange.sells[0]["rem_amount"], 1)