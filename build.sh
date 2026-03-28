#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Enter the Django project directory
cd backend/task_analyzer

# 3. Collect static files
python manage.py collectstatic --no-input

# 4. Apply database migrations
python manage.py migrate

# 5. Create superuser from environment variables (skips if already exists)
python manage.py shell << 'END'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL", "")
password = os.environ.get("ADMIN_PASSWORD")

if not username or not password:
    print("Skipping superuser creation: ADMIN_USERNAME or ADMIN_PASSWORD not set.")
elif User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists. Skipping.")
else:
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully.")
END
