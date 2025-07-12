# strong_app_project/settings/local.py
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '10.0.2.2']
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # آدرس فرانت‌اند React شما
]

# Database (برای توسعه، می‌تونه SQLite باشه یا PostgreSQL لوکال)
# اگه از PostgreSQL استفاده می‌کنی، اطلاعات دیتابیس لوکالت رو اینجا بذار
# و از python-dotenv برای امنیت اطلاعات حساس استفاده کن
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'your_local_db_name'),
        'USER': os.getenv('DB_USER', 'your_local_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'your_local_password'),
        'HOST':os.getenv('DB_HOST','localhost'),
        'PORT':os.getenv('DB_PORT','5432')
    }
}

# Optional: تنظیمات اضافی فقط برای محیط توسعه
# مثلاً برای Django Debug Toolbar اگه نصب کردی