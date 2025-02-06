"""
Django settings for shop_project project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tq$7sd3e)#-0#*&g2)9fjkjew%&x(4(5&dvyv694y2#^g939ry'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('IS_DEBUG', False)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'shop',
    'corsheaders',
    'django_cleanup.apps.CleanupConfig',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'shop_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'shop_project.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'EXCEPTION_HANDLER': 'utils.exception_handler.custom_exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',  # 保持过滤功能
    ),
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'shop_db'),
        'USER': os.getenv('DB_USER', 'shop_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password123'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'shop.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'static-files/'

# media files

MEDIA_URL = 'media/'  # 媒体文件的访问路径
MEDIA_ROOT = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# auth todo remove sensitive data
GOOGLE_OAUTH2_CALLBACK_URL=os.getenv('GOOGLE_OAUTH2_CALLBACK_URL', 'http://localhost:8000/auth/google/callback/')
GOOGLE_OAUTH2_KEY=os.getenv('GOOGLE_OAUTH2_KEY')
GOOGLE_OAUTH2_SECRET=os.getenv('GOOGLE_OAUTH2_SECRET')
SERVER_BASE_URL=os.getenv('SERVER_BASE_URL', 'http://localhost:8000')

# cors domains
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:8080').split(",")

# djangorestframework-simplejwt settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Example: 5 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Example: 7 days
    'ROTATE_REFRESH_TOKENS': True,  # Get a new refresh token when using refresh
    'BLACKLIST_AFTER_ROTATION': True,  # Blacklist old refresh tokens after rotation
    'AUTH_HEADER_TYPES': ('Bearer',),  # Use "Bearer <token>"
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 输出到控制台
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',  # 输出到文件
            'filename': 'logs/django.log',  # 日志文件路径
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',  # Adjust this level as needed (e.g., INFO, WARNING, ERROR)
            'propagate': True,
        }
    },
}

# django-allauth
ACCOUNT_AUTHENTICATION_METHOD = "email"  # Use email instead of username
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory" # Require email confirmation
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  # No need to sent POST request to confirmation link
LOGIN_URL = "/admin"  # Path, users will be redirected to after email verification
# # The URL to redirect to after a successful email confirmation, in case no user is logged in.
# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = os.environ.get(
#     "EMAIL_CONFIRM_REDIRECT_URL", "https://myapp.com/login"
# )
# # The URL to redirect to after a successful email confirmation, in case of an authenticated user.
# ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = os.environ.get(
#     "EMAIL_CONFIRM_REDIRECT_URL", "https://myapp.com/login"
# )

# allauth.socialaccount
# Authenticate if local account with this email address already exists
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
# Connect local account and social account if local account with that email address already exists
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APPS": [
            {
                "client_id": GOOGLE_OAUTH2_KEY,
                "secret": GOOGLE_OAUTH2_SECRET,
                "key": "",
            },
        ],
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# LOGIN_REDIRECT_URL = '/callback/'
#
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': ['profile', 'email'],
#         'AUTH_PARAMS': {'access_type': 'online'},
#         'OAUTH_PKCE_ENABLED': True,
#         'FETCH_USERINFO': True,
#     }
# }
#
# SOCIALACCOUNT_STORE_TOKEN = True

# django.contrib.sites
SITE_ID = 1

# Django SMTP todo remove sensitive data
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

