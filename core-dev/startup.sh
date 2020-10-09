#!/bin/bash
echo "starting"
if [ ! -z "${INSTANCE_NAME}" ] ; then
    export PS1="${INSTANCE_NAME}\\$ "
fi

while :; do sleep 200000; done
