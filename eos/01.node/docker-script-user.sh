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

pushd $HOME
git clone https://github.com/joequant/eos.git --recursive
pushd eos
./scripts/eosio_build.sh -y
unset HOME
./scripts/eosio_install.sh
popd
export HOME=/home/`whoami`
git config --unset --global http.proxy || true
git config --unset --global http.sslVerify || true
git config --unset --global url."http://localhost:8080/".insteadOf || true
popd
