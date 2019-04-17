#!/bin/bash
set -e
set -v
export http_proxy=http://172.17.0.1:3128/
export https_proxy=http://172.17.0.1:3128/
export ftp_proxy=http://172.17.0.1:3128/
export HTTP_PROXY=http://172.17.0.1:3128/
export PIP_INDEX_URL=http://localhost:3141/root/pypi/+simple/
export GIT_PROXY=http://localhost:8080/

if [[ ! -z "$http_proxy" ]] ; then
    npm config set registry http://registry.npmjs.org/
    npm install -g yarn
    npm set strict-ssl false
    yarn config set registry http://registry.yarnpkg.com/
    yarn config set strict-ssl false
fi

npm install -g truffle

dnf install -y --allowerasing --best --setopt=install_weak_deps=False --nodocs cmake

su user -p -c '/bin/bash /tmp/docker-script-user.sh'
npm config delete registry
