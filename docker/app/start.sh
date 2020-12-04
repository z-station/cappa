#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --bind 0:8001 cappa.wsgi:application --reload -w ${GUNICORN_WORKERS:=1}