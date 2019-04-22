proxy-set:
	cp -f proxy.sh polymath
	cp -f proxy.sh polymath-dev
	cp -f proxy.sh basedev

proxy-install:
	sudo dnf install squid python3-pip
	sudo pip3 install devpi-server
	sudo npm install -g git-cache-http-server verdaccio

proxy-start:
	devpi-server > devpi-server.log &
	git-cache-http-server > git-cache-http-server.log &
	verdaccio > verdaccio.log &
