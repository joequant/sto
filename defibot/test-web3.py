#!/usr/bin/python3
import defibotlocal

dfb = defibotlocal.DefibotLocal()
w3 = dfb.web3()
#dfb.load(["0x7a250d5630b4cf539739df2c5dacb4c659f2488d"])

dai = w3.toChecksumAddress("0x6b175474e89094c44da98b954eedeac495271d0f")
weth = w3.toChecksumAddress("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
u = dfb.uniswap()
pair = u.get_pair(weth, dai)
print(pair)
print(u.get_k_last(pair))
print(u.get_amounts_in(1, [weth, dai]))
print(u.get_amounts_out(1000000000, [dai, weth]))

