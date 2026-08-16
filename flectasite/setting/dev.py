from flectasite.settings import *
import os
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(nsq+!49s62qhu=)1%jf(y*q2l+sy$ki%xctb$k=gmz%2vh!ue'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# INSTALLED_APPS = []

#sites framework
SITE_ID = 2



# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]



# ==================================
# Django Compressor
# ==================================

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_ROOT = STATIC_ROOT

COMPRESS_ENABLED = False  # Set to True in production

# For production / offline compression
COMPRESS_OFFLINE = False  # Set to True in production



X_FRAME_OPTIONS = 'SAMEORIGIN'
# X-Content-Type-Options
SECURE_CONTENT_TYPE_NOSNIFF = True
# Strict-Transport-Security
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Redirect HTTP requests to HTTPS
SECURE_SSL_REDIRECT = False  # Set to True in production

# For more security
CSRF_COOKIE_SECURE = False  # Set to True in production
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = False  # Set to True in production
SESSION_COOKIE_SAMESITE = "Strict"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER