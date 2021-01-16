#!/usr/bin/python3
import os
import sys
import logging
import asyncio
import datetime
import requests
import pprint
from typing import Optional, Union, Dict, List, Sequence, cast
from uniswap.uniswap import UniswapV2Client
from hexbytes import HexBytes
import web3
from web3 import Web3
from web3.types import BlockIdentifier, TxData
import json5 # type: ignore
from dictcache import DictCache
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

numeric = Union[int, float]
zero_address = '0x0000000000000000000000000000000000000000'

async def txn_loop(defibot, event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            try:
                txn = defibot.web3().eth.getTransaction(event)
                defibot.handle_txn(txn)
            except web3.exceptions.TransactionNotFound:
                pass
            except Exception as exc:
                logger.error(traceback.format_exc())
                logger.error(exc)
        await asyncio.sleep(poll_interval)

async def block_loop(defibot, event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            block = defibot.web3().eth.getBlock(event)
            defibot.handle_block(block)
        await asyncio.sleep(poll_interval)

def match_nocase(a: str, b: str) -> bool:
    return a.lower() == b.lower()

def normalize_decimal(
        a: numeric,
        b: numeric) -> float:
    return a / pow(10, b)

def denormalize_decimal(
        a: numeric,
        b: numeric) -> int:
    return int(a * pow(10, b))

ETH_DECIMALS=18

class Defibot:
    def __init__(self,
                 router_config: str='uniswap',
                 name: Optional[str]=None):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.name = type(self).__name__ if name is None else name
        with open(os.path.join(script_dir, 'config.json')) as f:
            self._config = json5.load(f)
        self._uniswap: Optional[UniswapV2Client] = None
        self.router_config = router_config
        self._uniswap_write: Optional[UniswapV2Client] = None
        self._web3: Optional[Web3] = None
        self._web3_write: Optional[Web3] = None
        self._abi_cache: Dict[str, str] = {}
        self.wait_async = 1
        self.token_cache = DictCache("token-" + self.name)
        self.pair_cache = DictCache("pair-" + self.name)
        self.reserves_cache = DictCache("reserves-" + self.name)
        self.deadline = 1800.0
        self.default_gas_price = \
            self.web3().toWei(15, "gwei")
        self._weth_address: Optional[str] = None
        self.execute_trade = False
        self.router = [ self.uniswap().router_address ]

    def config(self, s):
        return self._config.get(s, None)

    def get_weth_address(self) -> str:
        if self._weth_address is None:
            self._weth_address = \
                self.uniswap().get_weth_address()
        return cast(str, self._weth_address)

    def web3(self) -> Web3:
        if self._web3 is None:
            provider = self.config('provider')
            if "http:" in provider or "https:" in provider:
                self._web3 = Web3(Web3.HTTPProvider(provider))
            elif "ws:" in provider or "wss:" in provider:
                self._web3 = Web3(Web3.WebsocketProvider(provider))
            else:
                raise NotImplementedError
        return self._web3
    def web3_write(self) -> Web3:
        if 'provider_write' not in self._config:
            return self.web3()
        if self._web3_write is None:
            provider = self.config('provider_write')
            if "http:" in provider or "https:" in provider:
                self._web3_write = Web3(Web3.HTTPProvider(provider))
            elif "ws:" in provider or "wss:" in provider:
                self._web3_write = Web3(Web3.WebsocketProvider(provider))
            else:
                raise NotImplementedError
        return self._web3_write
    def uniswap(self) -> UniswapV2Client:
        if self._uniswap is None:
            if 'provider_archive' in self._config:
                provider = self.config('provider_archive')
            else:
                provider = self.config('provider')
            self._uniswap = UniswapV2Client(
                self.config('address'),
                self.config('private_key'),
                provider=provider,
                router_config=self.router_config
            )
        return self._uniswap
    def uniswap_write(self) -> UniswapV2Client:
        if 'provider_write' not in self._config:
            return self.uniswap()
        if self._uniswap_write is None:
            self._uniswap_write = UniswapV2Client(
                self.config('address'),
                self.config('private_key'),
                provider=self.config('provider_write'),
                router_config=self.router_config
            )
        return self._uniswap_write
    def pending_txns(self):
        return None

    def handle_txn(self, txn: TxData, block_identifier: BlockIdentifier='latest'):
        if self.router is None or \
           (txn is not None and txn['to'] is not None \
            and txn['to'].lower() in self.router):
            self.process_txn(txn, block_identifier)

    def handle_block(self, event):
        print("block - ", event)
    def process_txn(self, txn: TxData,
                    block_identifier: BlockIdentifier='latest'):
        print(txn)

    def gasnow(self) -> Dict:
        response = requests.get('https://www.gasnow.org/api/v3/gas/price?utm_source=defibot')
        response.raise_for_status()
        return response.json()

    def get_abi(self, contract: str):
        if contract not in self._abi_cache:
            response = \
                requests.get("https://api.etherscan.io/api?module=contract&action=getabi&address={}".format(contract))
            response.raise_for_status()
            self._abi_cache[contract] = response.json()['result']
        return self._abi_cache[contract]
    def run_eventloop(self):
        logger.info("object %s", pprint.pformat(vars(self)))
        logger.info("current time %s", datetime.datetime.utcnow().isoformat()[:-3]+ 'Z')

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
                    self.process_txn(v1)
    def data(self):
        return []

    def query(self, endpoint: str, query: str) -> Dict:
        request = requests.post(
            'https://api.thegraph.com/subgraphs/name/{}'.format(endpoint),
            json={'query': query}
        )
        request.raise_for_status()
        return request.json()

    def token_info_graphql(self, token: str) -> Dict:
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
                logger.error('invalid query %s', query)
            retval = retval['data']['token']
            self.token_cache[token] = retval
        return self.token_cache[token]

    def token_info(self, token: str) -> Dict:
        return self.token_info_graphql(token.lower())

    def denormalize(self, a: numeric, token: str) -> int:
        decimals = int(self.token_info(token)['decimals'])
        return int(a * pow(10, decimals))

    def normalize(self, a: numeric, token: str) -> float:
        decimals = int(self.token_info(token)['decimals'])
        return float(a) / pow(10, decimals)

    def pair_info(self, token0: str, token1: str) -> str:
        key = token0.lower() + token1.lower()
        if key not in self.pair_cache:
            self.pair_cache[key] = \
                self.uniswap().get_pair(token0, token1)
        return self.pair_cache[key]
    def now(self):
        return datetime.datetime.now().timestamp()
    def gas_use(self, d: Dict):
        if not isinstance(d, dict):
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

    def backtest(self, block_start_id: BlockIdentifier='latest',
                 block_finish_id: Optional[BlockIdentifier]=None):
        block_start = self.web3().eth.blockNumber\
            if block_start_id == 'latest' else int(block_start_id)
        if block_finish_id is None:
            block_finish = block_start
        elif block_finish_id == 'latest':
            block_finish = self.web3().eth.blockNumber
        else:
            block_finish = int(block_finish_id)

        prev_execute_trade = self.execute_trade
        self.execute_trade = False
        for i in range(block_start, block_finish+1):
            block = self.web3().eth.getBlock(i)
            for t in block['transactions']:
                ht = cast(HexBytes, t)
                logger.debug("txn - %s", ht.hex())
                self.handle_txn(self.web3().eth.getTransaction(ht), i-1)
            self.handle_block(block)
        self.execute_trade = prev_execute_trade

    def get_balance(self, contract:Optional[str]=None,
                    normalize: bool =False,
                    block_identifier: BlockIdentifier="latest"):
        if contract is None or \
           contract.lower() == zero_address:
            balance = self.web3().eth.getBalance(
                self.config('address'),
                block_identifier=block_identifier
            )
            return normalize_decimal(balance, 18) if normalize else balance
        else:
            erc20_contract = self.web3().eth.contract(
                address=self.web3().toChecksumAddress(contract),
                abi=self.uniswap().ERC20_ABI
            )
            balance = erc20_contract.functions.balanceOf(self.config('address')).call()
            return self.normalize(balance, contract) if normalize else balance

    def eth_price(self,
                  qty: float=1.0,
                  block_identifier: BlockIdentifier="latest") -> numeric:
        usdt = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
        usdt_decimals = int(self.token_info(usdt)['decimals'])
        reserve = self.get_reserves(self.get_weth_address(),
                                    usdt,
                                    block_identifier)
        return normalize_decimal(
            reserve[1]/reserve[0],
            usdt_decimals - ETH_DECIMALS
        ) * qty
    def token_price(self, token :str, qty: float = 1.0,
                    block_identifier: BlockIdentifier="latest") -> Optional[numeric]:
        if match_nocase(token, self.get_weth_address()):
            return self.eth_price(qty, block_identifier)
        token_decimals = int(self.token_info(token)['decimals'])
        try:
            reserve = self.get_reserves(self.get_weth_address(),
                                        token,
                                        block_identifier)
        except:
            return None
        token_to_eth = normalize_decimal(
            reserve[0]/reserve[1],
            ETH_DECIMALS - token_decimals
        ) * qty
        return token_to_eth * self.eth_price(1.0, block_identifier)

    def get_reserves(self,
                     token_a: str, token_b: str,
                     block_identifier: BlockIdentifier) -> List[int]:
        if block_identifier == "latest":
            u = self.uniswap()
            return u.get_reserves(
                self.web3().toChecksumAddress(token_a),
                self.web3().toChecksumAddress(token_b),
                block_identifier)
        key = "%s%s%d" % (token_a.lower(),
                          token_b.lower(),
                          int(block_identifier))
        if key not in self.reserves_cache:
            u = self.uniswap()
            self.reserves_cache[key] = \
                u.get_reserves(token_a,
                               token_b,
                               block_identifier)
        return self.reserves_cache[key]

    def trade(self, d: Dict) -> str:
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
            ).hex()
        if action == "addLiquidityETH":
            return u.add_liquidity_eth(
                d['token'],
                d['amountTokenDesired'],
                d['amountETH'],
                d['amountTokenMin'],
                d['amountETHMin'],
                to,
                deadline
            ).hex()
        if action == "removeLiquidity":
            return u.remove_liquidity(
                d['tokenA'],
                d['tokenB'],
                d['liquidity'],
                d['amountAMin'],
                d['amountBMin'],
                to,
                deadline
            ).hex()
        if action == "removeLiquidityETH":
            return u.remove_liquidity_eth(
                d['token'],
                d['liquidity'],
                d['amountTokenMin'],
                d['amountETHMin'],
                to,
                deadline
            ).hex()
        if action == "removeLiquidityWithPermit":
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
            ).hex()
        if action == "removeLiquidityETHWithPermit":
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
            ).hex()
        if action == "swapExactTokensForTokens":
            return u.swap_exact_tokens_for_tokens(
                d['amountIn'],
                d['amountOutMin'],
                d['path'],
                to,
                deadline
            ).hex()
        if action == "swapTokensForExactTokens":
            return u.swap_tokens_for_exact_tokens(
                d['amountOut'],
                d['amountInMax'],
                d['path'],
                to,
                deadline
            ).hex()
        if action == "swapExactETHForTokens":
            return u.swap_exact_eth_for_tokens(
                d['amountIn'],
                d['amountOutMin'],
                d['path'],
                to,
                deadline
            ).hex()
        if action == "swapTokensForExactETH":
            return u.swap_tokens_for_exact_eth(
                d['amountOut'],
                d['amountInMax'],
                d['path'],
                to,
                deadline
            ).hex()
        if action == "swapExactTokensForETH":
            return u.swap_exact_tokens_for_eth(
                d['amountIn'],
                d['amountOutMin'],
                d['path'],
                to,
                deadline
            ).hex()
        if action == "swapETHForExactTokens":
            return u.swap_eth_for_exact_tokens(
                d['amountOut'],
                d['amountInMax'],
                d['path'],
                to,
                deadline
            ).hex()
        raise Exception("invalid action")

if __name__ == '__main__':
    dfb = Defibot()
    dfb.run_eventloop()
