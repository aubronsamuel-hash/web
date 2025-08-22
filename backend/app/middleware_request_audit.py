from __future__ import annotations
import re
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .audit_log import write_audit
from .security import decode_token
from .db import get_sessionmaker


class RequestAuditMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._sess_maker = get_sessionmaker()

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            try:
                actor = self._extract_actor(request)
                entity, entity_id = self._extract_entity(request.url.path)
                payload = {
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                }
                with self._sess_maker() as db:
                    write_audit(
                        db,
                        actor=actor or "-",
                        action="request",
                        entity=entity or "-",
                        entity_id=entity_id or 0,
                        payload=payload,
                    )
            except Exception:
                # Ne pas casser la reponse si l'audit echoue
                pass
        return response

    def _extract_actor(self, request: Request) -> Optional[str]:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]
            sub = decode_token(token)
            if sub:
                return sub
        return None

    def _extract_entity(self, path: str) -> tuple[str, int]:
        parts = [p for p in path.split("/") if p]
        entity = parts[0] if parts else "-"
        entity_id = 0
        if len(parts) > 1 and re.fullmatch(r"\d+", parts[1] or ""):
            try:
                entity_id = int(parts[1])
            except Exception:
                entity_id = 0
        return entity, entity_id
