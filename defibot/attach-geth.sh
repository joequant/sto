#!/bin/bash
IMAGE=$(podman ps | awk 'FNR >=2 {print $2" "$NF}' | grep ethereum | awk '{print $2}')
exec podman exec -it $IMAGE geth attach



