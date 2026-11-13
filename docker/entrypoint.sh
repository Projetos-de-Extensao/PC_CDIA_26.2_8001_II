#!/bin/sh
# Runs on every container start (each deploy): migrations, static files,
# optional superuser and demo data, then the CMD (gunicorn).
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput 2>/dev/null \
        && echo "Superuser $DJANGO_SUPERUSER_USERNAME created." \
        || echo "Superuser $DJANGO_SUPERUSER_USERNAME already exists."
fi

if [ "$SEED_DEMO" = "true" ]; then
    python manage.py seed_demo
fi

exec "$@"
