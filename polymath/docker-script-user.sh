#!/bin/bash
set -e
export HOME=/home/user
cd $HOME

if [[ ! -z "$http_proxy" ]] ; then
    git config --global http.proxy $http_proxy
    if [[ ! -z "$GIT_PROXY" ]] ; then
	git config --global url."$GIT_PROXY".insteadOf https://
    fi
    git config --global http.sslVerify false
fi

git clone https://github.com/PolymathNetwork/polymath-core.git -b dev-2.2.0
pushd polymath-core
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
rm -f yarn.lock
yarn
truffle compile
rm -f yarn.lock
popd

git config --unset --global http.proxy || true
git config --unset --global http.sslVerify || true
git config --unset --global url."http://127.0.0.1:8080/".insteadOf || true
