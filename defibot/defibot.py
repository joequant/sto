#!/usr/bin/python3
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
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler())

async def txn_loop(defibot, event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            defibot.handle_txn(event)
        await asyncio.sleep(poll_interval)

async def block_loop(defibot, event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            block = defibot.web3().eth.getBlock(event)
            defibot.handle_block(block)
        await asyncio.sleep(poll_interval)

def match_nocase(a, b):
    return a.lower() == b.lower()

def normalize_decimal(a, b):
    return a / pow(10, b)

ETH_DECIMALS=18

class Defibot:
    def __init__(self,
                 router=["0x7a250d5630b4cf539739df2c5dacb4c659f2488d"],
                 name=None):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.name = type(self).__name__ if name is None else name
        with open(os.path.join(script_dir, 'config.json')) as f:
            self._config = json5.load(f)
        self._uniswap = None
        self.router = router
        self._uniswap_write = None
        self._web3 = None
        self._web3_write = None
        self._abi_cache = {}
        self.wait_async = 1
        self.token_cache = DictCache("token-" + self.name)
        self.pair_cache = DictCache("pair-" + self.name)
        self.deadline = 600.0
        self.default_gas_price = \
            self.web3().toWei(15, "gwei")
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
            if 'provider_archive' in self._config:
                provider = self.config('provider_archive')
            else:
                provider = self.config('provider')
            self._uniswap = UniswapV2Client(self.config('address'),
                                            self.config('private_key'),
                                            provider=provider)
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
    def handle_txn(self, event, block_identifier='latest'):
        try:
            txn = self.web3().eth.getTransaction(event.hex())
            if self.router is None or \
               (txn is not None and txn['to'] is not None \
                and txn['to'].lower() in self.router):
                self.process_txn(event.hex(), txn, block_identifier)
        except web3.exceptions.TransactionNotFound:
            pass
        # and whatever
    def handle_block(self, event):
        print("block - ", event);
    def process_txn(self, txid, txn, block_identifier='latest'):
        print(txid, txn)
    def test_pending(self):
        web3 = self.web3()
        return web3.geth.txpool.content()
#transactions = [web3.eth.getTransaction(h) for h in transaction_hashes]
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
    def run_eventloop(self):
        w3 = self.web3()
        block_filter = w3.eth.filter('latest')
        tx_filter = w3.eth.filter('pending')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(
                    block_loop(self, block_filter, self.wait_async),
                    txn_loop(self, tx_filter, self.wait_async)))
        finally:
            loop.close()
    def load(self):
        w3 = self.web3()
        for k,v in w3.geth.txpool.content()['pending'].items():
            for k1, v1 in v.items():
                if v1['to'] is not None and v1['to'].lower() in self.router:
                    self.process_txn(v1['hash'], v1)
    def data(self):
        return []
    def query(self, endpoint, query):
        request = requests.post('https://api.thegraph.com/subgraphs/name/{}'.format(endpoint), json={'query': query})
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    def token_info_graphql(self, token):
        if token not in self.token_cache:
            query = """{
  token(id:"%s") {
    id
    symbol
    name
    decimals
    tradeVolumeUSD
    totalLiquidity
  }
}
""" % token.lower()
            try:
                retval = self.query("uniswap/uniswap-v2", query)
            except:
                logger.error("invalid query" + query)
            retval = retval['data']['token']
            self.token_cache[token] = retval
        return self.token_cache[token]
    def token_info(self, token):
        return self.token_info_graphql(token.lower())
    def pair_info(self, token0, token1):
        key = token0.lower() + token1.lower()
        if key not in self.pair_cache:
            self.pair_cache[key] = \
                self.uniswap().get_pair(token0, token1)
        return self.pair_cache[key]
    def now(self):
        return datetime.datetime.now().timestamp()
    def gasUse(self, d):
        if not isinstance(d, dict):\
           return None
        if 'func' not in d:
            return None
        func = d['func']
        if func in [
                'swapExactTokensForETH',
                'swapTokensForExactETH',
                'swapETHForExactTokens',
                'swapExactETHForTokens',
                'swapTokensForExactTokens',
                'swapExactTokensForTokens']:
            return 120000
    def backtest(self, block_start='latest',
                 block_finish='latest'):
        if block_start == 'latest':
            block_start = self.web3().eth.blockNumber
        if block_finish == 'latest':
            block_finish = self.web3().eth.blockNumber
        for i in range(block_start, block_finish+1):
            block = self.web3().eth.getBlock(i)
            for t in block['transactions']:
                logger.debug("txn - " + t.hex())
                self.handle_txn(t, i-1)
            self.handle_block(block)
    def get_balance(self, contract=None, block_identifier="latest"):
        if contract == self.uniswap().get_weth_address() or \
           contract is None:
            return self.web3().eth.getBalance(
                self.config('address'),
                block_identifier=block_identifier
            )
        else:
            erc20_contract = self.web3().eth.contract(
                address=self.web3().toChecksumAddress(contract),
                abi=self.uniswap().ERC20_ABI
            )
            return erc20_contract.functions.balanceOf(self.config('address')).call()
    def eth_price(self, block_identifier="latest"):
        u = self.uniswap()
        weth = u.get_weth_address()
        usdt = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
        usdt_decimals = int(self.token_info(usdt)['decimals'])
        reserve = u.get_reserves(u.get_weth_address(),
                                 usdt,
                                 block_identifier)
        return normalize_decimal(
            reserve[1]/reserve[0],
            usdt_decimals - ETH_DECIMALS
        )
    def token_price(self, token, block_identifier="latest"):
        u = self.uniswap()
        weth = u.get_weth_address()
        token_decimals = int(self.token_info(token)['decimals'])
        reserve = u.get_reserves(u.get_weth_address(),
                                 token,
                                 block_identifier)
        token_to_eth = normalize_decimal(
            reserve[0]/reserve[1],
            ETH_DECIMALS - token_decimals
        )
        return token_to_eth * self.eth_price(block_identifier)
    def trade(self, d):
        u = self.uniswap_write()
        action = d['action']
        to = d['to'] if 'to' in d else self.config('address')
        deadline = d['deadline'] if 'deadline' in d \
            else int(self.now() + self.deadline)
        u.gasPrice = d['gasPrice'] if 'gasPrice' \
            in d else self.default_gas_price
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

if __name__ == '__main__':
    dfb = Defibot()
    dfb.run_eventloop(["0x7a250d5630b4cf539739df2c5dacb4c659f2488d"])
