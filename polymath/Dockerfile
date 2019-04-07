FROM joequant/basedev
COPY docker-script-user.sh /tmp/
RUN source /tmp/docker-script-user.sh
COPY docker-script-user.sh /home/user
COPY truffle-config.js /home/user/polymath-core/
USER user
CMD ["/bin/bash"]


