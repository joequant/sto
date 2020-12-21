import os
import json5
import web3
from web3 import Web3
from uniswap import Uniswap
import requests
from requests.exceptions import HTTPError
import asyncio
import time

async def log_loop(defibot, contract, event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            defibot.handle_event(event, contract)
        await asyncio.sleep(poll_interval)

class Defibot:
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(script_dir, 'config.json')) as f:
            self._config = json5.load(f)
        self._uniswap = None
        self._uniswap_write = None
        self._web3 = None
        self._web3_write = None
        self._abi_cache = {}
        self.wait_async = 1
    def config(self, s):
        return self._config[s]
    def web3(self):
        if self._web3 is None:
            provider = self.config('provider')
            if "http:" in provider or "https:" in provider:
                self._web3 = Web3(Web3.HTTPProvider(provider))
            elif "ws:" in provider or "wss:" in provider:
                self._web3 = Web3(Web3.WebsocketProvider(provider))
        return self._web3
    def web3_write(self):
        if 'provider_write' not in self._config:
            return self.web3()
        if self._web3_write is None:
            provider = self.config('provider_write')
            if "http:" in provider or "https:" in provider:
                self._web3_write = Web3(Web3.HTTPProvider(provider))
            elif "ws:" in provider or "wss:" in provider:
                self._web3_write = Web3(Web3.WebsocketProvider(provider))
        return self._web3_write
    def uniswap(self):
        if self._uniswap is None:
            self._uniswap = Uniswap(self.config('address'),
                                    self.config('private_key'),
                                    web3=self.web3(),
                                    version=2)
        return self._uniswap
    def uniswap_write(self):
        if self._uniswap_write is None:
            self._uniswap_write = Uniswap(self.config('address'),
                                          self.config('private_key'),
                                          web3=self.web3_write(),
                                          version=2)
        return self._uniswap_write
    def uniswap_gql(self, query):
        return {}
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
    def handle_event(self, event, contract):
        try:
            txn = self.web3().eth.getTransaction(event.hex())
            if contract is None or (txn is not None and txn['to'] is not None \
                                    and txn['to'].lower() in contract):
                self.process_txn(event.hex(), txn)
        except web3.exceptions.TransactionNotFound:
            pass
        # and whatever
    def process_txn(self, txid, txn):
        print(txid, txn)
    def test_pending(self):
        web3 = self.web3()
        return web3.geth.txpool.content()
#transactions = [web3.eth.getTransaction(h) for h in transaction_hashes]
    def test_uniswap(self):
        s = ""
        s += repr(self.uniswap().get_fee_maker()) + "\n"
        return s
    def gasnow(self):
        response = requests.get('https://www.gasnow.org/api/v3/gas/price?utm_source=defibot')
        response.raise_for_status()
        return response.json()
    def get_abi(self, contract):
        if contract not in self._abi_cache:
            response = \
                requests.get("https://api.etherscan.io/api?module=contract&action=getabi&address={}".format(contract))
            response.raise_for_status()
            self._abi_cache[contract] = response.json()['result']
        return self._abi_cache[contract]
    def run_eventloop(self, contract=None):
        w3 = self.web3()
        block_filter = w3.eth.filter('latest')
        tx_filter = w3.eth.filter('pending')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(
                    log_loop(self, contract, tx_filter, self.wait_async)))
        finally:
            loop.close()
    def load(self, contracts):
        w3 = self.web3()
        for k,v in w3.geth.txpool.content()['pending'].items():
            for k1, v1 in v.items():
                if v1['to'] is not None and v1['to'].lower() in contracts:
                    self.process_txn(v1['hash'], v1)
    def data(self):
        return []
    def query(self, endpoint, query):
        request = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2', json={'query': query})
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
