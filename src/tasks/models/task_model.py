from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from shared.database import Base

class TaskStatus(str, Enum):
    REVIEW = "REVIEW"
    IN_PROGRESS = "IN PROGRESS"
    DONE = "DONE"
    TO_DO = "TO DO"


class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus),
        default=TaskStatus.TO_DO.value,
        nullable=False,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    expiration_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )