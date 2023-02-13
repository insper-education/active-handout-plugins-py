#!/bin/sh

docker-compose -f docker-compose.deploy.yml exec app python manage.py migrate --noinput
docker-compose -f docker-compose.deploy.yml exec app python manage.py collectstatic --no-input --clear