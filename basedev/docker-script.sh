#!/bin/bash
useradd user
dnf install -y --allowerasing --best --setopt=install_weak_deps=False --nodocs git npm make gcc-c++ curl cmake llvm sudo --refresh
npm install -g truffle@v4 yarn ganache-cli
su user -c '/bin/bash /tmp/docker-script-user.sh'
cat <<EOF > /etc/sudoers.d/90user
user ALL=(ALL) NOPASSWD:ALL
EOF

cat <<EOF >> /etc/dnf/dnf.conf
excludepkgs=filesystem
EOF
