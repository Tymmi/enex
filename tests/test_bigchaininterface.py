import unittest

from bigchain_interface.bigchain_interface import BigchainInterface
from utils import BigchainUtilities


class CheckTransactionTest(unittest.TestCase):
    def test(self):

        bigDB = BigchainInterface("http://localhost", 59984)

        status = bigDB.check_status("4b225cb5aa3493c91d04c3bfa37cab5b80b01c62ac8286c0596782696e219335")
        print(status)


class BigchainInterfaceTest(unittest.TestCase):
    def test(self):

        bcDB = BigchainInterface("http://localhost", 59984)

        alice, bob = BigchainUtilities.gen_random_keypair(), BigchainUtilities.gen_random_keypair()

        print("ALICE: " + alice.public_key + "\t" + alice.private_key)
        print("  BOB: " + bob.public_key + "\t" + bob.private_key)

        energy_token = {
            'data': {
                'kwh': {
                    'id': 0xbeef,
                    'manufacturer': 'vattenfall'
                }
            }
        }

        metadata = {'location': 'NL'}

        msg = {
            "asset": energy_token,
            "metadata": metadata
        }

        data = {
            "operation": "CREATE",
            "signer": alice,
            "asset": msg
        }

        txid = bcDB.create_asset(data)

        '''
        txid = bcDB.create_asset(
            operation="CREATE",
            signer=alice,
            asset=msg
        )
        '''

        status = bcDB.conn.transactions.status(txid)
        print(status)

        self.assertIsNotNone(status["status"])


if __name__ == "__main__":
    unittest.main()