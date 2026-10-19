"""
WSGI config for flectasite project.

This is the entrypoint Vercel actually imports for Django projects: the
Python builder resolves ``WSGI_APPLICATION`` from settings and runs this
module, so it must select the correct settings module itself.

On Vercel we always use ``flectasite.setting.vercel`` (it allows
``*.vercel.app`` preview hosts). A DJANGO_SETTINGS_MODULE env var set in the
dashboard must not override it.
"""

import os
import sys
import traceback

_ON_VERCEL = bool(os.getenv("VERCEL"))
_SETTINGS_MODULE = (
    "flectasite.setting.vercel" if _ON_VERCEL else "flectasite.setting.prod"
)

if _ON_VERCEL:
    os.environ["DJANGO_SETTINGS_MODULE"] = _SETTINGS_MODULE
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", _SETTINGS_MODULE)


def _plain_500(title, detail):
    body = ("%s\n\n%s" % (title, detail)).encode("utf-8", "replace")[:8000]

    def app(environ, start_response):
        start_response(
            "500 Internal Server Error",
            [
                ("Content-Type", "text/plain; charset=utf-8"),
                ("Content-Length", str(len(body))),
            ],
        )
        return [body]

    return app


def _log(message):
    try:
        sys.stderr.write(message + "\n")
        sys.stderr.flush()
    except Exception:
        pass


try:
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
except BaseException:
    _startup_tb = traceback.format_exc()
    _log("[flecta] wsgi STARTUP FAILED settings=%s\n%s" % (_SETTINGS_MODULE, _startup_tb))
    application = _plain_500(
        "[flecta] Django startup failed (settings=%s)" % _SETTINGS_MODULE,
        _startup_tb,
    )
else:
    try:
        from django.conf import settings as _settings

        _log(
            "[flecta] wsgi READY settings=%s DEBUG=%s ALLOWED_HOSTS=%s DB=%s"
            % (
                _SETTINGS_MODULE,
                _settings.DEBUG,
                _settings.ALLOWED_HOSTS,
                list(_settings.DATABASES),
            )
        )
    except Exception:
        _log("[flecta] wsgi READY (could not read settings summary)")
