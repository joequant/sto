#!/bin/bash
cd /home/user
git clone https://github.com/PolymathNetwork/polymath-core.git -b dev-2.2.0
cd polymath-core
yarn
truffle compile

