import os
import json5
import web3
from web3 import Web3
from uniswap import Uniswap
import requests
from requests.exceptions import HTTPError
import asyncio
import time

async def log_loop(defibot, event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            defibot.handle_event(event)
        await asyncio.sleep(poll_interval)

class Defibot:
    def __init__(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(script_dir, 'config.json')) as f:
            self._config = json5.load(f)
        self._uniswap = None
        self._web3 = None
    def config(self, s):
        return self._config[s]
    def web3(self):
        if self._web3 is None:
            self._web3 = Web3(Web3.HTTPProvider(self.config('provider')))
        return self._web3
    def uniswap(self):
        if self._uniswap is None:
            self._uniswap = Uniswap(self.config('address'),
                                    self.config('private_key'),
                                    web3=self.web3(),
                                    version=1)
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
    def handle_event(self, event):
        try:
            print(self.web3().eth.getTransaction(event.hex()))
        except web3.exceptions.TransactionNotFound:
            pass
        # and whatever

    def test_pending(self):
        web3 = self.web3()
        return web3.geth.txpool.content()
#transactions = [web3.eth.getTransaction(h) for h in transaction_hashes]
    def test_uniswap(self):
        s = ""
        s += self.uniswap().exchange_address_from_token(Web3.toChecksumAddress("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")) + "\n"
        s += repr(self.uniswap().get_fee_maker()) + "\n"
        return s
    def gasnow(self):
        response = requests.get('https://www.gasnow.org/api/v3/gas/price?utm_source=defibot')
        response.raise_for_status()
        return response.json()
    def test_eventloop(self):
        w3 = self.web3()
        block_filter = w3.eth.filter('latest')
        tx_filter = w3.eth.filter('pending')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(
                    log_loop(self, tx_filter, 2)))
        finally:
            loop.close()
