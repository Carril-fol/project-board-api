from secrets import token_urlsafe

from collaborators.models.collaborators_model import Collaborators
from collaborators.repositories.collaborator_repository import CollaboratorRepository
from collaborators.schemas.collaborators_schema import RegisterCollaboratorsInputSchema
from projects.repositories.project_repository import ProjectRepository

from ..exceptions.project_invitation_exceptions import (
    InvitationAlreadyExistsError,
    InvitationNotFoundError,
)
from ..models.project_invitation_model import InvitationStatus, ProjectInvitation
from ..repositories.project_invitation_repository import ProjectInvitationRepository
from ..schemas.project_invitations_schemas import CreateProjectInvitation


class ProjectInvitationService:
    def __init__(
        self,
        repository: ProjectInvitationRepository,
        project_repo: ProjectRepository,
        collaborator_repo: CollaboratorRepository,
    ):
        self.repository = repository
        self.project_repo = project_repo
        self.collaborator_repo = collaborator_repo

    def _get_invite_already_exists_or_none(self, project_id: int, invitee_id: int):
        invite = self.repository.get_invite_by_project_id_and_invitee_id(
            project_id, invitee_id
        )
        return invite

    def create_project_invitation(
        self,
        data: CreateProjectInvitation,
        inviter_id: int,
    ):
        project = self.project_repo.get_project_by_id(data.id_project)

        if project is None:
            raise ValueError("Project not found.")

        collaborators_from_project = len(
            self.collaborator_repo.get_collaborators_from_project(data.id_project)
        )

        if project.max_collaborators <= 0:
            raise Exception("Project does not allow collaborators.")

        if project.max_collaborators <= collaborators_from_project:
            raise Exception("Project is full.")

        invite = self._get_invite_already_exists_or_none(
            data.id_project, data.id_invitee
        )

        if invite and (
            invite.status == InvitationStatus.PENDING
            or invite.status == InvitationStatus.ACCEPTED
        ):
            raise InvitationAlreadyExistsError("Invite already exists.")

        if int(project.owner_id) != int(inviter_id):
            raise PermissionError(
                "You do not have permission to invite users to this project."
            )

        token = token_urlsafe(32)

        project_invitation_instance = ProjectInvitation(
            **data.model_dump(), id_inviter=inviter_id, token=token
        )

        self.repository.create_project_invitation(project_invitation_instance)

        return token

    def remove_project_invitation(self, id_invite: int, user_id: int):
        invite = self.repository.get_invite_by_id(id_invite)

        if not invite:
            raise InvitationNotFoundError("Invite not found.")

        if int(invite.id_inviter) != int(user_id):
            raise PermissionError("You do not have permission to remove this invite.")

        self.repository.delete_project_invitation(invite)

    def respond_project_invitation(
        self,
        token: str,
        user_id: int,
        accepted: bool,
    ):
        invite = self.repository.get_by_token(token)

        if not invite:
            raise InvitationNotFoundError("Invitation not found.")

        if int(invite.id_invitee) != int(user_id):
            raise PermissionError(
                "You do not have permission to respond to this invitation."
            )

        if (
            invite.status == InvitationStatus.ACCEPTED
            or invite.status == InvitationStatus.REJECTED
        ):
            raise Exception("Invitation has already been responded.")

        if accepted and invite.status == InvitationStatus.PENDING:
            data = RegisterCollaboratorsInputSchema(
                role=invite.role,
                id_project=invite.id_project,
                id_user=user_id,
            )
            collaborator_entity = Collaborators(**data.dict())
            self.collaborator_repo.create_collaborator(collaborator_entity)

        invite.status = (
            InvitationStatus.ACCEPTED if accepted else InvitationStatus.REJECTED
        )

        self.repository.update_project_invitation(invite)
