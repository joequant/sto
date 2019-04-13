#!/bin/bash
set -e
set -v

export HOME=/home/`whoami`
export PATH=$PATH:$HOME/bin

if [[ ! -z "$http_proxy" ]] ; then
    git config --global http.proxy $http_proxy
    if [[ ! -z "$GIT_PROXY" ]] ; then
	git config --global url."$GIT_PROXY".insteadOf https://
    fi
    git config --global http.sslVerify false
fi

pushd /home/user
git clone https://github.com/joequant/eos.git
pushd eos
git submodule update --init --recursive
./scripts/eosio_build.sh -y
popd

git clone https://github.com/joequant/eosio.cdt.git
pushd eosio.cdt
git submodule update --init --recursive
./build.sh
popd
git config --unset --global http.proxy || true
git config --unset --global http.sslVerify || true
git config --unset --global url."http://localhost:8080/".insteadOf || true
popd
