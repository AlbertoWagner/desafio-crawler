#!/bin/sh

python manage.py makemigrations --fake-initial

python manage.py migrate --fake-initial

if [ "$MODE" = "production" ]; then
  python manage.py collectstatic --noinput -v 0
else
  python manage.py createsuperuser --noinput
fi


exec "$@"
