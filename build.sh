#!/usr/bin/env bash
set -o errexit # Exit on error
set -x         # Print commands for debugging

echo "--- Starting Django Backend Build Process ---"

echo "Current working directory: $(pwd)"
echo "Listing contents of the current directory (should be my-backend/):"
ls -la .

echo "Python version:"
python --version

echo "Pip version:"
python -m pip --version

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing Python dependencies from requirements.txt..."
# requirements.txt is directly in the root of this repo (my-backend/)
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found in the root of my-backend folder. Please ensure it exists."
    exit 1
fi
python -m pip install -r requirements.txt

echo "Verifying installed packages after installation:"
python -m pip freeze

echo "--- Dependencies Installed. Proceeding with Django commands ---"

echo "Running Django migrations..."
# manage.py is directly in the root of this repo (my-backend/)
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --no-input

# --- NEW: Create Superuser if CREATE_SUPERUSER environment variable is set to True ---
if [[ "$CREATE_SUPERUSER" == "True" ]]; then
  echo "Creating Django superuser..."
  # Ensure the environment variables are passed to the createsuperuser command
  # --no-input prevents interactive prompts
  # You need to ensure your manage.py is at the root of your project,
  # if your project structure is different, adjust the path accordingly.
  python manage.py createsuperuser --no-input \
    --username="$DJANGO_SUPERUSER_USERNAME" \
    --email="$DJANGO_SUPERUSER_EMAIL" || true # Using || true to prevent build failure if user already exists
fi
# --- END NEW SUPERUSER CODE ---

echo "--- Django Backend Build Process Complete ---"
