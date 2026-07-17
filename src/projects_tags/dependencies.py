from fastapi import Depends
from sqlalchemy.orm import Session

from projects.dependencies import get_project_repository
from projects.repositories.project_repository import ProjectRepository
from shared.database import get_database

from .repositories.project_tag_repository import ProjectTagRepository
from .services.project_tag_service import ProjectTagService


def get_project_tag_repository(
    db: Session = Depends(get_database),
) -> ProjectTagRepository:
    return ProjectTagRepository(db)


def get_project_tag_service(
    repo: ProjectTagRepository = Depends(get_project_tag_repository),
    project_repo: ProjectRepository = Depends(get_project_repository),
):
    return ProjectTagService(repo, project_repo)
