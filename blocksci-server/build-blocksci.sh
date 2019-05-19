#!/bin/sh

. /tmp/proxy.sh

apt-get update && apt-get install -y software-properties-common python3-software-properties
add-apt-repository ppa:ubuntu-toolchain-r/test -y && apt-get update
apt install -y autoconf autogen build-essential c++17 catch clang-5.0 cmake g++-7 gcc-7 git libargtable2-dev libboost-all-dev libboost-filesystem-dev libboost-iostreams-dev libboost-serialization-dev libboost-test-dev libboost-thread-dev libbz2-dev libcurl4-openssl-dev libgflags-dev libhiredis-dev libjemalloc-dev libjsoncpp-dev libjsonrpccpp-dev libjsonrpccpp-tools liblmdb-dev liblz4-dev libmicrohttpd-dev libsnappy-dev libsparsehash-dev libsqlite3-dev libssl-dev libtool libzstd-dev python3-dev python3-pip wget zlib1g-dev
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 60 --slave /usr/bin/g++ g++ /usr/bin/g++-7
cd /root
git clone https://github.com/bitcoin-core/secp256k1
cd /root/secp256k1
sh ./autogen.sh
./configure --enable-module-recovery
make install
cd /root
git clone https://github.com/citp/BlockSci.git
cd /root/BlockSci
git submodule init
git submodule update --recursive
git fetch origin 'v0.6':'v0.6'
git checkout 'v0.6'
ln -s external libs
cp -r libs/range-v3/include/meta /usr/local/include
cp -r libs/range-v3/include/range /usr/local/include
mkdir -p /root/BlockSci/release
cd /root/BlockSci/external/rocksdb
make static_lib
make shared_lib
make install

cd /root/BlockSci/release
CC=gcc-7 CXX=g++-7 cmake -DCMAKE_BUILD_TYPE=Release ..
make install

cd /root/BlockSci/
CC=gcc-7 CXX=g++-7 pip3 install -e blockscipy

pip3 install --upgrade pip
pip3 install --upgrade multiprocess psutil jupyter pycrypto matplotlib pandas dateparser

mkdir /root/BlockSci/external/bitcoin-api-cpp/release
cd /root/BlockSci/external/bitcoin-api-cpp/release
cmake -DCMAKE_BUILD_TYPE=Release ..
make install
mkdir /data
