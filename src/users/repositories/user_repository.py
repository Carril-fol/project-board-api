from sqlalchemy.orm import Session
from ..models.user import User

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user

    def get(self, id: int) -> User | None:
        return self.db.get(User, id)

    def list(self) -> list[User]:
        return self.db.query(User).all()
    
    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()