target:
	docker build -t joequant/polymath . --no-cache

volume:
	../utils/copy-docker-dir.sh joequant/polymath /home/user
	docker volume create --driver local --opt device=`pwd`/user --opt type=none --opt o=bind user-volume

volume-clean:
	docker volume rm user-volume
