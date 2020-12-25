#!/usr/bin/python3
from defibotlocal import DefibotLocal

dfbl = DefibotLocal()
w3 = dfbl.web3()

#kovan
dai = w3.toChecksumAddress("0x4f96fe3b7a6cf9725f59d353f723c1bdb64ca6aa")
weth = w3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab")
uw = dfbl.uniswap_write()
#pair = uw._create_pair(dai, weth).hex()
#print(pair)
print(uw.get_pair(dai, weth))

r = dfbl.trade({
    "action": "addLiquidityETH",
    "token": dai,
    "amountTokenDesired": 10000000,
    "amountETH": 1000000,
    "amountTokenMin": 10000,
    "amountETHMin": 10000
    })
print(r.hex())

r = dfbl.trade({
    "action": "removeLiquidityETH",
    "token": dai,
    "liquidity": 10000,
    "amountTokenMin": 1000,
    "amountETHMin": 1000
    })
print(r.hex())

