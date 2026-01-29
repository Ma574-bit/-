#!/bin/sh
set -e

# Apply database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if env vars provided (optional)
if [ -n "${DJANGO_SUPERUSER_USERNAME}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL}" ]; then
  echo "Creating superuser..."
  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); username='${DJANGO_SUPERUSER_USERNAME}'; email='${DJANGO_SUPERUSER_EMAIL}'; password='${DJANGO_SUPERUSER_PASSWORD}';
if not User.objects.filter(username=username).exists(): User.objects.create_superuser(username, email, password)"
fi

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3
