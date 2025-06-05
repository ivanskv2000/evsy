up:
	docker compose up --build -d

down:
	docker compose down

migrate:
	docker compose exec backend alembic upgrade head

revision: # e. g. make revision name="add auth"
	docker compose exec backend alembic revision --autogenerate -m "$(name)"

dev:
	docker compose -f docker-compose.dev.yaml up --build -d