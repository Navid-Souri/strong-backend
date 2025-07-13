#!/usr/bin/env bash
# Exit on error
set -o errexit

# Ensure Python is available and use it to install dependencies
# Render's Python runtime usually makes 'python' or 'python3' available.
# We'll use 'python -m pip' for a more robust installation.

echo "Installing Python dependencies from requirements.txt..."
# Use the python interpreter to run pip, ensuring it's the correct one
python -m pip install --upgrade pip  # Upgrade pip first
python -m pip install -r requirements.txt # Install dependencies

echo "Running Django migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --no-input
