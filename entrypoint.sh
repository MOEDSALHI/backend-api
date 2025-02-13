#!/bin/bash

# Stop execution on error
set -e

echo "Appliquer les migrations..."
poetry run python manage.py migrate --noinput

echo "Collecte des fichiers statiques..."
poetry run python manage.py collectstatic --noinput

echo "Démarrage du serveur Django..."
exec poetry run python manage.py runserver 0.0.0.0:8000
