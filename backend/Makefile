.PHONY: format lint test test-cov test-html dev

APP_MODULE=app.main:app
HOST=0.0.0.0
PORT=8000

dev:
	poetry run uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT) --reload

run:
	poetry run uvicorn $(APP_MODULE) --host $(HOST) --port $(PORT)

migrate:
	poetry run alembic upgrade head

format:
	poetry run isort .
	poetry run black .

lint:
	poetry run flake8 .

test:
	@echo "Starting test database container..."
	@docker run --name evsy-db-test -e POSTGRES_USER=evsy_test -e POSTGRES_PASSWORD=evsy_test -e POSTGRES_DB=evsy_test -p 5433:5432 -d postgres:15-alpine > /dev/null
	@echo "Waiting for database to be ready..."
	@until docker exec evsy-db-test pg_isready -U evsy_test > /dev/null 2>&1; do sleep 1; done
	@echo "Database is ready. Running tests..."
	-@ENV=test poetry run pytest --cov=app --cov-report=term --cov-report=html tests
	@echo "Cleaning up..."
	@docker rm -f evsy-db-test > /dev/null

test-fast:
	@echo "Starting test database container..."
	@docker run --name evsy-db-test -e POSTGRES_USER=evsy_test -e POSTGRES_PASSWORD=evsy_test -e POSTGRES_DB=evsy_test -p 5433:5432 -d postgres:15-alpine > /dev/null
	@echo "Waiting for database to be ready..."
	@until docker exec evsy-db-test pg_isready -U evsy_test > /dev/null 2>&1; do sleep 1; done
	@echo "Database is ready. Running tests..."
	-@ENV=test poetry run pytest tests
	@echo "Cleaning up..."
	@docker rm -f evsy-db-test > /dev/null