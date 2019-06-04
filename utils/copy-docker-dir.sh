#!/bin/bash
if [[ $# -ge 3 ]] ; then
    echo "Change directory to $3"
    cd $3
fi

docker run \
       -v `pwd`:/mnt \
       $1 \
       cp -a -P -R $2 /mnt
