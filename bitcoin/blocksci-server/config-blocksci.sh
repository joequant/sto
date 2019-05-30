#!/bin/bash
mkdir /var/lib/blocksci
mkdir /var/lib/bitcoin
cp /tmp/startup.sh /root/startup.sh
chmod a+x /root/startup.sh
/usr/bin/blocksci_parser /root/blocksci_config generate-config bitcoin /var/lib/blocksci --disk /var/lib/bitcoin
