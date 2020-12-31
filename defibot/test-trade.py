#!/usr/bin/python3
from defibotlocal import DefibotLocal

dfbl = DefibotLocal()
w3 = dfbl.web3()

#kovan
dai = w3.toChecksumAddress("0x4f96fe3b7a6cf9725f59d353f723c1bdb64ca6aa")
weth = w3.toChecksumAddress("0xc778417e063141139fce010982780140aa0cd5ab")
uw = dfbl.uniswap_write()
a = dfbl.trade({'action': 'swapETHForExactTokens',
 'amountInMax': 50000000000000000,
 'amountOut': 84892002913747888,
 'gasPrice': 80000000000,
 'path': ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
          '0xb753428af26E81097e7fD17f40c88aaA3E04902c']})
print(a.hex())


