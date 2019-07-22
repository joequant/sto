#!/bin/bash
. /tmp/proxy.sh

#add-apt-repository -y ppa:bitcoin/bitcoin
#apt-get update -y
#apt-get install -y bitcoind
apt-get install -y graphviz gdb google-perftools

pip3 install --upgrade rpyc python-daemon lockfile Flask gevent bitcoin-etl
pip3 install --upgrade multiprocess psutil jupyterlab pycrypto matplotlib pandas dateparser \
     graphviz python-rocksdb sqlalchemy yep pybind11 sortedcontainers \
     seaborn

mkdir -p /var/lib/bitcoin
mkdir -p /var/lib/blocksci
mkdir -p /root/apps

cd /tmp
cp startup.sh rpycd.py rpycd.conf app-server.py hello-world.py jupyter_notebook_config.py /root/apps
chmod a+x /root/apps/startup.sh
/usr/bin/blocksci_parser /root/apps/blocksci_config generate-config bitcoin /var/lib/blocksci --disk /var/lib/bitcoin -m -6
