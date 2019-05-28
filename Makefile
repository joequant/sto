proxy-set:
	cp -f proxy.sh polymath
	cp -f proxy.sh polymath-dev
	cp -f proxy.sh basedev
	cp -f proxy.sh bitcoin/blocksci-server
	cp -f proxy.sh eos/01.node
	cp -f proxy.sh eos/02.cdt

proxy-install:
	sudo dnf install squid python3-pip
	sudo pip3 install devpi-server
	sudo npm install -g git-cache-http-server verdaccio

proxy-start:
	mkdir -p log
	devpi-server >> log/devpi-server.log 2>&1 &
	git-cache-http-server >> log/git-cache-http-server.log 2>&1 &
	verdaccio >> log/verdaccio.log 2>&1 &
