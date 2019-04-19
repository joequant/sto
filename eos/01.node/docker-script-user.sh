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
git clone https://github.com/EOSIO/eos.git --recursive
pushd eos
curl https://github.com/EOSIO/eos/commit/f834f7fe4b150751123bed4da7f93445c85d24aa.patch | patch -p1
./scripts/eosio_build.sh -y
unset HOME
./scripts/eosio_install.sh
popd
export HOME=/home/`whoami`
git config --unset --global http.proxy || true
git config --unset --global http.sslVerify || true
git config --unset --global url."http://localhost:8080/".insteadOf || true
popd
