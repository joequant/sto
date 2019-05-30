#!/bin/bash
while true; do
    echo "Updating"
    blocksci_parser /root/blocksci_config update
    sleep 60
done
