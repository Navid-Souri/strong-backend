    # strong_app_project/strong_app_project/settings.py
    import os
    from pathlib import Path
    import dj_database_url # Make sure you've installed dj-database-url

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    # Read SECRET_KEY from environment variable for production
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-insecure-default-key-for-development-ONLY')
    # If DJANGO_SECRET_KEY is not set in environment, it will use this default.
    # On Render, you MUST set DJANGO_SECRET_KEY environment variable.

    # SECURITY WARNING: don't run with debug turned on in production!
    # Read DEBUG from environment variable
    DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True' # Default to True for local dev

    # Allowed hosts for your deployed application
    # Read ALLOWED_HOSTS from environment variable, split by comma
    ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
    # On Render, you MUST set DJANGO_ALLOWED_HOSTS to your Render app's URL (e.g., your-app.onrender.com)


    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Third-party apps
        'rest_framework',
        'rest_framework_simplejwt',
        'corsheaders', # For handling CORS requests from your React frontend
        # Your apps
        'accounts',
        'core',
        'workouts',
        'progress_tracking',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware', # NEW: Add WhiteNoise middleware
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware', # NEW: Add CORS middleware
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

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


    # Database
    # https://docs.djangoproject.com/en/5.0/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    # NEW: Configure database for Render (PostgreSQL)
    # This will override the SQLite3 database when DATABASE_URL is set in environment
    if 'DATABASE_URL' in os.environ:
        DATABASES['default'] = dj_database_url.config(
            conn_max_age=600,  # Optional: keep database connections alive for 10 minutes
            ssl_require=True   # Required for Render's PostgreSQL
        )


    # Password validation
    # https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


    # Internationalization
    # https://docs.djangoproject.com/en/5.0/topics/i18n/

    LANGUAGE_CODE = 'en-us' # Or 'fa-ir' if you want Persian Django admin/messages

    TIME_ZONE = 'UTC' # Important for consistent timestamps

    USE_I18N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/5.0/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles' # NEW: Directory where static files will be collected for production

    # Default primary key field type
    # https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # CORS Headers settings (for React frontend)
    # pip install django-cors-headers
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000", # Your React dev server
        "https://your-react-app.vercel.app", # Replace with your Vercel/Netlify domain
        "https://your-react-app.netlify.app", # Example for Netlify
    ]
    # Or, if you want to allow all origins (less secure for production):
    # CORS_ALLOW_ALL_ORIGINS = True

    # SIMPLE JWT settings (if you're using it)
    from datetime import timedelta
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True,
        'ALGORITHM': 'HS256',
        'SIGNING_KEY': SECRET_KEY, # Use the same SECRET_KEY for JWT signing
        'VERIFYING_KEY': None,
        'AUDIENCE': None,
        'ISSUER': None,
        'AUTH_HEADER_TYPES': ('Bearer',),
        'USER_ID_FIELD': 'id',
        'USER_ID_CLAIM': 'user_id',
        'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
        'TOKEN_TYPE_CLAIM': 'token_type',
        'JTI_CLAIM': 'jti',
        'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
        'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
        'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    }

    # REST Framework settings
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        )
    }