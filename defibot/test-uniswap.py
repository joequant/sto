#!/usr/bin/python3
import defibotlocal

dfb = defibotlocal.DefibotLocal()
print(dfb.test_uniswap())
u = dfb.uniswap_write()
print(u.get_weth_address())

