FROM joequant/basedev
COPY docker-script.sh docker-script-user.sh /tmp/
RUN source /tmp/docker-script-user.sh
COPY docker-script-user.sh /home/user
COPY truffle-config.js /home/user/polymath-core/
COPY truffle-config.js /home/user/simple-restricted-token/truffle.js
COPY srt-package.json /home/user/simple-restricted-token/package.json


