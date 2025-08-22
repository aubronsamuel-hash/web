from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, model_validator


class MissionCreate(BaseModel):
    title: str
    start_at: datetime
    end_at: datetime

    @model_validator(mode="after")
    def check_dates(self) -> MissionCreate:
        if self.end_at <= self.start_at:
            raise ValueError("end_at must be after start_at")
        return self


class MissionUpdate(BaseModel):
    title: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None

    @model_validator(mode="after")
    def check_dates(self) -> MissionUpdate:
        if self.start_at and self.end_at and self.end_at <= self.start_at:
            raise ValueError("end_at must be after start_at")
        return self


class MissionOut(BaseModel):
    id: int
    title: str
    start_at: datetime
    end_at: datetime
    is_published: bool

    class Config:
        from_attributes = True
