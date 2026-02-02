#!/bin/bash
set -e

echo "Waiting for database..."
sleep 5

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting development server..."
exec python manage.py runserver 0.0.0.0:8000