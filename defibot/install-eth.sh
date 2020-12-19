#!/bin/bash
sudo urpmi python3-devel
pip install web3
pip install poetry
pip install git+git://github.com/joequant/uniswap-python.git
podman pull ethereum/client-go


