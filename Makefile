DC := docker compose

.PHONY: help up down restart ps logs build pull \
	bash-backend bash-db psql \
	migrate makemigrations test

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Lifecycle:"
	@echo "  up            Start all containers in background"
	@echo "  down          Stop and remove containers"
	@echo "  restart       Restart all services"
	@echo "  ps            Show running containers"
	@echo "  logs          Tail compose logs"
	@echo "  build         Build images"
	@echo "  pull          Pull base images"
	@echo ""
	@echo "Shell:"
	@echo "  bash-backend  Enter backend container shell"
	@echo "  bash-db       Enter db container shell"
	@echo "  psql          Open psql in db container"
	@echo ""
	@echo "Backend:"
	@echo "  migrate       Run Django migrations"
	@echo "  makemigrations Create Django migration files"
	@echo "  test          Run backend pytest"

up:
	$(DC) up -d

down:
	$(DC) down

restart:
	$(DC) restart

ps:
	$(DC) ps

logs:
	$(DC) logs -f --tail=100

build:
	$(DC) build

pull:
	$(DC) pull

bash-backend:
	$(DC) exec backend sh

bash-db:
	$(DC) exec db sh

psql:
	$(DC) exec db psql -U showcase -d showcase

migrate:
	$(DC) exec backend python manage.py migrate

makemigrations:
	$(DC) exec backend python manage.py makemigrations

test:
	$(DC) exec backend pytest -q
