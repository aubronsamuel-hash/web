import uuid
import contextvars

from starlette.types import ASGIApp, Receive, Scope, Send

from .settings import get_settings
from .logging_setup import REQUEST_ID_ATTR


_request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


def get_request_id() -> str:
    return _request_id_ctx.get()


class RequestIdMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.header_name = get_settings().request_id_header

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                # bytes header name/value
                hname = self.header_name.encode("latin-1")
                if hname not in headers:
                    rid = _request_id_ctx.get()
                    message["headers"] = list(headers.items()) + [(hname, rid.encode("latin-1"))]
            await send(message)

        # compute/generate request_id
        rid = None
        headers = dict(scope.get("headers") or [])
        hname = self.header_name.encode("latin-1")
        if hname in headers:
            try:
                rid = headers[hname].decode("latin-1")
            except Exception:
                rid = None
        if not rid:
            rid = str(uuid.uuid4())
        token = _request_id_ctx.set(rid)
        # attach to logging record via record attribute name
        scope[REQUEST_ID_ATTR] = rid  # hint for access logs
        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            _request_id_ctx.reset(token)
