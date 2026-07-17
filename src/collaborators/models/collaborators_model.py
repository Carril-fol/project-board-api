from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database import Base


class Collaborators(Base):
    __tablename__ = "collaborators"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    id_user: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    id_project: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    project: Mapped["Project"] = relationship(
        back_populates="collaborators",
    )

    user: Mapped["User"] = relationship(
        back_populates="collaborators",
    )
