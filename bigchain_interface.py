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

    def create_asset(self, data):

        operation = data["operation"]
        signer = data["signer"]
        asset = data["asset"]

        # Prepare transaction
        prep_tx = self.conn.transactions.prepare(operation=operation,signers=signer.public_key,asset=asset["asset"],metadata=asset["metadata"])

        # Sign transaction
        signed_tx = self.conn.transactions.fulfill(prep_tx, signer.private_key)
        # Send transaction
        send_tx = self.conn.transactions.send(signed_tx)
        # Verify and return txid if successful
        if send_tx == signed_tx:
            return signed_tx["id"]
        else:
            return False

    def send_asset(self, txid, signer, recipient):

        prev_tx = self.conn.transactions.retrieve(txid)

        prepared_transfer_tx = self._craft_tx(prev_tx, recipient.public_key)

        fulfilled_transfer_tx = self.conn.transactions.fulfill(
            prepared_transfer_tx,
            private_keys=signer.private_key,
        )
        sent_transfer_tx = self.conn.transactions.send(fulfilled_transfer_tx)
        return sent_transfer_tx["id"]

    def check_transaction(self, txid):
        try:
            status = self.conn.transactions.status(txid)
            return status
        except:
            return None

    def check_status(self, txid):
        return self.conn.transactions.status(txid)

    def _craft_tx(self, prev_tx, recipient_pub_key):

        transfer_asset = {"id": None}
        if prev_tx["operation"] == "CREATE":
            transfer_asset["id"] = prev_tx["id"]
        elif prev_tx["operation"] == "TRANSFER":
            transfer_asset["id"] = prev_tx['asset']['id']

        output_index = 0
        output = prev_tx['outputs'][output_index]

        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output': output_index,
                'txid': prev_tx['id'],
            },
            'owners_before': output['public_keys']
        }
        return self.conn.transactions.prepare(operation="TRANSFER", asset=transfer_asset, inputs=transfer_input, recipients=recipient_pub_key)


def main():
    pass


if __name__ == "__main__":
    main()