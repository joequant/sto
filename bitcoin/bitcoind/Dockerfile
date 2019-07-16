FROM joequant/cauldron
LABEL maintainer="Joseph Wang joequant@gmail.com"
COPY proxy.sh build-bitcoind.sh /tmp/
RUN . /tmp/build-bitcoind.sh
WORKDIR /var/lib/bitcoind


