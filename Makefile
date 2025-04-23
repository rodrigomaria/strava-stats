ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)
EXEC = docker exec -it strava-statistics

# HELP COMMANDS
help: ## show this help
	@echo 'usage: make [target]'
	@echo ''
	@echo 'Common sequence of commands:'
	@echo '- make build'
	@echo '- make run'
	@echo '- make jupyter'
	@echo '- make sh'
	@echo '- make bash'
	@echo '- make logs'
	@echo '- make stop'
	@echo '- make restart'
	@echo '- make black'
	@echo ''
	@echo 'targets:'
	@egrep '^(.+)\:\ .*##\ (.+)' ${MAKEFILE_LIST} | sed 's/:.*##/#/' | column -t -c 2 -s '#'

.PHONY : build
build: stop ## build application containers
ifeq ($(ARGS), nocache)
	@ docker-compose build --no-cache
else
	@ docker-compose build
endif

.PHONY : run
run: ## start the application
	@ docker-compose up -d

.PHONY: jupyter
jupyter: run ## execute jupyter notebook server directly in the container
	@ $(EXEC) jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

.PHONY: sh
sh: run ## runs pure shell on application container
	@ $(EXEC) sh

.PHONY: bash
bash: run ## runs pure shell on application container
	@ $(EXEC) bash

.PHONY: logs
logs: run ## show the logs on terminal
	@ docker logs -f strava-statistics

.PHONY: stop
stop: ## stop all docker compose services
	@ docker-compose down -v

.PHONY: restart
restart: ## stop and recreate the docker compose services
	@ make stop
	@ sleep 2
	@ make run

.PHONY: black
black: run ## run black over the code
	@ $(EXEC) /bin/sh -c "black ."