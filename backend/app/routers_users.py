from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .crud_user import create_user, delete_user, get_user, list_users, update_user
from .deps import get_db_dep, require_auth
from .schemas_user import UserCreate, UserOut, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_auth)],
)  # noqa: B008


@router.get("", response_model=dict)
def list_users_api(
    db: Session = Depends(get_db_dep),  # noqa: B008
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> dict[str, Any]:
    items, total = list_users(db, page, size)
    pages = (total + size - 1) // size if size else 1
    return {
        "items": [UserOut.model_validate(i) for i in items],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }


@router.post("", response_model=UserOut, status_code=201)
def create_user_api(
    payload: UserCreate,
    db: Session = Depends(get_db_dep),  # noqa: B008
) -> UserOut:
    try:
        u = create_user(db, payload.email, payload.full_name, payload.is_active)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email deja utilise."
        ) from e
    return UserOut.model_validate(u)


@router.get("/{user_id}", response_model=UserOut)
def get_user_api(user_id: int, db: Session = Depends(get_db_dep)) -> UserOut:  # noqa: B008
    u = get_user(db, user_id)
    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User introuvable."
        )
    return UserOut.model_validate(u)


@router.put("/{user_id}", response_model=UserOut)
def update_user_api(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db_dep),  # noqa: B008
) -> UserOut:
    try:
        u = update_user(
            db,
            user_id,
            email=payload.email,
            full_name=payload.full_name,
            is_active=payload.is_active,
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email deja utilise."
        ) from e
    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User introuvable."
        )
    return UserOut.model_validate(u)


@router.delete("/{user_id}", status_code=204, response_class=Response)
def delete_user_api(
    user_id: int, db: Session = Depends(get_db_dep),  # noqa: B008
) -> Response:
    ok = delete_user(db, user_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User introuvable."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

