#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --bind 0:8999 app.wsgi:application --reload -w 1