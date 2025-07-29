#!/usr/bin/env bash
# build.sh para Render

echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Aplicando migraciones..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput