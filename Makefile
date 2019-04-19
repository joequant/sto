install-proxy:
	sudo dnf install squid python3-pip
	sudo pip3 install devpi-server
	sudo npm install -g git-cache-http-server
