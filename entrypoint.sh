#!/bin/sh

#while ! nc -z 127.0.0.1 5432; do
    echo "Waiting for postgres..."
    sleep 5
#done

echo "PostgreSQL started"


python manage.py flush --no-input
python manage.py migrate

exec "$@"
