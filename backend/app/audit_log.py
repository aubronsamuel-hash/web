from __future__ import annotations

import json
from typing import Any

from sqlalchemy.orm import Session

from .middleware import get_request_id
from .models_audit import AuditLog


def write_audit_log(
    db: Session,
    actor: str,
    action: str,
    entity: str,
    entity_id: int | None,
    payload: Any,
) -> None:
    log = AuditLog(
        request_id=get_request_id(),
        actor=actor,
        action=action,
        entity=entity,
        entity_id=entity_id,
        payload=json.dumps(payload, default=str) if payload is not None else None,
    )
    db.add(log)
    db.commit()
