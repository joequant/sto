#!/usr/bin/python3
from defibotlocal import DefibotLocal

dfbl = DefibotLocal()
def test_market_data():
    assert(dfbl.query("uniswap/uniswap-v2", """
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
""") == {'data': {'swaps': [{'amount0In': '35', 'amount0Out': '0', 'amount1In': '0', 'amount1Out': '0.10349616554278207', 'id': '0x5ed0ee8ff25e0a368519ba10822d2f1d4261ca8cf3fe42b4f5806a515865d88f-0', 'pair': {'token0': {'id': '0x6b175474e89094c44da98b954eedeac495271d0f', 'symbol': 'DAI'}, 'token1': {'id': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 'symbol': 'WETH'}}, 'sender': '0x7a250d5630b4cf539739df2c5dacb4c659f2488d', 'timestamp': '1602084507', 'to': '0x7a250d5630b4cf539739df2c5dacb4c659f2488d'}]}})
    assert(dfbl.query("uniswap/uniswap-v2", """
{
  tokens(where:{id:"0x6b175474e89094c44da98b954eedeac495271d0f"}) {
    id
    symbol
    name
    decimals
  }
}
""") == {'data': {'tokens': [{'decimals': '18', 'id': '0x6b175474e89094c44da98b954eedeac495271d0f', 'name': 'Dai Stablecoin', 'symbol': 'DAI'}]}})
    assert(dfbl.token_info("0x6B175474E89094C44Da98b954EedeAC495271d0F")['decimals'] == '18') 
    assert(dfbl.pair_info("0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
                     "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2") == '0xBb2b8038a1640196FbE3e38816F3e67Cba72D940')

