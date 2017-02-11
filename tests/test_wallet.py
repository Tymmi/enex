import unittest
from wallet.wallet import TokenWallet
from bigchain_interface.bigchain_interface import BigchainInterface
from bigchaindb_driver.crypto import CryptoKeypair


class MatchingTest(unittest.TestCase):
    def test(self):

        bcDB = BigchainInterface("http://localhost", 59984)

        identity = CryptoKeypair("5X7WjcbQr8tbbQh6PY2r6sE6zGqNsfGRkXXPm32uUnNQ", "FS4AzZbaZypPiYQJdFu4mY3hR2SDzZX6z5UaMQssWWeJ")
        wallet = TokenWallet(bcDB, identity=identity)

        self.assertEqual(wallet.identity.private_key, "5X7WjcbQr8tbbQh6PY2r6sE6zGqNsfGRkXXPm32uUnNQ")


if __name__ == "__main__":
    unittest.main()