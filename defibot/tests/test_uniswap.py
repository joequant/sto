#!/usr/bin/python3
import defibotlocal

def test_uniswap():
    dfb = defibotlocal.DefibotLocal()
    u = dfb.uniswap()
    assert (u.get_fee() == '0x0000000000000000000000000000000000000000')
    assert (u.get_weth_address() == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
    assert (len(u.get_reserves('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                               '0x329319eBE02Eac3DE77a9aa379d620bA653B2136')) == 3)
    assert (u.get_reserves_graphql('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                                   '0x329319eBE02Eac3DE77a9aa379d620bA653B2136',
                                   11548680) == [368376117274674840357, 1795233433826889826557050, 1608048232])

