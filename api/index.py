from __future__ import annotations

import io
import os
import sys
import traceback
from pathlib import Path
from urllib.parse import urlencode

_application = None


def _get_application():
    global _application
    if _application is None:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "telegram_bot_project"))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_bot_project.settings")
        import django
        from django.core.handlers.wsgi import WSGIHandler
        django.setup()
        _application = WSGIHandler()
    return _application


def handler(request, context):
    try:
        application = _get_application()

        query_string = request.query if isinstance(request.query, str | None) else urlencode(request.query or {})

        environ = {
            "REQUEST_METHOD": request.method,
            "PATH_INFO": request.path,
            "QUERY_STRING": query_string,
            "SERVER_NAME": request.headers.get("host", "localhost"),
            "SERVER_PORT": request.headers.get("x-forwarded-port", "443"),
            "HTTP_HOST": request.headers.get("host", "localhost"),
            "SERVER_PROTOCOL": "HTTP/1.1",
            "wsgi.url_scheme": request.headers.get("x-forwarded-proto", "https"),
            "wsgi.input": io.BytesIO(request.body or b""),
            "wsgi.errors": sys.stderr,
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
            "CONTENT_LENGTH": str(len(request.body or b"")),
        }

        content_type = request.headers.get("content-type")
        if content_type:
            environ["CONTENT_TYPE"] = content_type

        for key, value in request.headers.items():
            key = key.upper().replace("-", "_")
            if key not in ("CONTENT_TYPE", "CONTENT_LENGTH"):
                environ[f"HTTP_{key}"] = value

        response_status: list[str] = []
        response_headers: list[tuple[str, str]] = []

        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            response_status.append(status)
            response_headers.extend(headers)

        body = b"".join(application(environ, start_response))
        status_code = int(response_status[0].split(" ")[0])

        return {
            "statusCode": status_code,
            "headers": dict(response_headers),
            "body": body.decode("utf-8"),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"content-type": "text/plain"},
            "body": f"{type(e).__name__}: {e}\n\n{traceback.format_exc()}",
        }
