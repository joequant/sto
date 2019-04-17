target:
	docker build -t joequant/polymath3 . --no-cache

volume:
	../utils/copy-docker-dir.sh joequant/polymath3 /home/user
	docker volume create --driver local --opt device=`pwd`/user --opt type=none --opt o=bind user-volume-dev

volume-clean:
	docker volume rm user-volume-dev

