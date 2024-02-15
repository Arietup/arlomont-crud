#!/usr/bin/env bash
# exit on error
set -o errexit
python3 -c "import sys; print(sys.path)"
#poetry install

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate