#!/bin/sh
set -e  # Exit immediately on error

echo "ENV MODE: $ENV_MODE"

# Run Django setup based on environment variables
if [ "$MAKE_MIGRATION" = "True" ]; then
    python manage.py makemigrations user main
fi

if [ "$MIGRATE" = "True" ]; then
    python manage.py migrate
fi

if [ "$COLLECTSTATIC" = "True" ]; then
    python manage.py collectstatic --noinput
fi

if [ "$ENV_MODE" = "production" ]; then
    echo "Running in production mode"
    gunicorn Memeniac.wsgi:application --bind 0.0.0.0:8000
elif [ "$ENV_MODE" = "daphne" ]; then
    echo "Running in daphne mode"
    daphne -b 0.0.0.0 -p 8080 Memeniac.asgi:application
else
    echo "Running in development mode"
    python manage.py runserver 0.0.0.0:8000
fi
