DC := docker compose

.PHONY: help up down restart ps logs build pull \
	bash-backend bash-db psql \
	migrate makemigrations test \
	lint-backend lint-backend-fix pre-commit-install \
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
	@echo "  lint-backend      Ruff (check + format --check) on backend/ (要: python3 -m pip install -r backend/requirements-dev.txt)"
	@echo "  lint-backend-fix  Ruff で自動修正（check --fix + format 書き込み）"
	@echo "  pre-commit-install  pip install pre-commit && pre-commit install（ルート）"
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

lint-backend:
	@python3 -m ruff --version >/dev/null 2>&1 || (echo "ruff が必要です: python3 -m pip install -r backend/requirements-dev.txt" && false)
	cd backend && python3 -m ruff check . && python3 -m ruff format --check .

lint-backend-fix:
	@python3 -m ruff --version >/dev/null 2>&1 || (echo "ruff が必要です: python3 -m pip install -r backend/requirements-dev.txt" && false)
	cd backend && python3 -m ruff check . --fix && python3 -m ruff format .

pre-commit-install:
	python3 -m pip install -q pre-commit
	python3 -m pre_commit install

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
