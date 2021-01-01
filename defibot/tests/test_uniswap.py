#!/usr/bin/python3
import defibot

dfb = defibot.Defibot(name="test-uniswap")
u = dfb.uniswap()
def test_uniswap():
    assert (u.get_fee() == '0x0000000000000000000000000000000000000000')
    assert (u.get_weth_address() == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')
    assert (len(u.get_reserves('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                               '0x329319eBE02Eac3DE77a9aa379d620bA653B2136')) == 3)
    assert (u.get_reserves_graphql('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                                   '0x329319eBE02Eac3DE77a9aa379d620bA653B2136',
                                   11548680) == [368376117274674840357, 1795233433826889826557050, 1608048232])

def test_prices():
    assert(dfb.eth_price(11548680)== 723.4845356694213)
    # current price of USDT should be close to 1
    assert((dfb.token_price('0xdAC17F958D2ee523a2206206994597C13D831ec7') - 1.0) < 0.01)

def test_write():
    u = dfb.uniswap_write()

def test_amounts():
    assert(u.get_amounts_out(
        5000000000000000000,
        ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
         '0xb753428af26E81097e7fD17f40c88aaA3E04902c'],
        11564628) == [5000000000000000000, 17713957022299021312])
    assert(u.get_amounts_out_from_reserves(
        5000000000000000000,
        [[874023675905800463768, 3123514926223333812093, 1605434469]]) \
           == [5000000000000000000, 17713957022299021312])
    assert(u.get_amounts_in(
         1400000000000000000,
        ['0xb753428af26E81097e7fD17f40c88aaA3E04902c',
         '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'],
        11554934)  == [4626352242171670528, 1400000000000000000])
    assert(u.get_amounts_in_from_reserves(
         1400000000000000000,
        [[3223416058367995504345, 979786713651899511776, 1605434469]]) \
           == [4626352242171670528, 1400000000000000000])
