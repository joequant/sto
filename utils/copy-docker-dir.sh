#!/bin/bash
docker run \
       -v `pwd`:/mnt \
       $1 \
       cp -a -P -R $2 /mnt
