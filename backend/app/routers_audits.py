from __future__ import annotations
from typing import Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .deps import get_db_dep, require_auth
from .crud_audit import list_audits as list_audits_crud

router = APIRouter(prefix="/audits", tags=["audits"], dependencies=[Depends(require_auth)])


class AuditOut(BaseModel):
    id: int
    ts: datetime
    actor: str
    action: str
    entity: str
    entity_id: int
    request_id: str
    payload: str | None = None

    class Config:
        from_attributes = True


@router.get("", response_model=dict)
def list_audits(
    db: Session = Depends(get_db_dep),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    actor: Optional[str] = Query(None),
    entity: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    request_id: Optional[str] = Query(None),
    from_ts: Optional[datetime] = Query(None),
    to_ts: Optional[datetime] = Query(None),
) -> dict[str, Any]:
    if from_ts and to_ts and from_ts > to_ts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plage temporelle invalide.",
        )
    items, total = list_audits_crud(
        db,
        page,
        size,
        actor=actor,
        entity=entity,
        action=action,
        request_id=request_id,
        from_ts=from_ts.isoformat() if from_ts else None,
        to_ts=to_ts.isoformat() if to_ts else None,
    )
    pages = (total + size - 1) // size if size else 1
    return {
        "items": [AuditOut.model_validate(i) for i in items],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }
