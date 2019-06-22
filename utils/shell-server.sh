#!/bin/bash
export LANG=C LC_ALL=C

if [ $# -ge 1 ]; then
    IMAGE=$($SUDO docker ps | tail -n +2 | grep $1 | awk '{print $NF}' )
    echo $IMAGE
else 
    IMAGE=$($SUDO docker ps | awk 'FNR==2 {print $NF}')
fi

exec $SUDO docker exec -it $IMAGE /bin/bash

