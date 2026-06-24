from fastapi import Depends
from sqlalchemy.orm import Session

from shared.database import get_database
from .repositories.project_repository import ProjectRepository
from .services.project_service import ProjectService

def get_project_repository(db: Session = Depends(get_database)) -> ProjectRepository:
    return ProjectRepository(db)

def get_project_service(repo: ProjectRepository = Depends(get_project_repository)):
    return ProjectService(repo)