from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from .audit_log import write_audit_log
from .crud_mission import (
    create_mission,
    delete_mission,
    duplicate_mission,
    get_mission,
    list_missions,
    publish_mission,
    update_mission,
)
from .deps import get_db_dep, require_auth
from .schemas_mission import MissionCreate, MissionOut, MissionUpdate

router = APIRouter(prefix="/missions", tags=["missions"])


@router.get("", response_model=dict)
def list_missions_api(
    db: Session = Depends(get_db_dep),  # noqa: B008
    _: str = Depends(require_auth),  # noqa: B008
    q: str | None = Query(default=None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> dict[str, Any]:
    items, total = list_missions(db, q, page, size)
    pages = (total + size - 1) // size if size else 1
    return {
        "items": [MissionOut.model_validate(i) for i in items],
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }


@router.post("", response_model=MissionOut, status_code=201)
def create_mission_api(
    payload: MissionCreate,
    db: Session = Depends(get_db_dep),  # noqa: B008
    actor: str = Depends(require_auth),  # noqa: B008
) -> MissionOut:
    m = create_mission(db, payload.title, payload.start_at, payload.end_at)
    write_audit_log(db, actor, "create", "mission", m.id, payload.model_dump())
    return MissionOut.model_validate(m)


@router.get("/{mission_id}", response_model=MissionOut)
def get_mission_api(
    mission_id: int,
    db: Session = Depends(get_db_dep),  # noqa: B008
    _: str = Depends(require_auth),  # noqa: B008
) -> MissionOut:
    m = get_mission(db, mission_id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission introuvable.",
        )
    return MissionOut.model_validate(m)


@router.put("/{mission_id}", response_model=MissionOut)
def update_mission_api(
    mission_id: int,
    payload: MissionUpdate,
    db: Session = Depends(get_db_dep),  # noqa: B008
    actor: str = Depends(require_auth),  # noqa: B008
) -> MissionOut:
    m = update_mission(
        db,
        mission_id,
        title=payload.title,
        start_at=payload.start_at,
        end_at=payload.end_at,
    )
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission introuvable.",
        )
    write_audit_log(db, actor, "update", "mission", m.id, payload.model_dump(exclude_unset=True))
    return MissionOut.model_validate(m)


@router.delete("/{mission_id}", status_code=204, response_class=Response)
def delete_mission_api(
    mission_id: int,
    db: Session = Depends(get_db_dep),  # noqa: B008
    actor: str = Depends(require_auth),  # noqa: B008
) -> Response:
    ok = delete_mission(db, mission_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission introuvable.",
        )
    write_audit_log(db, actor, "delete", "mission", mission_id, None)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{mission_id}/publish", response_model=MissionOut)
def publish_mission_api(
    mission_id: int,
    db: Session = Depends(get_db_dep),  # noqa: B008
    actor: str = Depends(require_auth),  # noqa: B008
) -> MissionOut:
    m = publish_mission(db, mission_id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission introuvable.",
        )
    write_audit_log(db, actor, "publish", "mission", m.id, None)
    return MissionOut.model_validate(m)


@router.post("/{mission_id}/duplicate", response_model=MissionOut, status_code=201)
def duplicate_mission_api(
    mission_id: int,
    db: Session = Depends(get_db_dep),  # noqa: B008
    actor: str = Depends(require_auth),  # noqa: B008
) -> MissionOut:
    m = duplicate_mission(db, mission_id)
    if not m:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission introuvable.",
        )
    write_audit_log(db, actor, "duplicate", "mission", m.id, {"source_id": mission_id})
    return MissionOut.model_validate(m)
