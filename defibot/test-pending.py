#!/usr/bin/python3
import defibotlocal

dfb = defibotlocal.DefibotLocal()
web3 = dfb.web3()

contract = ["0x7a250d5630b4cf539739df2c5dacb4c659f2488d"]
dfb.test_eventloop(contract)
