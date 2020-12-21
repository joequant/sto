#!/bin/bash
exec podman run -it -v ./data/ethereum:/root/.ethereum -p 8545:8545 -p 8546:8546 -p 30303:30303 -p 30304:30304 ethereum/client-go --http  --http.api web3,eth,personal,miner,net,txpool --http.addr "127.0.0.1" --graphql --cache=2048 --txpool.globalqueue=1000000
