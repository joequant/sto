#!/bin/bash
sudo urpmi python3-devel
pip install web3
pip install poetry
pip install git+git://github.com/shanefontaine/uniswap-python.git
podman pull ethereum/client-go
podman run -it -v /home/joe/ethereum:/root/.ethereum -p 8545:8545 -p 8546:8546 -p 30303:30303 -p 30304:30304 ethereum/client-go --rpc  --rpcapi web3,eth,personal,miner,net,txpool --rpcaddr "127.0.0.1" --graphql >& ethereum.log &

