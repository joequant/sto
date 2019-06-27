#!/bin/bash -f
export HOME=/root
cd /root/apps
for i in 540000 560000 580000 ; do
echo $i
/usr/bin/blocksci_parser /root/apps/blocksci_config generate-config bitcoin /var/lib/blocksci --disk /var/lib/bitcoin -m $i                                    
/usr/bin/blocksci_parser /root/apps/blocksci_config update                     
done
