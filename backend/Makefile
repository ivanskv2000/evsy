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
	poetry run pytest --cov=app --cov-report=term --cov-report=html tests

test-fast:
	poetry run pytest tests