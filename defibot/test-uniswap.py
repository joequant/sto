#!/usr/bin/python3
import defibotlocal

dfb = defibotlocal.DefibotLocal()
print(dfb.eth_price())
print(dfb.test_uniswap())
u = dfb.uniswap_write()
print(u.get_weth_address())
print(dfb.get_balance())
#SFI
print(dfb.get_balance('0xb753428af26e81097e7fd17f40c88aaa3e04902c'))
