COMPOSE = docker compose

up:
	$(COMPOSE) up --build

down:
	$(COMPOSE) down

start:
	$(COMPOSE) start

stop:
	$(COMPOSE) stop

logs:
	$(COMPOSE) logs -f

migrate:
	$(COMPOSE) exec backend python manage.py migrate

makemigrations:
	$(COMPOSE) exec backend python manage.py makemigrations

shell:
	$(COMPOSE) exec backend python manage.py shell

clean:
	$(COMPOSE) down --rmi local

fclean:
	$(COMPOSE) down --volumes --rmi all

prune: fclean
	docker system prune -a --volumes -f

re: fclean up