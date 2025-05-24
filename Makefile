up:
	docker compose up --build -d

down:
	docker compose down

migrate: # e. g. make revision name="add auth"
	docker compose exec backend alembic upgrade head

revision:
	docker compose exec backend alembic revision -m "$(name)"

dev:
	docker compose -f docker-compose.dev.yaml up --build -d