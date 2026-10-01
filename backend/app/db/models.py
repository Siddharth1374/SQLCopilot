from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class HistoryItem(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), default="")
    natural_language: Mapped[str] = mapped_column(Text, default="")
    sql: Mapped[str] = mapped_column(Text)
    direction: Mapped[str] = mapped_column(String(20))  # nl_to_sql | sql_to_nl
    saved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
