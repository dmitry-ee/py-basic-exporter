.EXPORT_ALL_VARIABLES:
APP_VERSION			= $(shell git describe --abbrev=0 --tags)
APP_NAME				= wt-bitmex-orderbook
DOCKER_ID_USER	= dmi7ry
BUILD_DIR				= $(shell pwd)

.ONESHELL:

all: build

build:
	export COMPOSE_PROJECT_NAME=$(APP_NAME) ;\
	docker-compose build

release:
	export APP_VERSION=latest ;\
	docker-compose build

run: build
	docker-compose up app

up: build
	docker-compose up -d app

stop:
	docker-compose stop app

shell:
	docker exec -it $(APP_NAME) bash

push-latest:
	export APP_VERSION=latest ;\
	docker-compose push

push:
	docker-compose push

publish: build push release push-latest
