#!/bin/bash
set -e
set -v
source /tmp/proxy.sh

npm install -g truffle --unsafe-perm

dnf install -y --allowerasing --best --refresh \
        --setopt=install_weak_deps=False \
	--nodocs libedit-devel ncurses-devel git sudo procps-ng which \
	gcc gcc-c++ autoconf automake libtool make bzip2-devel wget \
	bzip2 compat-openssl10 graphviz doxygen openssl-devel \
	gmp-devel libstdc++-devel python2 python2-devel python3 \
	python3-devel libedit ncurses-devel swig libcurl-devel \
	libusb-devel patch

dnf upgrade -y --setopt=install_weak_deps=False --nodocs --allowerasing --best
rpm -Uvh \
    http://download-ib01.fedoraproject.org/pub/fedora/linux/releases/28/Everything/x86_64/os/Packages/l/llvm4.0-4.0.1-5.fc28.x86_64.rpm \
    http://download-ib01.fedoraproject.org/pub/fedora/linux/releases/28/Everything/x86_64/os/Packages/l/llvm4.0-libs-4.0.1-5.fc28.x86_64.rpm \
    http://download-ib01.fedoraproject.org/pub/fedora/linux/releases/28/Everything/x86_64/os/Packages/l/llvm4.0-devel-4.0.1-5.fc28.x86_64.rpm

rpm -Uvh --nodeps http://download-ib01.fedoraproject.org/pub/fedora/linux/releases/28/Everything/x86_64/os/Packages/l/llvm4.0-static-4.0.1-5.fc28.x86_64.rpm
su user -p -c '/bin/bash /tmp/docker-script-user.sh'
cd /home/user/eos && echo "master:$(git rev-parse HEAD)" > /etc/eosio-version
