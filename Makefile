CONTAINER_LABEL := argyle_upwork

default: build

build: clean
	docker build -t $(CONTAINER_LABEL) .

run:
	docker run --rm -t -v --env-file .env `pwd`:/opt/app/upwork/output $(CONTAINER_LABEL)

interactive:
	docker run --rm -v `pwd`:`pwd` -w `pwd` -it $(CONTAINER_LABEL) /bin/bash
