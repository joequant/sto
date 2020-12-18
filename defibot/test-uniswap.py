#!/usr/bin/python3
import os
import json
from uniswap import Uniswap
import defibot
from web3 import Web3

dfb = defibot.Defibot()

uniswap = Uniswap(dfb.config('address'),
                  dfb.config('private_key'),
                  web3=dfb.web3(),
                  version=1)
print(uniswap.exchange_address_from_token(Web3.toChecksumAddress("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")))
print(uniswap.get_fee_maker())
