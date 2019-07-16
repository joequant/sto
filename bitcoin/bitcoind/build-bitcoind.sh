#!/bin/bash
set -e
. /tmp/proxy.sh

dnf install -y bitcoind sudo
dnf clean all
rm -f /var/log/*.log
rm -rf /var/cache/dnf/*
rm -rf /usr/lib/udev
rm -rf /usr/lib/.build-id
rm -rf /code

#remove systemd
#Prevent systemd from starting unneeded services
rm -f /usr/etc/systemd/system/*.wants/*
pushd /usr/lib/systemd

(cd system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done)
rm -f system/multi-user.target.wants/*
rm -f system/local-fs.target.wants/*
rm -f system/sockets.target.wants/*udev*
rm -f system/sockets.target.wants/*initctl*
rm -f system/basic.target.wants/*
rm -f system/anaconda.target.wants/*
rm -f *udevd* *networkd* *machined* *coredump*
popd
