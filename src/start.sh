#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --bind 0:9000 app.wsgi:application --reload -w 1