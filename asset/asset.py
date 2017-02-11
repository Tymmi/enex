import hashlib
import random


class EnergyToken(object):

    @staticmethod
    def fetch(manufacturer, timestamp, source):
        id = hashlib.sha256(hex(random.getrandbits(256)).encode()).hexdigest()

        energy_token = {
            'data': {
                'id': id,
                'manufacturer': manufacturer,
                'timestamp': str(timestamp),
                'source': source
            }
        }
        return energy_token
