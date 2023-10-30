#!/bin/sh

python manage.py makemigrations

python manage.py migrate


if [ "$MODE" = "production" ]; then
  python manage.py collectstatic --noinput -v 0
else
  python manage.py createsuperuser --noinput
fi


exec "$@"
