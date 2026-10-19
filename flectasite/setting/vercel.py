import os

# Ensure base settings import never crashes the Vercel build when
# SECRET_KEY is only available as a Vercel Environment Variable.
os.environ.setdefault("SECRET_KEY", "vercel-build-placeholder-change-me")

from flectasite.settings import *  # noqa: F401,F403

try:
    import dj_database_url
except ImportError:  # local env without Vercel deps (offline); Vercel build installs them
    dj_database_url = None

# ---------------------------------------------------------------
# Vercel (serverless) settings for Flecta_MQL + Supabase Postgres
# ---------------------------------------------------------------

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY", "vercel-build-placeholder-change-me")

# Vercel domains + production domain, comma separated via env.
# Django matches subdomains with a leading dot: ".vercel.app" covers
# project.vercel.app AND project-git-branch-user.vercel.app.
# NOTE: "*.vercel.app" is NOT valid in Django ALLOWED_HOSTS; use ".vercel.app".
def _parse_hosts(raw):
    raw = (raw or "").replace("[", "").replace("]", "").replace('"', "").replace("'", "")
    return [h.strip() for h in raw.split(",") if h.strip()]


_core_hosts = [
    ".vercel.app",  # every Vercel production/preview/deployment host
    "flectamql.ir",
    "www.flectamql.ir",
    "localhost",
    "127.0.0.1",
    "[::1]",
]
ALLOWED_HOSTS = _parse_hosts(os.getenv("ALLOWED_HOSTS", ""))

# Always include the core hosts, even if the dashboard env var is wrong,
# missing, or quoted/bracketed wrong. Dedupe, preserve order.
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS + _core_hosts))

# Behind Vercel's proxy, Django must trust X-Forwarded-Proto.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True
SESSION_COOKIE_SAMESITE = "Strict"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# CSRF origins for admin login on Vercel + custom domain.
# Example: CSRF_TRUSTED_ORIGINS="https://xxx.vercel.app,https://flectamql.ir"
_csrf_default = "https://*.vercel.app,https://flectamql.ir,https://www.flectamql.ir"
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.getenv("CSRF_TRUSTED_ORIGINS", _csrf_default).split(",")
    if o.strip()
]

# ---------------- Database: Supabase Postgres ------------------
# On Vercel set DATABASE_URL to the Supabase **pooled** connection string
# (Session mode, port 6543), e.g.:
# postgresql://postgres.PROJECT_REF:PASSWORD@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
# Local fallback (no DATABASE_URL): sqlite, so `check`/`collectstatic` work.
DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL and dj_database_url is not None:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=0,  # serverless: no persistent connections
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }

# Supabase pooler + serverless: keep connections short-lived.
CONN_MAX_AGE = 0

# ---------------- Static files via WhiteNoise ------------------
MIDDLEWARE = [
    m for m in MIDDLEWARE  # noqa: F405
    if "debug_toolbar" not in m
]
try:
    import whitenoise  # noqa: F401
    _has_whitenoise = True
except ImportError:  # local offline env; installed on Vercel via requirements.txt
    _has_whitenoise = False
if _has_whitenoise and "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:
    # Must sit directly after SecurityMiddleware.
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405
STATICFILES_DIRS = [BASE_DIR / "statics"]  # noqa: F405

if _has_whitenoise:
    _static_backend = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    # Never 500 a page just because a hashed static name is missing from the
    # manifest; fall back to the plain static path instead.
    _static_options = {"manifest_strict": False}
else:
    _static_backend = "django.contrib.staticfiles.storage.StaticFilesStorage"
    _static_options = {}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # WhiteNoise is installed on Vercel via requirements.txt.
        # Local offline fallback keeps `check` green without it.
        "BACKEND": _static_backend,
        "OPTIONS": _static_options,
    },
}

# django-compressor: templates use {% compress css %}, so offline
# compression must run at build time (filesystem is read-only at runtime).
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# ---------------- Media (ephemeral on Vercel!) -----------------
# Files written to /media disappear on redeploy/cold start.
# v1 keeps FileSystemStorage so bundled media/blog/* keeps working.
# For permanent uploads later, move to Supabase Storage (S3 API).
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # noqa: F405

# ---------------- Email (env-based, Gmail/SMTP friendly) -------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "20"))
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "FLECTA <noreply@example.com>")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
CONTACT_RECIPIENT_EMAIL = os.getenv("CONTACT_RECIPIENT_EMAIL", EMAIL_HOST_USER or "noreply@example.com")

# ---------------- Vercel-specific hardening --------------------
# debug_toolbar must never load in serverless prod.
INSTALLED_APPS = [a for a in INSTALLED_APPS if a != "debug_toolbar"]  # noqa: F405

SITE_ID = int(os.getenv("SITE_ID", "1"))

# Logging to stderr so `vercel logs` shows Django errors.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "WARNING"),
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "WARNING"),
            "propagate": False,
        },
    },
}
