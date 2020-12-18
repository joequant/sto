import os
import json5
from web3 import Web3
from uniswap import Uniswap

class Defibot:
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(script_dir, 'config.json')) as f:
            self._config = json5.load(f)
        self._web3 = Web3(Web3.HTTPProvider(self.config('provider')))
        self._uniswap = Uniswap(self.config('address'),
                                self.config('private_key'),
                                web3=self.web3(),
                                version=1)
    def config(self, s):
        return self._config[s]
    def web3(self):
        return self._web3
    def uniswap(self):
        return self._uniswap
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
    def test_pending(self):
        event_filter = \
            self._web3.eth.filter({"address":
                                  Web3.toChecksumAddress(self.config('token')),
                                  "fromBlock": "pending",
                                  "toBlock": "pending"})
#transaction_hashes = web3.eth.getFilterChanges(web3_filter.filter_id)
#transactions = [web3.eth.getTransaction(h) for h in transaction_hashes]
    def test_uniswap(self):
        print(self.uniswap().exchange_address_from_token(Web3.toChecksumAddress("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")))
        print(self.uniswap().get_fee_maker())