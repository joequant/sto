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
    def pending_txns(self):
        return None
    def process(self, pending_list):
        return None
    def trade(self, trade_list):
        return None
    def run_once(self):
        pending = self.pending_txns()
        trades = self.process(pending)
        self.trade(trades)
