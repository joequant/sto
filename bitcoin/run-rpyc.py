#!/usr/bin/python3

import rpyc
conn = rpyc.classic.connect('localhost')
rsys = conn.modules.sys
print(rsys.argv)

chain = conn.modules.blocksci.Blockchain("/root/blocksci_config")
blocks = chain.range('2019')

