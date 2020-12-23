#!/usr/bin/python3
from defibotlocal import DefibotLocal

dfbl = DefibotLocal()
w3 = dfbl.web3()
r = dfbl.trade({
    "action": "addLiquidityETH",
    "token": w3.toChecksumAddress("0x4f96fe3b7a6cf9725f59d353f723c1bdb64ca6aa"),
    "amountTokenDesired": 0,
    "amountETH": 10000,
    "amountTokenMin": 0,
    "amountETHMin": 10000
    })
print(r.hex())
