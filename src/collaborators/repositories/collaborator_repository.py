from sqlalchemy import select

from users.models.user import User
from shared.database.base_repository import BaseRepository

from ..models.collaborators_model import Collaborators


class CollaboratorRepository(BaseRepository[Collaborators]):

    def __init__(self, db):
        super().__init__(Collaborators, db)

    def get_collaborators_from_project(self, id_project: int):
        stmt = select(Collaborators).join(Collaborators.user).filter(User.id == Collaborators.id_user, Collaborators.id_project == id_project)
        result = self.db.execute(stmt).scalars().fetchall()
        return result

    def get_collaborator_by_user_id(self, user_id: int):
        stmt = select(Collaborators).where(Collaborators.id_user == user_id)
        return self.db.execute(stmt).scalar_one_or_none()
    
    def get_collaborator_by_user_id_and_project_id(self, user_id: int, id_project: int):
        stmt = select(Collaborators).where(Collaborators.id_user == user_id, Collaborators.id_project == id_project)   
        return self.db.execute(stmt).scalar_one_or_none()