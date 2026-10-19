"""Vercel serverless entrypoint for the Flecta_MQL Django project."""
import os
import sys
import traceback

# Force the Vercel settings module. A DJANGO_SETTINGS_MODULE env var set in
# the Vercel dashboard would otherwise win via setdefault and load settings
# with ALLOWED_HOSTS that reject *.vercel.app.
os.environ["DJANGO_SETTINGS_MODULE"] = "flectasite.setting.vercel"


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


try:
    from django.core.wsgi import get_wsgi_application

    _django_app = get_wsgi_application()
except BaseException:
    _startup_tb = traceback.format_exc()
    print("[flecta] STARTUP FAILED\n" + _startup_tb, file=sys.stderr, flush=True)
    app = _plain_500("[flecta] Django startup failed", _startup_tb)
    application = app
else:
    from django.conf import settings as _settings

    print(
        "[flecta] settings=%s DEBUG=%s ALLOWED_HOSTS=%s DATABASES=%s"
        % (
            os.environ.get("DJANGO_SETTINGS_MODULE"),
            _settings.DEBUG,
            _settings.ALLOWED_HOSTS,
            list(_settings.DATABASES),
        ),
        file=sys.stderr,
        flush=True,
    )

    def app(environ, start_response):
        try:
            return _django_app(environ, start_response)
        except BaseException:
            _request_tb = traceback.format_exc()
            print(
                "[flecta] REQUEST FAILED host=%s path=%s\n%s"
                % (
                    environ.get("HTTP_HOST"),
                    environ.get("PATH_INFO"),
                    _request_tb,
                ),
                file=sys.stderr,
                flush=True,
            )
            return _plain_500("[flecta] request failed", _request_tb)(
                environ, start_response
            )

    application = app
