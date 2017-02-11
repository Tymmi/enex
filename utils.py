import bigchaindb_driver.crypto
from collections import namedtuple


class BigchainUtilities(object):

    @staticmethod
    def gen_random_keypair():
        return bigchaindb_driver.crypto.generate_keypair()


    @staticmethod
    def gen_keypair(public_key, private_key):
        return namedtuple('CryptoKeypair', ('private_key', 'public_key'))