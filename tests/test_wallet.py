import unittest
from wallet.wallet import TokenWallet
from bigchain_interface.bigchain_interface import BigchainInterface
from bigchaindb_driver.crypto import CryptoKeypair, generate_keypair


class MatchingTest(unittest.TestCase):
    def test(self):

        bc_db = BigchainInterface("http://kyber.ipdb.foundation", 80)

        identity = CryptoKeypair("5X7WjcbQr8tbbQh6PY2r6sE6zGqNsfGRkXXPm32uUnNQ", "FS4AzZbaZypPiYQJdFu4mY3hR2SDzZX6z5UaMQssWWeJ")
        wallet = TokenWallet(bc_db, identity=identity)

        self.assertEqual(wallet.identity.private_key, "5X7WjcbQr8tbbQh6PY2r6sE6zGqNsfGRkXXPm32uUnNQ")


class PythonContractTest(unittest.TestCase):

    def test(self):

        import time
        bc_db = BigchainInterface("http://kyber.ipdb.foundation", 80)

        def check_tx(txid):
            trials = 0
            while trials < 60:
                try:
                    if bc_db.conn.transactions.status(txid).get('status') == 'valid':
                        print('Tx valid in:', trials, 'secs')
                        break
                except bigchaindb_driver.exceptions.NotFoundError:
                    trials += 1
                    time.sleep(1)

        identity = CryptoKeypair("3P7GQqgPFv4EtuSxUKfynnsGRFaiqDs5yiesPGPXWN48",
                                 "HuXxaCfYmqxJGxf3o2cK51XFvE7hqYiurZfdky3VeMZD")
        debt_identity = CryptoKeypair("4JqJ118C31Dy6VbG8CR7NaGGvh2jufuvB2QY9QKuMiWD",
                                      "6Ew2xojsYk4363hgBWM4JGGckqpQbwUfvUc6XvdSD7jD")

        identity = generate_keypair()
        debt_identity = generate_keypair()

        print(debt_identity)

        wallet = TokenWallet(bc_db, identity=identity)
        debt_wallet = TokenWallet(bc_db, identity=debt_identity)

        token = {
            "data": { "script": "if len(bigchain.get_outputs_filtered('{}', True)) > 0: raise".format(debt_identity.public_key)}
        }

        txid = wallet.issue(token)
        check_tx(txid)

        txid = debt_wallet.issue({
            "data": {"script": "if False: raise"}
        })
        check_tx(txid)

        print("ok")

        try:
            txid = wallet.issue(token)
            check_tx(txid)
        except:
            pass



if __name__ == "__main__":
    unittest.main()