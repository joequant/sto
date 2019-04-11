#!/bin/bash
cd /home/user
git clone https://github.com/PolymathNetwork/polymath-core.git -b dev-2.2.0
pushd polymath-core
yarn
truffle compile
popd
git clone https://github.com/simple-restricted-token/simple-restricted-token.git
pushd simple-restricted-token
yarn
truffle compile
popd

