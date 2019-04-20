#!/bin/bash
set -e
set -v

export HOME=/home/user
if [[ ! -z "$http_proxy" ]] ; then
    git config --global http.proxy $http_proxy
    if [[ ! -z "$GIT_PROXY" ]] ; then
	git config --global url."$GIT_PROXY".insteadOf https://
    fi
    git config --global http.sslVerify false
fi

cd /home/user

git clone https://github.com/PolymathNetwork/polymath-core.git -b dev-3.0.0
pushd polymath-core
curl https://github.com/joequant/polymath-core/commit/0032ffc1c3fbf3f3aa08c7daec2f3eff5457ec3d.patch | patch -p1
cp /tmp/truffle-config.js .
rm -f yarn.lock
yarn
truffle compile
rm -f yarn.lock
pushd CLI
rm -f yarn.lock
yarn
truffle compile
rm -f yarn.lock
popd
popd

git clone https://github.com/simple-restricted-token/simple-restricted-token.git
pushd simple-restricted-token
cp /tmp/srt/truffle-config.js ./truffle-config.js
cp /tmp/srt/package.json ./package.json
rm -f yarn.lock
yarn
truffle compile
rm -f yarn.lock
popd
git config --unset --global http.proxy || true
git config --unset --global http.sslVerify || true
git config --unset --global url."http://127.0.0.1:8080/".insteadOf || true
npm config delete registry

