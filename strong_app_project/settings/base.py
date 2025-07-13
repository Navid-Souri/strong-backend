# strong_app_project/settings/base.py
from datetime import timedelta
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '..', '.env'))

# مسیر اصلی پروژه
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # برای محیط production
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_dev')] # برای فایل‌های استاتیک در توسعه

# --- تنظیمات امنیتی و پایه ---

SECRET_KEY = os.getenv('SECRET_KEY', 'your-insecure-default-secret-key-for-testing-only-change-this-in-production')
# ^^^ مهم: در محیط پروداکشن حتماً از یک SECRET_KEY امن در متغیر محیطی استفاده کنید!

DEBUG = False # پیش‌فرض برای base.py روی False است. در local.py آن را True کنید.

ALLOWED_HOSTS = [] # در local.py و production.py این لیست را پر کنید


# --- اپلیکیشن‌ها ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt', # برای احراز هویت با JWT
    #'corsheaders', # اگر نیاز به Cross-Origin Resource Sharing دارید، این را اضافه کنید و پیکربندی کنید

    # Your apps (اینها را پس از ایجاد با startapp اضافه کنید)
    'core',
    'accounts',
    'workouts',
    'progress_tracking',
    'corsheaders', # اگر از corsheaders استفاده می‌کنید
    'django_filters',
]


# --- میان‌افزارها (Middleware) ---

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # اضافه کنید
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# --- تنظیمات URL و Templates ---

ROOT_URLCONF = 'strong_app_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'strong_app_project.wsgi.application'
ASGI_APPLICATION = 'strong_app_project.asgi.application' # برای استفاده از ASGI (مثلاً با channels)


# --- دیتابیس ---

# از متغیرهای محیطی برای تنظیمات دیتابیس استفاده کنید
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}




# --- احراز هویت و اعتبارسنجی رمز عبور ---

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# --- بین‌المللی‌سازی (Internationalization) ---

LANGUAGE_CODE = 'fa-ir' # برای زبان فارسی

TIME_ZONE = 'Asia/Tehran' # برای منطقه زمانی ایران

USE_I18N = True # فعال‌سازی سیستم بین‌المللی‌سازی جنگو

USE_L10N = True # فعال‌سازی سیستم بومی‌سازی جنگو (برای فرمت اعداد و تاریخ)

USE_TZ = True # فعال‌سازی پشتیبانی از تایم‌زون‌ها


# --- فایل‌های استاتیک (CSS, JavaScript, Images) ---

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # محل جمع‌آوری فایل‌های استاتیک در تولید
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_dev'), # محل فایل‌های استاتیک شما در توسعه
]


# --- فایل‌های مدیا (فایل‌های آپلودی کاربر) ---

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # محل ذخیره فایل‌های آپلودی


# --- تنظیمات Django REST Framework ---

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', # برای راحتی تست در مرورگر
        'rest_framework.authentication.BasicAuthentication', # برای راحتی تست در مرورگر
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # پیش‌فرض: نیاز به احراز هویت برای اکثر APIها
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10, # تعداد آیتم‌ها در هر صفحه برای صفحه‌بندی پیش‌فرض
    'DEFAULT_RENDERER_CLASSES': ( # برای نمایش JSON و فرمت‌های دیگر در مرورگر
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}


# --- تنظیمات Django REST Framework Simple JWT ---

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60), # طول عمر اکسس توکن
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # طول عمر رفرش توکن
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True, # آخرین ورود کاربر را به‌روزرسانی می‌کند

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY, # کلید امضا توکن، بهتر است همان SECRET_KEY پروژه باشد
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",), # نوع هدر احراز هویت (مثلاً Authorization: Bearer <token>)
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "TOKEN_SLIDING_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "TOKEN_SLIDING_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


# --- تنظیمات مدل‌های سفارشی ---
# اگر مدل کاربر سفارشی خودتان را می‌سازید (که در آینده از AbstractUser ارث‌بری می‌کند)#
AUTH_USER_MODEL = 'accounts.User' # باید نام اپ و مدل کاربر سفارشی شما باشد


# --- سایر تنظیمات ---

# مشخص کردن نوع پیش‌فرض Primary Key برای مدل‌ها (از جنگو 3.2 به بعد توصیه می‌شود)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'