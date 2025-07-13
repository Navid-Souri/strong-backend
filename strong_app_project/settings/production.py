# strong_app_project/settings/production.py
from .base import *
import os
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts for your deployed application
# Read ALLOWED_HOSTS from environment variable, split by comma
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# Database configuration for Render (PostgreSQL)
# This will unconditionally use the DATABASE_URL environment variable from Render
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=True # REQUIRED for Render's PostgreSQL
    )
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY') # MUST be loaded from environment variable

# HTTPS/SSL related settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files (for production, usually collected and served by WhiteNoise)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles_prod')

# CORS Headers settings for production
# This list should include the exact URL(s) of your deployed React frontend
CORS_ALLOWED_ORIGINS = [
    "https://your-react-app.vercel.app", # Replace with your Vercel domain
    "https://your-react-app.netlify.app", # Replace with your Netlify domain
    # Add your Render backend URL itself if it's accessed directly (e.g., for API testing)
    # "https://strong-app-backend.onrender.com",
]
