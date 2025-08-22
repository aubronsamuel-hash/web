from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from .crud_availability import (
    create_availability,
    delete_availability,
    get_availability,
    list_availabilities,
    update_availability,
)
from .deps import get_db_dep, require_auth
from .schemas_availability import AvailabilityCreate, AvailabilityOut, AvailabilityUpdate

router = APIRouter(
    prefix="/availabilities",
    tags=["availabilities"],
    dependencies=[Depends(require_auth)],  # noqa: B008
)


@router.get("", response_model=dict)
def list_api(
    db: Session = Depends(get_db_dep),  # noqa: B008
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    intermittent_id: int | None = Query(None),
    start_from: str | None = Query(None, description="ISO start of window"),
    end_to: str | None = Query(None, description="ISO end of window"),
) -> dict[str, Any]:
    items, total = list_availabilities(db, page, size, intermittent_id, start_from, end_to)
    pages = (total + size - 1) // size if size else 1
    return {
        "items": [AvailabilityOut.model_validate(i) for i in items],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }


@router.post("", response_model=AvailabilityOut, status_code=201)
def create_api(payload: AvailabilityCreate, db: Session = Depends(get_db_dep)) -> AvailabilityOut:  # noqa: B008
    a = create_availability(db, **payload.model_dump())
    return AvailabilityOut.model_validate(a)


@router.get("/{aid}", response_model=AvailabilityOut)
def get_api(aid: int, db: Session = Depends(get_db_dep)) -> AvailabilityOut:  # noqa: B008
    a = get_availability(db, aid)
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Availability introuvable.")
    return AvailabilityOut.model_validate(a)


@router.put("/{aid}", response_model=AvailabilityOut)
def update_api(
    aid: int, payload: AvailabilityUpdate, db: Session = Depends(get_db_dep)  # noqa: B008
) -> AvailabilityOut:
    a = update_availability(db, aid, **payload.model_dump())
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Availability introuvable.")
    return AvailabilityOut.model_validate(a)


@router.delete("/{aid}", status_code=204, response_class=Response)
def delete_api(aid: int, db: Session = Depends(get_db_dep)) -> Response:  # noqa: B008
    ok = delete_availability(db, aid)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Availability introuvable.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
