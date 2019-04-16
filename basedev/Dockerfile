FROM joequant/cauldron
COPY docker-script.sh docker-script-user.sh /tmp/
RUN source /tmp/docker-script.sh ; rm /tmp/*.sh
COPY docker-script-user.sh /home/user

FROM scratch
COPY --from=0 / /
RUN chown user:user -R /home/user
USER user
CMD ["/bin/bash"]


