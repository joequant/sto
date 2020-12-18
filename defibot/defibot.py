import os
import json
from web3 import Web3

class Defibot:
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(script_dir, 'config.json')) as f:
            self._config = json.load(f)
    def config(self, s):
        return self._config[s]
    def web3(self):
        return  Web3(Web3.HTTPProvider(self.config('provider')))
