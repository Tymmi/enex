from bigchaindb_driver import BigchainDB

from utils import BigchainUtilities

PUSHTX = False

class BigchainConnection(object):

    def __init__(self, url, port):

        self.conn = BigchainDB(url + ":" + str(port))

    def create_asset(self, signer_key, operation, signers, asset, metadata):

        # Prepare transaction
        prep_tx = self.conn.transactions.prepare(
            operation=operation,
            signers=signers,
            asset=asset,
            metadata=metadata
        )

        print("Prepared tx")

        # Sign transaction
        signed_tx = self.conn.transactions.fulfill(prep_tx, signer_key)

        print("Signed tx")

        # Send transaction
        send_tx = self.conn.transactions.send(signed_tx)

        print("Sent tx")

        # Verify and return txid if successful
        if send_tx == signed_tx:
            return signed_tx["id"]
        else:
            return False

    def check_status(self, txid):

        return self.conn.transactions.status(txid)


def main():

    bigDB = BigchainConnection("http://vanilla.ipdb.foundation", 9984)

    alice, bob = BigchainUtilities.gen_random_keypair(), BigchainUtilities.gen_random_keypair()

    energy_token = {
        'data': {
            'kwh': {
                'id': '0',
                'manufacturer': 'vattenfall'
            }
        }
    }

    metadata = {'location': 'NL'}

    if PUSHTX == True:
        txid = bigDB.create_asset(alice.private_key,
            operation="CREATE",
            signers=alice.public_key,
            asset=energy_token,
            metadata=metadata
        )
        print("success: " + txid)

    print("checking status")
    status = bigDB.conn.transactions.status("6d527d02c7d0cea0652fb2c4adaff16548a6f3ffbcbf6fb7be7a4f7433dbd3a5")
    print(status)

if __name__ == "__main__":
    main()