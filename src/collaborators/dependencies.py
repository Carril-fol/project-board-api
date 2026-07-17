from fastapi import Depends
from sqlalchemy.orm import Session

from projects.repositories.project_repository import ProjectRepository
from shared.database import get_database

from .repositories.collaborator_repository import CollaboratorRepository
from .services.collaborators_service import CollaboratorService


def get_collaborators_repository(
    db: Session = Depends(get_database),
):
    return CollaboratorRepository(db)


def get_collaborators_service(
    db: Session = Depends(get_database),
):
    collaborator_repo = CollaboratorRepository(db)
    project_repo = ProjectRepository(db)

    return CollaboratorService(collaborator_repo, project_repo)
