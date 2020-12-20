#!/usr/bin/python3
import defibotlocal

dfb = defibotlocal.DefibotLocal()
web3 = dfb.web3()
# WBTC/ETH
contract = "0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852"

content = web3.geth.txpool.content()
print("get content")
for k, v in content['pending'].items():
    for k1, v1 in v.items():
        print(v1['to'], contract)
        if v1['to'] == contract:
            print(v1)


