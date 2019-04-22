#!/bin/bash
set -e -v
source /tmp/proxy.sh
npm install -g truffle@v4
su user -p -c '/bin/bash /tmp/docker-script-user.sh'
