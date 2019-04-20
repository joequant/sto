#!/bin/bash
set -e

export HOME=/home/user

if [[ ! -z "$http_proxy" ]] ; then
    npm config set registry http://registry.npmjs.org/
    npm set strict-ssl false
    yarn config set registry http://registry.yarnpkg.com/
    yarn config set strict-ssl false
fi

cd /home/user

git clone https://github.com/PolymathNetwork/polymath-core.git -b dev-3.0.0
pushd polymath-core
curl https://github.com/PolymathNetwork/polymath-core/commit/dc50fcb3778f37ab1f6fa580aa1b6fabb362e824.patch | patch -p1
cp /tmp/truffle-config.js .
yarn
truffle compile
pushd CLI
yarn
truffle compile
popd
popd

git clone https://github.com/simple-restricted-token/simple-restricted-token.git
pushd simple-restricted-token
cp /tmp/srt/truffle-config.js ./truffle-config.js
cp /tmp/srt/package.json ./package.json
yarn
truffle compile
popd

npm config delete registry
