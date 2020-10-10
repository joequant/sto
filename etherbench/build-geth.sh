pushd /tmp
git clone --depth=1 https://github.com/ethereum/go-ethereum.git
pushd go-ethereum
make geth
popd
mv go-ethereum/build/bin/geth /usr/bin
popd
