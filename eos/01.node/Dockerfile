FROM joequant/basedev as builder
USER root
COPY docker-script.sh docker-script-user.sh config.ini nodeosd.sh /tmp/
RUN source /tmp/docker-script.sh
COPY docker-script-user.sh /home/user

FROM joequant/cauldron
COPY --from=builder /home/user/opt/eosio/bin /opt/eosio/bin
COPY --from=builder /tmp/config.ini /
COPY --from=builder /tmp/nodeosd.sh /opt/eosio/bin
COPY --from=builder /etc/eosio-version /etc
ENV EOSIO_ROOT=/opt/eosio
RUN chmod +x /opt/eosio/bin/nodeosd.sh
ENV LD_LIBRARY_PATH /usr/lib
ENV PATH /opt/eosio/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin


CMD ["/bin/bash"]


