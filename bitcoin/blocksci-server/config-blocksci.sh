#!/bin/bash
pip3 install --upgrade rpyc python-daemon lockfile Flask gevent bitcoin-etl
pip3 install --upgrade multiprocess psutil jupyterlab pycrypto matplotlib pandas dateparser

add-apt-repository -y ppa:bitcoin/bitcoin
apt-get update -y 
apt-get install -y bitcoind

mkdir /var/lib/blocksci
mkdir /root/apps
cd /tmp
cp startup.sh rpycd.py rpycd.conf app-server.py hello-world.py /root/apps
chmod a+x /root/apps/startup.sh
/usr/bin/blocksci_parser /root/apps/blocksci_config generate-config bitcoin /var/lib/blocksci --disk /var/lib/bitcoin -m -6
