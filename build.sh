#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies from the root
pip install -r requirements.txt

# 2. Enter the backend directory where manage.py lives
cd backend/task_analyzer

# 3. Run Django commands
python manage.py collectstatic --no-input
python manage.py migrate

# 4. Create superuser
python manage.py shell << END
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get("ADMIN_USERNAME")
email = os.environ.get("ADMIN_EMAIL")
password = os.environ.get("ADMIN_PASSWORD")
if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser {username} created successfully.")
END
