#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Use 'find' to locate manage.py if it's not in the root
MANAGE_PY=$(find . -name "manage.py" | head -n 1)

if [ -z "$MANAGE_PY" ]; then
    echo "Error: manage.py not found!"
    exit 1
fi

python "$MANAGE_PY" collectstatic --no-input
python "$MANAGE_PY" migrate

# Create superuser
python "$MANAGE_PY" shell << END
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
