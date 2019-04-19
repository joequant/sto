#!/bin/bash
set -e
export HOME=/home/user
cd $HOME
git clone https://github.com/PolymathNetwork/polymath-core.git -b dev-2.2.0
pushd polymath-core
yarn
truffle compile
pushd CLI
yarn
truffle compile
popd
popd
git clone https://github.com/simple-restricted-token/simple-restricted-token.git
pushd simple-restricted-token
yarn
truffle compile
popd

