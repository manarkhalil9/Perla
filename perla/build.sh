#!/usr/bin/env bash
set -o errexit

source ./venv/bin/activate

pip install -r requirements.txt


python manage.py collectstatic --no-input


python manage.py migrate
