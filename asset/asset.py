import hashlib
import random


class EnergyToken(object):

    @staticmethod
    def fetch(data):
        id = hashlib.sha256(hex(random.getrandbits(256)).encode()).hexdigest()

        energy_token = {
            'data': {
                'id': id,
                'manufacturer': data["manufacturer"],
                'timestamp': data["timestamp"],
                'source': data["source"]
            }
        }
        return energy_token
