run-tests:
	docker-compose -f tests/docker-compose.testing.yml build --no-cache
	docker-compose -f tests/docker-compose.testing.yml up --attach tests --exit-code-from tests

tests-down:
	docker-compose -f tests/docker-compose.testing.yml down


run-tests-no-build:
	docker-compose -f tests/docker-compose.testing.yml up --attach tests --exit-code-from tests

up:
	make remove-all
	make build
	make start

build:
	docker-compose build --no-cache

start:
	docker-compose up -d

stop:
	docker-compose stop

remove:
	docker-compose down

remove-all:
	docker-compose down -v

force-remove:
	docker-compose down --remove-orphans -v
