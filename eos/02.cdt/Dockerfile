FROM joequant/basedev
USER root
COPY docker-script.sh docker-script-user.sh proxy.sh /tmp/
RUN source /tmp/docker-script.sh ; rm /tmp/*.sh
COPY docker-script-user.sh /home/user
USER user
CMD ["/bin/bash"]


