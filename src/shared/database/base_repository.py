from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar("T")


class BaseRepository(Generic[T]):

    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[T]:
        return self.db.get(self.model, id)

    def get_all(self) -> List[T]:
        return self.db.execute(select(self.model)).scalars().all()

    def delete(self, id: int) -> bool:
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

    def create(self, entity):
        self.db.add(entity)
        self.db.commit()
        return entity

    def update(self, entity):
        self.db.commit()
        self.db.refresh(entity)
        return entity
