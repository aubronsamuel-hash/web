from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from .deps import get_db_dep, require_auth
from .models_availability import Availability
from .models_mission import Mission

router = APIRouter(
    prefix="/planning",
    tags=["planning"],
    dependencies=[Depends(require_auth)],  # noqa: B008
)


def _overlap(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    return a_start < b_end and b_start < a_end


class PlanningCheckIn(BaseModel):
    start_at: datetime
    end_at: datetime
    intermittent_id: int | None = None
    exclude_mission_id: int | None = None

    @field_validator("end_at")
    @classmethod
    def _validate_dates(cls, v: datetime, info):  # type: ignore[override]
        start = info.data.get("start_at")
        if start and v <= start:
            raise ValueError("end_at must be after start_at")
        return v


class MissionMini(BaseModel):
    id: int
    title: str
    start_at: datetime
    end_at: datetime

    class Config:
        from_attributes = True


class AvailMini(BaseModel):
    id: int
    intermittent_id: int
    start_at: datetime
    end_at: datetime

    class Config:
        from_attributes = True


class PlanningCheckOut(BaseModel):
    conflicts: dict[str, list[Any]]


@router.post("/check", response_model=PlanningCheckOut)
def check_conflicts(
    payload: PlanningCheckIn, db: Session = Depends(get_db_dep)  # noqa: B008
) -> PlanningCheckOut:
    s0 = payload.start_at
    e0 = payload.end_at

    # Missions en conflit (chevauchement temps)
    q = select(Mission)
    if payload.exclude_mission_id:
        q = q.where(Mission.id != payload.exclude_mission_id)
    missions = db.scalars(q).all()
    m_conf = [m for m in missions if _overlap(s0, e0, m.start_at, m.end_at)]

    # Indisponibilites en conflit pour un intermittent (si fourni)
    a_conf: list[Availability] = []
    if payload.intermittent_id is not None:
        avs = db.scalars(
            select(Availability).where(
                Availability.intermittent_id == payload.intermittent_id,
                Availability.busy.is_(True),
            )
        ).all()
        a_conf = [a for a in avs if _overlap(s0, e0, a.start_at, a.end_at)]

    out = {
        "missions": [MissionMini.model_validate(m).model_dump() for m in m_conf],
        "availabilities": [AvailMini.model_validate(a).model_dump() for a in a_conf],
    }
    return PlanningCheckOut(conflicts=out)
