FROM ubuntu
LABEL maintainer="Joseph Wang joequant@gmail.com"
COPY proxy.sh build-blocksci.sh /tmp/
RUN . /tmp/build-blocksci.sh
COPY config-blocksci.sh startup.sh /tmp/
RUN . /tmp/config-blocksci.sh

