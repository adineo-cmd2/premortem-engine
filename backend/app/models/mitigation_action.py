from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class MitigationAction(Base):
    __tablename__ = "mitigation_actions"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("failure_scenarios.id"), index=True
    )
    action: Mapped[str] = mapped_column(Text, default="")
    owner_role: Mapped[str] = mapped_column(String(100), default="")
    effort: Mapped[str] = mapped_column(String(20), default="medium")
    timeline_weeks: Mapped[int] = mapped_column(Integer, default=0)
