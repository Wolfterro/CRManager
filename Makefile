run:
	@python manage.py runserver

run-lan:
	@python manage.py runserver 0.0.0.0:8000

shell:
	@python manage.py shell

migrate:
	@python manage.py migrate

makemigrations:
	@python manage.py makemigrations

