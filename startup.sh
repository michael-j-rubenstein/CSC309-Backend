#!/bin/bash
pip3 install virtualenv
virtualenv -p `which python3` venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
DJANGO_SUPERUSER_PASSWORD=admin \
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@admin.com \
./manage.py createsuperuser \
--no-input