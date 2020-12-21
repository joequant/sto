#!/usr/bin/python3
from defibotlocal import DefibotLocal

dfbl = DefibotLocal()
print(dfbl.query("https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2", """
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

