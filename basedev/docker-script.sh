#!/bin/bash
set -e
: '
export http_proxy=http://192.168.1.139:3128/
export https_proxy=http://192.168.1.139:3128/
export ftp_proxy=http://192.168.1.139:3128/
export HTTP_PROXY=http://192.168.1.139:3128/
export PIP_INDEX_URL=http://localhost:3141/root/pypi/+simple/
export GIT_PROXY=http://localhost:8080/
'

useradd user
dnf install -y --allowerasing --best --setopt=install_weak_deps=False --nodocs git npm make gcc-c++ curl sudo patch --refresh
npm install -g yarn modclean
cat <<EOF > /etc/sudoers.d/90user
user ALL=(ALL) NOPASSWD:ALL
EOF

# filesystem
# replacing chkconfig will fail on dockerhub
cat <<EOF >> /etc/dnf/dnf.conf
excludepkgs=filesystem,chkconfig
EOF
npm cache clean --force
pushd /usr/lib/node_modules
modclean -r -f
popd
dnf autoremove -y urpmi
dnf clean all
rm -f /var/log/*.log
rm -rf /code
