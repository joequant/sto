#!/bin/bash
pip3 install --upgrade rpyc python-daemon lockfile

mkdir /var/lib/blocksci
mkdir /var/lib/bitcoin
cd /tmp
cp startup.sh rpycd.py rpycd.conf /root
chmod a+x /root/startup.sh
/usr/bin/blocksci_parser /root/blocksci_config generate-config bitcoin /var/lib/blocksci --disk /var/lib/bitcoin
