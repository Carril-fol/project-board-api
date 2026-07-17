from fastapi import Depends
from sqlalchemy.orm import Session

from collaborators.dependencies import get_collaborators_repository
from collaborators.repositories.collaborator_repository import CollaboratorRepository
from projects.dependencies import get_project_repository
from projects.repositories.project_repository import ProjectRepository
from shared.database import get_database

from .repositories.project_invitation_repository import ProjectInvitationRepository
from .services.project_invitations_service import ProjectInvitationService


def get_project_invitation_repository(
    db: Session = Depends(get_database),
) -> ProjectInvitationRepository:
    return ProjectInvitationRepository(db)


def get_project_invitation_service(
    repository: ProjectInvitationRepository = Depends(
        get_project_invitation_repository
    ),
    project_repo: ProjectRepository = Depends(get_project_repository),
    collaborator_repo: CollaboratorRepository = Depends(get_collaborators_repository),
):
    return ProjectInvitationService(repository, project_repo, collaborator_repo)
