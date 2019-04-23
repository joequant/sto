#!/bin/bash
set -e
set -v
source /tmp/proxy.sh

npm install -g truffle eosjs --unsafe-perm
dnf install -y --allowerasing --best --setopt=install_weak_deps=False --nodocs cmake patch
su user -p -c '/bin/bash /tmp/docker-script-user.sh'
