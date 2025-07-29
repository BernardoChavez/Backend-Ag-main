#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r api/requirements.txt

# Ejecutar migraciones
python manage.py collectstatic --no-input
python manage.py migrate 