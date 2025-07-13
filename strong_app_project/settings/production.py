# strong_app_project/settings/production.py
from .base import *
import os
from dotenv import load_dotenv
import dj_database_url # Make sure dj-database-url is installed

load_dotenv() # Load environment variables from .env file (for local testing of production settings)

DEBUG = False

# Read ALLOWED_HOSTS from environment variable
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# Database (تنظیمات دیتابیس پروداکشن)
# Render provides DATABASE_URL, which dj_database_url can parse
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL_DEFAULT_LOCAL', 'sqlite:///db.sqlite3'), # Fallback for local testing
        conn_max_age=600,
        ssl_require=True # Required for Render's PostgreSQL
    )
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY') # حتماً از متغیر محیطی لود شود

# HTTPS/SSL تنظیمات مربوط به
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files (برای پروداکشن، معمولاً از جمع‌آوری استاتیک و سرور وب مثل Nginx استفاده میشه)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles_prod')

# CORS Headers settings for production
# این لیست را با URLهای واقعی فرانت‌اند خود در Vercel/Netlify به‌روز کنید
CORS_ALLOWED_ORIGINS = [
    "https://your-react-app.vercel.app", # Replace with your Vercel domain
    "https://your-react-app.netlify.app", # Replace with your Netlify domain
]
# اگر در production.py این را تعریف کنید، CORS_ALLOWED_ORIGINS در base.py را override می‌کند.
# اگر می‌خواهید هر دو (local و production) در یک لیست باشند، این را به base.py منتقل کنید
# و لیست را با هر دو URL پر کنید.