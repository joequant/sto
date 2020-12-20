#!/bin/bash
sudo urpmi python3-devel
pip install web3
pip install poetry
pip install pancake
pip install git+git://github.com/joequant/uniswap-python.git
pip install git+https://github.com/joequant/uniswap-v2-py.git
podman pull ethereum/client-go


