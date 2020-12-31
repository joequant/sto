#!/usr/bin/python3
import defibot

def test_uniswap():
    dfb = defibot.Defibot()
    u = dfb.uniswap()
    assert (u.get_fee() == '0x0000000000000000000000000000000000000000')
    assert (u.get_weth_address() == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
    assert (len(u.get_reserves('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                               '0x329319eBE02Eac3DE77a9aa379d620bA653B2136')) == 3)
    assert (u.get_reserves_graphql('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                                   '0x329319eBE02Eac3DE77a9aa379d620bA653B2136',
                                   11548680) == [368376117274674840357, 1795233433826889826557050, 1608048232])

def test_prices():
    dfb = defibot.Defibot()
    assert(dfb.eth_price(11548680)== 723.4845356694213)
    # current price of USDT should be close to 1
    assert((dfb.token_price('0xdAC17F958D2ee523a2206206994597C13D831ec7') - 1.0) < 0.01)

def test_write():
    dfb = defibot.Defibot()
    u = dfb.uniswap_write()
