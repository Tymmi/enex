import unittest

from Main import BigchainConnection
from utils import BigchainUtilities


class BigchainInterfaceTest(unittest.TestCase):
    def test(self):

        bigDB = BigchainConnection("http://localhost", 59984)

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

        txid = bigDB.create_asset(
            operation="CREATE",
            signer=alice,
            asset=energy_token,
            metadata=metadata
        )

        status = bigDB.conn.transactions.status(txid)
        print(status)

        self.assertIsNotNone(status["status"])