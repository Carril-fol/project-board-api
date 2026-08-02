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
    UpdateCollaboratorsSchema
)


class CollaboratorService:
    def __init__(
        self, repository: CollaboratorRepository, project_repo: ProjectRepository
    ):
        self.repository = repository
        self.project_repo = project_repo

    def _is_user_owner(self, user_id: int, project_id: int) -> bool:
        project = self.project_repo.get_project_by_id(project_id)
        if int(project.owner_id) == int(user_id):
            raise ProjectInsufficientPrivileges("You are not the owner of this project")

    def create_collaborator(self, data: RegisterCollaboratorsInputSchema):
        create_collaborator_schema = CreateCollaboratorsSchema(**data.model_dump())
        collaborator_entity = Collaborators(**create_collaborator_schema.model_dump())
        self.repository.create(collaborator_entity)

    def get_collaborators(self, id_project: int, user_id: int) -> ListDetailCollaboratorsSchema:
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
        collaborator = self.repository.get_by_id(collaborator_id)
        if not collaborator:
            raise CollaboratorNotFound("Collaborator not founded")
        
        project = self.project_repo.get_project_by_id(collaborator.id_project)
        if not project:
            raise ProjectNotFoundError("Project not founded")
        
        self._is_user_owner(user_id, project.id)
        self.repository.delete(collaborator)

    def change_role_collaborator(self, collaborator_id: int, data: UpdateCollaboratorsSchema, user_id: int):
        collaborator = self.repository.get_by_id(collaborator_id)
        if not collaborator:
            raise CollaboratorNotFound("Collaborator not founded")
        
        project = self.project_repo.get_project_by_id(collaborator.id_project)
        if not project:
            raise ProjectNotFoundError("Project not founded")
        
        self._is_user_owner(user_id, project.id)

        for key, value in data.model_dump().items():
            setattr(collaborator, key, value)

        self.repository.update(collaborator)