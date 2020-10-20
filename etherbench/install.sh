#!/usr/bin/env bash

set -e -v

mkimg="$(basename "$0")"
scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
container=$(buildah from joequant/cauldron)

buildah config --label maintainer="Joseph C Wang <joequant@gmail.com>" $container
buildah config --user root $container
mountpoint=$(buildah mount $container)

export rootfsDir=$mountpoint
export rootfsArg="--installroot=$mountpoint"
export rootfsRpmArg="--root $mountpoint"
export LC_ALL=C
export LANGUAGE=C
export LANG=C
name="joequant/etherbench"

set -e -v

cat <<EOF >> $rootfsDir/etc/dnf/dnf.conf
fastestmirror=true
max_parallel_downloads=15
EOF
if [ -e $rootfsDir/tmp/proxy.sh ]; then
    source $rootfsDir/tmp/proxy.sh
fi

dnf upgrade --best --nodocs --allowerasing --refresh -y \
    --setopt=install_weak_deps=False $rootfsArg

dnf --setopt=install_weak_deps=False --best --allowerasing install -v -y --nodocs $rootfsArg \
      npm \
      nodejs \
      golang \
      git \
      make \
      gcc-c++ \
      libudev-devel \
      libusb1-devel \
      glibc-devel \
      distcc \
      vim-minimal

# openethereum
#      cargo \
#      clang \
#      llvm-devel

buildah run $container -- npm install -g --unsafe-perm=true truffle ganache-cli solc

cp $scriptDir/*.sh $rootfsDir/tmp
chmod a+rwx $rootfsDir/tmp/*.sh
buildah run $container -- /bin/bash /tmp/install-build.sh
buildah run $container -- /bin/bash /tmp/install-user.sh

rpm --rebuilddb --root $rootfsDir
pushd $rootfsDir
rm -rf var/cache/*
rm -f lib/*.so lib/*.so.* lib/*.a lib/*.o
rm -rf usr/lib/.build-id usr/lib64/mesa
rm -rf usr/local usr/games
rm -rf usr/lib/gcc/*/*/32
#modclean seems to interfere with verdaccio
#https://github.com/verdaccio/verdaccio/issues/1883
popd

cp $scriptDir/startup.sh $rootfsDir/sbin/startup.sh
chmod a+rwx $rootfsDir/sbin/startup.sh
buildah config --user user $container
buildah config --cmd "/sbin/startup.sh" $container
buildah commit --format docker --rm $container $name

