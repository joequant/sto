#!/bin/bash
set -e
#export http_proxy=http://172.17.0.1:3128/
#export https_proxy=http://172.17.0.1:3128/
#export ftp_proxy=http://172.17.0.1:3128/
#export HTTP_PROXY=http://172.17.0.1:3128/
#export PIP_INDEX_URL=http://localhost:3141/root/pypi/+simple/
#export GIT_PROXY=http://localhost:8080/

useradd user
dnf install -y --allowerasing --best --setopt=install_weak_deps=False --nodocs git npm make gcc-c++ curl cmake llvm sudo --refresh
npm install -g truffle@v4 yarn modclean
su user -p -c '/bin/bash /tmp/docker-script-user.sh'
cat <<EOF > /etc/sudoers.d/90user
user ALL=(ALL) NOPASSWD:ALL
EOF

cat <<EOF >> /etc/dnf/dnf.conf
excludepkgs=filesystem
EOF
npm cache clean --force
pushd /usr/lib/node_modules
modclean -r -f
popd
