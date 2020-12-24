#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --bind 0:8001 app.wsgi:application --reload -w ${GUNICORN_WORKERS:=1}