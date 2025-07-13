# strong_app_project/settings/production.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your_server_ip'] # آدرس‌های واقعی سرور شما

# Database (تنظیمات دیتابیس پروداکشن)
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME_PROD'),
        'USER': os.getenv('DB_USER_PROD'),
        'PASSWORD': os.getenv('DB_PASSWORD_PROD'),
        'HOST': os.getenv('DB_HOST_PROD'), # آدرس سرور دیتابیس پروداکشن
        'PORT': os.getenv('DB_PORT_PROD', '5432'),
    }
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

# Email settings (مثلاً برای ارسال ایمیل در محیط تولید)
# ...