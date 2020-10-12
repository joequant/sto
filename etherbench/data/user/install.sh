git clone https://github.com/joequant/EnCore.git
git clone https://github.com/cVault-finance/CORE-v1.git
mkdir -p encore-contract
pushd encore-contract
truffle init
popd
cp -r EnCore/* encore-contract/contracts
cp truffle-config.js encore-contract # use compiler 0.6.12
pushd encore-contract
npm init -y
npm i --save @uniswap/v2-core
npm i --save @uniswap/v2-periphery
npm i --save @nomiclabs/buidler
npm i --save @openzeppelin/contracts-ethereum-package
npm i --save @openzeppelin/contracts
npm i --save truffle-hdwallet-provider
truffle compile
popd
pushd CORE-v1
npm i --save
popd
