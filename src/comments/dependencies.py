from fastapi import Depends
from sqlalchemy.orm import Session

from shared.database.database import get_database

from collaborators.repositories.collaborator_repository import CollaboratorRepository
from projects.repositories.project_repository import ProjectRepository
from tasks.repositories.task_repository import TaskRepository

from .repositories.comment_repository import CommentRepository
from .services.comment_service import CommentService

def get_projects_repository(
    db: Session = Depends(get_database),
):
    return ProjectRepository(db)


def get_collaborators_repository(
    db: Session = Depends(get_database),
):
    return CollaboratorRepository(db)


def get_tasks_repository(
    db: Session = Depends(get_database),
):
    return TaskRepository(db)

def get_comments_repository(
    db: Session = Depends(get_database),
):
    return CommentRepository(db)

def get_comments_service(
    repo: CommentRepository = Depends(get_comments_repository),
    collaborator_repo: CollaboratorRepository = Depends(get_collaborators_repository),
    task_repo: TaskRepository = Depends(get_tasks_repository),
):
    return CommentService(
        repo,
        collaborator_repo,
        task_repo,
    )