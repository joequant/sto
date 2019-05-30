#!/bin/bash
cd /root
rm -f ./rpycd.pid
python3 ./rpycd.py &
while true; do
    echo "Updating"
    blocksci_parser /root/blocksci_config update || true
    sleep 120
done
