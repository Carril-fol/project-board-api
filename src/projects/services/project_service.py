from ..models.project import Project
from ..schemas.project_schema import RegisterProjectInputSchema, UpdateProjectInputSchema, ProjectCreateSchema, ProjectUpdateSchema, ProjectDetail, ListProjectDetail
from ..repositories.project_repository import ProjectRepository
from ..exceptions.project_exception import ProjectNotFound, ProjectInsufficientPrivileges, ProjectAlreadyHasStatus

class ProjectService:

    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    def _get_project_by_id_or_raise(self, id: int) -> Project:
        project = self.project_repo.get_project_by_id(id)
        if not project:
            raise ProjectNotFound("Project not found")
        return project

    def create_project(self, data: RegisterProjectInputSchema, user_id: int):
        project_to_created = ProjectCreateSchema(
            **data.model_dump(), 
            owner_id=user_id
        )

        project_entity = Project(
            **project_to_created.model_dump()
        )
        return self.project_repo.create(project_entity)
    
    def detail_project_by_id(self, id: int):
        project = self._get_project_by_id_or_raise(id)
        return ProjectDetail.model_validate(project)
    
    def update_project(self, id: int, data: UpdateProjectInputSchema, user_id: int) -> None:
        project = self._get_project_by_id_or_raise(id)

        if project.owner_id != user_id:
            raise ProjectInsufficientPrivileges(
                "You don't have privileges for this action."
            )

        project_update = ProjectUpdateSchema(
            **data.model_dump(exclude_unset=True),
            owner_id=user_id
        )

        update_fields = project_update.model_dump(
            exclude_unset=True,
            exclude={"owner_id"}
        )

        for field, value in update_fields.items():
            setattr(project, field, value)

        self.project_repo.update(project)

    def delete_project(self, id: int, user_id: int, data: dict) -> None:
        project = self._get_project_by_id_or_raise(id)
        if project.owner_id != user_id:
            raise ProjectInsufficientPrivileges("You don't have privileges for this action.")
        
        if project.status == "CANCELLED":
            raise ProjectAlreadyHasStatus("The project has already been cancelled.")

        for field, value in data.items():
            setattr(project, field, value)

        self.project_repo.delete_logic(project)
    
    def get_all_project(self, per_page: int, page: int) -> ListProjectDetail:
        projects_db, total = self.project_repo.get_all_project(per_page, page)
        projects = [ProjectDetail.model_validate(project) for project in projects_db]
        return ListProjectDetail(projects=projects, total=total)