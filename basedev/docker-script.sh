#!/bin/bash
useradd user
dnf install -y --allowerasing --best --setopt=install_weak_deps=False --nodocs git npm make gcc-c++ curl cmake llvm --refresh
npm install -g truffle@v4 yarn ganache-cli
su user -c '/bin/bash /tmp/docker-script-user.sh'

