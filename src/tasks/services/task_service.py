from fastapi import HTTPException

from collaborators.repositories.collaborator_repository import CollaboratorRepository

from ..repositories.task_repository import TaskRepository
from ..models.task_model import Task
from ..schemas.task_schemas import (
    CreateTaskInputSchema, 
    ListDetailTaskOutputSchema, 
    RegisterTaskInputSchema, 
    DetailTaskOutputSchema, 
    UpdateTaskInputSchema
)


class TaskService:

    def __init__(self, repo: TaskRepository, collaborator_repo: CollaboratorRepository):
        self.repo = repo
        self.collaborator_repo = collaborator_repo

    def _format_tasks(self, tasks):
        tasks_formatted = [
            DetailTaskOutputSchema.model_validate(task)
            for task in tasks
        ]
        return ListDetailTaskOutputSchema(tasks=tasks_formatted)

    def _get_task(self, task_id: int):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def _require_project_owner(self, project_id: int, user_id: int):
        collaborator = self.collaborator_repo.get_collaborator_by_user_id_and_project_id(user_id, project_id)

        if not collaborator:
            raise PermissionError("User is not a collaborator of the project")

        if collaborator.role != "OWNER":
            raise PermissionError("User does not have permission")

        return collaborator

    def create(self, data: RegisterTaskInputSchema, user_id: int, project_id: int):
        collaborator = self.collaborator_repo.get_collaborator_by_user_id_and_project_id(user_id, project_id)
        if not collaborator:
            raise PermissionError("User is not a collaborator of the project")

        task_data = data.model_dump()
        task_data["project_id"] = project_id

        validated_data = CreateTaskInputSchema.model_validate(task_data)

        task_entity = Task(**validated_data.model_dump())
        self.repo.create(task_entity)

    def delete_task(self, task_id: int, user_id: int):
        task = self._get_task(task_id)

        self._require_project_owner(task.project_id, user_id)
        
        self.repo.delete(task_id)

    def update_task(self, task_id: int, data: UpdateTaskInputSchema, user_id: int):
        task = self._get_task(task_id)

        self._require_project_owner(task.project_id, user_id)

        for key, value in data.model_dump().items():
            setattr(task, key, value)

        self.repo.update(task)

    def assign_user_to_task(self, task_id: int, target_user_id: int, actor_user_id: int):
        task = self._get_task(task_id)

        actor_collab = self.collaborator_repo.get_collaborator_by_user_id_and_project_id(actor_user_id, task.project_id)
        if not actor_collab or actor_collab.role != "OWNER":
            raise PermissionError("Only the project owner can assign users to tasks")

        target_collab = self.collaborator_repo.get_collaborator_by_user_id_and_project_id(target_user_id, task.project_id)
        if not target_collab:
            raise PermissionError("The target user is not a collaborator of this project")

        self.repo.assign_user(task_id, target_user_id)

    def unassign_user_from_task(self, task_id: int, user_id: int):
        task = self._get_task(task_id)

        self._require_project_owner(task.project_id, user_id)

        self.repo.unassign_user(task_id, user_id)

    def get_task_by_id(self, task_id: int, user_id: int) -> DetailTaskOutputSchema:
        task = self._get_task(task_id)

        if not self.collaborator_repo.get_collaborator_by_user_id_and_project_id(user_id, task.project_id):
            raise PermissionError("User is not a collaborator of the project")

        return DetailTaskOutputSchema.model_validate(task).model_dump()

    def get_tasks_by_project(self, user_id: int, project_id: int):
        if not self.collaborator_repo.get_collaborator_by_user_id_and_project_id(user_id, project_id):
            raise PermissionError("User is not a collaborator of the project")

        tasks_raw = self.repo.get_tasks_by_project(project_id)
        tasks_formated = self._format_tasks(tasks_raw).tasks
        return tasks_formated

    def get_tasks_from_user(self, user_id: int):
        tasks = self.repo.get_tasks_from_user(user_id)
        return self._format_tasks(tasks)

    def get_tasks_by_priority(self, priority: str):
        tasks = self.repo.get_tasks_with_priority(priority.upper())
        return self._format_tasks(tasks)

    def get_tasks_by_title_or_description(self, search_term: str):
        tasks = self.repo.get_tasks_by_title_or_description(search_term)
        return self._format_tasks(tasks)

    def get_tasks_by_status(self, status: str):
        tasks = self.repo.get_tasks_by_status(status.upper())
        return self._format_tasks(tasks)