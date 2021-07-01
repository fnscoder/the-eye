all: build migrate

up:
	docker-compose up

stop:
	docker-compose stop

build:
	docker-compose build --no-cache

test:
	docker-compose run --rm web python manage.py test

migrate:
	docker-compose run --rm web python manage.py migrate

collectstatic:
	docker-compose run --rm web python manage.py collectstatic

createuser:
	docker-compose run --rm web python manage.py createsuperuser
