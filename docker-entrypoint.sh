#!/bin/sh

# Wait for database to be ready (if using external database in the future)
# sleep 10

# Run database migrations
python manage.py migrate

# Start server
exec "$@" 