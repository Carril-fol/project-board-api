from sqlalchemy.orm import Session

from users.models.user import User

from ..models.collaborators_model import Collaborators


class CollaboratorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_collaborator(self, collaborator: Collaborators):
        self.db.add(collaborator)
        self.db.flush()
        return collaborator

    def get_collaborators_from_project(self, id_project: int):
        query = (
            self.db.query(Collaborators)
            .join(Collaborators.user)
            .filter(User.id == Collaborators.id_user)
            .all()
        )
        return query

    def remove_collaborator(self, collaborator):
        self.db.delete(collaborator)
        self.db.flush()
        return collaborator

    def get_collaborator(self, collaborator_id: int):
        return (
            self.db.query(Collaborators)
            .filter(Collaborators.id == collaborator_id)
            .first()
        )

    def get_collaborator_by_user_id(self, user_id: int):
        return (
            self.db.query(Collaborators)
            .filter(Collaborators.id_user == user_id)
            .first()
        )
