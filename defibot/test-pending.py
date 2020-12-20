#!/usr/bin/python3
import defibotlocal

dfb = defibotlocal.DefibotLocal()
print(dfb.test_pending())
web3 = dfb.web3()
dfb.test_eventloop()

