from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PrecedentRecord(Base):
    __tablename__ = "precedent_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("failure_scenarios.id"), index=True
    )
    project_name: Mapped[str] = mapped_column(String(255), default="")
    year: Mapped[int] = mapped_column(Integer, default=0)
    industry: Mapped[str] = mapped_column(String(100), default="")
    what_happened: Mapped[str] = mapped_column(Text, default="")
    prevention: Mapped[str] = mapped_column(Text, default="")
