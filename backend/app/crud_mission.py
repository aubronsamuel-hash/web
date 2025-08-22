from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models_mission import Mission


def list_missions(
    db: Session,
    q: str | None,
    page: int,
    size: int,
) -> tuple[Sequence[Mission], int]:
    if page < 1:
        page = 1
    size = max(1, min(size, 100))
    offset = (page - 1) * size

    query = select(Mission)
    if q:
        pattern = f"%{q.lower()}%"
        query = query.where(func.lower(Mission.title).like(pattern))
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    rows = db.scalars(query.offset(offset).limit(size)).all()
    return rows, int(total or 0)


def create_mission(
    db: Session,
    title: str,
    start_at: datetime,
    end_at: datetime,
) -> Mission:
    m = Mission(title=title, start_at=start_at, end_at=end_at, is_published=False)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


def get_mission(db: Session, mission_id: int) -> Mission | None:
    return db.get(Mission, mission_id)


def update_mission(db: Session, mission_id: int, **changes) -> Mission | None:
    m = db.get(Mission, mission_id)
    if not m:
        return None
    for k, v in changes.items():
        if v is not None:
            setattr(m, k, v)
    db.commit()
    db.refresh(m)
    return m


def delete_mission(db: Session, mission_id: int) -> bool:
    m = db.get(Mission, mission_id)
    if not m:
        return False
    db.delete(m)
    db.commit()
    return True


def publish_mission(db: Session, mission_id: int) -> Mission | None:
    m = db.get(Mission, mission_id)
    if not m:
        return None
    if not m.is_published:
        m.is_published = True
        db.commit()
        db.refresh(m)
    return m


def duplicate_mission(db: Session, mission_id: int) -> Mission | None:
    m = db.get(Mission, mission_id)
    if not m:
        return None
    m2 = Mission(
        title=m.title,
        start_at=m.start_at,
        end_at=m.end_at,
        is_published=False,
    )
    db.add(m2)
    db.commit()
    db.refresh(m2)
    return m2
