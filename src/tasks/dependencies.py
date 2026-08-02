from fastapi import Depends
from sqlalchemy.orm import Session

from shared.database import get_database
from collaborators.repositories.collaborator_repository import CollaboratorRepository

from .repositories.task_repository import TaskRepository
from .services.task_service import TaskService

def get_collaborator_repository(
    db: Session = Depends(get_database),
) -> CollaboratorRepository:
    return CollaboratorRepository(db)


def get_task_repository(
    db: Session = Depends(get_database),
) -> TaskRepository:
    return TaskRepository(db)


def get_task_repository(
    db: Session = Depends(get_database),
) -> TaskRepository:
    return TaskRepository(db)


def get_task_service(
    repo: TaskRepository = Depends(get_task_repository),
    collaborator_repo: CollaboratorRepository = Depends(get_collaborator_repository),
) -> TaskService:
    return TaskService(repo, collaborator_repo)
