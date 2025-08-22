from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models_user import User


def list_users(db: Session, page: int, size: int) -> tuple[Sequence[User], int]:
    if page < 1:
        page = 1
    size = max(1, min(size, 100))
    offset = (page - 1) * size
    total = db.scalar(select(func.count()).select_from(User))
    rows = db.scalars(select(User).offset(offset).limit(size)).all()
    return rows, int(total or 0)


def create_user(db: Session, email: str, full_name: str | None, is_active: bool) -> User:
    u = User(email=email, full_name=full_name, is_active=is_active)
    db.add(u)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(u)
    return u


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def update_user(db: Session, user_id: int, **changes) -> User | None:
    u = db.get(User, user_id)
    if not u:
        return None
    for k, v in changes.items():
        if v is not None:
            setattr(u, k, v)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(u)
    return u


def delete_user(db: Session, user_id: int) -> bool:
    u = db.get(User, user_id)
    if not u:
        return False
    db.delete(u)
    db.commit()
    return True

