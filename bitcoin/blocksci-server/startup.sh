#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
cd /root/apps
rm -f ./rpycd.pid
python3 ./rpycd.py &
python3 ./app-server.py


