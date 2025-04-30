up:
	docker-compose up --build

down:
	docker-compose down

migrate:
	docker-compose exec backend alembic upgrade head
