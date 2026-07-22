from collaborators.exceptions import CollaboratorAlreadyExists
from collaborators.models.collaborators_model import Collaborators
from collaborators.repositories.collaborator_repository import CollaboratorRepository
from project_invitations.repositories.project_invitation_repository import (
    ProjectInvitationRepository,
)
from projects.exceptions.project_exception import ProjectNotFound
from projects.repositories.project_repository import ProjectRepository

from ..exceptions import RequestAlreadyExists, RequestNotFound
from ..models.requests_model import Request
from ..repositories.requests_repository import RequestsRepository
from ..schemas.requests_schemas import (
    CreateRequestSchema,
    DetailRequestSchema,
    RegisterRequestsInputSchema,
    RequestStatus,
)


class RequestsService:
    def __init__(
        self,
        requests_repository: RequestsRepository,
        collaborator_repository: CollaboratorRepository,
        project_repository: ProjectRepository,
        project_invitations_repo: ProjectInvitationRepository,
    ):
        self.requests_repository = requests_repository
        self.collaborator_repository = collaborator_repository
        self.project_repository = project_repository
        self.project_invitations_repo = project_invitations_repo

    def create_request(
        self,
        data: RegisterRequestsInputSchema,
        user_id: int,
        project_id: int,
    ):
        requests_exists = (
            self.requests_repository.get_request_by_user_id_and_project_id(
                user_id, project_id
            )
        )
        if requests_exists:
            raise RequestAlreadyExists("Request already exists")

        project_invitations = self.project_invitations_repo.get_project_invitation_by_project_id_and_user_id(
            project_id, user_id
        )
        if project_invitations:
            raise Exception("User is already invited to this project")

        project = self.project_repository.get_project_by_id(project_id)
        if not project:
            raise ProjectNotFound("Project not found")

        user_exists = self.collaborator_repository.get_collaborator_by_user_id(user_id)
        if user_exists:
            raise CollaboratorAlreadyExists("User already is a collaborator")

        create_request = CreateRequestSchema(
            **data.dict(), user_id=user_id, project_id=project_id
        )
        request = Request(**create_request.dict())
        return self.requests_repository.create(request)

    def respond_request(self, request_id: int, user_id: int, accepted: bool):
        request = self.requests_repository.get_request_by_id(request_id)
        if not request:
            raise RequestNotFound("Request not found")

        project = self.project_repository.get_project_by_id(request.project_id)
        if not project:
            raise ProjectNotFound("Project not found")

        if int(project.owner_id) != int(user_id):
            raise PermissionError("Only the project owner can approve requests")

        if accepted and request.status == RequestStatus.PENDING:
            request.status = RequestStatus.APPROVED
            self.collaborator_repository.create_collaborator(
                Collaborators(id_user=user_id, id_project=project.id, role=request.role)
            )
        else:
            request.status = RequestStatus.REJECTED

        self.requests_repository.update(request)

    def get_all_requests(self, project_id: int, user_id: int):
        project = self.project_repository.get_project_by_id(project_id)
        if not project:
            raise ProjectNotFound("Project not found")

        if int(project.owner_id) != int(user_id):
            raise PermissionError("Only the project owner can view requests")

        requests = self.requests_repository.get_requests_by_project_id(project_id)
        return [DetailRequestSchema.model_validate(request) for request in requests]

    def get_request(self, request_id: int, user_id: int):
        request = self.requests_repository.get_request_by_id(request_id)
        if not request:
            raise RequestNotFound("Request not found")

        project = self.project_repository.get_project_by_id(request.project_id)
        if not project:
            raise ProjectNotFound("Project not found")

        if int(request.user_id) != int(user_id) and (
            int(project.owner_id) != int(user_id)
        ):
            raise PermissionError("Only the request owner can view this request")

        return DetailRequestSchema.model_validate(request)
