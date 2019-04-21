#!/bin/bash
set -e
set -v

source "/tmp/proxy.sh"
npm install -g truffle --unsafe-perm
su user -p -c '/bin/bash /tmp/docker-script-user.sh'

