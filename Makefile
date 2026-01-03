# Makefile para facilitar comandos comunes

.PHONY: help install run test migrate clean docker-up docker-down

help:
	@echo "Comandos disponibles:"
	@echo "  make install     - Instalar dependencias"
	@echo "  make run         - Ejecutar servidor de desarrollo"
	@echo "  make test        - Ejecutar pruebas unitarias"
	@echo "  make test-cov    - Ejecutar pruebas con reporte de cobertura"
	@echo "  make migrate     - Ejecutar migraciones"
	@echo "  make docker-up   - Levantar PostgreSQL con Docker"
	@echo "  make docker-down - Detener PostgreSQL"
	@echo "  make clean       - Limpiar archivos generados"
	@echo "  make lint        - Ejecutar linters (requiere ruff)"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest -v

test-cov:
	pytest --cov=app --cov-report=html --cov-report=term-missing

migrate:
	alembic upgrade head

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage

lint:
	ruff check app/ tests/
	ruff format --check app/ tests/
