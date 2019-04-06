FROM joequant/basedev
COPY docker-script-user.sh /tmp/
RUN source /tmp/docker-script-user.sh
COPY docker-script-user.sh /home/user
USER user
CMD ["/bin/bash"]


