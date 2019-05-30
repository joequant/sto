#!/bin/bash
while true; do
    echo "Updating"
    blocksci_parser /root/blocksci_config update >> /root/update.log
    sleep 120
done
