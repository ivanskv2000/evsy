.PHONY: format lint test test-cov test-html dev

format:
	poetry run isort .
	poetry run black .

lint:
	poetry run flake8 .

# Тесты с покрытием
test:
	poetry run pytest --cov=app --cov-report=term --cov-report=html app/tests

# Тесты без покрытия (быстро)
test-fast:
	poetry run pytest app/tests

dev:
	poetry run uvicorn app.main:app --reload

seed:
	poetry run python -m app.seeds

drop-db:
	PYTHONPATH=./ poetry run python app/database/seeds/reset_db.py

reseed: drop-db seed