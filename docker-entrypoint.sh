#!/bin/sh

# Wait for database to be ready (if using external database in the future)
# sleep 10

# Check if database exists
if [ ! -f "/app/database/db.sqlite3" ]; then
    echo "Creating new database..."
    python manage.py migrate
    echo "Creating superuser..."
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME:-admin}', '${DJANGO_SUPERUSER_EMAIL:-admin@admin.com}', '${DJANGO_SUPERUSER_PASSWORD:-admin}')" | python manage.py shell
else
    echo "Checking for pending migrations..."
    python manage.py migrate
fi

# Compile languages
echo "Compiling languages..."
python manage.py compilemessages

python manage.py collectstatic --noinput 

# Start server
exec "$@" 