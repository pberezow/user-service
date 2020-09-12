#!/bin/sh

#while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
#  >&2 echo "Waiting for postgres..."
#  sleep 1
#done
#echo "PostgreSQL started"

# Get id of container
export CONTAINER_ID=$(cut -c9-20 < /proc/1/cpuset)

python manage.py flush --no-input
python manage.py migrate
python manage.py initadmin

gunicorn user_service.wsgi

