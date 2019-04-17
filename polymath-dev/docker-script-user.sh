#!/bin/bash
export HOME=/home/user
cd /home/user
git clone https://github.com/PolymathNetwork/polymath-core.git -b dev-3.0.0
pushd polymath-core
cp /tmp/truffle-config.js .
yarn
truffle compile
popd
git clone https://github.com/simple-restricted-token/simple-restricted-token.git
pushd simple-restricted-token
cp /tmp/RegulatedToken.sol contracts/token/R-Token
yarn
truffle compile
popd

