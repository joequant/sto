FROM joequant/cauldron
COPY docker-script.sh docker-script-user.sh /tmp/
RUN source /tmp/docker-script.sh ; rm /tmp/*.sh
COPY docker-startup.sh /home/user
RUN chmod a+x /home/user/docker-startup.sh
CMD ["/home/user/docker-startup.sh"]
