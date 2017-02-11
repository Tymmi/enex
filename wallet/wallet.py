from utils import BigchainUtilities


class TokenWallet(object):

    def __init__(self, bcDB, identity=None):

        if identity is None:
            self.identity = BigchainUtilities.gen_random_keypair()
        else:
            self.identity = identity
        print(identity.public_key, identity.private_key)
        self.bc_interface = bcDB

        self.utxos = list()
        self.utxos.extend(self.bc_interface.get_utxos(identity.public_key))

    def send(self, amount, recipient):

        for i in range(0, amount):
            self.bc_interface.send_asset(self.utxos.pop(), self.identity, recipient)


def main():
    pass

if __name__ == "__main__":
    main()