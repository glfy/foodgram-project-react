#!/bin/bash


if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
# set -e


python manage.py migrate --noinput
python manage.py import_csv
python manage.py create_tags
python manage.py collectstatic --noinput

exec "$@"
