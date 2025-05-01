up:
	docker compose up --build -d

down:
	docker compose down

migrate:
	docker compose exec backend alembic upgrade head

dev:
	docker compose -f docker-compose.dev.yaml up --build -d
