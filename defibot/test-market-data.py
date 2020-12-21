#!/usr/bin/python3
from defibotlocal import DefibotLocal

dfbl = DefibotLocal()
print(dfbl.query("uniswap/uniswap-v2", """
query swaps{
  swaps(where:{transaction:"0x5ed0ee8ff25e0a368519ba10822d2f1d4261ca8cf3fe42b4f5806a515865d88f"}) {
    id
    timestamp
    amount0In
    amount1In
    amount0Out
    amount1Out
    sender
    to
    pair {
      token0 {
        id
        symbol
      }
      token1 {
        id
        symbol
      }
    }
  }
}
"""))

print(dfbl.query("uniswap/uniswap-v2", """
{
  tokens(where:{id:"0x6b175474e89094c44da98b954eedeac495271d0f"}) {
    id
    symbol
    name
    decimals
  }
}
"""))
print(dfbl.token_info("0x6B175474E89094C44Da98b954EedeAC495271d0F".lower()))
print(dfbl.pair_info("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
                     "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"))
