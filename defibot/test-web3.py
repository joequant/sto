#!/usr/bin/python3
import defibot

dfb = defibot.Defibot()
web3 = dfb.web3()
print(web3.net.peer_count)
print(web3.eth.chainId)
print(web3.eth.blockNumber)
print(web3.eth.accounts)
print(web3.eth.syncing)

block = web3.eth.getBlock('latest')
print(block['number'])
print(web3.geth.txpool.inspect())
print(dfb.gasnow())



