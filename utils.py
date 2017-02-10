from bigchaindb_driver.crypto import generate_keypair
class BigchainUtilities(object):

    @staticmethod
    def gen_random_keypair():
        return generate_keypair()