#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python tikitaster/manage.py collectstatic --no-input

python tikitaster/manage.py migrate