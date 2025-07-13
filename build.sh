#!/usr/bin/env bash
# Exit on error
set -o errexit
# Print commands and their arguments as they are executed
set -x

# Define the path to your Django project's requirements.txt
DJANGO_PROJECT_DIR="strong_app_project"
REQUIREMENTS_FILE="$DJANGO_PROJECT_DIR/requirements.txt"

echo "--- Starting Build Process ---"

echo "Current working directory: $(pwd)"
echo "Listing contents of the root directory:"
ls -la .

echo "Listing contents of the Django project directory: $DJANGO_PROJECT_DIR"
ls -la "$DJANGO_PROJECT_DIR"

echo "Checking if requirements.txt exists at $REQUIREMENTS_FILE..."
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "ERROR: requirements.txt not found at $REQUIREMENTS_FILE. Please ensure it exists."
    exit 1
fi

echo "Python version:"
python --version

echo "Pip version:"
python -m pip --version

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing Python dependencies from $REQUIREMENTS_FILE..."
python -m pip install -r "$REQUIREMENTS_FILE"

echo "Verifying installed packages after installation:"
python -m pip freeze

echo "--- Dependencies Installed. Proceeding with Django commands ---"

echo "Running Django migrations..."
# The manage.py script is at the root of the project (src on Render)
# We need to explicitly call it with the correct Python interpreter
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "--- Build Process Complete ---"
