#!/bin/sh

# Wait for database to be ready (if using external database in the future)
# sleep 10

# Check if database exists
if [ ! -f "/app/database/db.sqlite3" ]; then
    echo "Creating new database..."
    python manage.py migrate
    echo "Creating superuser..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.com', 'admin')" | python manage.py shell
else
    echo "Database exists, running migrations..."
    python manage.py migrate
fi

# Start server
exec "$@" 