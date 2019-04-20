install-proxy:
	sudo dnf install squid python3-pip
	sudo pip3 install devpi-server
	sudo npm install -g git-cache-http-server verdaccio

start-proxy:
	devpi-server > devpi-server.log &
	git-cache-http-server > git-cache-http-server.log &
	verdaccio > verdaccio.log &
