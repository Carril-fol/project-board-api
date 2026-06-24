from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey
from shared.database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    max_collaborators = Column(Integer, nullable=False)
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    