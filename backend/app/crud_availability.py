from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models_availability import Availability


def list_availabilities(
    db: Session,
    page: int,
    size: int,
    intermittent_id: int | None = None,
    start_from: str | None = None,
    end_to: str | None = None,
) -> tuple[Sequence[Availability], int]:
    if page < 1:
        page = 1
    size = max(1, min(size, 100))
    offset = (page - 1) * size

    stmt = select(Availability)
    if intermittent_id is not None:
        stmt = stmt.where(Availability.intermittent_id == intermittent_id)
    if start_from is not None:
        stmt = stmt.where(Availability.end_at >= start_from)  # ends after window start
    if end_to is not None:
        stmt = stmt.where(Availability.start_at <= end_to)  # starts before window end

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.offset(offset).limit(size)).all()
    return rows, int(total)


def create_availability(db: Session, **fields) -> Availability:
    a = Availability(**fields)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def get_availability(db: Session, aid: int) -> Availability | None:
    return db.get(Availability, aid)


def update_availability(db: Session, aid: int, **changes) -> Availability | None:
    a = db.get(Availability, aid)
    if not a:
        return None
    for k, v in changes.items():
        if v is not None:
            setattr(a, k, v)
    db.commit()
    db.refresh(a)
    return a


def delete_availability(db: Session, aid: int) -> bool:
    a = db.get(Availability, aid)
    if not a:
        return False
    db.delete(a)
    db.commit()
    return True
