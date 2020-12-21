#!/bin/bash
exec podman run -it -v ./data/ipfs:/data/ipfs -p 5001:5001 ipfs/go-ipfs

