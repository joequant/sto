#!/bin/bash

pushd /data
blocksci_parser blocksci_config generate-config bitcoin /data --disk /var/lib/bitcoin
popd
