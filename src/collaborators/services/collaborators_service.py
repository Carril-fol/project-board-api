from projects.exceptions.project_exception import (
    ProjectInsufficientPrivileges,
    ProjectNotFoundError,
)
from projects.repositories.project_repository import ProjectRepository

from ..exceptions import CollaboratorNotAuthorized, CollaboratorNotFound
from ..models.collaborators_model import Collaborators
from ..repositories.collaborator_repository import CollaboratorRepository
from ..schemas.collaborators_schema import (
    CreateCollaboratorsSchema,
    DetailCollaboratorsSchema,
    ListDetailCollaboratorsSchema,
    RegisterCollaboratorsInputSchema,
)


class CollaboratorService:
    def __init__(
        self, repository: CollaboratorRepository, project_repo: ProjectRepository
    ):
        self.repository = repository
        self.project_repo = project_repo

    def create_collaborator(
        self, register_collaborator_input_schema: RegisterCollaboratorsInputSchema
    ):
        create_collaborator_schema = CreateCollaboratorsSchema(
            **register_collaborator_input_schema.model_dump()
        )
        collaborator_entity = Collaborators(**create_collaborator_schema.model_dump())
        self.repository.create_collaborator(collaborator_entity)

    def get_collaborators(
        self, id_project: int, user_id: int
    ) -> ListDetailCollaboratorsSchema:
        collaborators_raw = self.repository.get_collaborators_from_project(id_project)
        collaborators = [
            int(collaborator.id_user) for collaborator in collaborators_raw
        ]

        if int(user_id) not in collaborators:
            raise CollaboratorNotAuthorized(
                "You are not a collaborator of this project"
            )

        collaborators_list = [
            DetailCollaboratorsSchema.model_validate(collaborator)
            for collaborator in collaborators_raw
        ]
        return ListDetailCollaboratorsSchema(collaborators=collaborators_list)

    def remove_collaborator(self, collaborator_id: int, user_id: int):
        collaborator = self.repository.get_collaborator(collaborator_id)
        if not collaborator:
            raise CollaboratorNotFound("Collaborator not founded")
        project = self.project_repo.get_project_by_id(collaborator.id_project)
        if not project:
            raise ProjectNotFoundError("Project not founded")
        if project.owner_id != user_id:
            raise ProjectInsufficientPrivileges(
                "You are not the owner of this collaborator"
            )
        self.repository.remove_collaborator(collaborator)
