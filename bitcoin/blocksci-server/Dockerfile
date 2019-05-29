FROM ubuntu
LABEL maintainer="Allen Day allenday@allenday.com"
COPY proxy.sh build-blocksci.sh startup.sh update-blocksci.sh /tmp/
RUN . /tmp/build-blocksci.sh
WORKDIR /data
