#!/usr/bin/python3
import os
import json
from web3 import Web3
script_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(script_dir, 'config.json')) as f:
    config = json.load(f)
w3 = Web3(Web3.HTTPProvider(config['provider']))
print (w3.eth.blockNumber)

event_filter = w3.eth.filter({"address": Web3.toChecksumAddress(config['token']),
                              "fromBlock": "pending",
                              "toBlock": "pending"})

#transaction_hashes = web3.eth.getFilterChanges(web3_filter.filter_id)
#transactions = [web3.eth.getTransaction(h) for h in transaction_hashes]

