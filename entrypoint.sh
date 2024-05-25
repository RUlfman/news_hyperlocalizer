#!/bin/bash

# Check if the OpenAI API key is set
if ! grep -q "OPENAI_API_KEY" .env
then
  echo "The OpenAI API key is not set. Please enter it now:"
  read OPENAI_API_KEY
  echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env
fi

# Check if the SmartOcto API key is set
if ! grep -q "SMARTOCTO_API_KEY" .env
then
  echo "The SmartOcto API key is not set. Please enter it now:"
  read SMARTOCTO_API_KEY
  echo "SMARTOCTO_API_KEY=$SMARTOCTO_API_KEY" >> .env
fi

# Apply database migrations
python manage.py makemigrations --noinput
python manage.py migrate

# Create superuser if not exists
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'News1234')" | python manage.py shell
echo "from django.contrib.auth.models import User; User.objects.filter(username='api').exists() or User.objects.create_superuser('api', 'api@example.com', 'aP1')" | python manage.py shell

# Start Django server
python manage.py runserver 0.0.0.0:8000