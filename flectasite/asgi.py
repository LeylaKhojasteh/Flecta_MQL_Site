"""
ASGI config for flectasite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

if os.getenv("VERCEL"):
    os.environ["DJANGO_SETTINGS_MODULE"] = "flectasite.setting.vercel"
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flectasite.setting.prod")

application = get_asgi_application()
