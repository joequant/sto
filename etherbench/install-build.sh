source /tmp/proxy.sh
pushd /tmp
git clone --depth=1 https://github.com/ethereum/go-ethereum.git
pushd go-ethereum
make geth
popd
mv go-ethereum/build/bin/geth /usr/bin

#git clone --depth=1 https://github.com/openethereum/openethereum
#cd openethereum
#git submodule init
#git submodule update
#cargo build --release && cp target/release/openethereum /usr/bin
popd
