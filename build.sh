#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# This applies migrations to your Render PostgreSQL DB
python manage.py migrate

# This creates your login using the Env Vars you set in Render
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
import os
username = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_PASSWORD")
if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
END
