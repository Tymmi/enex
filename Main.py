from bigchaindb_driver import BigchainDB

from utils import BigchainUtilities

PUSHTX = True

class BigchainConnection(object):

    # docker run --rm -v "/storage/bigchaindb_docker:/data" -ti bigchaindb/bigchaindb -y configure rethinkdb

    # docker run -v "/storage/bigchaindb_docker:/data" -d --name bigchaindb -p "58080:8080" -p "59984:9984" bigchaindb/bigchaindb start

    # http://localhost:59984/api/v1/transactions/007ff51453a3a0814f47dcc6521c913c962c7cf66f90eb67f5dc8acbf05b956d

    # http://localhost:58080/

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

    bigDB = BigchainConnection("http://localhost", 59984)

    alice, bob = BigchainUtilities.gen_random_keypair(), BigchainUtilities.gen_random_keypair()

    print("ALICE: " + alice.public_key + "\t" + alice.private_key)
    print("  BOB: " + bob.public_key + "\t" + bob.private_key)

    i = 0
    while True:
        energy_token = {
            'data': {
                'kwh': {
                    'id': str(i),
                    'manufacturer': 'vattenfall'
                }
            }
        }

        i += 1

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
        status = bigDB.conn.transactions.status(txid)
        print(status)


if __name__ == "__main__":
    main()