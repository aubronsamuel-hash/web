from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class AvailabilityBase(BaseModel):
    intermittent_id: int
    start_at: datetime
    end_at: datetime
    busy: bool = Field(default=True)
    note: str | None = None

    @field_validator("end_at")
    @classmethod
    def _validate_dates(cls, v: datetime, info):  # type: ignore[override]
        start = info.data.get("start_at")
        if start and v <= start:
            raise ValueError("end_at must be after start_at")
        return v


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityUpdate(BaseModel):
    intermittent_id: int | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    busy: bool | None = None
    note: str | None = None


class AvailabilityOut(BaseModel):
    id: int
    intermittent_id: int
    start_at: datetime
    end_at: datetime
    busy: bool
    note: str | None

    class Config:
        from_attributes = True
