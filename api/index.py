"""Vercel serverless entrypoint for the Flecta_MQL Django project."""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flectasite.setting.vercel")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
application = app
