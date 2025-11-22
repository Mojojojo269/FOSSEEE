import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create test user
username = 'testuser'
password = 'testpass123'

if not User.objects.filter(username=username).exists():
    User.objects.create_user(username=username, password=password, email='test@example.com')
    print(f"Test user created: {username} / {password}")
else:
    print(f"Test user already exists: {username}")
