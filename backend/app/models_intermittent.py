from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Intermittent(Base):
    __tablename__ = "intermittents"
    __table_args__ = (
        UniqueConstraint("first_name", "last_name", name="uq_intermittents_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    skills: Mapped[str | None] = mapped_column(String(200), nullable=True)
