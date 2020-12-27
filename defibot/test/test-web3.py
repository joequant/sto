#!/usr/bin/python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
import defibotlocal

dfb = defibotlocal.DefibotLocal(name="test-web3")
w3 = dfb.web3()
#dfb.load(["0x7a250d5630b4cf539739df2c5dacb4c659f2488d"])

dai = w3.toChecksumAddress("0x6b175474e89094c44da98b954eedeac495271d0f")
weth = w3.toChecksumAddress("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
u = dfb.uniswap()
def test_pair():
    pair = u.get_pair(weth, dai)
    assert (pair == "0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11")
#    print(u.get_k_last(pair))
    assert(u.get_amounts_in(1, [weth, dai]) == [1, 1])
    assert(len(u.get_amounts_out(1000000000, [dai, weth])) == 2)

"""
{'amountIn': 3750000000000000000,
 'amountOutEst': 12799092113258770,
 'amountOutMin': 5327018469003122896264,
 'deadline': 1609019139,
 'func': 'swapExactETHForTokens',
 'gas': 308475,
 'gasPrice': 63000000000,
 'pair': ['0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11',
          '0xAE461cA67B15dc8dc81CE7615e0320dA1A9aB8D5',
          '0xDfa42Ba0130425b21a1568507B084CC246fb0C8F'],
 'path': ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
          '0x6B175474E89094C44Da98b954EedeAC495271d0F',
          '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
          '0xc944E90C64B2c07662A292be6244BDf05Cda44a7'],
 'path.name': ['Wrapped Ether', 'Dai Stablecoin', 'USD//C', 'Graph Token'],
 'path.symbol': ['WETH', 'DAI', 'USDC', 'GRT'],
 'price.baseAB': 0.0034444257157076764,
 'price.baseBA': 290.324159246542,
 'price.estAB': 0.0034130912302023386,
 'price.estBA': 292.9895313524089,
 'reserves': [[68333106864607400847853786,
               105311186234758760560845,
               1609017939],
              [9944878483147073097114734, 10010759907320, 1609017932],
              [1697854455387, 3769696436800431426069318, 1609017938]],
 'timestamp': 1609017962.252856,
 'to': '0xc8cf5271d906b453132f0d9949c2672eb34dbdfe',
 'txid': '0xb26959559d83253824ea699c40ec36094b3258dd885cfe0de0f9104bb4081fa5'}
"""

def test_reserves():
    assert(len(u.get_reserves(
        '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        '0x6B175474E89094C44Da98b954EedeAC495271d0F'
    )) == 3)
    assert(len(u.get_amounts_out(
        3750000000000000000,
        ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
         '0x6B175474E89094C44Da98b954EedeAC495271d0F',
         '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
         '0xc944E90C64B2c07662A292be6244BDf05Cda44a7'])) == 4)


