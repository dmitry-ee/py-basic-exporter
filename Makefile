.EXPORT_ALL_VARIABLES:
APP_VERSION			= $(shell git describe --abbrev=0 --tags)
APP_NAME				= py-basic-exporter
DOCKER_ID_USER	= dmi7ry
BUILD_DIR				= $(pwd)

.ONESHELL:

all: build

build:
	docker build --squash -t $(DOCKER_ID_USER)/$(APP_NAME):$(APP_VERSION) -f docker/Dockerfile .

push:
	docker push $(DOCKER_ID_USER)/$(APP_NAME):$(APP_VERSION)

publish: build push
