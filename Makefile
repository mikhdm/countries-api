build:
	docker compose build app

up: migrate
	docker compose --profile app up --remove-orphans -d

down:
	docker compose --profile app down --remove-orphans

train: up
	docker exec -it app \
	/venv/bin/python /app/commands/train.py $(TRAIN_PATH) $(TEST_PATH)

load: up
	docker exec -it app \
		/venv/bin/python /app/commands/load.py $(LOAD_PATH)

test: up
	docker exec -it app /venv/bin/pytest -c /app/pytest.ini

migrate:
	docker compose --profile migration run --rm migrate

.PHONY: up down train load test migrate build