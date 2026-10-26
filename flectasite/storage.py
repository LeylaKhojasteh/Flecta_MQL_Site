"""Static files storage used on Vercel.

``manifest_strict`` is a class attribute in Django's manifest storage (it is
not accepted as an ``__init__`` kwarg), so it must be set on a subclass.
With it disabled, a missing hashed entry falls back to the plain static path
instead of raising ``ValueError`` and turning a page into a 500.
"""

try:
    from whitenoise.storage import CompressedManifestStaticFilesStorage as _Base
except ImportError:  # local offline env without Vercel deps
    from django.contrib.staticfiles.storage import (
        StaticFilesStorage as _Base,
    )


class StaticFilesStorage(_Base):
    manifest_strict = False
