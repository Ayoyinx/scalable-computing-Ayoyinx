import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR/".env")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.getenv("DEBUG") == 'true')

CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS = [
    'wallet-env.eba-gr5bgv3s.eu-north-1.elasticbeanstalk.com',
    'localhost',
    '127.0.0.1'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'whitenoise',
    'oauth2_provider',
    'rest_framework',
    'rest_framework.authtoken',
    'account',
    'wallet',
    'oauth'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'walletapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
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

WSGI_APPLICATION = 'walletapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': int(os.getenv('DB_PORT')),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv("DB_PASSWORD")
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR/"static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ],
    "DEFAULT_PAGINATION_CLASS": "walletapi.pagination.CustomPagination"
}

AUTH_USER_MODEL = "account.Account"
OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'transfer': 'Ability to Transfer money from account',
        'read': 'Retrieve Account details'
    }
}
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET"),
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URL = os.getenv("GOOGLE_REDIRECT_URL")

BOOK_STORE_CLIENT_ID = os.getenv("BOOK_STORE_CLIENT_ID")
BOOK_STORE_CLIENT_SECRET = os.getenv("BOOK_STORE_CLIENT_SECRET")
BOOK_STORE_CODE_VERIFIER = os.getenv("BOOK_STORE_CODE_VERIFIER")
BOOK_STORE_REDIRECT_URL = os.getenv("BOOK_STORE_REDIRECT_URL")

FINTRACK_CLIENT_ID = os.getenv("FINTRACK_CLIENT_ID")
FINTRACK_CLIENT_SECRET = os.getenv("FINTRACK_CLIENT_SECRET")
FINTRACK_CODE_VERIFIER = os.getenv("FINTRACK_CODE_VERIFIER")
FINTRACK_REDIRECT_URL = os.getenv("FINTRACK_REDIRECT_URL")

LOGIN_URL = '/oauth/login/'
