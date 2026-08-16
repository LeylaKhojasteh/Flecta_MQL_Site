from flectasite.settings import *
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(nsq+!49s62qhu=)1%jf(y*q2l+sy$ki%xctb$k=gmz%2vh!ue'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['flectamql.ir', 'www.flectamql.ir','127.0.0.1']



# INSTALLED_APPS = []

#sites framework
SITE_ID = 2


X_FRAME_OPTIONS = 'SAMEORIGIN'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'flectamq_flecta',
        'USER': 'flectamq_nasim',
        'PASSWORD': 'Ug]a5@u*NWtcr@8b',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}



MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]


COMPRESS_ROOT = STATIC_ROOT

# با DEBUG=False خودش به صورت پیش‌فرض True است،
# ولی برای واضح بودن می‌توانی بنویسی:
COMPRESS_ENABLED = True

# مناسب Production
COMPRESS_OFFLINE = True


SECURE_BROWSER_XSS_FILTER = True
# CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'SAMEORIGIN'
# X-Content-Type-Options
SECURE_CONTENT_TYPE_NOSNIFF = True
# Strict-Transport-Security
SECURE_HSTS_SECONDS = 15768000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Redirect HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# For more security
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Strict"


# Production email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "flectamql.ir"
EMAIL_PORT = 465

EMAIL_HOST_USER = "manager@flectamql.ir"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_TIMEOUT = 20

DEFAULT_FROM_EMAIL = "FLECTA MQL <manager@flectamql.ir>"
SERVER_EMAIL = DEFAULT_FROM_EMAIL