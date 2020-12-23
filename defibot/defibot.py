import os
import json5
import web3
from web3 import Web3
from uniswap.uniswap import UniswapV2Client
import requests
from requests.exceptions import HTTPError
import asyncio
import time
from functools import lru_cache
from dictcache import DictCache
import datetime

async def txn_loop(defibot, contract, event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            defibot.handle_txn(event, contract)
        await asyncio.sleep(poll_interval)

async def block_loop(defibot, event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            defibot.handle_block(event)
        await asyncio.sleep(poll_interval)

class Defibot:
    def __init__(self, suffix=""):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(script_dir, 'config.json')) as f:
            self._config = json5.load(f)
        self._uniswap = None
        self._uniswap_write = None
        self._web3 = None
        self._web3_write = None
        self._abi_cache = {}
        self.wait_async = 1
        self.token_cache = DictCache("token" + suffix)
        self.pair_cache = DictCache("pair" + suffix)
        self.deadline = 600.0
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
            self._uniswap = UniswapV2Client(self.config('address'),
                                            self.config('private_key'),
                                            provider=self.config('provider'))
        return self._uniswap
    def uniswap_write(self):
        if 'provider_write' not in self._config:
            return self.uniswap()
        elif self._uniswap_write is None:
            self._uniswap_write = UniswapV2Client(self.config('address'),
                                                  self.config('private_key'),
                                                  provider=self.config('provider_write'))
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
    def handle_txn(self, event, contract):
        try:
            txn = self.web3().eth.getTransaction(event.hex())
            if contract is None or (txn is not None and txn['to'] is not None \
                                    and txn['to'].lower() in contract):
                self.process_txn(event.hex(), txn)
        except web3.exceptions.TransactionNotFound:
            pass
        # and whatever
    def handle_block(self, event):
        print("block - ", event.hex());
    def process_txn(self, txid, txn):
        print(txid, txn)
    def test_pending(self):
        web3 = self.web3()
        return web3.geth.txpool.content()
#transactions = [web3.eth.getTransaction(h) for h in transaction_hashes]
    def test_uniswap(self):
        return {
            "fee": self.uniswap().get_fee(),
            "weth" : self.uniswap().get_weth_address()
            }
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
                    block_loop(self, block_filter, self.wait_async),
                    txn_loop(self, contract, tx_filter, self.wait_async)))
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
        request = requests.post('https://api.thegraph.com/subgraphs/name/{}'.format(endpoint), json={'query': query})
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    def token_info_lowered(self, token):
        if token not in self.token_cache:
            query = """
query tokens {
  tokens(where:{id:"%s"}) {
    id
    symbol
    name
    decimals
    tradeVolumeUSD
    totalLiquidity
  }
}
""" % token.lower()
            retval = self.query("uniswap/uniswap-v2", query)['data']['tokens']
            self.token_cache[token] = None if len(retval) == 0 else retval[0]
        return self.token_cache[token]
    def token_info(self, token):
        return self.token_info_lowered(token)
    def pair_info_lowered(self, token0, token1):
        if token0 + token1 not in self.pair_cache:
            self.pair_cache[token0 + token1] = self.uniswap().get_pair(token0, token1)
        return self.pair_cache[token0 + token1]
    def pair_info(self, token0, token1):
        return self.pair_info_lowered(token0, token1)
    def utcnow(self):
        return datetime.datetime.utcnow().timestamp()
    def trade(self, d):
        u = self.uniswap_write()
        action = d['action']
        to = d['to'] if 'to' in d else self.config('address')
        deadline = d['deadline'] if 'deadline' in d \
            else int(self.utcnow() + self.deadline)
        print(deadline)
        if action == "addLiquidity":
            return u.add_liquidity(
                d['tokenA'],
                d['tokenB'],
                d['amountADesired'],
                d['amountBDesired'],
                d['amountAMin'],
                d['amountBMin'],
                to,
                deadline
            )
        elif action == "addLiquidityETH":
            return u.add_liquidity_eth(
                d['token'],
                d['amountTokenDesired'],
                d['amountETH'],
                d['amountTokenMin'],
                d['amountETHMin'],
                to,
                deadline
            )
        elif action == "removeLiquidity":
            return u.remove_liquidity(
                d['tokenA'],
                d['tokenB'],
                d['liquidity'],
                d['amountAMin'],
                d['amountBMin'],
                to,
                deadline
            )
        elif action == "removeLiquidityETH":
            return u.remove_liquidity_eth(
                d['token'],
                d['liquidity'],
                d['amountTokenMin'],
                d['amountETHMin'],
                to,
                deadline
            )
        elif action == "removeLiquidityWithPermit":
            return u.remove_liquidity_with_permit(
                d['tokenA'],
                d['tokenB'],
                d['liquidity'],
                d['amountAMin'],
                d['amountBMin'],
                to,
                deadline,
                d['approveMax'],
                d['v'],
                d['r'],
                d['s']
            )
        elif action == "removeLiquidityETHWithPermit":
            return u.remove_liquidity_eth_with_permit(
                d['token'],
                d['liquidity'],
                d['amountTokenMin'],
                d['amountETHMin'],
                to,
                deadline,
                d['approveMax'],
                d['v'],
                d['r'],
                d['s']
            )
        elif action == "swapExactTokensForTokens":
            return u.swap_exact_tokens_for_tokens(
                d['amountIn'],
                d['amountOutMin'],
                d['path'],
                to,
                deadline
            )
        elif action == "swapTokensForExactTokens":
            return u.swap_exact_tokens_for_tokens(
                d['amountOut'],
                d['amountInMax'],
                d['path'],
                to,
                deadline
            )
        elif action == "swapExactETHForTokens":
            return u.swap_exact_eth_for_tokens(
                d['amountIn'],
                d['amountOutMin'],
                d['path'],
                to,
                deadline
            )
        elif action == "swapTokensForExactETH":
            return u.swap_exact_tokens_for_tokens(
                d['amountOut'],
                d['amountInMax'],
                d['path'],
                to,
                deadline
            )        
        elif action == "swapExactTokensForETH":
            return u.swap_exact_eth_for_tokens(
                d['amountIn'],
                d['amountOutMin'],
                d['path'],
                to,
                deadline
            )
        elif action == "swapETHForExactTokens":
            return u.swap_eth_for_exact_tokens(
                d['amountOut'],
                d['amountInMax'],
                d['path'],
                to,
                deadline
            )
        else:
            raise InvalidValue
