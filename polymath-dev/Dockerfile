FROM joequant/basedev
COPY docker-script.sh docker-script-user.sh truffle-config.js /tmp/
ADD srt /tmp/srt/
RUN source /tmp/docker-script.sh ; rm -rf /tmp/*
