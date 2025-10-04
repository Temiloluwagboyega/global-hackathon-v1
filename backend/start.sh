#!/bin/bash

# Production startup script for Render deployment

echo "Starting Disaster Response API..."

# Check Python version
echo "Python version:"
python --version

# Run migrations (fake for MongoDB with djongo)
echo "Running migrations..."
python manage.py migrate --fake

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "Starting Gunicorn server..."
exec gunicorn disaster_response.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
