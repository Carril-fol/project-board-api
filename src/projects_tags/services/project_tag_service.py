from projects.repositories.project_repository import ProjectRepository

from ..exceptions.project_tag_exceptions import ProjectTagNotFound
from ..models.project_tag_model import ProjectTag
from ..repositories.project_tag_repository import ProjectTagRepository
from ..schemas.project_tag_schema import CreateProjectTag, RegisterProjectTagInputSchema


class ProjectTagService:
    def __init__(self, repo: ProjectTagRepository, project_repo: ProjectRepository):
        self.repo = repo
        self.project_repo = project_repo

    def _get_project_tag_or_raise(self, id_tag: int):
        project_tag = self.repo.get_project_tag_by_id(id_tag)
        if not project_tag:
            raise ProjectTagNotFound("Project tag not found")
        return project_tag

    def create_project_tag(
        self, id_project: int, data: RegisterProjectTagInputSchema, user_id: int
    ):
        project = self.project_repo.get_project_by_id(id_project)
        if not project:
            raise ProjectTagNotFound("Project not found")

        if project.owner_id != user_id:
            raise ProjectTagNotFound("Project not found")

        project_tag_data = CreateProjectTag(tag=data.tag, id_project=id_project)
        project_to_create = ProjectTag(**project_tag_data.model_dump())
        return self.repo.create(project_to_create)

    def delete_tag_from_project(self, id_tag: int, user_id: int):
        project_tag = self._get_project_tag_or_raise(id_tag)
        if project_tag.id_project != user_id:
            raise ProjectTagNotFound("Project tag not found")

        return self.repo.delete(project_tag)
