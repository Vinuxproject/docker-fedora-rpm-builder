SPECDIR := ./rpm
DOCKERNAME := fedora-rpm-builder

all: docker-build docker-run

docker-build:
	docker build -t $(DOCKERNAME) .

docker-run:
	docker run -v $(realpath $(SPECDIR)):/tmp/rpm -t $(DOCKERNAME)