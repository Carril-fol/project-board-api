from fastapi import Depends
from sqlalchemy.orm import Session
from shared.database import get_database
from .repositories.user_repository import UserRepository


def get_user_repository(db: Session = Depends(get_database)) -> UserRepository:
    return UserRepository(db)
