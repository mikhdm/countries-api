up: migrate
	docker compose --profile app up --remove-orphans -d

down:
	docker compose --profile app down --remove-orphans

train: up
	docker exec -it app train

load: up
	docker exec -it app load

test: up
	docker exec -it app /venv/bin/pytest -c /app/pytest.ini

migrate:
	docker compose --profile migration run --rm migrate
