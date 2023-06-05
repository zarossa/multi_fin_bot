#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn proj.wsgi:application --bind 0.0.0.0:8000 &

celery -A proj worker -l INFO &

celery -A proj beat -l INFO
