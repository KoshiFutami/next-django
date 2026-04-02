DC := docker compose

.PHONY: help up down restart ps logs build pull \
	bash-backend bash-db psql \
	migrate makemigrations test \
	pr pr-draft pr-web \
	commit review approve push

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
	@echo ""
	@echo "Git / GitHub:"
	@echo "  commit        git commit (staged changes required)"
	@echo "  push          git push -u origin HEAD"
	@echo "  pr            gh pr create --fill (needs gh)"
	@echo "  pr-draft      gh pr create --draft --fill"
	@echo "  pr-web        gh pr create --web"
	@echo "  review        gh pr view"
	@echo "  approve       gh pr review --approve"

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

pr:
	@command -v gh >/dev/null || (echo "gh が必要です: https://cli.github.com/ （例: brew install gh）" && false)
	gh pr create --fill

pr-draft:
	@command -v gh >/dev/null || (echo "gh が必要です: https://cli.github.com/" && false)
	gh pr create --draft --fill

pr-web:
	@command -v gh >/dev/null || (echo "gh が必要です: https://cli.github.com/" && false)
	gh pr create --web

commit:
	@if [ -z "$$(git diff --cached --name-only)" ]; then \
		echo "ステージされた変更がありません。git add してから再実行してください。"; \
		exit 1; \
	fi
	git commit

push:
	git push -u origin HEAD

review:
	@command -v gh >/dev/null || (echo "gh が必要です: https://cli.github.com/" && false)
	gh pr view

approve:
	@command -v gh >/dev/null || (echo "gh が必要です: https://cli.github.com/" && false)
	gh pr review --approve
