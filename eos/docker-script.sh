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

dnf install -y --allowerasing --best --setopt=install_weak_deps=False --nodocs libedit-devel ncurses-devel
rpm -Uvh \
    http://download-ib01.fedoraproject.org/pub/fedora/linux/releases/28/Everything/x86_64/os/Packages/l/llvm4.0-4.0.1-5.fc28.x86_64.rpm \
    http://download-ib01.fedoraproject.org/pub/fedora/linux/releases/28/Everything/x86_64/os/Packages/l/llvm4.0-libs-4.0.1-5.fc28.x86_64.rpm \
    http://download-ib01.fedoraproject.org/pub/fedora/linux/releases/28/Everything/x86_64/os/Packages/l/llvm4.0-devel-4.0.1-5.fc28.x86_64.rpm

rpm -Uvh --nodeps http://download-ib01.fedoraproject.org/pub/fedora/linux/releases/28/Everything/x86_64/os/Packages/l/llvm4.0-static-4.0.1-5.fc28.x86_64.rpm
su user -p -c '/bin/bash /tmp/docker-script-user.sh'

npm config delete registry