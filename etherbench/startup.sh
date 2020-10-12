#!/bin/bash
echo "starting"
if [ ! -z "${INSTANCE_NAME}" ] ; then
    export PS1="${INSTANCE_NAME}\\$ "
fi

if [ -e /home/user/startup.sh ] ; then
    echo "running user startup"
    pushd /home/user
    sudo -u user /bin/bash /home/user/startup.sh
    popd
fi

while :; do sleep 200000; done
