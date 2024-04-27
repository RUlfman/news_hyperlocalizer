#!/bin/bash

# Apply database migrations
python manage.py makemigrations --noinput
python manage.py migrate

# Create superuser if not exists
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'News1234')" | python manage.py shell
echo "from django.contrib.auth.models import User; User.objects.filter(username='api').exists() or User.objects.create_superuser('api', 'api@example.com', 'aP1')" | python manage.py shell

# Start Django server
python manage.py runserver 0.0.0.0:8000
