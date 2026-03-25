#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
# Create a superuser if it doesn't exist (using environment variables)
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="$ADMIN_USERNAME").exists():
    User.objects.create_superuser("$ADMIN_USERNAME", "$ADMIN_EMAIL", "$ADMIN_PASSWORD")
END
