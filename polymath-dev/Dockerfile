FROM joequant/basedev
COPY docker-script.sh docker-script-user.sh truffle-config.js RegulatedToken.sol /tmp/
RUN source /tmp/docker-script.sh
COPY truffle-config.js /home/user/simple-restricted-token/truffle.js
COPY srt-package.json /home/user/simple-restricted-token/package.json


