from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from shared.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.now)
    date_updated = Column(DateTime, nullable=False, default=datetime.now)