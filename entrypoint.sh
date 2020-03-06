#!/bin/sh

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  >&2 echo "Waiting for postgres..."
  sleep 1
done

echo "PostgreSQL started"


python manage.py flush --no-input
python manage.py migrate
python manage.py initadmin

set -m
gunicorn user_service.wsgi &
/opt/java/openjdk/bin/java -jar /sidecar/app.jar
fg %1

