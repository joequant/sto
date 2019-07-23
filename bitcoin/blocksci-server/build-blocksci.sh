#!/bin/bash

. /tmp/proxy.sh

set -e

apt-get update && apt-get install -y software-properties-common python3-software-properties
add-apt-repository ppa:ubuntu-toolchain-r/test -y && apt-get update
apt install -y autoconf autogen build-essential c++17 catch clang cmake g++-8 gcc-8 git libargtable2-dev libboost-all-dev libboost-filesystem-dev libboost-iostreams-dev libboost-serialization-dev libboost-test-dev libboost-thread-dev libbz2-dev libcurl4-openssl-dev libgflags-dev libhiredis-dev libjemalloc-dev libjsoncpp-dev libjsonrpccpp-dev libjsonrpccpp-tools liblmdb-dev liblz4-dev libmicrohttpd-dev libsnappy-dev libsparsehash-dev libsqlite3-dev libssl-dev libtool libzstd-dev python3-dev python3-pip wget zlib1g-dev
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-8

if [ ! -z "$http_proxy" ] ; then
    git config --global http.proxy $http_proxy
    if [ ! -z "$GIT_PROXY" ] ; then
	git config --global url."$GIT_PROXY".insteadOf https://
    fi
    git config --global http.sslVerify false
fi

cd /root
git clone https://github.com/bitcoin-core/secp256k1
cd /root/secp256k1
sh ./autogen.sh
./configure --enable-module-recovery --enable-debug --prefix=/usr
make install
cd /root
git clone https://github.com/citp/BlockSci.git
cd /root/BlockSci
git config --global user.email "user@example.com"
git config --global user.name "Example User"
git submodule init
git submodule update --recursive
git fetch origin 'v0.6':'v0.6'
git checkout 'v0.6'
cd external/rocksdb
patch -p1 < /tmp/3736.patch
patch -p1 < /tmp/3870.patch
git commit -m "gcc8" .
cd ..
git commit -m "gcc8" rocksdb
cd /root/BlockSci
ln -s external libs
cp -r libs/range-v3/include/meta /usr/local/include
cp -r libs/range-v3/include/range /usr/local/include
mkdir -p /root/BlockSci/release
cd /root/BlockSci/external/rocksdb
make static_lib
make shared_lib
make install

cd /root/BlockSci/release
CC=gcc-8 CXX=g++-8 cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_INSTALL_PREFIX:PATH=/usr ..
make install

cd /root/BlockSci/
CC=gcc-8 CXX=g++-8 pip3 install -v --no-binary :all: --global-option build --global-option --debug -e blockscipy

mkdir /root/BlockSci/external/bitcoin-api-cpp/release
cd /root/BlockSci/external/bitcoin-api-cpp/release
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=/usr ..
make install

# Reset npm registry
git config --unset --global http.proxy || true
git config --unset --global http.sslVerify || true
git config --unset --global url."http://localhost:8080/".insteadOf || true
