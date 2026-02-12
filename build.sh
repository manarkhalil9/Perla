#!/usr/bin/env bash
set -o errexit

pip install -r perla/requirements.txt

python perla/manage.py collectstatic --no-input

python perla/manage.py migrate
