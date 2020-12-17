#!/bin/bash
sudo urpmi python3-devel
pip install web3
pip install poetry
pip install git+git://github.com/shanefontaine/uniswap-python.git
podman pull ethereum/client-go
podman run -it -v /home/joe/local3/ethereum:/root/.ethereum -p 30303:30303 ethereum/client-go >& ethereum.log &

