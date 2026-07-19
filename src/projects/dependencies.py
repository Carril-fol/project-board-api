from fastapi import Depends
from sqlalchemy.orm import Session

from collaborators.dependencies import get_collaborators_repository
from collaborators.services.collaborators_service import CollaboratorRepository
from shared.database import get_database

from .repositories.project_repository import ProjectRepository
from .services.project_service import ProjectService


def get_project_repository(db: Session = Depends(get_database)) -> ProjectRepository:
    return ProjectRepository(db)


def get_project_service(
    repo: ProjectRepository = Depends(get_project_repository),
    collaborator_repo: CollaboratorRepository = Depends(get_collaborators_repository),
):
    return ProjectService(repo, collaborator_repo)
