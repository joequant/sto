#!/bin/bash
set -e
set -v

export HOME=/home/`whoami`
export PATH=$PATH:$HOME/bin
export MAKEFLAGS=-j4

if [[ ! -z "$http_proxy" ]] ; then
    git config --global http.proxy $http_proxy
    if [[ ! -z "$GIT_PROXY" ]] ; then
	git config --global url."$GIT_PROXY".insteadOf https://
    fi
    git config --global http.sslVerify false
fi

pushd /home/user
git clone https://github.com/EOSIO/eosio.cdt.git
pushd eosio.cdt
curl https://github.com/EOSIO/eosio.cdt/commit/8f0cf0c6da12732071fd3caf8bb5afa0dadf637e.patch | patch -p1
git submodule update --init --recursive
./build.sh
popd
git config --unset --global http.proxy || true
git config --unset --global http.sslVerify || true
git config --unset --global url."http://localhost:8080/".insteadOf || true
popd
