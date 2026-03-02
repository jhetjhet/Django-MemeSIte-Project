#!/bin/sh
set -e  # Exit immediately on error

echo "ENV MODE: $ENV_MODE"

echo "Waiting for MySQL..."

for i in {1..30}; do
    if mysqladmin ping -h "mysql" --silent; then
        break
    fi
    sleep 2
done

echo "MySQL is ready."

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

exec "$@" # Execute the command passed as arguments to the container