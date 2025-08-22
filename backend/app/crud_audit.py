from __future__ import annotations
from typing import Optional, Sequence
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from .models_audit import AuditLog


def list_audits(
    db: Session,
    page: int,
    size: int,
    *,
    actor: Optional[str] = None,
    entity: Optional[str] = None,
    action: Optional[str] = None,
    request_id: Optional[str] = None,
    from_ts: Optional[str] = None,
    to_ts: Optional[str] = None,
) -> tuple[Sequence[AuditLog], int]:
    if page < 1:
        page = 1
    size = max(1, min(size, 100))
    offset = (page - 1) * size

    stmt = select(AuditLog)
    conds = []
    if actor:
        conds.append(AuditLog.actor == actor)
    if entity:
        conds.append(AuditLog.entity == entity)
    if action:
        conds.append(AuditLog.action == action)
    if request_id:
        conds.append(AuditLog.request_id == request_id)
    if from_ts:
        conds.append(AuditLog.ts >= from_ts)
    if to_ts:
        conds.append(AuditLog.ts <= to_ts)

    if conds:
        stmt = stmt.where(*conds)

    total = db.scalar(select(func.count(AuditLog.id)).where(*conds)) or 0
    rows = db.scalars(
        stmt.order_by(AuditLog.ts.desc()).offset(offset).limit(size)
    ).all()
    return rows, int(total)
