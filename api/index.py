"""Vercel serverless entrypoint for the Flecta_MQL Django project."""
import os

# Force the Vercel settings module. A DJANGO_SETTINGS_MODULE env var set in
# the Vercel dashboard would otherwise win via setdefault and load settings
# with ALLOWED_HOSTS that reject *.vercel.app.
os.environ["DJANGO_SETTINGS_MODULE"] = "flectasite.setting.vercel"

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
application = app

from django.conf import settings as _settings

# One line per cold start, visible in Vercel function logs.
print(
    "[flecta] settings=%s ALLOWED_HOSTS=%s"
    % (os.environ.get("DJANGO_SETTINGS_MODULE"), _settings.ALLOWED_HOSTS)
)
