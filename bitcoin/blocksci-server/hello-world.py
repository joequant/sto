#!/usr/bin/python3
import blocksci
import pandas as pd
chain = blocksci.Blockchain("/root/apps/blocksci_config")

net_coins_per_block = chain.map_blocks(lambda block: block.net_address_type_value())

df = pd.DataFrame(net_coins_per_block).fillna(0).cumsum()/1e8
df = chain.heights_to_dates(df)
df = df.rename(columns={t:str(t) for t in df.columns})
df.to_csv("data.csv")
print(df)

