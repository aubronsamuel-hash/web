from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Availability(Base):
    __tablename__ = "availabilities"
    __table_args__ = (
        Index("ix_avail_inter_id", "intermittent_id"),
        Index("ix_avail_time", "start_at", "end_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    intermittent_id: Mapped[int] = mapped_column(Integer, ForeignKey("intermittents.id"), nullable=False)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    busy: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    note: Mapped[str | None] = mapped_column(String(200), nullable=True)
