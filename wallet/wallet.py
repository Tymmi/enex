from utils import BigchainUtilities


class TokenWallet(object):

    def __init__(self, bc_db, identity=None):

        if identity is None:
            self.identity = BigchainUtilities.gen_random_keypair()
        else:
            self.identity = identity
        print("New wallet:\t", self.identity.public_key, self.identity.private_key)
        self.bc_interface = bc_db

        self.utxos = list()
        self.utxos.extend(self.bc_interface.get_utxos(self.identity.public_key))

    def send(self, amount, recipient):
        for i in range(0, amount):
            self.bc_interface.send_asset(self.utxos.pop(), self.identity, recipient)

    def issue(self, token):
        data = {
            "operation": "CREATE",
            "signer": self.identity,
            "asset": token
        }

        txid = self.bc_interface.create_asset(data)
        status = self.bc_interface.check_status(txid)

        if status["status"] == "valid" or status["status"] == "backlog":
            self.utxos.extend([txid])
            return txid
        else:
            return None

    def get_balance(self):
        return len(self.get_utxos())

    def get_utxos(self):
        return self.bc_interface.get_utxos(self.identity.public_key)


def main():
    pass

if __name__ == "__main__":
    main()