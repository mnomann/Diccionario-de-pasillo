# =============================================================================
# DESENREDA - Makefile
# Comandos utiles para desarrollo con Docker
# =============================================================================

# Variables
COMPOSE_FILE   := docker-compose.yml
BACKEND_DIR    := backend
FRONTEND_DIR   := frontend
DOCKER_COMPOSE := docker compose

.PHONY: help dev build down logs test seed shell-backend shell-db \
        clean restart ps prod build-backend build-frontend

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Inicia el entorno de desarrollo con docker compose up
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up --build

dev-detach: ## Inicia en segundo plano
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) up --build -d

build: ## Construye todas las imagenes
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) build

build-backend: ## Construye solo la imagen del backend
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) build backend

build-frontend: ## Construye solo la imagen del frontend
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) build frontend

down: ## Detiene y elimina contenedores, redes y volumenes
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down -v

stop: ## Detiene los contenedores sin eliminarlos
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) stop

logs: ## Muestra los logs de todos los servicios en tiempo real
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f

logs-backend: ## Muestra logs del backend
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f backend

logs-frontend: ## Muestra logs del frontend
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f frontend

logs-db: ## Muestra logs de la base de datos
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) logs -f db

test: ## Ejecuta los tests del backend dentro del contenedor
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec backend python -m pytest

test-backend: ## Ejecuta tests del backend
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec backend python -m pytest -v

test-frontend: ## Ejecuta tests del frontend
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec frontend npm run test

seed: ## Recarga los datos semilla en la base de datos
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec db psql -U desenreda -d desenreda -f /docker-entrypoint-initdb.d/02-seed.sql

shell-backend: ## Abre una shell interactiva en el contenedor backend
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec backend /bin/bash

shell-db: ## Abre psql en el contenedor de base de datos
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec db psql -U desenreda -d desenreda

clean: ## Limpia contenedores, imagenes y volumenes no utilizados
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) down -v --rmi all --remove-orphans
	docker system prune -f

restart: down dev ## Reinicia el entorno completo

ps: ## Muestra el estado de los contenedores
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) ps

migrate: ## Ejecuta migraciones de Alembic
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec backend alembic upgrade head

migrate-auto: ## Crea una nueva migracion automatica de Alembic
	@read -p "Nombre de la migracion: " name; \
	$(DOCKER_COMPOSE) -f $(COMPOSE_FILE) exec backend alembic revision --autogenerate -m "$$name"
