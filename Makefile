ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)
COMPOSE := $(shell docker compose version >/dev/null 2>&1 && echo "docker compose" || echo "docker-compose")
EXEC = docker exec -it strava-statistics
.PHONY : build run execute sh bash logs stop restart ruff audit env

# HELP COMMANDS
help: ## show this help
	@echo 'usage: make [target]'
	@echo ''
	@echo 'target:'
	@egrep '^(.+)\:\ .*##\ (.+)' ${MAKEFILE_LIST} | sed 's/:.*##/#/' | column -t -c 2 -s '#'

build: stop ## [nocache] build application containers
ifeq ($(ARGS), nocache)
	@ $(COMPOSE) build --no-cache
else
	@ $(COMPOSE) build
endif

run: ## start the application
	@ $(COMPOSE) up -d

execute: run ## execute jupyter notebook server directly in the container
	@ $(EXEC) jupyter notebook --ip=0.0.0.0 --port=8888 --port-retries=0 --no-browser --allow-root

sh: run ## runs pure shell on application container
	@ $(EXEC) sh

bash: run ## runs extended shell on application container
	@ $(EXEC) bash

logs: run ## show the logs on terminal
	@ docker logs -f strava-statistics

stop: ## stop all docker compose services
	@ $(COMPOSE) down -v

restart: ## stop and recreate the docker compose services
	@ make stop
	@ sleep 2
	@ make run

ruff: run ## run ruff over the code
	@ $(EXEC) /bin/sh -c "ruff check --fix"
	@ $(EXEC) /bin/sh -c "ruff format"

audit: ## run pip-audit package auditor on docker environment
	@ $(EXEC) /bin/sh -c "pip-audit --desc --format columns --aliases"

env: ## [STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET] create .env file with Strava credentials
	@echo "Creating .env file..."
	@if [ -z "$(STRAVA_CLIENT_ID)" ] || [ -z "$(STRAVA_CLIENT_SECRET)" ]; then \
		echo "Usage: make env STRAVA_CLIENT_ID=your_id STRAVA_CLIENT_SECRET=your_secret"; \
		exit 1; \
	fi
	@echo "STRAVA_CLIENT_ID=$(STRAVA_CLIENT_ID)" > .env
	@echo "STRAVA_CLIENT_SECRET=$(STRAVA_CLIENT_SECRET)" >> .env
	@echo ".env file created successfully with provided credentials."