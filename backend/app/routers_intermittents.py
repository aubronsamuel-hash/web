from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .crud_intermittent import (
    create_intermittent,
    delete_intermittent,
    get_intermittent,
    list_intermittents,
    update_intermittent,
)
from .deps import get_db_dep, require_auth
from .schemas_intermittent import IntermittentCreate, IntermittentOut, IntermittentUpdate

router = APIRouter(
    prefix="/intermittents",
    tags=["intermittents"],
    dependencies=[Depends(require_auth)],
)  # noqa: B008


@router.get("", response_model=dict)
def list_intermittents_api(
    db: Session = Depends(get_db_dep),  # noqa: B008
    q: str | None = Query(default=None),
    active: bool | None = Query(default=None),
    skill: str | None = Query(default=None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> dict[str, Any]:
    items, total = list_intermittents(db, q, active, skill, page, size)
    pages = (total + size - 1) // size if size else 1
    return {
        "items": [IntermittentOut.model_validate(i) for i in items],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }


@router.post("", response_model=IntermittentOut, status_code=201)
def create_intermittent_api(
    payload: IntermittentCreate,
    db: Session = Depends(get_db_dep),  # noqa: B008
) -> IntermittentOut:
    try:
        i = create_intermittent(
            db,
            payload.first_name,
            payload.last_name,
            payload.is_active,
            payload.skills,
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Intermittent deja existant.",
        ) from e
    return IntermittentOut.model_validate(i)


@router.get("/{intermittent_id}", response_model=IntermittentOut)
def get_intermittent_api(
    intermittent_id: int,
    db: Session = Depends(get_db_dep),  # noqa: B008
) -> IntermittentOut:
    i = get_intermittent(db, intermittent_id)
    if not i:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intermittent introuvable.",
        )
    return IntermittentOut.model_validate(i)


@router.put("/{intermittent_id}", response_model=IntermittentOut)
def update_intermittent_api(
    intermittent_id: int,
    payload: IntermittentUpdate,
    db: Session = Depends(get_db_dep),  # noqa: B008
) -> IntermittentOut:
    try:
        i = update_intermittent(
            db,
            intermittent_id,
            first_name=payload.first_name,
            last_name=payload.last_name,
            is_active=payload.is_active,
            skills=payload.skills,
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Intermittent deja existant.",
        ) from e
    if not i:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intermittent introuvable.",
        )
    return IntermittentOut.model_validate(i)


@router.delete("/{intermittent_id}", status_code=204, response_class=Response)
def delete_intermittent_api(
    intermittent_id: int,
    db: Session = Depends(get_db_dep),  # noqa: B008
) -> Response:
    ok = delete_intermittent(db, intermittent_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intermittent introuvable.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
