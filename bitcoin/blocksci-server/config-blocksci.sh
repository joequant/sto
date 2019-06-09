#!/bin/bash
pip3 install --upgrade rpyc python-daemon lockfile Flask gevent bitcoin-etl

mkdir /var/lib/blocksci
mkdir /var/lib/bitcoin
mkdir /root/apps
cd /tmp
cp startup.sh rpycd.py rpycd.conf app-server.py /root/apps
chmod a+x /root/apps/startup.sh
/usr/bin/blocksci_parser /root/apps/blocksci_config generate-config bitcoin /var/lib/blocksci --disk /var/lib/bitcoin
