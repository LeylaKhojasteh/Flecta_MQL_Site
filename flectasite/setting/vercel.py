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

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # Manifest storage with manifest_strict=False: a missing hashed name
        # falls back to the plain path instead of raising a 500.
        # The plain fallback class keeps `check` green without WhiteNoise.
        "BACKEND": (
            "flectasite.storage.StaticFilesStorage"
            if _has_whitenoise
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
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

# ---------------- Media ----------------------------------------
# Serverless filesystem is ephemeral: uploads vanish on redeploy/cold
# start. Set the SUPABASE_STORAGE_* env vars to keep uploads in a
# Supabase Storage bucket (S3-compatible). Local bundled files keep
# working through FileSystemStorage when the bucket is not configured.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # noqa: F405

_s3_bucket = os.getenv("SUPABASE_STORAGE_BUCKET", "")
_s3_access_key = os.getenv("SUPABASE_STORAGE_ACCESS_KEY", "")
_supabase_url = os.getenv("SUPABASE_URL", "").rstrip("/")
_s3_endpoint = os.getenv(
    "SUPABASE_S3_ENDPOINT",
    (_supabase_url + "/storage/v1/s3") if _supabase_url else "",
)
_s3_public_url = os.getenv(
    "SUPABASE_STORAGE_PUBLIC_URL",
    (
        _supabase_url + "/storage/v1/object/public/" + _s3_bucket + "/"
        if _supabase_url and _s3_bucket
        else ""
    ),
)
if _s3_bucket and _s3_access_key and _s3_endpoint:
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": _s3_access_key,
            "secret_key": os.getenv("SUPABASE_STORAGE_SECRET_KEY", ""),
            "bucket_name": _s3_bucket,
            "endpoint_url": _s3_endpoint,
            "region_name": os.getenv("SUPABASE_S3_REGION", "eu-west-1"),
            "signature_version": "s3v4",
            "addressing_style": "path",
            "default_acl": None,
            "querystring_auth": False,
            "file_overwrite": False,
        },
    }
    MEDIA_URL = _s3_public_url or MEDIA_URL

# ---------------- Email (env-based) ---------------------------
# Defaults point at the project's own mail server; override with env.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "flectamql.ir")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "465"))
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "False").lower() == "true"
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False").lower() == "true"
if EMAIL_USE_SSL and EMAIL_USE_TLS:
    # Django refuses both at once; SSL on 465 is the intended default.
    EMAIL_USE_TLS = False
elif not EMAIL_USE_SSL and not EMAIL_USE_TLS:
    # No explicit choice: 465 means implicit SSL, anything else STARTTLS.
    if EMAIL_PORT == 465:
        EMAIL_USE_SSL = True
    else:
        EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "manager@flectamql.ir")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "20"))
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL", "FLECTA MQL <manager@flectamql.ir>"
)
SERVER_EMAIL = DEFAULT_FROM_EMAIL
CONTACT_RECIPIENT_EMAIL = os.getenv(
    "CONTACT_RECIPIENT_EMAIL", EMAIL_HOST_USER or "noreply@example.com"
)

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
