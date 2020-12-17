#!/usr/bin/python3
import os
import json
from uniswap import Uniswap
script_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(script_dir, 'config.json')) as f:
    config = json.load(f)
os.environ['PROVIDER'] = config['provider']

uniswap = Uniswap(config['address'],
                  config['private_key'],
                  version=2)
print(uniswap.get_fee_maker())
