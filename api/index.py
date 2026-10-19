"""Vercel serverless entrypoint for the Flecta_MQL Django project.

Vercel's Django builder resolves ``WSGI_APPLICATION`` and imports
``flectasite.wsgi`` directly, so this file just mirrors that entrypoint for
setups that point at ``api/index.py`` explicitly.
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flectasite.setting.vercel")

from flectasite.wsgi import application  # noqa: E402

app = application
