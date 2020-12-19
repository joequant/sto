#!/usr/bin/python3
import defibotlocal

dfb = defibotlocal.DefibotLocal()
print(dfb.test_pending())
web3 = dfb.web3()
new_transaction_filter = web3.eth.filter('pending')
print(new_transaction_filter.get_new_entries())
dfb.test_eventloop()

