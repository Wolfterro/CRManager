run:
	@python manage.py runserver

run-lan:
	@python manage.py runserver 0.0.0.0:8000

run-web:
	@gunicorn CRManager.wsgi

shell:
	@python manage.py shell

migrate:
	@python manage.py migrate

makemigrations:
	@python manage.py makemigrations

test:
	@python manage.py test

install:
	@pip install -r requirements.txt
	@python manage.py migrate
	@python manage.py loaddata cr_manager_theme.json
	@python manage.py createsuperuser
	@python manage.py runserver
	@xdg-open http://localhost:8000 &

