import unittest

from bigchain_interface.bigchain_interface import BigchainInterface
from utils import BigchainUtilities


class CheckTransactionTest(unittest.TestCase):
    def test(self):

        bc_db = BigchainInterface("http://kyber.ipdb.foundation", 80)

        #status = bc_db.check_status("4b225cb5aa3493c91d04c3bfa37cab5b80b01c62ac8286c0596782696e219335")
        #print(status)


class BigchainInterfaceTest(unittest.TestCase):
    def test(self):
        bc_db = BigchainInterface("http://kyber.ipdb.foundation", 80)

        alice, bob = BigchainUtilities.gen_random_keypair(), BigchainUtilities.gen_random_keypair()

        print("ALICE: " + alice.public_key + "\t" + alice.private_key)
        print("  BOB: " + bob.public_key + "\t" + bob.private_key)

        energy_token = {
            'data': {
                'id': 0,
                'manufacturer': "Dummy",
                'timestamp': "Dummy",
                'source': "Dummy"
            }
        }

        data = {
            "operation": "CREATE",
            "signer": alice,
            "asset": energy_token
        }

        txid = bc_db.create_asset(data)

        status = bc_db.conn.transactions.status(txid, headers=None)
        print(status)

        self.assertIsNotNone(status["status"])


if __name__ == "__main__":
    unittest.main()