FROM ubuntu:eoan
LABEL maintainer="Joseph Wang joequant@gmail.com"
COPY proxy.sh build-blocksci.sh 3736.patch 3870.patch /tmp/
RUN . /tmp/build-blocksci.sh
COPY config-blocksci.sh startup.sh rpycd.py rpycd.conf app-server.py hello-world.py jupyter_notebook_config.py /tmp/
RUN . /tmp/config-blocksci.sh
