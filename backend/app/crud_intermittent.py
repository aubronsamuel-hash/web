from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models_intermittent import Intermittent


def list_intermittents(
    db: Session,
    q: str | None,
    active: bool | None,
    skill: str | None,
    page: int,
    size: int,
) -> tuple[Sequence[Intermittent], int]:
    if page < 1:
        page = 1
    size = max(1, min(size, 100))
    offset = (page - 1) * size

    query = select(Intermittent)
    if q:
        pattern = f"%{q.lower()}%"
        query = query.where(
            or_(
                func.lower(Intermittent.first_name).like(pattern),
                func.lower(Intermittent.last_name).like(pattern),
            )
        )
    if active is not None:
        query = query.where(Intermittent.is_active == active)
    if skill:
        skill_pattern = f"%{skill.lower()}%"
        query = query.where(func.lower(Intermittent.skills).like(skill_pattern))

    total = db.scalar(select(func.count()).select_from(query.subquery()))
    rows = db.scalars(query.offset(offset).limit(size)).all()
    return rows, int(total or 0)


def create_intermittent(
    db: Session,
    first_name: str,
    last_name: str,
    is_active: bool,
    skills: str | None,
) -> Intermittent:
    i = Intermittent(
        first_name=first_name, last_name=last_name, is_active=is_active, skills=skills
    )
    db.add(i)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(i)
    return i


def get_intermittent(db: Session, intermittent_id: int) -> Intermittent | None:
    return db.get(Intermittent, intermittent_id)


def update_intermittent(db: Session, intermittent_id: int, **changes) -> Intermittent | None:
    i = db.get(Intermittent, intermittent_id)
    if not i:
        return None
    for k, v in changes.items():
        if v is not None:
            setattr(i, k, v)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(i)
    return i


def delete_intermittent(db: Session, intermittent_id: int) -> bool:
    i = db.get(Intermittent, intermittent_id)
    if not i:
        return False
    db.delete(i)
    db.commit()
    return True
