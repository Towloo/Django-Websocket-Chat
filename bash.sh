#!/usr/bin/env bash
python manage.py makemigrations
python manage.py migrate
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    (python manage.py createsuperuser --no-input)
fi
python manage.py collectstatic
daphne -e ssl:443:privateKey=cert/key.key:certKey=cert/cert.crt assessment.asgi:application